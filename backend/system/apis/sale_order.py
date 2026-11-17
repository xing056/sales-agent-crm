from rest_framework import viewsets
from rest_framework import serializers
from rest_framework import status
from rest_framework.response import Response
from ..serializers import SaleOrderSerializer
from ..models import SaleOrder,SaleOrderItem
from ..utils.customer_stats import sync_customer_stats
from django.db import transaction
from datetime import datetime
from decimal import Decimal
import random

# 订单接口类
class SaleOrderViewSet(viewsets.ModelViewSet):
    queryset =  SaleOrder.objects.all()
    serializer_class = SaleOrderSerializer
    rbac_permissions = {
        'list': 'api:sale_order:list',
        'retrieve': 'api:sale_order:detail',
        'create': 'api:sale_order:create',
        'update': 'api:sale_order:update',
        'partial_update': 'api:sale_order:update',
        'destroy': 'api:sale_order:destroy',
    }
    # authentication_classes=[]
    # permission_classes=[]

    def get_queryset(self):
        """行级隔离：非超管只能看自己的订单。

        和客户接口同一个问题：权限码只管"能不能调接口"，不管"能看哪一条"。
        没有这段，普通销售换个 id 就能读到别人的订单金额和收货信息。
        订单表自己带 user 外键，所以按 user_id 过滤，不用绕到 customer。
        """
        queryset = super().get_queryset()
        user = self.request.user
        if user.is_superuser:
            return queryset
        return queryset.filter(user_id=user.id)

    def perform_create(self, serializer):
        with transaction.atomic():
            # 计算订单编号
            serializer.validated_data['order_no']=datetime.now().strftime('%Y%m%d%H%M%S')+str(random.randint(1000,9999))
            # 取出订单商品数据
            order_items=serializer.validated_data.pop('order_items',None)
            if not order_items:
                raise serializers.ValidationError({'message':'参数错误:缺少参数order_items'})
            # 计算订单总金额
            # 金额一律用 Decimal：float 累加会产生 0.1+0.2=0.30000000000000004 这类误差，
            # 单笔落库只留两位看不出来，但金额和佣金一旦累计、对账就会差几分钱。
            serializer.validated_data['amount']=sum(
                (Decimal(str(item['num']))*Decimal(str(item['price'])) for item in order_items),
                Decimal('0.00'),
            )
            # 计算订单佣金
            serializer.validated_data['commission']=sum(
                (Decimal(str(item['num']))*Decimal(str(item['commission_rate']))*Decimal(str(item['price']))
                 for item in order_items),
                Decimal('0.00'),
            )
            # 保存订单
            sale_order=serializer.save(user=self.request.user)
            # 保存订单商品数据
            if order_items:
                for item in order_items:
                    # 取出商品
                    product_id=item.pop('id',None)
                    if not product_id:
                        raise serializers.ValidationError({'message':'参数错误:缺少参数product_id'})
                    # 对商品id参数进行重命名
                    item['product_id']=product_id    
                    # 保存订单商品
                    SaleOrderItem.objects.create(order=sale_order,**item)
            # 客户身上的「消费次数/消费总额」跟着订单走。
            # 注意是"重算"不是"加一"——幂等，重复执行也不会多算。
            sync_customer_stats(sale_order.customer_id)

    def perform_update(self, serializer):
        # 订单可能被改到别的客户名下，改前、改后两个客户都要重算
        old_customer_id=serializer.instance.customer_id
        with transaction.atomic():
            sale_order=serializer.save()
            sync_customer_stats(old_customer_id)
            if sale_order.customer_id!=old_customer_id:
                sync_customer_stats(sale_order.customer_id)

    def destroy(self, request, *args, **kwargs):
        instance=self.get_object()
        customer_id=instance.customer_id
        with transaction.atomic():
            self.perform_destroy(instance)
            # 删单之后重算，客户统计自然回落，不会留下"多算一次"的尾巴
            sync_customer_stats(customer_id)
        return Response(status=status.HTTP_204_NO_CONTENT)
