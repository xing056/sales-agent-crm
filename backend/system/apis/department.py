from django.db import transaction
from rest_framework.exceptions import APIException
from rest_framework.decorators import action
from rest_framework.response import Response
from ..models import Department, Employee
from ..serializers import DepartmentSerializer
from rest_framework.viewsets import ModelViewSet
from ..utils.util import build_tree
# 部门接口类
class DepartmentViewSet(ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    # 认证/权限沿用全局配置（CustomJwtAuth + CustomPermission），不再单独放行
    # authentication_classes = []
    # permission_classes = []
    rbac_permissions={
        'list':'api:department:list',
        'retrieve': 'api:department:detail',
        'create': 'api:department:create',
        'update': 'api:department:update',
        'partial_update': 'api:department:update',
        'destroy': 'api:department:destroy',
        'set_manager': 'api:department:set_manager',
    }
    # 对list接口方法进行重写, 得到一个树形结构的列表
    def list(self, request, *args, **kwargs):
        # 获取数据集合
        queryset = self.filter_queryset(self.get_queryset())
        # 手动调佣序列化器
        serializer = self.get_serializer(queryset, many=True)
        # 将扁平列表转换为树形列表
        result=build_tree(serializer.data,parent_key='parent')
        return Response(result)

    # 重新perform_create: 目的将部门主管员工的department_id设置为当前部门
    def perform_create(self, serializer):
        instance=serializer.save()
        manager_id=serializer.validated_data.get('manager_id')
        if manager_id:
            # 修改部门主管员工的department_id
            Employee.objects.filter(id=manager_id).update(department=instance,is_manager=True)

    # 重新perform_update: 目的将部门主管员工的department_id设置为当前部门
    def perform_update(self, serializer):
        instance = serializer.save()
        manager_id = serializer.validated_data.get('manager_id')
        if manager_id:
            # 修改部门主管员工的department_id
            Employee.objects.filter(id=manager_id).update(department_id=instance.id, is_manager=True)

    @action(['post'],detail=True)
    def set_manager(self,request,pk):
        output={'message':'success'}
        # 接受客户端参数
        # 主管的员工id
        # 部门id
        employee_id = request.data.get('manager_id')
        try:
            department = Department.objects.get(pk=pk)
        except Department.DoesNotExist:
            raise APIException({'message':'部门信息不存在'})
        try:
            employee=Employee.objects.get(pk=employee_id)
        except Employee.DoesNotExist:
            raise APIException({'message': '员工信息不存在'})
        with transaction.atomic():
            # 修改部门表
            department.manager_id = employee_id
            # 保存部门信息
            department.save()
            # 修改员工的部门信息
            employee.department = department
            # 保存员工信息
            employee.save()
        return Response(output)
