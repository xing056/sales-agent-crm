from django.urls import path, include
from rest_framework import routers
# 导入接口类
from system.apis import *
# 创建路由实例对象
router=routers.DefaultRouter()
# 注册路由规则
router.register(r'permission',PermissionViewSet,basename='permission' )
router.register(r'role',RoleViewSet,basename='role' )
router.register(r'user',UserViewSet,basename='user' )
router.register(r'menu',MenuViewSet,basename='menu' )
router.register(r'department',DepartmentViewSet,basename='department' )
router.register(r'position',PositionViewSet,basename='position' )
router.register(r'employee',EmployeeViewSet,basename='employee' )
router.register(r'common',CommonViewSet,basename='common' )
router.register(r'customer_source',CustomerSourceViewSet,basename='customer_source' )
router.register(r'customer',CustomerViewSet,basename='customer' )
router.register(r'customer_tracking',CustomerTrackingViewSet,basename='customer_tracking' )
router.register(r'category',CategoryViewSet,basename='category' )
router.register(r'product',ProductViewSet,basename='product' )
router.register(r'sale_order',SaleOrderViewSet,basename='sale_order' )
router.register(r'sale_order_item',SaleOrderItemViewSet,basename='sale_order_item' )
router.register(r'stat',StatViewSet,basename='stat' )
router.register(r'commission',CommissionViewSet,basename='commission' )
router.register(r'llm_usage',LlmUsageViewSet,basename='llm_usage' )

urlpatterns = [
    # 放在 include(router.urls) 之前：否则 /llm_usage/report/ 会被
    # 详情路由 /llm_usage/{pk}/ 抢走（pk 匹配到字符串 "report"），报 405。
    path('llm_usage/report/',LlmUsageReportView.as_view(),name='llm_usage_report' ),
    path('',include(router.urls)),
]