from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from system.models import Customer
from system.serializers import CustomerSerializer

# 客户接口类
class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    # 临时禁用登录认证类和权限认证类
    # authentication_classes =[]
    # permission_classes = []
    rbac_permissions={
        'list':'api:customer:list',
        'retrieve': 'api:customer:detail',
        'create': 'api:customer:create',
        'update': 'api:customer:update',
        'partial_update': 'api:customer:update',
        'destroy': 'api:customer:destroy',
        'of_me': 'api:customer:of_me',
    }
    # 设置搜索字段 select * from customer where name=''
    filterset_fields=['name','phone']

    def get_queryset(self):
        """行级隔离：非超管只能看自己负责的客户。

        【为什么必须在这里做】
            之前只有接口权限码（api:customer:list）挡着，那是"能不能调这个接口"，
            不是"能看哪些数据"。只要知道 id，普通销售就能读到别人客户的姓名、
            手机、地址、消费金额 —— 这是典型的水平越权（IDOR）。
            列表接口返回 403 给了人一种"已经隔离了"的错觉，详情接口其实敞着。

        超管例外：本来就要看全量。
        """
        queryset = super().get_queryset()
        user = self.request.user
        if user.is_superuser:
            return queryset
        return queryset.filter(user_id=user.id)
    # 重写perform_create方法
    def perform_create(self, serializer):
        # 自动获取当前登录账号的id?
        serializer.validated_data['user_id'] = self.request.user.id
        # 执行保存操作
        serializer.save()

    # /api/customers/of_me/
    # 获取当前登录账号对应的客户数据
    @action(['get'],detail=False)
    def of_me(self,request):    
        # 获取当前登录账号数据
        user=request.user
        # 查询当前登录账号相关的客户数据
        queryset=self.filter_queryset(self.get_queryset()).filter(user_id=user.id)
        # 获取一个分页对象
        page=self.paginate_queryset(queryset)
        # 判断是否存在参数page
        if page is not None:
            # 手动调用序列化器:将分页对象传递给序列化器
            serializer=self.get_serializer(page,many=True)
            # 响应带有分页信息的响应对象
            return self.get_paginated_response(serializer.data)
        # 序列化查询结果
        serializer=self.get_serializer(queryset,many=True)
        # 返回序列化数据
        return Response(serializer.data)
