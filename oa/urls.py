"""ops URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from rest_framework.documentation import include_docs_urls
from rest_framework_jwt.views import obtain_jwt_token

# All app router
from account.router import account_router
from process.router import process_router

route = DefaultRouter()
route_list = [account_router, process_router]

for num in range(0, len(route_list)):
    route.registry.extend(route_list[num].registry)

urlpatterns = [
    url(r'^', include(route.urls)),
    url(r'^api-auth', include("rest_framework.urls", namespace="rest_framework")),
    url(r'^docs/', include_docs_urls("接口文档")),
    url(r'^api-token-auth/', obtain_jwt_token),
]

