from ..serializers import CommissionSerializer
from ..models import Commission, SaleOrder
from rest_framework import viewsets, mixins
from django.utils import timezone
from rest_framework.decorators import action
from rest_framework.response import Response
import calendar


# 员工提成接口类
class CommissionViewSet(
    viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.ListModelMixin
):
    queryset = Commission.objects.all()
    serializer_class = CommissionSerializer
    # 临时禁用登录认证和权限认证
    # authentication_classes = []
    # permission_classes = []
    # 接口方法权限编码
    rbac_permissions = {
        "list": "api:commission:list",
        "create": "api:commission:create",
        "of_me": "api:commission:of_me",
    }

    # 重新创建方法
    def perform_create(self, serializer):
         # 获取当前年月和月份
        year=timezone.localtime().year
        month=timezone.localtime().month
        _, days_in_month = calendar.monthrange(year, month)
        # 计算本月一号00:00:00
        first_day=timezone.now().replace(day=1,hour=0,minute=0,second=0,microsecond=0)
        # 计算本月最后一天23:59:59.999999
        last_day=timezone.now().replace(day=days_in_month,hour=23,minute=59,second=59,microsecond=999999)
        # 查询订单数据
        order_list = SaleOrder.objects.filter(
            user_id=self.request.user.id, pay_status=True,create_time__gte=first_day,create_time__lte=last_day
        )
        # 提成总金额
        total_commission = 0
        for item in order_list:
            total_commission += item.commission
        now = timezone.now()
        # 202601
        year_month = int(f"{now.year}{now.month:02d}")
        # 查询数据表中是否存在记录, 如果存在, 则执行更新, 否则执行新增
        try:
            # get方法数据不存在, 会抛出异常
            instance = Commission.objects.get(
                user_id=self.request.user.id, year_month=year_month
            )
            # 执行更新操作
            instance.commission = total_commission
            # 保存更新操作
            instance.save()
        except Commission.DoesNotExist:
            # 通过request对象获取登录用户id
            serializer.validated_data["user_id"] = self.request.user.id
            serializer.validated_data["commission"] = total_commission
            serializer.validated_data["year_month"] = year_month
            super().perform_create(serializer)

    @action(methods=["get"], detail=False)
    def of_me(self, request):
        queryset = self.filter_queryset(
            self.get_queryset().filter(user_id=request.user.id)
        )
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
