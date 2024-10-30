

from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.generic import TemplateView
from myapp.models import  OperationInfo
from myapp.utils.logging_config import LoggingConfig
from django.conf import settings


logger = LoggingConfig()

# 会员管理系统
# 操作日志的查询
class OperationLogView(TemplateView):
    template_name = settings.OPERATION_LOGIN_PATH

    # 通过字段来查询
    def get(self, request, *args, **kwargs):

        # 检查是否为ajax请求，用于查询日志数据
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            starttime = request.GET.get('starttime')
            endtime = request.GET.get('endtime')
            logname = request.GET.get('logname')
            logphone = request.GET.get('logphone')
            page = int(request.GET.get('page', 1))
            page_size = int(request.GET.get('page_size', 10))
            # 查询所有的日志记录
            logs = OperationInfo.objects.all()

            if starttime and endtime:
                logs = OperationInfo.objects.filter(operationtime__gte=starttime, operationtime__lte=endtime)

            if logname:
                logs = OperationInfo.objects.filter(membername__contains=logname)

            if logphone:
                logs = OperationInfo.objects.filter(membername__contains=logphone)

            if logname and logphone:
                logs = OperationInfo.objects.filter(membername__exact=logname, membertelphone__exact=logphone)

            if starttime and endtime and logname and logphone:
                logs = OperationInfo.objects.filter(operationtime__gte=starttime, operationtime__lte=endtime,
                                                    membername__exact=logname, membertelphone__exact=logphone)

            # if not starttime and not endtime and not logname and not logphone:
            #     logs = OperationInfo.objects.all()
            # 分页
            paginator = Paginator(logs, page_size)
            members_page = paginator.get_page(page)

            # 序列化并格式化数据
            logs_list = [
                {
                    'operation_id': log.operation_id,
                    'operationtime': log.operationtime.strftime('%Y-%m-%d'),  # 格式化为 YYYY-MM-DD
                    'membername': log.membername,
                    'membertelphone': log.membertelphone,
                    'operationitem': log.operationitem,
                    'operationrequest': log.operationrequest
                }
                for log in members_page.object_list
            ]

            jsonre = {
                'logs': logs_list,
                'total_pages': paginator.num_pages
            }
            # 返回JSON响应
            return JsonResponse(jsonre)
        return super().get(request, *args, **kwargs)

