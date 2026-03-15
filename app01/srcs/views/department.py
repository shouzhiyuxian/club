from django.shortcuts import render, redirect
from app01.models import Department, Club
from app01.utils.page_nav import PageNav
from app01.srcs.forms.form import DepartmentModelForm
from app01.srcs.utils.role_helper import get_request_role


def department_list(req):
    """部门列表（社长仅见本社团部门）"""
    role_type, club_id_role, _ = get_request_role(req)
    if role_type == "member":
        return redirect("/member/profile/")
    search_data_dict = {}
    search_data = req.GET.get("q", "")
    club_id = req.GET.get("club_id", "")
    if role_type == "president" and club_id_role:
        club_id = str(club_id_role)
        search_data_dict["club_id"] = club_id_role
    if search_data:
        search_data_dict["name__contains"] = search_data
    if club_id and role_type != "president":
        search_data_dict["club_id"] = club_id
    queryset = Department.objects.filter(**search_data_dict).order_by("department_id")
    page_nav_obj = PageNav(req, queryset)
    clubs = Club.objects.all() if role_type == "admin" else Club.objects.filter(club_id=club_id_role)
    content = {
        "queryset": page_nav_obj.page_queryset,
        "page_nav_string": page_nav_obj.get_html(),
        "search_data": search_data,
        "clubs": clubs,
        "selected_club_id": club_id,
    }
    return render(req, "department/department_list.html", content)


def department_add(req):
    """添加部门（社长仅能选本社团）"""
    role_type, club_id_role, _ = get_request_role(req)
    if role_type == "member":
        return redirect("/member/profile/")
    if req.method == "GET":
        form = DepartmentModelForm()
        if role_type == "president" and club_id_role:
            form.fields["club"].queryset = Club.objects.filter(club_id=club_id_role)
            form.fields["club"].initial = Club.objects.filter(club_id=club_id_role).first()
        return render(req, "department/department_add.html", {"form": form})
    form = DepartmentModelForm(data=req.POST)
    if form.is_valid():
        if role_type == "president" and club_id_role:
            form.instance.club_id = club_id_role
        form.save()
        return redirect("/department/list")
    return render(req, "department/department_add.html", {"form": form})


def department_delete(req):
    """删除部门（社长仅能删本社团部门）"""
    role_type, club_id_role, _ = get_request_role(req)
    if role_type == "member":
        return redirect("/member/profile/")
    nid = req.GET.get("nid")
    obj = Department.objects.filter(department_id=nid).first()
    if obj and role_type == "president" and obj.club_id != club_id_role:
        return redirect("/department/list")
    Department.objects.filter(department_id=nid).delete()
    return redirect("/department/list")


def department_edit(req, nid):
    """编辑部门（社长仅能编辑本社团部门）"""
    role_type, club_id_role, _ = get_request_role(req)
    if role_type == "member":
        return redirect("/member/profile/")
    row_obj = Department.objects.filter(department_id=nid).first()
    if row_obj is None:
        return redirect("/department/list")
    if role_type == "president" and row_obj.club_id != club_id_role:
        return redirect("/department/list")
    
    if req.method == "GET":
        form = DepartmentModelForm(instance=row_obj)
        return render(req, "department/department_edit.html", {"form": form})
    
    form = DepartmentModelForm(data=req.POST, instance=row_obj)
    if form.is_valid():
        form.save()
        return redirect("/department/list")
    return render(req, "department/department_edit.html", {"form": form})

