#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   : tanshuai
# @Contact  : tyh9436@gmail.com
# @Software : PyCharm
# @File     : ffilters.py
# @Time     : 18/7/3 16:37

from process.models import Process
import django_filters
from django.db.models import Q


class ProcessFilter(django_filters.FilterSet):
    """
    用户过滤器类
    """
    title          = django_filters.CharFilter(method='SearchProcess')

    def SearchProcess(self, queryset, title, value):
        return queryset.filter(Q(title__icontains=value))

    class Meta:
        model = Process
        fields = ['title', ]
