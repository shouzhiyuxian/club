from django.shortcuts import render, redirect
from app01.models import Department, Club
from app01.utils.page_nav import PageNav
from app01.srcs.forms.form import DepartmentModelForm


def department_list(req):
    """部门列表"""
    search_data_dict = {}
    search_data = req.GET.get("q", "")
    club_id = req.GET.get("club_id", "")
    
    if search_data:
        search_data_dict["name__contains"] = search_data
    
    if club_id:
        search_data_dict["club_id"] = club_id
    
    queryset = Department.objects.filter(**search_data_dict).order_by("-create_time")
    page_nav_obj = PageNav(req, queryset)
    page_queryset = page_nav_obj.page_queryset
    page_nav_string = page_nav_obj.get_html()
    
    # 获取所有社团用于筛选
    clubs = Club.objects.all()
    
    content = {
        "queryset": page_queryset,
        "page_nav_string": page_nav_string,
        "search_data": search_data,
        "clubs": clubs,
        "selected_club_id": club_id,
    }
    return render(req, "department/department_list.html", content)


def department_add(req):
    """添加部门"""
    if req.method == "GET":
        form = DepartmentModelForm()
        return render(req, "department/department_add.html", {"form": form})
    else:
        form = DepartmentModelForm(data=req.POST)
        if form.is_valid():
            form.save()
            return redirect("/department/list")
        else:
            return render(req, "department/department_add.html", {"form": form})


def department_delete(req):
    """删除部门"""
    nid = req.GET.get("nid")
    Department.objects.filter(department_id=nid).delete()
    return redirect("/department/list")


def department_edit(req, nid):
    """编辑部门"""
    row_obj = Department.objects.filter(department_id=nid).first()
    if row_obj is None:
        return redirect("/department/list")
    
    if req.method == "GET":
        form = DepartmentModelForm(instance=row_obj)
        return render(req, "department/department_edit.html", {"form": form})
    
    form = DepartmentModelForm(data=req.POST, instance=row_obj)
    if form.is_valid():
        form.save()
        return redirect("/department/list")
    return render(req, "department/department_edit.html", {"form": form})

