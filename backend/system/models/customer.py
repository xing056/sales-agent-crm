from django.db import models
from .index import User
# 客户来源数据表模型类
class CustomerSource(models.Model):
    name=models.CharField(max_length=20,unique=True,verbose_name='客户来源名称')
    status=models.BooleanField(default=True,verbose_name='来源状态')
    class Meta:
        db_table = 'customer_source'
        ordering = ['id']

# 客户数据表模型类
class Customer(models.Model):
    # 外键
    parent=models.ForeignKey('self',on_delete=models.SET_NULL,null=True,blank=True,verbose_name='推荐客户')
    user=models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True,verbose_name='销售人员')
    source=models.ForeignKey(CustomerSource,on_delete=models.SET_NULL,null=True,blank=True,verbose_name='客户来源')
    name=models.CharField(max_length=20,verbose_name='客户姓名')
    phone = models.CharField(max_length=20,null=True,blank=True, unique=True, verbose_name='客户手机号码')
    province=models.CharField(max_length=30,null=True,blank=True,verbose_name='省份')
    city = models.CharField(max_length=30, null=True, blank=True, verbose_name='城市')
    county = models.CharField(max_length=30, null=True, blank=True, verbose_name='区县')
    address = models.CharField(max_length=30, null=True, blank=True, verbose_name='详细地址')
    status=models.BooleanField(default=True,null=True,blank=True,verbose_name='客户状态')
    level=models.SmallIntegerField(default=1,null=True,blank=True,verbose_name='客户等级')
    order_count=models.SmallIntegerField(default=0,null=True,blank=True,verbose_name='消费次数')
    order_amount = models.DecimalField(max_digits=10,null=True,blank=True,decimal_places=2,default=0, verbose_name='消费总金额')
    remark=models.TextField(null=True,blank=True,verbose_name='客户备注')
    update_time=models.DateTimeField(auto_now=True,verbose_name='客户资料更新时间')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='客户添加时间')
    class Meta:
        db_table = 'customer'
        ordering = ['id']

# 客户跟踪记录数据表模型类
class CustomerTracking(models.Model):
    # 外键
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='客户')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='销售人员')
    tracking_way=models.CharField(max_length=30,verbose_name='跟踪方式')
    description = models.CharField(max_length=255, verbose_name='跟踪结果')
    status=models.BooleanField(default=True,verbose_name='跟踪状态')
    tracking_time = models.DateTimeField(auto_now_add=True, verbose_name='跟踪时间')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='跟踪记录添加时间')
    class Meta:
        db_table = 'customer_tracking'
        ordering = ['id']