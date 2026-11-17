<template>
    <div :id="renderDom" class="chart"></div>
</template>

<script setup>
import * as echarts from 'echarts'
import { onMounted, watch } from 'vue'

// 接收父组件通过自定义属性传递的数据
const { renderDom, options } = defineProps(['renderDom', 'options'])
onMounted(() => {
    // 获取绘制容器dom对象
    const dom = document.querySelector(`#${renderDom}`)
    // 创建echarts实例
    var myChart = echarts.init(dom)
    var option = {
        title: {
            text: ''
        },
        legend: {
            orient: 'horizontal',
            left: 300
        },
        xAxis: {
            type: 'category',
            data: []
        },
        yAxis: {
            type: 'value'
        },
        tooltip: {
            trigger: 'axis',
            axisPointer: {
                type: 'shadow'
            }
        },
        // 设置图表距离绘制容器的边界的空间大小
        grid: {
            left: '3%',
            right: '4%',
            bottom: '3%',
            containLabel: true
        },
        toolbox: {
            show: true,
            feature: {
                mark: { show: true },
                dataView: { show: true, readOnly: false },
                magicType: { show: true, type: ['line', 'bar'] },
                restore: { show: true },
                saveAsImage: { show: true }
            }
        },
        // 带展示的统计数据
        series: [
            {
                showBackground: true,
                // 商品销售金额
                data: [],
                type: 'bar'
            },
            {
                showBackground: true,
                // 商品销售数量
                data: [],
                type: 'bar'
            }
        ]
    }
    option && myChart.setOption(option)
    // nextState: 被侦听数据的最新状态
    watch(() => options, (nextState) => {
        // myChart.setOption(nextState)
        option && myChart.setOption(Object.assign({}, option, nextState))
    }, {
        // 启用深度侦听: 侦听对象属性的变换
        deep: true,
        // 让侦听器处理函数立即执行一次
        immediate: true
    })

    window.addEventListener('resize',()=>{
        myChart.resize()
    })
})
</script>

<style>
.chart {
    height: 420px;
    border: 1px solid #ccc;
    padding: 10px;
    margin: 10px 0;
}
</style>