#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   : tanshuai
# @Contact  : tyh9436@gmail.com
# @Software : PyCharm
# @File     : ffilters.py
# @Time     : 18/7/3 16:37

from account.models import User
import django_filters
from django.db.models import Q


class UserFilter(django_filters.FilterSet):
    """
    用户过滤器类
    """
    name          = django_filters.CharFilter(method='SearchUser')

    def SearchUser(self, queryset, name, value):
        return queryset.filter(Q(name__icontains=value) | Q(username__icontains=value))

    class Meta:
        model = User
        fields = ['name', ]
