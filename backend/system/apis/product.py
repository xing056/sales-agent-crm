from rest_framework.viewsets import ModelViewSet
from system.models import Product
from system.serializers import ProductSerializer

class ProductViewSet(ModelViewSet):
    queryset=Product.objects.all()
    serializer_class=ProductSerializer
    
    # 临时禁用登录认证和权限认证
    # authentication_classes=[]
    # permission_classes=[]

    # 设置接口权限码
    rbac_permissions={
        "list":"api:product:list",
        "retrieve":"api:product:detail",
        "create":"api:product:create",
        "update":"api:product:update",
        "partial_update":"api:product:update",
        "destroy":"api:product:destroy",
    }