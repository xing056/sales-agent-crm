<template>
    <div :id="renderDom" class="chart">
        <!-- 绘制容器 -->
    </div>
</template>

<script setup>
import * as echarts from 'echarts'
import { watch } from 'vue';
import { onMounted } from 'vue'
// 接收父组件通过自定义属性传递的数据
const { renderDom, options } = defineProps(['renderDom', 'options'])
onMounted(() => {
    // 获取绘制容器的dom对象
    const dom = document.querySelector(`#${renderDom}`)
    // 创建echarts实例
    const instance = echarts.init(dom)
    const option = {
        title: {
            text: '',
            left: 'center'
        },
        tooltip: {
            trigger: 'item'
        },
        legend: {
            orient: 'vertical',
            left: 'left'
        },
        toolbox: {
            show: true,
            feature: {
                mark: { show: true },
                dataView: { show: true, readOnly: false },
                saveAsImage: { show: true }
            }
        },
        series: [
            {
                name: '',
                type: 'pie',
                // radius: '50%',
                radius: ['45%', '70%'],
                itemStyle: {
                    borderRadius: 10,
                    borderColor: '#fff',
                    borderWidth: 2
                },
                // data: [
                //     { value: 1048, name: 'Search Engine' },
                //     { value: 735, name: 'Direct' },
                //     { value: 580, name: 'Email' },
                //     { value: 484, name: 'Union Ads' },
                //     { value: 300, name: 'Video Ads' }
                // ],
                emphasis: {
                    itemStyle: {
                        shadowBlur: 10,
                        shadowOffsetX: 0,
                        shadowColor: 'rgba(0, 0, 0, 0.5)'
                    }
                }
            }
        ]
    }
    // 设置配置对象, 渲染图标
    instance.setOption(option)
    watch(() => options, (nextState) => {
        instance.setOption(nextState)
    })
    window.addEventListener('resize', () => {
        instance.resize()
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