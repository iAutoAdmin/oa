#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   : tanshuai
# @Contact  : tyh9436@gmail.com
# @Software : PyCharm
# @File     : serializers.py
# @Time     : 18/6/24 09:29

from rest_framework import serializers
from process.models import Process, ApprovalProcess
from account.models import User


class ProcessSerializer(serializers.ModelSerializer):
    """
    流程序列化类
    """
    class Meta:
        model = Process
        # fields = '__all__'
        fields = ['id', 'title', 'approver', 'cur_priority', 'status', 'desc']
        read_only_fields = ('id',)

    def to_representation(self, instance):
        ret = super(ProcessSerializer, self).to_representation(instance)
        ret['approver'] = User.objects.get(pk=ret['approver']).username
        for status in Process.status_choices:
            if ret['status'] == status[0]:
                ret['status'] = status[1]

        # 根据Process ID 去ApprovalProcess表里查询，根据lavel排列审批路由顺序；
        applicant_list = ApprovalProcess.objects.filter(process__exact=ret['id'])
        route = {}
        for applicant_obj in applicant_list:
            if applicant_obj.priority not in route:
                route[applicant_obj.priority] = [applicant_obj.applicant.email]
            else:
                route.get(applicant_obj.priority).append(applicant_obj.applicant.email)
        ret['route'] = route
        return ret

    def create(self, validated_data):
        applicant_dict = {
            "1": ["1@123.com"],
            "2": ["2@123.com", "3@123.com"],
            "3": ["4@123.com"]
        }

        # 1、创建当前流程
        ret = self.Meta.model.objects.create(**validated_data)
        # 2、根据"流程审批路由（applicant_dict）" 创建用户审批单
        for level, user_email_list in applicant_dict.items():
            level = int(level)
            for user_email in user_email_list:
                userobj = User.objects.get(email__exact=user_email)
                approval_data = {
                    "process": ret,
                    "applicant": userobj,
                    "priority": level,
                    "show": 1 if level == 1 else 0, # 第一个审批人的show为True
                    "approval_result": 0
                }
                ApprovalProcess.objects.create(**approval_data)

                # 3、写入Process的priority为第一个审批级别
                if level == 1:
                    ret.priority = level
                    ret.save()
        return ret

    def update(self, instance, validated_data):
        self.Meta.model.objects.filter(id=instance.id).update(**validated_data)
        return instance


class ApprovalProcessSerializer(serializers.ModelSerializer):
    """
    审批序列化类
    """
    class Meta:
        model = ApprovalProcess
        # fields = '__all__'
        fields = ['id', 'process', 'applicant', 'priority', 'show', 'approval_result', 'approval_comment']
        read_only_fields = ('id',)

    def to_representation(self, instance):
        # print(self.context["request"].user.id) # 学习:序列化类中打印当前登陆用户的id
        ret = super(ApprovalProcessSerializer, self).to_representation(instance)
        ret['applicant'] = User.objects.get(pk=ret['applicant']).username
        ret['process'] = Process.objects.get(pk=ret['process']).title
        for status in ApprovalProcess.status_choices:
            if ret['approval_result'] == status[0]:
                ret['approval_result'] = status[1]
                break
        return ret

    # 审批单不需要创建功能，创建审批单是在创建审批表时通过 ApprovalProcess.objects.create 来完成
    # def create(self, validated_data):
    #     return self.Meta.model.objects.create(**validated_data)

    def update(self, instance, validated_data):
        # 首先获取一些常用数据
        flow = validated_data.get('approval_result')
        process_id = validated_data.get('process').id
        current_priority = validated_data.get('priority')
        next_priority = current_priority + 1

        # 1. 流程走向 1通过 2退回 其他则返回实例
        if flow == 1:
            # 1. 更新当前审批表状态
            instance.show = False
            instance.approval_result = validated_data.get("approval_result", instance.approval_result)
            instance.approval_comment = validated_data.get("approval_comment", instance.approval_comment)
            instance.save()

            # 2. 获取最后一个级别
            last_priority = 0
            approval_objs = ApprovalProcess.objects.filter(process__id=process_id)
            for approval_obj in approval_objs:
                if approval_obj.priority > last_priority:
                    last_priority = approval_obj.priority

            # 2.1 当前审批级别等于流程的最后审批级别，则流程通过审批，同时关闭同级别的审批单
            if last_priority == current_priority:
                # 1. 更新流程表状态
                obj = Process.objects.get(pk=process_id)
                obj.status = 1
                obj.save()

                # 2. 关闭同级别的审批单(因为有并联审批关系)
                current_approval_objs = ApprovalProcess.objects.filter(priority=current_priority)
                if len(current_approval_objs) > 1:
                    for approval_obj in current_approval_objs:
                        approval_obj.show = False
                        approval_obj.save()

                # 3. 更改 Process 当前审批的级别
                obj = Process.objects.get(pk=process_id)
                obj.cur_priority = next_priority
                obj.save()

            # 2.2 不是最后 change next
            else:

                # 1. 开启所有下一个级别审批单的show 字段为 True
                next_approval_objs = ApprovalProcess.objects.filter(priority=next_priority)
                for approval_obj in next_approval_objs:
                    approval_obj.show = True
                    approval_obj.save()

                # 2. 关闭同级别的审批单(因为有并联审批关系)
                current_approval_objs = ApprovalProcess.objects.filter(priority=current_priority)
                if len(current_approval_objs) > 1:
                    for approval_obj in current_approval_objs:
                        approval_obj.show = False
                        approval_obj.save()

                # 3. 更改 Process 当前审批的级别
                obj = Process.objects.get(pk=process_id)
                obj.cur_priority = next_priority
                obj.save()

            # 2.3 更新成功, 返回实例
            return instance
        # 2. 退回
        elif flow == 2:
            # 1. 更新流程表状态
            obj = Process.objects.get(pk=process_id)
            obj.status = 2
            obj.save()

            # 2. 更新审批表
            instance.show = False
            instance.approval_result = validated_data.get("approval_result", instance.approval_result)
            instance.approval_comment = validated_data.get("approval_comment", instance.approval_comment)
            instance.save()

            # 3. 更新成功, 返回实例
            return instance
        else:
            # 返回实例
            return instance
