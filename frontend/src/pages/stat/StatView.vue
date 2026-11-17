<template>
    <el-card>
        <h3 class="title">销售数据统计</h3>
        <el-divider></el-divider>
        <el-row :gutter="20">
            <el-col :span="24">
                <!-- 商品销售排行top0 -->
                <BarChart renderDom="chart01" :options="productOptions" />
            </el-col>
            <el-col :span="24">
                <!-- 销售顾问销售排行top10 -->
                <BarChart renderDom="chart02" :options="employeeOptions" />
            </el-col>
            <el-col :span="24">
                <!-- 客户分布 -->
                <PieChart renderDom="pie01" :options="customerOptions" />
            </el-col>
            <el-col :span="24">
                <!-- 本周每天销售额 -->
                <bar-chart renderDom="chart03" :options="currWeekOptions" />
            </el-col>
            <el-col :span="24">
                <!-- 本月每天销售业 -->
                <bar-chart renderDom="chart04" :options="currMonthOptions" />
            </el-col>
            <el-col :span="24">
                <!-- 本年每月销售额 -->
                <bar-chart renderDom="chart05" :options="currYearOptions" />
            </el-col>
        </el-row>
    </el-card>
</template>

<script setup>
import { getTopSaleProduct, getTop10Employee, getTop10Customer, getWeekDaySaleAmount, getMonthDaySaleAmount, getYearMonthSaleAmount } from '@/utils/api'
import { ref } from 'vue'
import BarChart from '@/components/BarChart.vue'
import PieChart from '@/components/PieChart.vue'
// 柱状图需要的配置对象: 只包含通过数据接口请求的到的统计数据
const productOptions = ref({})
// 请求商品销售数据
const getTopSaleProductHandler = async () => {
    const result = await getTopSaleProduct()
    if (result.status === 200) {
        const productList = result.data.map(item => item.name)
        const productAmount = result.data.map(item => item.total_amount)
        const productNum = result.data.map(item => item.total_num)
        productOptions.value = {
            title: {
                text: '商品销量排行TOP10'
            },
            xAxis: {
                data: productList
            },
            series: [
                {
                    name: '销售金额',
                    data: productAmount
                },
                {
                    name: '销售数量',
                    data: productNum
                }
            ]
        }
    }
}
getTopSaleProductHandler()
const employeeOptions = ref({})
// 获取销售额排名前10的销售人员信息
const getTop10EmployeeHandler = async () => {
    const result = await getTop10Employee()
    if (result.status === 200) {
        const employee = result.data.map(item => item.user__employee__name)
        const amount = result.data.map(item => item.total_amount)
        employeeOptions.value = {
            title: {
                text: '销售顾问销售额排行TOP10'
            },
            xAxis: {
                data: employee
            },
            series: [
                {
                    name: '销售金额',
                    data: amount,
                    type: 'line'
                }
            ]
        }
    }
}
getTop10EmployeeHandler()
const customerOptions = ref({})
const getTop10CustomerHandler = async () => {
    const result = await getTop10Customer()
    if (result.status === 200) {
        customerOptions.value = {
            title: {
                text: '客户分布省份TOP10'
            },
            series: [
                {
                    data: result.data.map(item => ({ value: item.total_customer, name: item.province }))
                }
            ]
        }
    }
}
getTop10CustomerHandler()
// 本周销售额数据
const currWeekOptions = ref({})
const getCurrWeekSaleAmount = async () => {
    const result = await getWeekDaySaleAmount()
    if (result.status === 200) {
        const week = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
        const data = []
        for (let i = 1; i < 8; i++) {
            data.push({
                day: i, total_amount: 0
            })
        }
        data.forEach((item) => {
            result.data.forEach(val => {
                if (item.day == val?.day) {
                    item.total_amount = val.total_amount
                }
            })
        })
        const last = data.shift()
        data.push(last)
        currWeekOptions.value = {
            title: {
                text: '本周每天销售额'
            },
            xAxis: {
                // 周一 => 周日
                data: week
            },
            series: [
                {
                    name: '销售金额',
                    data: data.map(item => ({ value: item.total_amount })),
                    type: 'bar'
                }
            ]
        }

    }
}
getCurrWeekSaleAmount()
// 本月销售额数据
const currMonthOptions = ref({})
const getCurrMonthSaleAmount = async () => {
    const result = await getMonthDaySaleAmount()
    if (result.status === 200) {
        const currDate = new Date()
        // 获取当前年份
        const currYear = currDate.getFullYear()
        // 获取当前月份 [0,11]
        const currMonth = currDate.getMonth()
        // 获取当前月份的天数: 下月最后一天等于当月最后一天
        const maxDay = new Date(currYear, currMonth + 1, 0).getDate()
        const days = new Array(maxDay).fill({ value: 0 })
        const dayData = days.map((item, index) => ({ name: index + 1, value: item.value }))
        dayData.forEach(item => {
            result.data.forEach(val => {
                if (item.name === val.day) {
                    item.value = val.total_amount
                }
            })
        })
        currMonthOptions.value = {
            title: {
                text: '本月每日销售额'
            },
            xAxis: {
                data: dayData.map(item => item.name + '日')
            },
            series: [
                {
                    data: dayData
                }
            ]
        }
    }
}
getCurrMonthSaleAmount()
// 本年度销售额数据
const currYearOptions = ref({})
const getCurrYearSaleAmount = async () => {
    const result = await getYearMonthSaleAmount()
    if (result.status === 200) {
        const years = new Array(12).fill({ value: 0 })
        const yearData = years.map((item, index) => ({ value: item.value, name: index + 1 }))
        yearData.forEach(item => {
            result.data.forEach(val => {
                if (item.name === val.month) {
                    item.value = val.total_amount
                }
            })
        })
        currYearOptions.value = {
            title: {
                text: '本年度月销售额'
            },
            xAxis: {
                data: yearData.map(item => item.name + '月')
            },
            series: [
                {
                    data: yearData,
                    type: 'line',
                    areaStyle: true
                }
            ]
        }
    }


}
getCurrYearSaleAmount()
</script>

<style>
.chart {
    height: 420px;
    border: 1px solid #ccc;
    padding: 10px;
    margin: 10px 0;
}
</style>