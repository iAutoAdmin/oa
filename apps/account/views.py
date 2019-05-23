from django.shortcuts import render

# Create your views here.

from rest_framework import viewsets, mixins
from .serializers import UserSerializer, AuthUserSerializer, DepartmentSerializer
from .filters import UserFilter
from account.models import User, Department
from rest_framework.response import Response
from django.http import JsonResponse
from django.contrib.auth import authenticate


class UserViewset(viewsets.ModelViewSet):
    """
    retrieve:
        返回指定单个用户信息
    list:
        返回用户列表
    update:
        更新用户信息
    destroy:
        删除用户记录
    create:
        创建用户资源
    partial_update:
        更新部分字段
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_class = UserFilter
    filter_fields = ("name",)
    extra_perm_map = {
        "GET": ['auth.view_user', ]
    }


class UserInfoAPIView(viewsets.GenericViewSet, mixins.ListModelMixin):
    """
    获取当前登陆的用户信息
    """
    def get_department_fields(self, instance):
        ret = {
            "id": instance.id,
            "department_name": instance.department_name,
            "leader": instance.leader.name,
            "email": instance.leader.email
        }
        return ret

    def list(self, request, *args, **kwargs):
        email = request.query_params.get('email', None)
        ret = {"code": 1, "msg": "请传入email地址获取用户信息."}
        department = {}

        try:
            userobj = User.objects.get(email=email)
        except:
            return JsonResponse(ret)

        if userobj.department is not None:
            if userobj.department.level == 'two':
                two_dp = self.get_department_fields(userobj.department)
                one_dp = self.get_department_fields(userobj.department.parent_dept)
                syb_dp = self.get_department_fields(userobj.department.parent_dept.parent_dept)
                syb_dp['one_children'] = one_dp
                syb_dp['one_children']['two_children'] = two_dp
                department = syb_dp
            elif userobj.department.level == 'one':
                one_dp = self.get_department_fields(userobj.department)
                syb_dp = self.get_department_fields(userobj.department.parent_dept)
                syb_dp['one_children'] = one_dp
                department = syb_dp
            else:
                syb_dp = self.get_department_fields(userobj.department)
                department = syb_dp

        ret = {"id": userobj.id, "name": userobj.name, "tel": userobj.tel, "email": userobj.email,
               'department': department}
        return JsonResponse(ret, safe=True)


class AuthUserAPIView(viewsets.GenericViewSet, mixins.CreateModelMixin):
    """
    create：
        接收用户认证POST请求，进行查询判断，返回用户认证结果
    """
    queryset = User.objects.all()
    serializer_class = AuthUserSerializer

    def create(self, request, *args, **kwargs):
        # print(request.data)
        # userToken = request.data.get('csrfmiddlewaretoken', None)
        username  = request.data.get('username', None)
        password  = request.data.get('password', None)
        ret = {"code": 1, "msg": '用户认证失败!'}
        # 验证用户名和密码
        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            # userobj = User.objects.get(username=username)
            ret = {
                "code": 0,
                "username": user.username,
                "email": user.email,
                "msg": '用户认证成功!'
            }
        return JsonResponse(ret, safe=True)


class DepartmentViewset(viewsets.ModelViewSet):
    """
    list:
        获取部门列表
    create:
        添加部门
    retrieve:
        获取指定部门记录
    update:
        修改部门记录
    """
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
