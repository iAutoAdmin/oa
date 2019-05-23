#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   : tanshuai
# @Contact  : tyh9436@gmail.com
# @Software : PyCharm
# @File     : router.py
# @Time     : 18/7/22 17:30

from rest_framework.routers import DefaultRouter
from .views import UserViewset
from .views import UserInfoAPIView
from .views import AuthUserAPIView
from .views import DepartmentViewset

account_router = DefaultRouter()
account_router.register("User", UserViewset, base_name='User')
account_router.register("UserInfo", UserInfoAPIView, base_name='UserInfo')
account_router.register("AuthUser", AuthUserAPIView, base_name='AuthUser')
account_router.register("Department", DepartmentViewset, base_name='Department')
