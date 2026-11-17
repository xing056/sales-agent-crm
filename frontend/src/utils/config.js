import { Setting, GoodsFilled, UserFilled, Goods, User } from '@element-plus/icons-vue'
// 菜单类型
export const menuType = {
    dir: { value: '目录', color: 'primary' },
    nav: { value: '导航', color: 'success' },
    link: { value: '链接', color: 'warning' },
    btn: { value: '按钮', color: 'danger' },
}

// 可选的菜单图标
export const icons = { Setting, GoodsFilled, UserFilled, Goods, User }

// 学历配置
export const educationLevel = {
    1: { 'value': 1, label: '高中及以下', color: 'danger' },
    2: { 'value': 2, label: '专科', color: 'warning' },
    3: { 'value': 3, label: '本科', color: 'info' },
    4: { 'value': 4, label: '硕士', color: 'success' },
    5: { 'value': 5, label: '博士', color: 'primary' },
}

// 跟踪方式
export const trackingWay={
    1:{value:'1',label:'微信'},
    2:{value:'2',label:'电话'},
    3:{value:'3',label:'上门'},
}
// 支付方式
export const payWay={
    'wxpay':{value:'wxpay',label:'微信支付'},
    'alipay':{value:'alipay',label:'支付宝支付'},
    'bank':{value:'bank',label:'银行转账'},
    'cash':{value:'cash',label:'现金支付'},
}