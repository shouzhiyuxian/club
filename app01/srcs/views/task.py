# 注意：Task 模型已被移除，此文件已废弃
from django.shortcuts import render, redirect
from django.http import HttpResponse

# from app01 import models
# from app01.utils.bootstrap_modelform import BootstrapModelForm
# from app01.utils.page_nav import PageNav


# class TaskModelForm(BootstrapModelForm):
#     class Meta:
#         model = models.Task
#         fields = "__all__"


def task_list(request):
    # Task 功能已移除
    return HttpResponse("此功能已移除", status=404)

import json
from django.views.decorators.csrf import csrf_exempt
@csrf_exempt # 免除csrf_token认证，就可发post
def task_ajax(request):
    print(request.GET)
    print(request.POST)
    json_string = json.dumps(request.GET)
    return HttpResponse(json_string)


@csrf_exempt # 免除csrf_token认证，就可发post
def task_add(request):
    # print(request.POST)
    form = TaskModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        data_dict = {"status": True}
        return HttpResponse(json.dumps(data_dict))
    data_dict = {"status": False, "error": form.errors}
    return HttpResponse(json.dumps(data_dict, ensure_ascii=False))



