from . import BaseSerializer,CustomerSerializer,UserBriefSerializer
from ..models import SaleOrder,SaleOrderItem
from rest_framework import serializers

# 订单数据表模型类序列化器
class SaleOrderSerializer(BaseSerializer):
    customer=CustomerSerializer(read_only=True)
    # 销售顾问：只回 id/账号/员工姓名，不带手机邮箱和角色
    user=UserBriefSerializer(read_only=True)
    customer_id=serializers.IntegerField(write_only=True,required=True,label='客户ID')
    # 添加一个虚拟字段接受客户端发送的订单商品数据
    order_items=serializers.ListField(write_only=True,required=True,label='订单商品数据')
    class Meta:
        model = SaleOrder
        fields = '__all__'

# 订单商品数据表模型类序列化器
class SaleOrderItemSerializer(BaseSerializer):
    class Meta:
        model = SaleOrderItem
        fields = '__all__'
        
