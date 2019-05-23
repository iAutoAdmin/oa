#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   : tanshuai
# @Contact  : tyh9436@gmail.com
# @Software : PyCharm
# @File     : pagination.py
# @Time     : 18/7/3 11:49

from rest_framework.pagination import PageNumberPagination


class Pagination(PageNumberPagination):
    page_size_query_param = 'page_size'

    # def get_page_size(self, request):
    #     try:
    #         page_size = int(request.query_params.get('page_size', 0))
    #         if page_size < 0:
    #             return self.page_size
    #         return page_size
    #     except:
    #         pass
    #     return self.page_size


