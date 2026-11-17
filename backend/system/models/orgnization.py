from django.db import models

from system.models import User


# 部门表模型类
class Department(models.Model):
    manager = models.ForeignKey('Employee',on_delete=models.SET_NULL,related_name='depart',null=True, blank=True, verbose_name='部门主管')
    parent=models.ForeignKey('self',on_delete=models.SET_NULL,null=True,blank=True,related_name='children',verbose_name='父级部门')
    name = models.CharField(max_length=20,unique=True,verbose_name='部门名称')
    status=models.BooleanField(default=True,verbose_name='部门状态')
    description=models.CharField(max_length=200,verbose_name='部门介绍')
    create_time=models.DateTimeField(auto_now_add=True,verbose_name='创建时间')
    class Meta:
        db_table='department'
        ordering=['id']

# 职位数据表模型类
class Position(models.Model):
    name=models.CharField(max_length=20,verbose_name='职位名称')
    level=models.SmallIntegerField(default=1,verbose_name='职务等级')
    status=models.BooleanField(default=True,verbose_name='职位状态')
    class Meta:
        db_table='position'
        ordering=['id']

# 员工 表模型类
class Employee(models.Model):
    gender_choices=[('male','男'),('female','女')]
    education_choices=[(1,'高中及以下'),(2,'专科'),(3,'本科'),(4,'硕士'),(5,'博士')]
    department=models.ForeignKey(Department,on_delete=models.SET_NULL,null=True,blank=True,verbose_name='所属部门')
    position=models.ForeignKey(Position,on_delete=models.SET_NULL,null=True,blank=True,verbose_name='职位')
    user=models.OneToOneField(User,on_delete=models.SET_NULL,unique=True,null=True,blank=True,related_name='employee')
    work_no=models.IntegerField(verbose_name='工号')
    name=models.CharField(max_length=10,verbose_name='员工姓名')
    gender=models.CharField(max_length=10,choices=gender_choices,verbose_name='性别')
    phone=models.CharField(max_length=11,unique=True,verbose_name='手机号码')
    email=models.CharField(max_length=50,unique=True,verbose_name='电子邮箱')
    photo=models.ImageField(upload_to='uploads/avatar',verbose_name='员工照片')
    birthday=models.DateField(verbose_name='出生年月日')
    education=models.CharField(max_length=10,choices=education_choices,null=True,blank=True,verbose_name='学历')
    school=models.CharField(max_length=30,null=True,blank=True,verbose_name='毕业院校')
    major=models.CharField(max_length=230,null=True,blank=True,verbose_name='专业')
    province=models.CharField(max_length=20,null=True,blank=True,verbose_name='省份')
    city = models.CharField(max_length=20,null=True,blank=True, verbose_name='城市')
    county = models.CharField(max_length=20,null=True,blank=True, verbose_name='区县')
    address = models.CharField(max_length=20,null=True,blank=True, verbose_name='详细地址')
    is_manager=models.BooleanField(default=False,null=True,blank=True,verbose_name='是否是部门主管')
    update_time=models.DateTimeField(auto_now=True,verbose_name='更新时间')
    create_time=models.DateTimeField(auto_now_add=True,verbose_name='添加时间')
    class Meta:
        db_table='employee'
        ordering=['id']
    # 将来无论执行新增操作还是更新操作都会执行save方法
    # Employee.objects.create()  Employee.objects.update()
    # emp=Employee()  emp.save()
    # 重写父类的save方法
    def save(self,*args,**kwargs):
        if not self.pk or self.pk is None:
            # 调用父类的save方法执行保存操作, 目的是得到pk
            super().save(*args,**kwargs)
            # 根据pk作为工号
            Employee.objects.filter(pk=self.pk).update(work_no=self.pk)
        else:
            # 正常执行更新操作
            super().save(*args, **kwargs)
