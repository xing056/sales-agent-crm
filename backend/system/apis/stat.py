from rest_framework import viewsets,status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import F, Sum,Count
from django.db.models.functions import ExtractMonth,ExtractDay,ExtractWeekDay,ExtractYear
from ..models import *
from django.utils import timezone
from datetime import timedelta
import calendar

class StatViewSet(viewsets.ViewSet):
    # 认证/权限沿用全局配置（CustomJwtAuth + CustomPermission），不再单独放行
    # authentication_classes = []
    # permission_classes = []
    # 接口方法权限代码
    rbac_permissions={
        'top_sale_product':'api:stat:top_sale_product',
        'top10_sale_employee':'api:stat:top10_sale_employee',
        'top10_province_customer':'api:stat:top10_province_customer',
        'weekday_sale_amount':'api:stat:weekday_sale_amount',
        'year_month_sale_amount':'api:stat:year_month_sale_amount',
        'month_day_sale_amount':'api:stat:month_day_sale_amount',
        'today_order_num_and_amount':'api:stat:today_order_num_and_amount',
    }
    # 统计销量排行前10的商品及销量信息
    @action(['get'],detail=False)
    def top_sale_product(self,request):
        # annotate: 增加额外的字段, 并对字段进行聚合操作
        result = (
            SaleOrderItem.objects
            .filter(order__pay_status=True) # 只统计已支付订单
            .values('name')
            .annotate(
                total_num=Sum('num'),  # 商品销售数量
                total_amount=Sum(F('num') * F('price'))  # 商品销售金额
            )
            .order_by('-total_amount')[:10]
        )
        return Response(result)

    # 统计销售顾问销售额排行
    @action(['get'],detail=False)
    def top10_sale_employee(self,request):
        result = (
            SaleOrder.objects.filter(pay_status=True)
            .values('user__employee__name','user__employee__work_no','user__employee__phone')
            .annotate(
                total_amount=Sum('amount')  # 销售顾问销售额
            )
            .order_by('-total_amount')[:10]
        )
        return Response(result)

    # 统计客户数量前10的省份
    @action(['get'],detail=False)
    def top10_province_customer(self,request):
        result = (
            Customer.objects
            .values('province')
            .annotate(
                total_customer=Count('id')  # 客户数量
            )
            .order_by('-total_customer')[:10]
        )
        return Response(result)

    # 统计当前周每天的销售额度
    @action(['get'],detail=False)
    def weekday_sale_amount(self,request):
        # 本周周一, 00:00:00 
        # weekday(): 返回值0-6 表示周一到周日   timezone.now()  datetime.now()
        monday=(timezone.now()-timedelta(days=timezone.now().weekday())).replace(hour=0,minute=0,second=0,microsecond=0)
        sunday=(monday+timedelta(days=6)).replace(hour=23,minute=59,second=59,microsecond=999999)
        result = (
            SaleOrder.objects
            .filter(
                pay_status=True,
                # 本周日>订单创建时间>本周一
                create_time__gte=monday,
                create_time__lte=sunday
            )
            .annotate(
                # ExtractWeekDay: 从一个日期字段中提取星期名称   [1,7]   => [星期天,星期六]
                # ExtractWeekDay()底层调用的是mysql中的dayofweek()函数
                day=ExtractWeekDay('create_time')  # 按周内天数分组，ExtractWeekDay返回1-7，对应周日到周六，2表示星期一
            )
            .values('day')
            .annotate(
                total_amount=Sum('amount')  # 销售额
            )
            .order_by('day')
        )
        return Response(result)
    # 按照月份统计销售额
    @action(['get'],detail=False)
    def month_day_sale_amount(self,request):
        # 获取当前年月和月份
        year=timezone.localtime().year
        month=timezone.localtime().month
        _, days_in_month = calendar.monthrange(year, month)
        # 计算本月一号00:00:00
        first_day=timezone.now().replace(day=1,hour=0,minute=0,second=0,microsecond=0)
        # 计算本月最后一天23:59:59.999999
        last_day=timezone.now().replace(day=days_in_month,hour=23,minute=59,second=59,microsecond=999999)
        result = (
            SaleOrder.objects.filter(
                pay_status=True,
                create_time__gte=first_day,
                create_time__lte=last_day
            )
            .annotate(
                day=ExtractDay('create_time')  # 按月份分组
            )
            .values('day')
            .annotate(
                total_amount=Sum('amount')  # 销售额
            )
            .order_by('day')
        )
        return Response(result)

    # 统计本年每个月的销售额
    @action(['get'],detail=False)
    def year_month_sale_amount(self,request):
        # 计算本年第一天00:00:00
        first_day=timezone.now().replace(month=1,day=1,hour=0,minute=0,second=0,microsecond=0)
        # 计算本年最后一天23:59:59.999999
        last_day=timezone.now().replace(month=12,day=31,hour=23,minute=59,second=59,microsecond=999999)
        result = (
            SaleOrder.objects.filter(
                pay_status=True,
                create_time__gte=first_day,
                create_time__lte=last_day
            )
            .annotate(
                year=ExtractYear('create_time'),  # 按年份分组
                month=ExtractMonth('create_time')  # 按月份分组
            )
            .values('year','month')
            .annotate(
                total_amount=Sum('amount')  # 销售额
            )
            .order_by('year','month')
        )
        return Response(result)

    # 统计当天订单数量和销售额
    @action(['get'],detail=False)
    def today_order_num_and_amount(self,request):
        # 计算今天00:00:00
        today=timezone.localtime().replace(hour=0,minute=0,second=0,microsecond=0)
        # 计算明天23:59:59.999999
        tomorrow=timezone.localtime().replace(hour=23,minute=59,second=59,microsecond=999999)
        result = (
            SaleOrder.objects.filter(
                pay_status=True,
                create_time__gte=today,
                create_time__lte=tomorrow
            )
            .annotate(
                year=ExtractYear('create_time'),  # 按年份分组
                month=ExtractMonth('create_time'),  # 按月份分组
                day=ExtractDay('create_time')  # 按天数分组
            )
            .values('year','month','day')
            .annotate(
                order_num=Count('id'),  # 订单数量
                total_amount=Sum('amount')  # 销售额
            )
            .order_by('year','month','day')
        )
        return Response(result)