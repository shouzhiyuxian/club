# -*- coding: utf-8 -*-
"""招新管理：招新批次、招新报名、审核通过（转为正式成员）"""
from django.shortcuts import render, redirect
from django.http import HttpResponse
from app01.models import Recruitment, RecruitmentApplication, Club, Department, Role, Member
from app01.utils.page_nav import PageNav
from app01.srcs.forms.form import RecruitmentModelForm, RecruitmentApplicationModelForm
from app01.srcs.utils.export_excel import export_to_excel
import datetime


def _recruitment_queryset(req):
    """招新批次列表筛选（与 list 一致，供导出复用）"""
    search_data_dict = {}
    club_id = req.GET.get("club_id", "")
    q = req.GET.get("q", "")
    if club_id:
        search_data_dict["club_id"] = club_id
    if q:
        search_data_dict["title__contains"] = q
    return Recruitment.objects.filter(**search_data_dict).order_by("-create_time")


def recruitment_list(req):
    """招新批次列表"""
    if req.GET.get("export") == "1":
        queryset = _recruitment_queryset(req)
        headers = ["招新ID", "社团", "批次名称", "开始日期", "结束日期", "状态", "创建时间"]
        rows = []
        status_map = {1: "报名中", 2: "已结束"}
        for r in queryset:
            rows.append([
                r.recruitment_id,
                r.club.name if r.club else "",
                r.title,
                r.start_date.strftime("%Y-%m-%d") if r.start_date else "",
                r.end_date.strftime("%Y-%m-%d") if r.end_date else "",
                status_map.get(r.status, ""),
                r.create_time,
            ])
        return export_to_excel(rows, headers, filename="招新批次列表.xlsx", sheet_name="招新批次")
    
    queryset = _recruitment_queryset(req)
    page_nav_obj = PageNav(req, queryset)
    content = {
        "queryset": page_nav_obj.page_queryset,
        "page_nav_string": page_nav_obj.get_html(),
        "clubs": Club.objects.all(),
        "selected_club_id": req.GET.get("club_id", ""),
        "search_data": req.GET.get("q", ""),
    }
    return render(req, "recruitment/recruitment_list.html", content)


def recruitment_add(req):
    if req.method == "GET":
        return render(req, "recruitment/recruitment_add.html", {"form": RecruitmentModelForm()})
    form = RecruitmentModelForm(data=req.POST)
    if form.is_valid():
        if form.instance.create_time is None:
            form.instance.create_time = datetime.datetime.now()
        form.save()
        return redirect("/recruitment/list")
    return render(req, "recruitment/recruitment_add.html", {"form": form})


def recruitment_edit(req, nid):
    row = Recruitment.objects.filter(recruitment_id=nid).first()
    if not row:
        return redirect("/recruitment/list")
    if req.method == "GET":
        return render(req, "recruitment/recruitment_edit.html", {"form": RecruitmentModelForm(instance=row)})
    form = RecruitmentModelForm(data=req.POST, instance=row)
    if form.is_valid():
        form.save()
        return redirect("/recruitment/list")
    return render(req, "recruitment/recruitment_edit.html", {"form": form})


def recruitment_delete(req):
    nid = req.GET.get("nid")
    Recruitment.objects.filter(recruitment_id=nid).delete()
    return redirect("/recruitment/list")


def _application_queryset(req):
    search_data_dict = {}
    recruitment_id = req.GET.get("recruitment_id", "")
    status = req.GET.get("status", "")
    q = req.GET.get("q", "")
    if recruitment_id:
        search_data_dict["recruitment_id"] = recruitment_id
    if status:
        search_data_dict["status"] = status
    if q:
        search_data_dict["name__contains"] = q
    return RecruitmentApplication.objects.filter(**search_data_dict).order_by("-apply_time")


def application_list(req):
    """招新报名列表"""
    if req.GET.get("export") == "1":
        queryset = _application_queryset(req)
        headers = ["报名ID", "招新批次", "学号", "姓名", "性别", "年级", "专业", "手机", "邮箱", "申请部门", "状态", "申请时间", "备注"]
        rows = []
        gender_map = {1: "男", 2: "女"}
        grade_map = {1: "大一", 2: "大二", 3: "大三", 4: "大四", 5: "研究生"}
        status_map = {1: "待审核", 2: "已通过", 3: "已拒绝"}
        for a in queryset:
            rows.append([
                a.application_id,
                a.recruitment.title if a.recruitment else "",
                a.student_id,
                a.name,
                gender_map.get(a.gender, ""),
                grade_map.get(a.grade, ""),
                a.major or "",
                a.phone or "",
                a.email or "",
                a.apply_department.name if a.apply_department else "",
                status_map.get(a.status, ""),
                a.apply_time,
                (a.remark or "")[:50],
            ])
        return export_to_excel(rows, headers, filename="招新报名列表.xlsx", sheet_name="招新报名")
    
    queryset = _application_queryset(req)
    page_nav_obj = PageNav(req, queryset)
    content = {
        "queryset": page_nav_obj.page_queryset,
        "page_nav_string": page_nav_obj.get_html(),
        "recruitments": Recruitment.objects.all().order_by("-create_time"),
        "selected_recruitment_id": req.GET.get("recruitment_id", ""),
        "selected_status": req.GET.get("status", ""),
        "search_data": req.GET.get("q", ""),
    }
    return render(req, "recruitment/application_list.html", content)


def application_add(req):
    if req.method == "GET":
        form = RecruitmentApplicationModelForm()
        recruitment_id = req.GET.get("recruitment_id")
        if recruitment_id:
            r = Recruitment.objects.filter(recruitment_id=recruitment_id).first()
            if r:
                form.fields["recruitment"].initial = r
                form.fields["apply_department"].queryset = Department.objects.filter(club=r.club)
        return render(req, "recruitment/application_add.html", {"form": form})
    form = RecruitmentApplicationModelForm(data=req.POST)
    if form.is_valid():
        rec = form.cleaned_data.get("recruitment")
        sid = form.cleaned_data.get("student_id")
        if RecruitmentApplication.objects.filter(recruitment=rec, student_id=sid).exists():
            form.add_error("student_id", "该学号已在此批次报名")
            return render(req, "recruitment/application_add.html", {"form": form})
        if form.instance.apply_time is None:
            form.instance.apply_time = datetime.datetime.now()
        form.save()
        return redirect("/recruitment/applications/")
    return render(req, "recruitment/application_add.html", {"form": form})


def application_edit(req, nid):
    row = RecruitmentApplication.objects.filter(application_id=nid).first()
    if not row:
        return redirect("/recruitment/applications/")
    if req.method == "GET":
        form = RecruitmentApplicationModelForm(instance=row)
        if row.recruitment and row.recruitment.club_id:
            form.fields["apply_department"].queryset = Department.objects.filter(club_id=row.recruitment.club_id)
        return render(req, "recruitment/application_edit.html", {"form": form})
    form = RecruitmentApplicationModelForm(data=req.POST, instance=row)
    if form.is_valid():
        form.save()
        return redirect("/recruitment/applications/")
    return render(req, "recruitment/application_edit.html", {"form": form})


def application_delete(req):
    nid = req.GET.get("nid")
    RecruitmentApplication.objects.filter(application_id=nid).delete()
    return redirect("/recruitment/applications/")


def application_approve(req, nid):
    """审核通过：创建正式成员并更新报名状态"""
    app = RecruitmentApplication.objects.filter(application_id=nid).first()
    if not app or app.status != 1:
        return redirect("/recruitment/applications/")
    club = app.recruitment.club
    if not club:
        return redirect("/recruitment/applications/")
    # 普通成员角色
    role = Role.objects.filter(level=5).first() or Role.objects.first()
    if Member.objects.filter(member_id=app.student_id).exists():
        app.status = 3
        app.remark = (app.remark or "") + " [审核失败: 学号已存在]"
        app.save()
        return redirect("/recruitment/applications/")
    Member.objects.create(
        member_id=app.student_id,
        name=app.name,
        gender=app.gender,
        grade=app.grade,
        major=app.major,
        phone=app.phone,
        email=app.email,
        club=club,
        department=app.apply_department,
        role=role,
        join_time=datetime.datetime.now(),
        status=1,
    )
    app.status = 2
    app.save()
    return redirect("/recruitment/applications/")
