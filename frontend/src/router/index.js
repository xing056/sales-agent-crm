import { createRouter, createWebHistory } from 'vue-router'
import { storeToRefs } from 'pinia'
import useUserStore from '@/stores/user'
const routes = [
  {
    name: 'layout',
    path: '/',
    component: () => import('../pages/LayoutView.vue'),
    // 登录后直接落到工作台，不再是一块空白
    redirect: '/dashboard',
    meta: {
      requireLogin: true,
      title: "管理中心"
    },
    children: [
      {
        name: 'dashboard',
        path: '/dashboard',
        component: () => import('../pages/DashboardView.vue'),
        meta: {
          requireLogin: true,
          title: "工作台"
        }
      },
      {
        name: 'perm',
        path: '/permission',
        component: () => import('../pages/perm/PermView.vue'),
        meta: {
          requireLogin: true,
          title: "权限管理"
        },
      },
      {
        name: 'role',
        path: '/role',
        component: () => import('../pages/role/RoleView.vue'),
        meta: {
          requireLogin: true,
          title: "角色管理"
        },
      },
      {
        name: 'menu',
        path: '/menu',
        component: () => import('../pages/menu/MenuView.vue'),
        meta: {
          requireLogin: true,
          title: "菜单管理"
        },
      },
      {
        name: 'user',
        path: '/user',
        component: () => import('../pages/user/UserView.vue'),
        meta: {
          requireLogin: true,
          title: "账号管理"
        },
      },
      {
        name: 'department',
        path: '/department',
        component: () => import('../pages/department/DepartmentView.vue'),
        meta: {
          requireLogin: true,
          title: "部门管理"
        },
      },
      {
        name: 'departmentEmp',
        path: '/departmentEmp/:id',
        component: () => import('../pages/department/DepartmentEmp.vue'),
        meta: {
          requireLogin: true,
          title: "部门员工"
        },
      },
      {
        name: 'position',
        path: '/position',
        component: () => import('../pages/position/PositionView.vue'),
        meta: {
          requireLogin: true,
          title: "职位管理"
        },
      },
      {
        name: 'employee',
        path: '/employee',
        component: () => import('../pages/employee/EmployeeView.vue'),
        meta: {
          requireLogin: true,
          title: "员工管理"
        },
      },

      {
        name: 'empDetail',
        path: '/empDetail/:id',
        component: () => import('../pages/employee/EmployeeDetail.vue'),
        meta: {
          requireLogin: true,
          title: "员工资料"
        },
      },
      {
        name: 'profile',
        path: '/profile',
        component: () => import('../pages/user/UserProfile.vue'),
        meta: {
          requireLogin: true,
          title: "个人资料"
        },
      },
      {
        name: 'customerSource',
        path: '/customerSource',
        component: () => import('../pages/customer_source/CustomerSource.vue'),
        meta: {
          requireLogin: true,
          title: "客户来源管理"
        },
      },
      {
        name: 'customer',
        path: '/customer',
        component: () => import('../pages/customer/CustomerView.vue'),
        meta: {
          requireLogin: true,
          title: "客户管理"
        },
      },
      {
        name: 'customerTracking',
        path: '/customer/:id/tracking',
        component: () => import('../pages/customer/TrackingListView.vue'),
        meta: {
          requireLogin: true,
          title: "客户跟踪记录"
        },
      },
      {
        name: 'customerDetail',
        path: '/customerDetail/:id',
        component: () => import('../pages/customer/CustomerDetail.vue'),
        meta: {
          requireLogin: true,
          title: "客户详情"
        },
      },
      {
        name: 'customerOfMe',
        path: '/customerOfMe',
        component: () => import('../pages/customer/CustomerOfMe.vue'),
        meta: {
          requireLogin: true,
          title: "我的客户"
        },
      },
      {
        name: 'allCustomerTracking',
        path: '/customerTracking',
        component: () => import('../pages/customer_tracking/CustomerTracking.vue'),
        meta: {
          requireLogin: true,
          title: "客户跟踪记录管理"
        }
      },
      {
        name: 'category',
        path: '/category',
        component: () => import('../pages/category/CategoryView.vue'),
        meta: {
          requireLogin: true,
          title: "商品分类管理"
        }
      },
      {
        name: 'product',
        path: '/product',
        component: () => import('../pages/product/ProductView.vue'),
        meta: {
          requireLogin: true,
          title: "商品管理"
        }
      },
      {
        name: 'saleOrder',
        path: '/saleOrder',
        component: () => import('../pages/sale_order/OrderView.vue'),
        meta: {
          requireLogin: true,
          title: "销售订单管理"
        }
      },
      {
        name: 'saleOrderDetail',
        path: '/saleOrderDetail/:id',
        component: () => import('../pages/sale_order/OrderDetailView.vue'),
        meta: {
          requireLogin: true,
          title: "销售订单详情"
        }
      },
      {
        name: 'orderCreate',
        path: '/orderCreate',
        component: () => import('../pages/sale_order/OrderCreateView.vue'),
        meta: {
          requireLogin: true,
          title: "创建订单"
        }
      },
      {
        name: 'stat',
        path: '/stat',
        component: () => import('../pages/stat/StatView.vue'),
        meta: {
          requireLogin: true,
          title: "销量统计"
        }
      },
      {
        name: '员工销售提成',
        path: '/commission',
        component: () => import('../pages/commission/CommissionView.vue'),
        meta: {
          requireLogin: true,
          title: "员工销售提成"
        }
      },
       {
        name: '我的销售提成',
        path: '/myCommission',
        component: () => import('../pages/commission/MyCommissionView.vue'),
        meta: {
          requireLogin: true,
          title: "我的销售提成"
        }
      },
      {
        name: 'Tokens 用量',
        path: '/llm-usage',
        component: () => import('../pages/llm_usage/UsageView.vue'),
        meta: {
          requireLogin: true,
          title: "Tokens 用量"
        }
      },
      {
        name: 'notfound',
        path: '/:pathMatch(.*)',
        component: () => import('../pages/NotFound.vue'),
        meta: {
          requireLogin: true,
          title: "404-页面不存在"
        },
      }
    ]
  },
  {
    name: 'login',
    path: '/login',
    component: () => import('../pages/LoginView.vue'),
    meta: {
      requireLogin: false,
      title: "管理员登录"
    }
  }
]
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
})

// 路由导航守卫
router.beforeResolve((to, from, next) => {
  // 表示当前页面需要登录
  if (to.meta.requireLogin) {
    // 检测登录状态
    const userStore = useUserStore()
    const { accessToken, currRole } = storeToRefs(userStore)
    // 未登录状态
    if (!accessToken.value) {
      return next({ name: 'login' })
    }
    // 用户可以访问的页面路径地址
    let allowUrl = ['/', '/profile']
    allowUrl = allowUrl.concat(currRole.value.link_url)
    //   /empDetail/10
    const toPath = to.path.replace(/\/\d+/, '/:id')
    // 判断即将访问的页面是否在权限范围内
    if (!allowUrl.includes(toPath)) {
      // return next({ name: "layout" })
    }
  }
  next()
  // 动态设置页面标题
  if (to.meta.title) {
    document.title = to.meta.title
  }
})

export default router
