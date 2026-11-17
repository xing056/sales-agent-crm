from django.contrib.auth.models import AnonymousUser
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import BasePermission
from ..models import Permission

# 自定义接口权限验证类
class CustomPermission(BasePermission):
    # 重写has_permission方法
    # view: 当前访问的接口方法对象, 保存了当前接口方法相关信息
    def has_permission(self, request, view):
        # 未登录直接拒绝 —— 这一步必须放在最前面
        # 之前它排在"没有 rbac_permissions 就放行"之后，等于给所有未定义
        # 权限码的接口（department / stat / common 等）留了匿名后门。
        # 注意：本项目的 User 是普通 models.Model，没有 is_authenticated 属性，
        # 所以只能用 AnonymousUser 判断登录态。
        user = request.user
        if user is None or isinstance(user, AnonymousUser):
            raise PermissionDenied({"message": "没有登录, 请先登录"})
        # 接口方法名称 view.action
        action = getattr(view, "action", None)
        # 获取当前接口方法所在类的权限列表
        rbac_perms = getattr(view, "rbac_permissions", None)
        # 如果某个接口类中没有定义自定义属性rbac_permissions
        if not rbac_perms:
            # 只要求"已登录"，不细分权限码（如 common 下的拼音/二维码/上传）
            return True
        # 当前访问接口方法的权限编码:使用get方法获取字段属性, 防止属性不存在, 代码报错
        curr_code = rbac_perms.get(action)
        # 是否为超级用户
        if user.is_superuser:
            return True
        # 获取当前登录用户对象所有的接口权限编码
        all_code = [
            val.code for item in user.role.all() for val in item.permission.all()
        ]
        # 查询公开类型的接口权限编码
        public_permission_code = [
            item["code"]
            for item in Permission.objects.filter(is_public=True).values("code")
        ]
        # 如果当前访问接口权限编码不在当前登录账号拥有的接口权限编码列表中
        if curr_code not in all_code + public_permission_code:
            raise PermissionDenied({"message": "暂无接口访问权限"})
        # 返回True表示有访问权限, 如果没有访问权限, 抛出异常
        return True
