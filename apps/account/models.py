from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractUser
# from process.models import ApprovalProcess, Process


class User(AbstractUser):
    name             = models.CharField('姓名', max_length=32, null=True, help_text="姓名")
    tel              = models.CharField('电话', max_length=15, null=True, help_text="电话")
    department       = models.ForeignKey('Department', null=True, verbose_name='部门', help_text='部门',on_delete=models.CASCADE)
    # approver         = models.ForeignKey(ApprovalProcess, null=True, verbose_name='用户对应的审批表', help_text='用户对应的审批表')
    # applicant        = models.ForeignKey(Process, null=True, verbose_name='用户对应的申请流程', help_text='用户对应的申请流程')

    class Meta:
        verbose_name = "用户扩展表"
        db_table     = "auth_user"
        ordering     = ["id"]
        #permissions  = (
        #    ('view_user', 'cat view user'),
        #)

    def __str__(self):
        if self.name:
            # 如果不为空则返回用户名
            return self.name
        else:
            # 如果用户名为空则返回不能为空的对象
            return self.username


class Department(models.Model):
    is_deleted_choices = (
        (0, '启用'),
        (1, '禁用')
    )
    level_choices = (
        ('syb', '事业部'),
        ('one', '一级部门'),
        ('two', '二级部门')
    )
    department_name  = models.CharField('部门名称',  max_length=64, null=False, help_text='部门名称')
    parent_dept      = models.ForeignKey('self', related_name='children', null=True, verbose_name="子部门", help_text="子部门门",on_delete=models.CASCADE)
    # leader           = models.IntegerField(db_index=True, null=True, verbose_name="部门领导", help_text="领导")
    leader           = models.ForeignKey('User', related_name='department_leader', null=True, verbose_name="部门领导", help_text="领导",on_delete=models.CASCADE)
    level            = models.CharField(choices=level_choices, max_length=32, verbose_name='部门级别', help_text='事业部，一级部门，还是二级部门', default='syb')
    is_deleted       = models.IntegerField(choices=is_deleted_choices, verbose_name=u'部门状态', help_text='请选择新建部门的状态', default=0)

    class Meta:
        verbose_name = "用户部门表"
        ordering     = ["id"]
        db_table     = "auth_user_department"
        #permissions  = (
        #    ('view_department', 'cat view department'),
        #)

    def __str__(self):
        return self.department_name
