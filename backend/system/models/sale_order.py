from django.db import models
from . import User,Customer,Product

# 支付方式的取值必须和数据库列保持一致：
#   sale_order.pay_way 是 enum('wxpay','alipay','bank','cash')
# 这里显式声明 choices，让 DRF 在序列化层就拦下非法值并返回 400；
# 否则任何其它字符串会一路走到 MySQL，抛 Data truncated 变成 500。
PAY_WAY_CHOICES = [
    ('wxpay', '微信支付'),
    ('alipay', '支付宝支付'),
    ('bank', '银行转账'),
    ('cash', '现金支付'),
]

# 订单数据表模型类
class SaleOrder(models.Model):
    # 客户名称
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True,verbose_name='客户')
    # 销售人员
    user=models.ForeignKey(User, on_delete=models.SET_NULL, null=True,verbose_name='销售人员')
    # 订单编号
    order_no = models.CharField(null=True,blank=True,max_length=255, unique=True)
    # 收货人
    consignee=models.CharField(max_length=20,verbose_name='收货人'  )
    # 客户手机号
    phone = models.CharField(max_length=11,verbose_name='收货人手机号')
    # 订单金额
    amount = models.DecimalField(null=True,blank=True,max_digits=10, decimal_places=2,verbose_name='订单金额')
    status = models.BooleanField(default=True,null=True,blank=True,verbose_name='订单状态')
    # 创建时间
    create_time = models.DateTimeField(auto_now_add=True,null=False,verbose_name='创建时间')
    # 支付方式（限定取值，与库里的 enum 对齐）
    pay_way = models.CharField(max_length=20, choices=PAY_WAY_CHOICES, null=True, blank=True, verbose_name='支付方式')
    # 订单支付状态
    pay_status = models.BooleanField(default=False,null=True,blank=True,verbose_name='支付状态')
    # 订单支付时间
    pay_time = models.DateTimeField(null=True,blank=True,verbose_name='支付时间')
    # 订单佣金
    commission = models.DecimalField(null=True,blank=True,max_digits=10, decimal_places=2,verbose_name='订单佣金')
    express_name=models.CharField(max_length=255,null=True,blank=True,verbose_name='快递公司名称')
    express_no=models.CharField(max_length=255,null=True,blank=True,verbose_name='快递编号')
    express_status=models.BooleanField(default=False,null=True,blank=True,verbose_name='快递状态')
    province=models.CharField(max_length=20,null=True,blank=True,verbose_name='省份')
    city=models.CharField(max_length=20,null=True,blank=True,verbose_name='城市')
    county=models.CharField(max_length=20,null=True,blank=True,verbose_name='区县')
    address=models.CharField(max_length=255,null=True,blank=True,verbose_name='详细地址')

    class Meta:
        db_table = 'sale_order'
        ordering=['-id']

# 订单商品数据表模型类
class SaleOrderItem(models.Model):
    # 订单
    order = models.ForeignKey(SaleOrder, on_delete=models.CASCADE, related_name='order_items',verbose_name='订单')
    # 商品
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True,verbose_name='订单商品')
    # 商品名称
    name=models.CharField(max_length=50,verbose_name='商品名称')
    # 商品封面
    cover=models.CharField(max_length=255,verbose_name='商品封面')
    # 商品数量
    num = models.PositiveIntegerField(verbose_name='商品数量')
    # 商品金额
    price = models.DecimalField(max_digits=10, decimal_places=2,verbose_name='商品金额')
    # 佣金比例
    commission_rate=models.DecimalField(max_digits=10, decimal_places=2,verbose_name='佣金比例')

    class Meta:
        db_table = 'sale_order_item'
        ordering=['-id']
