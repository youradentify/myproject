import json
from datetime import datetime

from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.generic import TemplateView
from myapp.models import MemberInfo, OperationInfo
from django.contrib.auth.mixins import LoginRequiredMixin
from myapp.utils.logging_config import LoggingConfig
from myapp.forms import MemberForm
from django.conf import settings


logger = LoggingConfig()

# 会员管理系统
# 会员管理主页面
class MemberManagementView(LoginRequiredMixin,TemplateView):
    template_name = settings.MEMBER_MANAGEMENT_PATH
    # POST新增会员的逻辑是先查询存量的数据是不是存在，如果存在则直接返回存量的数据，如果不存在，则新增数据，然后返回新增的数据
    def post(self, request, *args, **kwargs):
        # 处理新增会员请求
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            logger.get_logger().info(request.body)
            data = json.loads(request.body)
            # 一般技术校验
            form = MemberForm(data)
            if form.is_valid():
                name = data.get('name')
                phone = data.get('phone')
                purchasecount = data.get('purchase_count')
                remainingcount = data.get('remaining_count')

            else:
                # 返回表单错误信息
                return JsonResponse({'errors': form.errors}, status=400)
            # 查询是否已存在相同姓名和电话的会员
            if MemberInfo.objects.filter(membername=name, membertelphone=phone).exists():
                return JsonResponse({'error': '存量数据已经存在，请查询后编辑'}, status=400)

            # 创建新会员
            new_member = MemberInfo.objects.create(membername=name, membertelphone=phone,
                                                   memberpurchasecount=purchasecount, memberremaincount=remainingcount)
            # 添加日志
            operation_request = {'membername': name, 'membertelphone': phone, 'memberpurchasecount': purchasecount,
                                 'memberremaincount': remainingcount}
            return JsonResponse({'message': '会员新增成功', 'membername': new_member.membername})
        else:
            return JsonResponse({'message': '不支持的请求方式'}, status=405)

    # 会员资料更新
    def put(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            data = json.loads(request.body)
            lable = int(data.get('lable'))
            form = MemberForm(data)
            try:
                if lable == 1:
                    if form.is_valid():
                        name = data.get('name')
                        phone = data.get('phone')
                        purchase_count = data.get('purchase_count')
                        remaining_count = data.get('remaining_count')
                        member = MemberInfo.objects.get(membername=name, membertelphone=phone)
                        if member:
                            oldmemberpurchasecount = member.memberpurchasecount
                            oldmemberremaincount = member.memberremaincount
                            # 更新会员信息
                            member.membername = name
                            member.membertelphone = phone
                            member.memberpurchasecount = purchase_count
                            member.memberremaincount = remaining_count
                            # 保存更新后的信息
                            member.save()
                            # 添加日志
                            operation_request = {'newmembername': name, 'newmembertelphone': phone,
                                                 'newmemberpurchasecount': purchase_count,
                                                 'oldmemberpurchasecount': oldmemberpurchasecount,
                                                 'newmemberremaincount': purchase_count,'oldmemberremaincount': oldmemberremaincount}
                            self.add_logs(name, phone, '更新剩余次数', operation_request)
                            return JsonResponse({'message': '会员更新成功', 'memberid': member.member_id})
                        else:
                            return JsonResponse({'message': '会员信息不存在'},status=405)
                    else:
                        return JsonResponse({'errors': form.errors}, status=400)
                if lable == 2:
                    name = data.get('name')
                    phone = data.get('phone')
                    purchase_count = data.get('purchase_count')
                    if purchase_count is not None and purchase_count !='' and purchase_count > 0 and isinstance(purchase_count, int) and purchase_count <= 100:
                        member = MemberInfo.objects.get(membername=name, membertelphone=phone)
                        if member:
                            oldmemberpurchasecount = member.memberpurchasecount
                            oldmemberremaincount = member.memberremaincount
                            # 更新会员信息
                            member.membername = name
                            member.membertelphone = phone
                            member.memberpurchasecount = purchase_count + int(oldmemberpurchasecount)
                            member.memberremaincount = purchase_count + int(oldmemberremaincount)
                            # 保存更新后的信息
                            member.save()
                            # 添加日志
                            operation_request = {'newmembername': name, 'newmembertelphone': phone,
                                                 'newmemberpurchasecount': purchase_count,
                                                 'oldmemberpurchasecount': oldmemberpurchasecount,
                                                 'newmemberremaincount': purchase_count,
                                                 'oldmemberremaincount': oldmemberremaincount}
                            self.add_logs(name, phone, '新增购买次数', operation_request)
                            return JsonResponse({'message': '会员更新成功', 'memberid': member.member_id})
                        else:
                            return JsonResponse({'message': '会员信息不存在'},status=405)
            except json.JSONDecodeError:
                return JsonResponse({'error': '无效的JSON数据'}, status=400)

    # 添加操作日志
    def add_logs(self, member_name, member_telphone, operation_item, operation_request):
        operation_time = datetime.now().strftime('%Y-%m-%d')
        new_log = OperationInfo.objects.create(operationtime=operation_time,
                                               membername=member_name, membertelphone=member_telphone,
                                               operationitem=operation_item, operationrequest=operation_request)
        return new_log.operation_id

    # 通过字段来查询
    def get(self, request, *args, **kwargs):
        # 检查是否为ajax请求，用于查询会员数据
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            name = request.GET.get('name')
            phone = request.GET.get('phone')
            page = int(request.GET.get('page', 1))
            page_size = int(request.GET.get('page_size', 10))

            # 查询会员数据
            members = MemberInfo.objects.all()
            if name:
                members = members.filter(membername__contains=name)
            if phone:
                members = members.filter(membertelphone__contains=phone)
            if name and phone:
                members = members.filter(membername=name, membertelphone=phone)

            if not members:
                members = MemberInfo.objects.all()

            members = members.values('member_id', 'membername', 'membertelphone', 'memberpurchasecount',
                                     'memberremaincount')
            # 分页
            paginator = Paginator(members, page_size)
            members_page = paginator.get_page(page)
            member_list = list(members_page)

            # 返回JSON响应
            return JsonResponse({
                'members': member_list,
                'total_pages': paginator.num_pages
            })

        return super().get(request, *args, **kwargs)

