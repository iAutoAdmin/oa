from django.shortcuts import render

# Create your views here.

from rest_framework import viewsets, mixins
from process.models import Process, ApprovalProcess
from process.serializers import ProcessSerializer, ApprovalProcessSerializer
from .filters import ProcessFilter


class ProcessViewSet(viewsets.ModelViewSet):
    """
    retrieve:
        返回指定单个流程信息
    list:
        返回流程列表
    update:
        更新流程信息
    destroy:
        删除流程记录
    create:
        创建流程资源
    partial_update:
        更新部分字段
    """
    queryset = Process.objects.all()
    serializer_class = ProcessSerializer
    filter_class = ProcessFilter
    filter_fields = ("title",)


# 线上场景，不单独开放审批表"创建"功能，审批表创建全部由业务逻辑调用ApprovalProcess.objects.create来完成
# class ApprovalProcessViewSet(viewsets.ModelViewSet):
class ApprovalProcessViewSet(viewsets.GenericViewSet,
                             mixins.RetrieveModelMixin,
                             mixins.UpdateModelMixin,
                             mixins.DestroyModelMixin,
                             mixins.ListModelMixin,):
    """
    retrieve:
        返回指定单个流程信息
    list:
        返回流程列表
    update:
        更新流程信息
    destroy:
        删除流程记录
    partial_update:
        更新部分字段
    """

    serializer_class = ApprovalProcessSerializer

    def get_queryset(self):
        return ApprovalProcess.objects.filter(applicant_id=self.request.user.id, show=True)
