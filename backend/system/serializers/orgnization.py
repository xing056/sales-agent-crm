from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from . import UserSerializer
from ..models import Department, Position, Employee
from .serializer import BaseSerializer

# 部门数据表模型类序列化器
class DepartmentSerializer(BaseSerializer):
    # 部门主管
    manager=serializers.SerializerMethodField(read_only=True)
    # 虚拟属性接受客户端发送的部门主管id
    manager_id=serializers.IntegerField(write_only=True,label='部门主管')
    def get_manager(self, obj):
        if obj.manager is not None:
            # 手动调用员工数据表序列化器
            return EmployeeSerializer(obj.manager).data
        return obj.manager


    class Meta:
        model = Department
        fields = "__all__"

# 职位数据表模型类序列化器
class PositionSerializer(BaseSerializer):
    class Meta:
        model = Position
        fields = "__all__"


# 员工数据表模型类序列化器
class EmployeeSerializer(BaseSerializer):
    # 指定父级序列化器
    department = DepartmentSerializer(read_only=True, fields=["id", "name"])
    position = PositionSerializer(read_only=True, fields=["id", "name"])
    user = UserSerializer(read_only=True, fields=["id", "username", "role", "status"])
    work_no = serializers.SerializerMethodField(read_only=True)
    # 虚拟属性(额外属性)
    department_id = serializers.IntegerField(write_only=True, label="部门id")
    position_id = serializers.IntegerField(write_only=True, label="职位id")
    # required=False: 表示该字段为非必填项
    user_id = serializers.IntegerField(
        write_only=True, allow_null=True, label="用户id", required=False
    )
    # 验证客户端提交过来的user_id是否被其他账号绑定
    # value: 表示客户端传递的参数值
    def validate_user_id(self, value):
        if value:
            exists = Employee.objects.filter(user_id=value).exists()
            if exists:
                raise ValidationError('该账号已经被其他员工绑定')
        return value

    @staticmethod
    def get_work_no(obj):
        # 对工号进行格式化: 如果不足6位, 自动补0
        if obj.work_no:
            return f"{obj.work_no:06d}"
        return obj.work_no

    class Meta:
        model = Employee
        fields = "__all__"


