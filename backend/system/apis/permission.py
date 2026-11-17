from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
# 导入权限数据表模型类
from system.models import Permission
from system.serializers.serializer import PermissionSerializer
from system.utils.authentication import CustomJwtAuth
from system.utils.permission import CustomPermission


# 权限接口类
# ModelViewSet: 自动生成 list, retrieve, create, update,partial_update,destroy, 接口方法
@extend_schema_view(
    list=extend_schema(summary='权限列表',tags=['权限管理'],description='获取权限列表'),
    retrieve=extend_schema(summary='权限详情',tags=['权限管理'], description='获取单条角色数据'),
    create=extend_schema(summary='新增权限',tags=['权限管理'], description='新增权限数据'),
    update=extend_schema(summary='更新权限',tags=['权限管理'], description='更新权限信息'),
    partial_update=extend_schema(summary='权限信息(部分更新)',tags=['权限管理'], description='更新角色信息中的部分属性字段'),
    destroy=extend_schema(summary='删除权限',tags=['权限管理'],description='删除权限数据')
)
class PermissionViewSet(ModelViewSet):
    # 指定数据集合
    queryset = Permission.objects.select_related('parent').all()
    # 指定序列化器
    serializer_class = PermissionSerializer
    # 禁用全局分页功能
    pagination_class = None
    # 可以配置自定义属性: 将来可以编写一个自定义的权限校验类, 在权限校验类型中可以获取当前客户端访问的接口方法以及对应的权限码
    # 此处的接口权限码必须和权限数据表中保存的接口权限码保持一致
    rbac_permissions={
        'list':'api:permission:list',
        'create':'api:permission:create',
        'retrieve': 'api:permission:detail',
        'update':'api:permission:update',
        'partial_update':'api:permission:update',
        'destroy':'api:permission:destroy',
    }
    # 设置登录认证类
    authentication_classes = [CustomJwtAuth]
    # 权限认证类
    permission_classes = [CustomPermission]
    # 对list方法进行重写
    def list(self, request, *args, **kwargs):
        # 将来如果添加了搜索功能, 那么这些功能需要在此处手动实现
        # self.filter_queryset: 可以继承全局配置的搜索功能...
        queryset = self.filter_queryset(Permission.objects.filter(parent_id__isnull=True).all())
        # 手动调用序列化器
        serializer = PermissionSerializer(queryset, many=True)
        # 返回查询结果
        return Response(serializer.data)

