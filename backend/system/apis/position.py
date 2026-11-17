from system.models import Position
from system.serializers import PositionSerializer
from rest_framework.viewsets import ModelViewSet
# 职位接口类
class PositionViewSet(ModelViewSet):
    queryset = Position.objects.all()
    serializer_class = PositionSerializer
    # 临时禁用登录认证类和权限认真类
    # authentication_classes = []
    # permission_classes = []

    rbac_permissions = {
        'list': 'api:position:list',
        'retrieve': 'api:position:detail',
        'create': 'api:position:create',
        'update': 'api:position:update',
        'partial_update': 'api:position:update',
        'destroy': 'api:position:destroy',
    }