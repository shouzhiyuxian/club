from django.shortcuts import render, redirect
from app01.models import Role
from app01.utils.page_nav import PageNav
from app01.srcs.forms.form import RoleModelForm
from app01.srcs.utils.role_helper import get_request_role


def role_list(req):
    """角色列表（仅管理员）"""
    if get_request_role(req)[0] != "admin":
        return redirect("/")
    queryset = Role.objects.all().order_by("role_id")
    content = {
        "queryset": queryset,
    }
    return render(req, "role/role_list.html", content)


def role_add(req):
    """添加角色（仅管理员）"""
    if get_request_role(req)[0] != "admin":
        return redirect("/")
    if req.method == "GET":
        form = RoleModelForm()
        return render(req, "role/role_add.html", {"form": form})
    else:
        form = RoleModelForm(data=req.POST)
        if form.is_valid():
            form.save()
            return redirect("/role/list")
        else:
            return render(req, "role/role_add.html", {"form": form})


def role_delete(req):
    """删除角色（仅管理员）"""
    if get_request_role(req)[0] != "admin":
        return redirect("/")
    nid = req.GET.get("nid")
    Role.objects.filter(role_id=nid).delete()
    return redirect("/role/list")


def role_edit(req, nid):
    """编辑角色（仅管理员）"""
    if get_request_role(req)[0] != "admin":
        return redirect("/")
    row_obj = Role.objects.filter(role_id=nid).first()
    if row_obj is None:
        return redirect("/role/list")
    
    if req.method == "GET":
        form = RoleModelForm(instance=row_obj)
        return render(req, "role/role_edit.html", {"form": form})
    
    form = RoleModelForm(data=req.POST, instance=row_obj)
    if form.is_valid():
        form.save()
        return redirect("/role/list")
    return render(req, "role/role_edit.html", {"form": form})

