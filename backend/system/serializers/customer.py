from rest_framework import serializers
from . import UserBriefSerializer
from .serializer import BaseSerializer
from ..models import CustomerSource, Customer, CustomerTracking

# 客户来源数据表模型类序列化器
class CustomerSourceSerializer(BaseSerializer):
    class Meta:
        model = CustomerSource
        fields = '__all__'

# 客户数据表模型类序列化器
class CustomerSerializer(BaseSerializer):
    # 指定外键关联字段对应的序列化器
    source=CustomerSourceSerializer(read_only=True)
    # 销售人员（最小字段集：只要"是谁"，不带手机/邮箱/角色）
    user=UserBriefSerializer(read_only=True)
    # 推荐者
    parent=serializers.SerializerMethodField()
    def get_parent(self,obj):
        if obj.parent:
            return CustomerSerializer(obj.parent).data
        return obj.parent
    # 虚拟属性: 负责接受客户端发送的参数 客户来源id
    source_id=serializers.IntegerField(label='客户来源')
    parent_id=serializers.IntegerField(label='推荐者',required=False,allow_null=True)
    class Meta:
        model = Customer
        fields = '__all__'

# 客户跟踪记录数据表模型类序列化器
class CustomerTrackingSerializer(BaseSerializer):
    # 指定外键关联字段对应的序列化器
    customer = CustomerSerializer(read_only=True)
    user = UserBriefSerializer(read_only=True)
    # 虚拟属性: 负责接受客户端发送的参数 客户id
    customer_id = serializers.IntegerField(write_only=True,label='客户id')

    class Meta:
        model = CustomerTracking
        fields = '__all__'
