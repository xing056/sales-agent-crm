from rest_framework.viewsets import ModelViewSet
from system.models import CustomerTracking
from system.serializers import CustomerTrackingSerializer

# 客户跟踪记录接口类
class CustomerTrackingViewSet(ModelViewSet):
    queryset = CustomerTracking.objects.all()
    serializer_class = CustomerTrackingSerializer
    # 临时禁用登录认证和权限验证
    # authentication_classes = []
    # permission_classes = []
    # 定义接口权限编码
    rbac_permissions={
        'list':'api:customer_tracking:list',
        'retrieve': 'api:customer_tracking:detail',
        'create': 'api:customer_tracking:create',
        'update': 'api:customer_tracking:update',
        'partial_update': 'api:customer_tracking:update',
        'destroy': 'api:customer_tracking:destroy',
    }
    # 配置搜索字段
    filterset_fields = ['customer_id','user_id']

    def get_queryset(self):
        """行级隔离：非超管只能看自己写的跟踪记录。

        目前普通销售没有 api:customer_tracking:list 权限码，所以被 403 挡在门外，
        看起来"没问题"。但只要哪天给某个角色开了这个权限，没有这段过滤
        就等于把全公司的客户跟进内容一次开放 —— 防御要跟着权限走，不能靠"暂时没开"。
        """
        queryset = super().get_queryset()
        user = self.request.user
        if user.is_superuser:
            return queryset
        return queryset.filter(user_id=user.id)

    def perform_create(self, serializer):
        # 获取当前登录账号数据
        user=self.request.user
        serializer.validated_data['user_id']=user.id
        serializer.save()

