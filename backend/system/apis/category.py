from rest_framework.viewsets import ModelViewSet
from system.models import Category
from system.serializers import CategorySerializer
from ..utils.util import build_tree
from rest_framework.response import Response

# 商品分类接口类
class CategoryViewSet(ModelViewSet):
    queryset=Category.objects.all()
    serializer_class=CategorySerializer
    
    # 临时禁用登录认证和权限认证
    # authentication_classes=[]
    # permission_classes=[]

    # 设置接口权限码
    rbac_permissions={
        "list":"api:category:list",
        "retrieve":"api:category:detail",
        "create":"api:category:create",
        "update":"api:category:update",
        "partial_update":"api:category:update",
        "destroy":"api:category:destroy",
    }
    
    # 对list接口方法进行重写, 将扁平列表转换成树形列表
    def list(self, request, *args, **kwargs):
        # 获取所有分类数据
        queryset=self.filter_queryset(self.get_queryset())
        # 手动调用序列化器
        serializer=CategorySerializer(queryset, many=True)
        # 调用工具函数将扁平列表转换为树形列表
        result=build_tree(serializer.data,parent_key='parent')
        return Response(result)
