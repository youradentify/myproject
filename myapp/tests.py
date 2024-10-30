
from django.test import TestCase

# Create your tests here.
import time
from django.contrib.auth.models import User

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myapp.settings')
django.setup()

# 替换 'your_project_name' 为你 Django 项目的名称
user = User.objects.get(username='mayor')  # 替换 'username' 为你要查询的用户名
print(user.last_login)









