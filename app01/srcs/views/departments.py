from django.shortcuts import render, redirect

from app01.models import Department
from app01.utils.page_nav import PageNav


# 注意：此文件已废弃，请使用 app01.srcs.views.department 中的视图
# 保留此文件仅用于向后兼容，避免导入错误

def depart_list(request):
    # 重定向到新的部门管理页面
    return redirect("/department/list")


def depart_add(request):
    return redirect("/department/add")


def depart_delete(req):
    nid = req.GET.get("nid")
    from app01.models import Department
    Department.objects.filter(department_id=nid).delete()
    return redirect("/department/list")


def depart_edit(req, nid):
    return redirect(f"/department/{nid}/edit")