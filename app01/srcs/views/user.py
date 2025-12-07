# 注意：此文件已废弃，UserInfo 模型已被 Member 模型替代
# 保留此文件仅用于向后兼容，避免导入错误
from django.shortcuts import render, redirect


# 已废弃的函数，重定向到新的成员管理页面
def user_list(req):
    return redirect("/member/list")


def user_add(req):
    return redirect("/member/add")


def user_delete(req):
    nid = req.GET.get("nid")
    from app01.models import Member
    Member.objects.filter(member_id=nid).delete()
    return redirect("/member/list")


def user_edit(req, nid):
    return redirect(f"/member/{nid}/edit")