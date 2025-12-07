# 注意：此文件已废弃，PhoneNumbers 模型已被移除
# 保留此文件仅用于向后兼容，避免导入错误
from django.shortcuts import render, redirect


# 已废弃的函数
def number_list(req):
    from django.http import HttpResponse
    return HttpResponse("此功能已移除，请使用成员管理功能", status=404)


def number_add(req):
    from django.http import HttpResponse
    return HttpResponse("此功能已移除，请使用成员管理功能", status=404)


def number_edit(req, nid):
    from django.http import HttpResponse
    return HttpResponse("此功能已移除，请使用成员管理功能", status=404)


def number_delete(req):
    from django.http import HttpResponse
    return HttpResponse("此功能已移除，请使用成员管理功能", status=404)