# myapp/urls.py
from django.urls import path
from myapp.views.views_member import MemberManagementView
from myapp.views.views_auth import LoginView
from myapp.views.views_logs import OperationLogView

urlpatterns = [
    path('member-management/', MemberManagementView.as_view(), name='member-management'), #会员管理页面
    path('operation-log/', OperationLogView.as_view(), name='operation-log'), #操作日志
    path('login/', LoginView.as_view(), name='login'), #登录
]

