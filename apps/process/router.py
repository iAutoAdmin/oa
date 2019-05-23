#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   : tanshuai
# @Contact  : tyh9436@gmail.com
# @Software : PyCharm
# @File     : router.py
# @Time     : 18/7/22 17:30

from rest_framework.routers import DefaultRouter
from .views import ProcessViewSet, ApprovalProcessViewSet

process_router = DefaultRouter()
process_router.register("Process", ProcessViewSet, base_name='Process')
process_router.register("ApprovalProcess", ApprovalProcessViewSet, base_name='ApprovalProcess')
