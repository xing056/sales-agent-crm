from black import datetime
from django.http import HttpResponse
from rest_framework.decorators import action, permission_classes
from openpyxl import Workbook
from rest_framework.viewsets import ModelViewSet
from ..models import Employee
from ..serializers import EmployeeSerializer

# 员工接口类
class EmployeeViewSet(ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    # 临时禁用登录认证和权限认证
    # authentication_classes = []
    # permission_classes = []
    rbac_permissions = {
        'list': 'api:employee:list',
        'retrieve': 'api:employee:detail',
        'create': 'api:employee:create',
        'update': 'api:employee:update',
        'partial_update': 'api:employee:update',
        'destroy': 'api:employee:destroy',
        'download':'api:employee:download',
    }
    # 配置搜索字段 select * from employee where name=''
    filterset_fields=['department_id','name','position_id','phone']
    # 导出员工数据  ,permission_classes=[],authentication_classes=[]
    @action(['get'], detail=False)
    def download(self, request):
        # 接受客户端传递的查询参数
        department_id=request.query_params.get('department_id',None)
        # 创建工作薄
        wb = Workbook()
        # 获取处于激活状态的表格对象
        ws = wb.active
        # 添加表头
        headers = ['工号', '部门', '职位', '姓名', '出生日期', '性别', '省份', '城市', '区县', '详细通信地址',
                   '入职日期']
        ws.append(headers)
        mapping={}
        if department_id:
            mapping['department_id'] = department_id
        # 查询员工信息
        queryset = Employee.objects.filter(**mapping).all()
        # 员工列表数据进行序列化器
        serializer = EmployeeSerializer(queryset, many=True)
        # 将员工信息添加到excel表格对象中
        for item in serializer.data:
            department = item.get('department').get('name')
            position = item.get('position').get('name')
            gender = '男' if item.get('gender') == 'male' else '女'
            ws.append([item.get('work_no'), department,position,item.get('name'),item.get('birthday'),
                       gender, item.get('province'),item.get('city'), item.get('county'), item.get('address'),
                       item.get('create_time')
                       ])
        # Response: 内置的content_type的响应头的值application/json
        # 手动构造一个响应对象
        # content_type: 设置响应内容的类型
        response = HttpResponse(content_type='application/vnd.ms-excel')
        # Content-Disposition: 告诉客户端该如何处理响应内容
        response['Content-Disposition'] = f"attachment; filename={datetime.now().strftime('%Y%m%d%H%M%S')}.xlsx"
        # 将响应对象保存到工作薄中
        wb.save(response)
        # 返回自定义响应对象
        return response
