import django_filters
from django.contrib.auth.hashers import check_password
from drf_spectacular.utils import extend_schema, OpenApiParameter, extend_schema_view
from rest_framework import status, serializers
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework.throttling import AnonRateThrottle
from system.models import User, Menu
from system.serializers import UserSerializer, EmployeeSerializer
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken

# 自定义登录认证类

class LoginThrottle(AnonRateThrottle):
    """登录接口按 IP 限流。

    没有这道闸，任何人都能对这个接口做字典爆破 —— 而演示账号的密码
    通常是公开的弱口令，一旦被猜到就等于拿到了整套 RBAC 的第一个立足点。
    速率见 settings.DEFAULT_THROTTLE_RATES["login"]，默认 10 次/分钟。
    """

    scope = "login"
from ..utils.authentication import CustomJwtAuth
from ..utils.permission import CustomPermission
from ..utils.util import get_user_menu


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(label="登录用户", required=True)
    password = serializers.CharField(label="用户密码", required=True)


class LoginResponseSerializer(serializers.Serializer):
    message = serializers.CharField(label="错误信息", required=True)


# 自定义搜索工具类
class UserFilter(django_filters.FilterSet):
    # 忽略大小写, 只要搜索关键词包含于字段值中即可
    # 如果属性名和字段名成相同, 则可以省略field_name关键字参数
    username=django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        # 指定模型类
        model=User
        # 指定搜索字段
        fields=('username',)


@extend_schema_view(
    list=extend_schema(
        summary="用户列表", tags=["用户管理"], description="获取用户列表接口"
    ),
    retrieve=extend_schema(
        summary="用户详情", tags=["用户管理"], description="获取单个用户数据"
    ),
    create=extend_schema(
        summary="新增用户", tags=["用户管理"], description="新增用户数据"
    ),
    update=extend_schema(
        summary="更新用户", tags=["用户管理"], description="更新用户信息"
    ),
    partial_update=extend_schema(
        summary="用户信息(部分更新)",
        tags=["用户管理"],
        description="更新用户信息中的部分属性字段",
    ),
    destroy=extend_schema(
        summary="删除用户", tags=["用户管理"], description="删除用户数据"
    ),
)
class UserViewSet(ModelViewSet):
    queryset = User.objects.prefetch_related("role").all()
    serializer_class = UserSerializer
    # 登录认证类
    # authentication_classes = [CustomJwtAuth]
    # 自定义属性保存接口方法的权限编码
    rbac_permissions = {
        "list": "api:user:list",
        "retrieve": "api:user:detail",
        "create": "api:user:create",
        "update": "api:user:update",
        "partial_update": "api:user:update",
        "destroy": "api:user:destroy",
        "whoami": "api:user:whoami",
    }
    # 用户登录
    # authentication_classes: 指定登录认证类
    # permission_classes: 指定权限认证类
    # 设置登录认证类
    authentication_classes = [CustomJwtAuth]
    # 权限认证类
    permission_classes = [CustomPermission]
    # 配置自定义搜索工具类
    filterset_class = UserFilter
    # 配置搜索字段: 定值搜索  select * from user where username=''
    filterset_fields=['username']

    @extend_schema(
        summary="用户登录",
        description="用户登录接口",
        tags=["用户管理"],
        # 设置请求体参数, 默认请求体参数参考数据表模型类
        request=LoginSerializer,
        responses={200: UserSerializer, 400: LoginResponseSerializer},
        # 指定查询参数
        # parameters=[
        #     OpenApiParameter(name='username', description='登录用户',required=True),
        #     OpenApiParameter(name='password', description='用户密码', required=True),
        # ]
    )
    @action(["post"], detail=False, authentication_classes=[], permission_classes=[],
            throttle_classes=[LoginThrottle])
    def login(self, request):
        output = {"message": "success"}
        # 接受客户端发送过来的用户和密码
        data = request.data
        username = data.get("username")
        password = data.get("password")
        if not username:
            output["message"] = "参数错误:缺少参数username"
            return Response(output, status=status.HTTP_400_BAD_REQUEST)
        if not password:
            output["message"] = "参数错误:缺少参数password"
            return Response(output, status=status.HTTP_400_BAD_REQUEST)
        try:
            # 根据用户名username查询用户表
            # prefetch_related:针对多对多关系的查询进行优化
            # .prefetch_related('role__permission')
            user = User.objects.get(username=username)
            # 验证密码是否正确
            if not check_password(password, user.password):
                output["message"] = "密码错误"
                return Response(output, status=status.HTTP_400_BAD_REQUEST)
            # 用户基本信息
            output["data"] = UserSerializer(user).data
            # 获取用户菜单数据
            output["data"]["role"] = get_user_menu(user)
            # 密码正确: 生成登录凭着jwt: json web token
            refresh = RefreshToken.for_user(user)
            # 将access_token转换为字符串类型
            output["refresh_token"] = str(refresh)
            output["access_token"] = str(refresh.access_token)
            # 获取账号对应的员工资料
            if getattr(user, "employee", None):
                # 手动对员工对象进行序列化
                output["employee"] = EmployeeSerializer(
                    user.employee, fields=["id", "work_no", "name"]
                ).data
        except User.DoesNotExist:
            output["message"] = "用户不存在"
            return Response(output, status=status.HTTP_400_BAD_REQUEST)
        return Response(output)

    @action(["get"], detail=False)
    def whoami(self, request):
        """我是谁：只凭令牌回答，不接受任何自报字段。

        用途：智能体服务拿到令牌后，用它确认"这个令牌背后到底是谁"，
        再把模型用量记到这个人头上。
        为什么不直接从请求体读用户名：那等于让员工自己填账本上的名字 ——
        他可以把消耗记到同事头上，看板立刻就不可信了。
        """
        user = request.user
        data = {
            "id": user.id,
            "username": user.username,
            "is_superuser": user.is_superuser,
        }
        # 员工资料可能不存在（有些账号只用来登录，不挂员工）
        employee = getattr(user, "employee", None)
        if employee is not None:
            data["employee"] = {
                "id": employee.id,
                "name": employee.name,
                "work_no": employee.work_no,
            }
            department = getattr(employee, "department", None)
            if department is not None:
                data["employee"]["department"] = {
                    "id": department.id,
                    "name": department.name,
                }
        return Response(data)
