from django.db import models


#新增书的数据库定义的类
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    published_date = models.DateField()
    isbn = models.CharField(max_length=13, unique=True, null=True, blank=True)  # 确保字段定义正确

    def __str__(self):
        return self.title

#新增模型的数据库定义类
class MyModel(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

#会员信息模型
class MemberInfo(models.Model):
    member_id = models.AutoField(primary_key=True)  # 自增主键
    membername = models.CharField(max_length=100)
    membertelphone = models.CharField(max_length=11)
    memberpurchasecount = models.CharField(max_length=3)
    memberremaincount = models.CharField(max_length=3)

    class Meta:
        unique_together = ('membername', 'membertelphone')  # 姓名和电话号码作为业务主键，必须唯一

    def __str__(self):
        return f"{self.membername} ({self.membertelphone})"

#操作日志模型 编号，操作时间，会员姓名，电话，操作内容，请求报文。operationid operationtime membername membertelephone operationitem operationrequest

class OperationInfo(models.Model):
    operation_id = models.AutoField(primary_key=True)
    operationtime = models.DateTimeField()
    membername = models.CharField(max_length=100)
    membertelphone = models.CharField(max_length=11)
    operationitem = models.CharField(max_length=100)
    operationrequest = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.membername} ({self.membertelphone})"
