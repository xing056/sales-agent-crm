from django.contrib.auth.hashers import make_password
from django.db import transaction
from rest_framework import serializers
# 导入数据表模型类
from ..models import Permission, Role, User, Menu
# 自定义基础序列化器类
class BaseSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        # 取出多余参数, 防止多余参数传递给父类, 导致报错
        fields = kwargs.pop("fields", None)
        super().__init__(*args, **kwargs)
        # 如果调用的时候通过fields参数指定了需要的字段, 那么只返回指定字段, 其余字段不返回
        if fields is not None:
            all_fields = set(self.fields)
            allow_fields = set(fields or [])
            for field in all_fields - allow_fields:
                # 删除不需要的字段
                self.fields.pop(field)
       


# 权限数据表模型类的序列化器
class PermissionSerializer(BaseSerializer):
    # 添加了一个额外属性字段, 该属性字段的值通过一个方法产生
    children = serializers.SerializerMethodField(method_name="generic_children")

    class Meta:
        # 指定数据表模型类
        model = Permission
        # 指定需要进行序列化的字段
        fields = "__all__"

    # obj: 系统参数, 表示当前要序列化的数据实例对象
    def generic_children(self, obj):
        # 当前要序列化的数据对象是否存在children属性
        if obj.children.exists():
            # 如果存在, 则调用当前序列化器对子级数据进行序列化
            return PermissionSerializer(obj.children, many=True).data
        return []


# 角色数据表序列化器
class RoleSerializer(BaseSerializer):
    # 指定父级序列化器
    permission = PermissionSerializer(many=True, read_only=True)
    # 接受客户端传递的权限id数据, 格式如:[1,2,3]
    permission_ids = serializers.PrimaryKeyRelatedField(
        queryset=Permission.objects.all(), many=True, write_only=True
    )

    class Meta:
        model = Role
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        # 取出多余参数, 防止多余参数传递给父类, 导致报错
        fields = kwargs.pop("fields", None)
        super().__init__(*args, **kwargs)
        # 如果调用的时候通过fields参数指定了需要的字段, 那么只返回指定字段, 其余字段不返回
        if fields is not None:
            all_fields = set(self.fields)
            allow_fields = set(fields or [])
            for field in all_fields - allow_fields:
                # 删除不需要的字段
                self.fields.pop(field)

    # 对create方法进行重写
    # validated_data: 表示通过验证的客户端参数
    def create(self, validated_data):
        # 手动启用事务功能
        with transaction.atomic():
            # validated_data['permission_ids']
            # 取出多余参数
            permission_ids = validated_data.pop("permission_ids", None)
            # 向角色表中写入数据
            role = Role.objects.create(**validated_data)
            # 向角色权限表中写入数据: 向角色权限表中写入数据
            role.permission.set(permission_ids)
        # 返回新增角色即可
        return role

    # 重写更新方法
    # instance: 表示即将更新的角色对象
    # validated_data: 校验通过的客户端参数
    def update(self, instance, validated_data):
        # 手动启用事务
        with transaction.atomic():
            permission_ids = validated_data.pop("permission_ids", None)
            # 更新角色表中的字段信息: 调用父类的update方法
            super().update(instance, validated_data)
            # 更新角色权限表中的数据
            instance.permission.set(permission_ids)
        # 返回更新角色对象
        return instance


# 用户模型序列化器
class UserSerializer(BaseSerializer):
    # 当前账号关联的员工数据
    employee=serializers.SerializerMethodField(method_name='get_employee')
    def get_employee(self,obj):
        employee=getattr(obj,'employee',None)
        # 如果当前用户关联了员工数据, 则返回员工数据
        if employee:
            # 局部导入, 避免全局导入导入引发的循环导入问题
            from . import EmployeeSerializer
            return EmployeeSerializer(employee).data
        return None
    # 设置父级序列化器
    role = RoleSerializer(
        many=True, read_only=True, fields=["id", "name", "status", "remark"]
    )
    # 角色id数据
    role_ids = serializers.PrimaryKeyRelatedField(
        label="角色id", queryset=Role.objects.all(), many=True, write_only=True
    )
    # 密码字段不展示
    password = serializers.CharField(write_only=True, label="密码")

    class Meta:
        model = User
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        # 必须调用父类初始化方法__init__
        super().__init__(*args, **kwargs)
        if self.instance:
            # 更新操作: password参数可选
            self.fields["password"].required = False

    # 对create方法进行重写
    # validated_data: 表示通过验证的客户端参数
    def create(self, validated_data):
        # 手动启用事务功能
        with transaction.atomic():
            # validated_data['permission_ids']
            # 取出多余参数
            role_ids = validated_data.pop("role_ids", None)
            # 对密码进行加密
            validated_data["password"] = make_password(validated_data["password"])
            # 向角色表中写入数据
            # user = User.objects.create(**validated_data)
            # 调用父类中的create方法实现新增
            user = super().create(validated_data)
            # 向用户角色表中写入数据: 向角色权限表中写入数据
            if role_ids:
                user.role.set(role_ids)
        # 返回新增角色即可
        return user

    # 重写更新方法
    # instance: 表示即将更新的角色对象
    # validated_data: 校验通过的客户端参数
    def update(self, instance, validated_data):
        # 手动启用事务
        with transaction.atomic():
            # 对密码进行加密
            if validated_data.get("password"):
                validated_data["password"] = make_password(validated_data["password"])
            # 更新用户表中的字段信息
            # for attr,value in validated_data.items():
            #     # 动态设置对象属性
            #     setattr(instance, attr, value)
            # # 保存更新操作
            # instance.save()
            # 调用父类的update方法
            super().update(instance, validated_data)
            role_ids=validated_data.get("role_ids", None)
            if role_ids:
                # 更新用户角色表中的数据
                instance.role.set(role_ids)
        # 返回更新角色对象
        return instance


# 业务数据里嵌套"这个人是谁"的最小字段集
class UserBriefSerializer(BaseSerializer):
    """客户 / 订单 / 提成接口里嵌的 user 只用这个，不用完整的 UserSerializer。

    【为什么要拆这个】
        完整的 UserSerializer 会带 phone、email、role、employee（再往下是部门、
        职位），于是一个客户详情响应就把归属销售的账号、手机、邮箱、组织关系
        全吐出来了。拿这个接口遍历一遍 id，等于把公司通讯录抄下来。
        业务接口真正需要的只有"是谁"——id、账号、员工姓名，够前端用了。

    【不影响到哪儿】
        登录接口和账号管理页面仍然用 UserSerializer（那里本来就要看全量），
        只有"顺带展示归属人"的场景才换成它。
    """

    employee = serializers.SerializerMethodField(method_name="get_employee")

    def get_employee(self, obj):
        employee = getattr(obj, "employee", None)
        if not employee:
            return None
        # 只给 id 和姓名：前端表格显示姓名，点进去用 id 跳转
        return {"id": employee.id, "name": employee.name}

    class Meta:
        model = User
        fields = ["id", "username", "employee"]


# 菜单模型类序列化器类
class MenuSerializer(BaseSerializer):
    # 添加了一个额外属性字段, 该属性字段的值通过一个方法产生
    children = serializers.SerializerMethodField()

    class Meta:
        model = Menu
        fields = "__all__"

    def get_children(self, obj):
        if obj.children.exists():
            return MenuSerializer(obj.children, many=True).data
        return []
