from rest_framework.viewsets import ModelViewSet
from system.models import CustomerSource
from system.serializers import CustomerSourceSerializer

# 客户来源接口类
class CustomerSourceViewSet(ModelViewSet):
    queryset = CustomerSource.objects.all()
    serializer_class = CustomerSourceSerializer
    # 临时禁用登录认证和权限认证
    # authentication_classes =[]
    # permission_classes = []
    # 接口方法权限编码
    rbac_permissions={
        'list':'api:customer_source:list',
        'create': 'api:customer_source:create',
        'retrieve': 'api:customer_source:detail',
        'update': 'api:customer_source:update',
        'partial_update': 'api:customer_source:update',
        'destroy': 'api:customer_source:destroy',
    }