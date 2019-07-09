from django.db import models
# Create your models here.
from account.models import User
''' 流程审批路由规则：
{
 "1": ["user1@abc.com"]
 "2": ["user1@abc.com", "user2@abc.com"],
}
"1": 代表审批优先级；
['email']: 代表对应的审批人；
'''


# Process 流程表
class Process(models.Model):
    status_choices = (
        (0, '审批中'),
        (1, '流程通过'),
        (2, '流程拒绝')
    )
    title            = models.CharField('申请标题', max_length=64, null=False, help_text='申请标题')
    approver         = models.ForeignKey(User, null=True, verbose_name="流程申请人", help_text="流程申请人",on_delete=models.CASCADE)
    # 记录当前审批级别，该字段提供"进度查询"
    cur_priority     = models.IntegerField('当前审批级别', null=True, blank=True, help_text='当前审批级别（默认：1）',default=1)
    status           = models.IntegerField(choices=status_choices, verbose_name="流程状态", help_text='流程状态', default=0)
    desc             = models.TextField('备注描述', max_length=255, null=True, help_text='备注描述')
    time_create      = models.DateTimeField('流程创建时间', auto_now_add=True, help_text='流程创建时间')
    time_finished    = models.DateTimeField('流程完结时间', auto_now=True, help_text='流程完结时间')

    class Meta:
        verbose_name = "流程表"
        db_table = "oa_process"
        ordering = ["id"]

    def __str__(self):
        return self.title


# ApprovalProcess用户审批表
class ApprovalProcess(models.Model):
    status_choices = (
        (0, '待处理'),
        (1, '审批通过'),
        (2, '退回申请')
    )
    applicant        = models.ForeignKey(User, null=True, verbose_name='审批人', help_text='审批人',on_delete=models.CASCADE)
    process          = models.ForeignKey(Process, verbose_name='所属流程', help_text='所属流程',on_delete=models.CASCADE)
    priority         = models.IntegerField('审批优先级', null=True, blank=True, help_text='审批优先级', default=1)
    # 展示字段（布尔值）, 审批单对用户是否展示, 优先级到当前用户，才展示该审批单
    show             = models.BooleanField("审批单展示", default=False, help_text='优先级到当前用户，才展示该审批单')
    # 处理结果: 分为"待处理"和"已处理(通过&退回)"
    approval_result  = models.IntegerField(choices=status_choices, verbose_name='审批结果', null=False, help_text='审批结果', default=0)
    approval_comment = models.TextField('审批意见', max_length=200, null=True, help_text='审批意见')
    time_approved    = models.DateTimeField('审批时间', auto_now_add=True, help_text='审批时间')
    time_received    = models.DateTimeField('到达时间', auto_now=True, help_text='到达时间')

    class Meta:
        verbose_name = "用户审批表"
        db_table = "oa_approval_process"
        ordering = ["id"]

    # def __str__(self):
    #     return self.priority
