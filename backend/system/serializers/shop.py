from .serializer import BaseSerializer
from rest_framework import serializers
from ..models import Category,Product

# 商品分类数据表模型类序列化器
class CategorySerializer(BaseSerializer):
    class Meta:
        model=Category
        fields="__all__"

# 商品数据表模型类序列化器
class ProductSerializer(BaseSerializer):
    # 指定外键字段关联数据序列化器
    category=CategorySerializer(read_only=True)
    # 添加一个虚拟字段, 接受客户端发送的分类id
    category_id=serializers.IntegerField(label="商品分类id")
    class Meta:
        model=Product
        fields="__all__"
