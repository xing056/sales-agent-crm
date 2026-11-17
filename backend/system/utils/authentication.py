from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed, NotAuthenticated
# TokenError: 令牌过期 / 签名不对 / 不是合法 JWT 的统一异常
# （ExpiredTokenError 是它的子类，接 TokenError 就把两种都盖住了）
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import AccessToken
from system.models import User
class CustomJwtAuth(BaseAuthentication):
    def authenticate_header(self, request):
        """DRF 只有看到这个方法，才会把认证失败渲染成 401。

        没有它的时候，未登录、令牌失效一律返回 403 —— 前端就没法区分
        "你没有这个权限"和"你的登录过期了"，也就不会跳回登录页。
        """
        return "Bearer"

    # 重写登录认证方法
    def authenticate(self, request):
        # 接受客户端发送的登录凭证access_token
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            raise NotAuthenticated({'message': '没有检测到登录凭证access_token'})
        access_token = auth_header.split('Bearer ')[1].strip()
        if not access_token:
            raise NotAuthenticated({'message': '没有检测到登录凭证access_token'})
        try:
            # 解析access_token：签名校验、有效期校验都在这一步
            payload = AccessToken(access_token)
        except TokenError as exc:
            # 过期 / 签名不对 / 不是合法 JWT 全部落在这里。
            # 以前只接了 ExpiredTokenError，其余 TokenError 会一路冒到最外层
            # 变成 500 + HTML 错误页，前端拿到的是一坨 HTML 而不是错误消息。
            reason = '已过期' if 'expired' in str(exc).lower() else '无效'
            raise AuthenticationFailed({'message': f'access_token登录凭证{reason}，请重新登录'})
        # 获取用户id
        user_id=payload.get('user_id')
        try:
            # 根据user_id查询用户表
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            raise AuthenticationFailed({
                'message':'用户信息不存在'
            })
        # 需要返回user和access_token
        return user, access_token
