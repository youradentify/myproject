

from django.http import JsonResponse
from django.contrib.auth import views as auth_views
from django.shortcuts import render  # 导入渲染和重定向函数
from django.contrib.auth import authenticate, login  # 导入认证和登录函数
from myapp.utils.logging_config import LoggingConfig
from django.conf import settings

logger = LoggingConfig()

# 会员管理系统
# 登录视图
class LoginView(auth_views.LoginView):
    template_name = settings.AUTH_PATH

    # 校验密码是不是正确
    def form_valid(self, form):
        if 'member_id' in self.request.session:  # 如果用户已登录
            return JsonResponse({'redirect_url': '/member-management/'})  # 重定向到会员管理页面

        if self.request.method == 'POST':  # 如果请求方法是 POST
            username = self.request.POST['username']  # 获取用户名
            password = self.request.POST['password']  # 获取密码
            # print(username, password)
            # 使用 authenticate 进行用户验证
            user = authenticate(username=username, password=password)  # 验证用户名和密码
            if user is not None:  # 如果用户存在
                login(self.request, user)  # 登录用户
                return JsonResponse({'redirect_url': '/member-management/'})  # 重定向到会员管理页面
            else:
                # print(username, password)
                return render(self.request, settings.AUTH_PATH,
                              {'error_message': '用户名或密码错误'})  # 用户名或密码错误
        elif self.request.method == 'GET':
            return render(self.request, settings.AUTH_PATH)  # 如果请求方法是 GET，则渲染登录页面

    def form_invalid(self, form):
        username = self.request.POST['username']  # 获取用户名
        password = self.request.POST['password']  # 获取密码
        return super().form_invalid(form)

