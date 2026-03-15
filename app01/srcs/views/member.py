from django.shortcuts import render, redirect
from app01.models import Member, Club, Department, Role
from app01.utils.page_nav import PageNav
from app01.srcs.forms.form import MemberModelForm
from app01.srcs.utils.export_excel import export_to_excel


def _member_queryset(req):
    search_data_dict = {}
    if req.GET.get("q"):
        search_data_dict["name__contains"] = req.GET.get("q")
    if req.GET.get("club_id"):
        search_data_dict["club_id"] = req.GET.get("club_id")
    return Member.objects.filter(**search_data_dict).order_by("-join_time")


def member_list(req):
    """成员列表"""
    if req.GET.get("export") == "1":
        queryset = _member_queryset(req)
        headers = ["学号", "姓名", "性别", "年级", "专业", "手机", "邮箱", "所属社团", "所属部门", "角色", "加入时间", "状态", "备注"]
        rows = []
        for m in queryset:
            rows.append([
                m.member_id,
                m.name,
                m.get_gender_display() if m.gender else "",
                m.get_grade_display() if m.grade else "",
                m.major or "",
                m.phone or "",
                m.email or "",
                m.club.name if m.club else "",
                m.department.name if m.department else "",
                m.role.name if m.role else "",
                m.join_time,
                m.get_status_display(),
                (m.remark or "")[:100],
            ])
        return export_to_excel(rows, headers, filename="成员列表.xlsx", sheet_name="成员")
    
    queryset = _member_queryset(req)
    page_nav_obj = PageNav(req, queryset)
    content = {
        "queryset": page_nav_obj.page_queryset,
        "page_nav_string": page_nav_obj.get_html(),
        "search_data": req.GET.get("q", ""),
        "clubs": Club.objects.all(),
        "selected_club_id": req.GET.get("club_id", ""),
    }
    return render(req, "member/member_list.html", content)


def member_add(req):
    """添加成员"""
    if req.method == "GET":
        form = MemberModelForm()
        return render(req, "member/member_add.html", {"form": form})
    else:
        form = MemberModelForm(data=req.POST)
        if form.is_valid():
            if form.instance.join_time is None:
                import datetime
                form.instance.join_time = datetime.datetime.now()
            form.save()
            return redirect("/member/list")
        else:
            return render(req, "member/member_add.html", {"form": form})


def member_delete(req):
    """删除成员"""
    nid = req.GET.get("nid")
    Member.objects.filter(member_id=nid).delete()
    return redirect("/member/list")


def member_edit(req, nid):
    """编辑成员"""
    row_obj = Member.objects.filter(member_id=nid).first()
    if row_obj is None:
        return redirect("/member/list")
    
    ct = row_obj.join_time
    if req.method == "GET":
        form = MemberModelForm(instance=row_obj)
        return render(req, "member/member_edit.html", {"form": form})
    
    form = MemberModelForm(data=req.POST, instance=row_obj)
    if form.is_valid():
        if form.instance.join_time is None:
            form.instance.join_time = ct
        form.save()
        return redirect("/member/list")
    return render(req, "member/member_edit.html", {"form": form})

