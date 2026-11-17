from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework.viewsets import ModelViewSet
from system.models import Role
from system.serializers.serializer import RoleSerializer
from system.utils.authentication import CustomJwtAuth
from system.utils.permission import CustomPermission


# 角色接口类
@extend_schema_view(
    list=extend_schema(summary='角色列表',tags=['角色管理'], description='获取角色列表'),
    retrieve=extend_schema(summary='角色详情',tags=['角色管理'], description='获取单条角色数据'),
    create=extend_schema(summary='新增角色',tags=['角色管理'], description='新增角色数据'),
    update=extend_schema(summary='更新角色',tags=['角色管理'], description='更新角色信息'),
    partial_update=extend_schema(summary='角色信息(部分更新)',tags=['角色管理'], description='更新角色信息中的部分属性字段'),
    destroy=extend_schema(summary='删除角色',tags=['角色管理'], description='删除角色数据')
)
class RoleViewSet(ModelViewSet):
    # 指定数据集合
    queryset = Role.objects.prefetch_related('permission').all()
    # 指定序列化器
    serializer_class = RoleSerializer
    # 设置登录认证类
    authentication_classes = [CustomJwtAuth]
    # 权限认证类
    permission_classes = [CustomPermission]
    # 自定义属性指定权限代码
    rbac_permissions = {
        'list': 'api:role:list',
        'retrieve': 'api:role:detail',
        'create': 'api:role:create',
        'update': 'api:role:update',
        'partial_update': 'api:role:update',
        'destroy': 'api:role:destroy',
    }
