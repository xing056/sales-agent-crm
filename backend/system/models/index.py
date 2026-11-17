from django.db import models


# 权限数据表模型类
class Permission(models.Model):
    # 单表自引用
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, related_name="children", null=True, blank=True
    )
    name = models.CharField(max_length=50, unique=True, verbose_name="权限名称")
    code = models.CharField(max_length=50, unique=True, verbose_name="权限编码")
    url = models.CharField(max_length=100, null=True, verbose_name="接口地址")
    method = models.CharField(max_length=20, null=True, verbose_name="接口请求方式")
    status = models.BooleanField(default=True, verbose_name="权限状态")
    is_public = models.BooleanField(default=False, verbose_name="是否为公开类型")

    class Meta:
        db_table = "sys_permission"
        ordering = ["id"]

    # 定义自定义方法: 可以通过模型类实例对象直接调用
    # permission_id:权限id
    @classmethod
    def get_permission_code(cls, permission_id):
        # 根据id查询到权限对象
        permission = cls.objects.get(pk=permission_id)
        # 返回权限对象中的code属性(权限编码)
        return permission.code


# 角色数据表模型类
class Role(models.Model):
    # 和权限表之间进行关联
    # related_name:如果查询的是权限表, 如何获取对应的角色数据
    permission = models.ManyToManyField(Permission, related_name="role")
    name = models.CharField(max_length=50, unique=True, verbose_name="角色名称")
    remark = models.CharField(max_length=200, verbose_name="角色说明")
    status = models.BooleanField(default=1, verbose_name="角色状态,1-启用0-禁用")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="新增时间")

    class Meta:
        db_table = "sys_role"
        ordering = ["id"]


#   用户数据表模型类
class User(models.Model):
    # 和角色表之间进行关联
    role = models.ManyToManyField(Role, related_name="user")
    username = models.CharField(max_length=50, unique=True, verbose_name="用户名")
    password = models.CharField(max_length=128, verbose_name="密码")
    phone = models.CharField(max_length=11, unique=True,null=True,blank=True, verbose_name="手机号码")
    email = models.CharField(max_length=50, unique=True,null=True,blank=True, verbose_name="邮箱地址")
    status = models.BooleanField(default=True, verbose_name="账号状态")
    # 是否为超级用户
    is_superuser = models.BooleanField(default=False, verbose_name="是否为超级用户")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        db_table = "sys_user"
        ordering = ["id"]


# 菜单数据表模型类
class Menu(models.Model):
    menu_type_choice = [
        ("dir", "目录"),
        ("nav", "导航"),
        ("link", "链接"),
        ("btn", "按钮"),
    ]
    parent = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        related_name="children",
        null=True,
        blank=True,
        verbose_name="父级菜单",
    )
    permission_id = models.IntegerField(null=True, blank=True, verbose_name="权限id")
    permission_code = models.CharField(
        max_length=50, null=True, blank=True, verbose_name="权限编码"
    )
    title = models.CharField(max_length=20, unique=True, verbose_name="菜单标题")
    path = models.CharField(
        max_length=100, null=True, blank=True, verbose_name="菜单链接地址"
    )
    icon = models.CharField(
        max_length=20, null=True, blank=True, verbose_name="菜单图标"
    )
    sort_order = models.SmallIntegerField(default=0, verbose_name="菜单排序")
    status = models.BooleanField(default=True, verbose_name="菜单状态")
    menu_type = models.CharField(
        max_length=20, choices=menu_type_choice, default="nav", verbose_name="菜单类型"
    )
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        db_table = "sys_menu"
        ordering = ["sort_order", "id"]
