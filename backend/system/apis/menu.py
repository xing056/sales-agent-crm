from drf_spectacular.utils import extend_schema_view, extend_schema
from jsonschema.validators import extend
from rest_framework.decorators import authentication_classes,permission_classes
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from system.models import Menu, Permission
from system.serializers.serializer import MenuSerializer
from system.utils.authentication import CustomJwtAuth
from system.utils.permission import CustomPermission

@extend_schema_view(
    list=extend_schema(summary='菜单列表',tags=['菜单管理'],description='获取菜单列表'),
    retrieve=extend_schema(summary='菜单详情',tags=['菜单管理'], description='获取单条用户数据'),
    create=extend_schema(summary='新增菜单',tags=['菜单管理'], description='新增菜单数据'),
    update=extend_schema(summary='更新菜单',tags=['菜单管理'], description='更新菜单信息'),
    partial_update=extend_schema(summary='菜单信息(部分更新)',tags=['菜单管理'], description='更新菜单信息中的部分属性字段'),
    destroy=extend_schema(summary='删除菜单',tags=['菜单管理'],description='删除菜单数据')
)
@authentication_classes([CustomJwtAuth])
@permission_classes([CustomPermission])
class MenuViewSet(ModelViewSet):
    queryset = Menu.objects.select_related('parent').all()
    serializer_class = MenuSerializer
    # 自定义属性指定权限代码
    rbac_permissions = {
        'list': 'api:menu:list',
        'retrieve': 'api:menu:detail',
        'create': 'api:menu:create',
        'update': 'api:menu:update',
        'partial_update': 'api:menu:update',
        'destroy': 'api:menu:destroy',
    }
    # 设置登录认证类
    # authentication_classes = [CustomJwtAuth]
    # 对list方法进行重写
    def list(self, request, *args, **kwargs):
        # 将来如果添加了搜索功能, 那么这些功能需要在此处手动实现
        # self.filter_queryset: 可以继承全局配置的搜索功能...
        queryset = self.filter_queryset(Menu.objects.filter(parent_id__isnull=True).all())
        # 手动调用序列化器
        serializer = MenuSerializer(queryset, many=True)
        # 返回查询结果
        return Response(serializer.data)
    def perform_create(self, serializer):
        permission_id=serializer.validated_data.get('permission_id')
        if permission_id:
            # 调用模型类中的自定义方法
            # 根据permission_id查询permission_code
            serializer.validated_data['permission_code'] = Permission.get_permission_code(permission_id)
        serializer.save()
    def perform_update(self, serializer):
        permission_id=serializer.validated_data.get('permission_id')
        if permission_id:
            # 调用模型类中的自定义方法
            # 根据permission_id查询permission_code
            serializer.validated_data['permission_code']=Permission.get_permission_code(permission_id)
        serializer.save()