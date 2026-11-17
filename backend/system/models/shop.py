from django.db import models
# 商品分类数据表模型类
class Category(models.Model):
    parent=models.ForeignKey("self",on_delete=models.SET_NULL,null=True,blank=True,verbose_name="父分类")
    name = models.CharField(max_length=32, verbose_name="分类名称")
    cover=models.ImageField(upload_to="category",null=True,blank=True,verbose_name="分类封面")
    status=models.BooleanField(default=True,verbose_name="分类状态")
    class Meta:
        db_table = "category"
        ordering=['id']

# 商品数据表模型类
class Product(models.Model):
    category=models.ForeignKey(Category,on_delete=models.SET_NULL,null=True,blank=True,verbose_name="商品分类")
    name=models.CharField(max_length=32,verbose_name="商品名称")
    price=models.DecimalField(max_digits=8,decimal_places=2,verbose_name="商品价格")
    stock_num=models.IntegerField(default=0,null=True,blank=True    ,verbose_name="商品库存")
    sale_num=models.IntegerField(default=0,null=True,blank=True,verbose_name="商品销售量")
    cover=models.ImageField(upload_to="product",null=True,blank=True,verbose_name="商品封面")
    commission_rate=models.DecimalField(max_digits=4,decimal_places=2,default=0,null=True,blank=True,verbose_name="商品佣金比例")
    status=models.BooleanField(default=True,verbose_name="商品状态")
    description=models.TextField(null=True,blank=True,verbose_name="商品描述")
    create_time=models.DateTimeField(auto_now_add=True,verbose_name="商品创建时间")
    class Meta:
        db_table="product"
        ordering=['id']

