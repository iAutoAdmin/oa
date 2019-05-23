#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   : tanshuai
# @Contact  : tyh9436@gmail.com
# @Software : PyCharm
# @File     : serializers.py
# @Time     : 18/6/24 09:29

from rest_framework import serializers
from account.models import User, Department


class UserSerializer(serializers.ModelSerializer):
    """
    用户序列化类
    """

    class Meta:
        model = User
        fields = ['id', 'name', 'tel', 'username', 'department']
        read_only_fields = ('id',)

    def to_representation(self, instance):
        ret = super(UserSerializer, self).to_representation(instance)
        ret['is_active'] = instance.is_active
        ret['last_login'] = instance.last_login
        return ret

    def create(self, validated_data):
        return User.objects.create(**validated_data)

    def update(self, instance, validated_data):
        User.objects.filter(id=instance.id).update(**validated_data)
        return instance


class AuthUserSerializer(serializers.Serializer):
    """
    用户序列化类
    """
    username        = serializers.CharField()
    password        = serializers.CharField()


class DepartmentSerializer(serializers.ModelSerializer):
    """
    部门序列化类
    """

    class Meta:
        model = Department
        fields = '__all__'

    def get_user_members(self, department_id):
        # 经测试不能使用department.user_set.all()这种方法来查询一个部门下都有哪些用户，故此使用User模型的filter来解决此问题
        user_objs = User.objects.filter(department=department_id)
        user_list = []
        # 使用循环获取用户的名字，存入列表并返回，提供接口展示(JSON里的字段不能是obj，所以必须给个字符串)
        for user_obj in user_objs:
            user_list.append(user_obj.name)
        return user_list

    def get_children_fields(self, instance):
        # 序列化部门字段
        ret = {
            "id": instance.id,
            "department_name": instance.department_name,
            "level": instance.level,
            "is_deleted": instance.is_deleted,
            "parent_dept": instance.parent_dept_id,
            "leader": instance.leader.name,
            "user_members": self.get_user_members(instance.id)
        }
        # print(instance.user_set.all())
        return ret

    def get_children(self, instance):
        # 序列化当前部门信息, 并存入最终返回的ret变量中
        ret = self.get_children_fields(instance)
        # 获取所有部门对象,用于查找出一级部门和二级部门
        all_obj = Department.objects.all()
        # 查找出当前事业部的所有一级部门, 序列化一级部门并保存一级部门对象,提供查找二级部门使用;
        children = []
        for dp_obj in all_obj:
            if instance.id == dp_obj.parent_dept_id:
                ret['children'] = children
                children.append(self.get_children_fields(dp_obj))
        # 查找出当前一级部门下有哪些二级部门,序列化二级部门并加入一级部门序列化中,
        for one_obj in children:
            one_obj_id = one_obj.get('id', None)
            children = []
            for dp_obj in all_obj:
                if one_obj_id == dp_obj.parent_dept_id:
                    one_obj['children'] = children
                    one_obj['children'].append(self.get_children_fields(dp_obj))
        return ret

    def to_representation(self, instance):
        # ret = super(DepartmentSerializer, self).to_representation(instance)
        # 根据部门级别来展示子部门信息
        if instance.level == 'syb':
            # 如果是事业部，则会向下查找该事业部有哪些一级部门，继续递归向下查找一级部门下有哪些二级部门
            ret = self.get_children(instance)
        elif instance.level == 'one':
            # 如果是一级部门，则向下查找该一级部门有哪些二级部门，序列化并展示
            ret = self.get_children(instance)
        else:
            # 如果以上两个都不满足，则只剩下二级部门，那直接序列化二级部门并展示即可
            ret = self.get_children(instance)
        return ret
