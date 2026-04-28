# -*- coding: utf-8 -*-
"""招新管理：招新批次、招新报名、审核通过（转为正式成员）"""
from django.shortcuts import render, redirect
from django.http import HttpResponse
from app01.models import Recruitment, RecruitmentApplication, Club, Department, Role, Member
from app01.utils.page_nav import PageNav
from app01.utils.md5 import get_md5
from app01.srcs.forms.form import RecruitmentModelForm, RecruitmentApplicationModelForm
from app01.srcs.utils.export_excel import export_to_excel
from app01.srcs.utils.role_helper import get_request_role
from django.db import IntegrityError
import datetime


def _recruitment_queryset(req):
    search_data_dict = {}
    club_id = req.GET.get("club_id", "")
    q = req.GET.get("q", "")
    role_type, club_id_role, _ = get_request_role(req)
    if role_type == "president" and club_id_role:
        search_data_dict["club_id"] = club_id_role
    elif role_type == "member" and club_id:
        search_data_dict["club_id"] = club_id
    elif club_id:
        search_data_dict["club_id"] = club_id
    if q:
        search_data_dict["title__contains"] = q
    if role_type == "member":
        search_data_dict["status"] = 1
    return Recruitment.objects.filter(**search_data_dict).order_by("recruitment_id")


def recruitment_list(req):
    """招新批次列表（成员/社长仅见本社团招新）"""
    role_type, club_id_role, _ = get_request_role(req)
    if req.GET.get("export") == "1" and role_type != "member":
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
    clubs = Club.objects.all() if role_type == "admin" else Club.objects.filter(club_id=club_id_role)
    my_apply_status_map = {}
    my_apply_department_map = {}  # 存储申请部门信息
    my_club_id = None  # 当前成员已加入的社团ID
    if role_type in ("member", "president"):
        _, _, member_id = get_request_role(req)
        if member_id:
            # 获取成员信息，检查是否已加入社团
            me = Member.objects.filter(member_id=member_id).first()
            if me:
                my_club_id = me.club_id
            
            # 获取每个招新批次的最新申请状态（按申请时间倒序）
            applications = RecruitmentApplication.objects.filter(
                student_id=member_id
            ).order_by('-apply_time')
            
            # 使用字典存储每个招新批次的最新状态（先遇到的即最新的）
            for app in applications:
                if app.recruitment_id not in my_apply_status_map:
                    my_apply_status_map[app.recruitment_id] = app.status
                    my_apply_department_map[app.recruitment_id] = app.apply_department
            
            for obj in page_nav_obj.page_queryset:
                obj.my_apply_status = my_apply_status_map.get(obj.recruitment_id)
                obj.my_apply_department = my_apply_department_map.get(obj.recruitment_id)

    apply_result = req.GET.get("apply_result", "")
    apply_message_map = {
        "applied": "报名成功，已提交审核。",
        "reapplied": "已重新提交申请，等待审核。",
        "pending": "你已提交过申请，请勿重复提交。",
        "approved": "你已通过该批次审核，无需重复报名。",
        "conflict": "你已申请或已通过其他社团，不能同时报名多个社团。",
        "closed": "该招新批次已结束，无法报名。",
        "invalid": "报名失败，批次不存在或账号状态异常。",
    }
    content = {
        "queryset": page_nav_obj.page_queryset,
        "page_nav_string": page_nav_obj.get_html(),
        "clubs": clubs,
        "selected_club_id": str(club_id_role) if role_type in ("president", "member") else req.GET.get("club_id", ""),
        "search_data": req.GET.get("q", ""),
        "role_type": role_type,
        "apply_message": apply_message_map.get(apply_result, ""),
        "my_club_id": my_club_id,  # 已加入的社团ID，用于判断是否显示报名按钮
    }
    return render(req, "recruitment/recruitment_list.html", content)


def recruitment_add(req):
    """招新批次（社长仅能为本社团创建）"""
    role_type, club_id_role, _ = get_request_role(req)
    if role_type == "member":
        return redirect("/member/profile/")
    if req.method == "GET":
        form = RecruitmentModelForm()
        if role_type == "president" and club_id_role:
            form.fields["club"].queryset = Club.objects.filter(club_id=club_id_role)
            form.fields["club"].initial = Club.objects.filter(club_id=club_id_role).first()
        return render(req, "recruitment/recruitment_add.html", {"form": form})
    form = RecruitmentModelForm(data=req.POST)
    if form.is_valid():
        if role_type == "president" and club_id_role:
            form.instance.club_id = club_id_role
        if form.instance.create_time is None:
            form.instance.create_time = datetime.datetime.now()
        form.save()
        return redirect("/recruitment/list")
    return render(req, "recruitment/recruitment_add.html", {"form": form})


def recruitment_edit(req, nid):
    role_type, club_id_role, _ = get_request_role(req)
    if role_type == "member":
        return redirect("/member/profile/")
    row = Recruitment.objects.filter(recruitment_id=nid).first()
    if not row:
        return redirect("/recruitment/list")
    if role_type == "president" and row.club_id != club_id_role:
        return redirect("/recruitment/list")
    if req.method == "GET":
        return render(req, "recruitment/recruitment_edit.html", {"form": RecruitmentModelForm(instance=row)})
    form = RecruitmentModelForm(data=req.POST, instance=row)
    if form.is_valid():
        form.save()
        return redirect("/recruitment/list")
    return render(req, "recruitment/recruitment_edit.html", {"form": form})


def recruitment_delete(req):
    role_type, club_id_role, _ = get_request_role(req)
    if role_type == "member":
        return redirect("/member/profile/")
    nid = req.GET.get("nid")
    obj = Recruitment.objects.filter(recruitment_id=nid).first()
    if obj and role_type == "president" and obj.club_id != club_id_role:
        return redirect("/recruitment/list")
    Recruitment.objects.filter(recruitment_id=nid).delete()
    return redirect("/recruitment/list")


def _application_queryset(req):
    search_data_dict = {}
    role_type, club_id_role, _ = get_request_role(req)
    if role_type == "president" and club_id_role:
        search_data_dict["recruitment__club_id"] = club_id_role
    recruitment_id = req.GET.get("recruitment_id", "")
    status = req.GET.get("status", "")
    q = req.GET.get("q", "")
    if recruitment_id:
        search_data_dict["recruitment_id"] = recruitment_id
    if status:
        search_data_dict["status"] = status
    if q:
        search_data_dict["name__contains"] = q
    return RecruitmentApplication.objects.filter(**search_data_dict).order_by("application_id")


def application_list(req):
    """招新报名列表（社长仅见本社团招新的报名）"""
    role_type, club_id_role, _ = get_request_role(req)
    if role_type == "member":
        return redirect("/member/profile/")
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
    recruitments = (Recruitment.objects.filter(club_id=club_id_role) if role_type == "president" else Recruitment.objects.all()).order_by("recruitment_id")
    content = {
        "queryset": page_nav_obj.page_queryset,
        "page_nav_string": page_nav_obj.get_html(),
        "recruitments": recruitments,
        "selected_recruitment_id": req.GET.get("recruitment_id", ""),
        "selected_status": req.GET.get("status", ""),
        "search_data": req.GET.get("q", ""),
        "role_type": role_type,
    }
    return render(req, "recruitment/application_list.html", content)


def application_add(req):
    role_type, club_id_role, _ = get_request_role(req)
    me = None
    if role_type == "member":
        _, _, member_id = get_request_role(req)
        me = Member.objects.filter(member_id=member_id).first()
        if not me or not me.club_id:
            return redirect("/recruitment/list")
    if req.method == "GET":
        form = RecruitmentApplicationModelForm()
        if role_type == "president" and club_id_role:
            form.fields["recruitment"].queryset = Recruitment.objects.filter(club_id=club_id_role)
        elif role_type == "member" and me and me.club_id:
            form.fields["recruitment"].queryset = Recruitment.objects.filter(club_id=me.club_id, status=1)
            form.fields["student_id"].initial = me.member_id
            form.fields["name"].initial = me.name
            form.fields["gender"].initial = me.gender
            form.fields["grade"].initial = me.grade
            form.fields["major"].initial = me.major
            form.fields["phone"].initial = me.phone
            form.fields["email"].initial = me.email
        recruitment_id = req.GET.get("recruitment_id")
        if recruitment_id:
            r = Recruitment.objects.filter(recruitment_id=recruitment_id).first()
            can_use = False
            if role_type == "president":
                can_use = bool(r and r.club_id == club_id_role)
            elif role_type == "member":
                can_use = bool(r and me and r.club_id == me.club_id and r.status == 1)
            else:
                can_use = bool(r)
            if can_use:
                form.fields["recruitment"].initial = r
                form.fields["apply_department"].queryset = Department.objects.filter(club=r.club)
        return render(req, "recruitment/application_add.html", {"form": form})
    form = RecruitmentApplicationModelForm(data=req.POST)
    if form.is_valid():
        rec = form.cleaned_data.get("recruitment")
        if role_type == "member" and (not me or not rec or rec.club_id != me.club_id or rec.status != 1):
            return redirect("/recruitment/list")
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
    role_type, club_id_role, _ = get_request_role(req)
    if role_type == "member":
        return redirect("/recruitment/applications/")
    row = RecruitmentApplication.objects.filter(application_id=nid).first()
    if not row:
        return redirect("/recruitment/applications/")
    if role_type == "president" and row.recruitment.club_id != club_id_role:
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
    role_type, club_id_role, _ = get_request_role(req)
    if role_type == "member":
        return redirect("/member/profile/")
    nid = req.GET.get("nid")
    obj = RecruitmentApplication.objects.filter(application_id=nid).first()
    if obj and role_type == "president" and obj.recruitment.club_id != club_id_role:
        return redirect("/recruitment/applications/")
    RecruitmentApplication.objects.filter(application_id=nid).delete()
    return redirect("/recruitment/applications/")


def application_approve(req, nid):
    """审核通过（社长仅能审核本社团招新报名）"""
    role_type, club_id_role, _ = get_request_role(req)
    if role_type == "member":
        return redirect("/member/profile/")
    app = RecruitmentApplication.objects.filter(application_id=nid).first()
    if not app or app.status != 1:
        return redirect("/recruitment/applications/")
    if role_type == "president" and app.recruitment.club_id != club_id_role:
        return redirect("/recruitment/applications/")
    club = app.recruitment.club
    if not club:
        return redirect("/recruitment/applications/")
    # 招新申请来自系统内成员：通过时更新其社团归属并标记通过
    member = Member.objects.filter(member_id=app.student_id).first()
    if not member:
        app.status = 3
        app.remark = (app.remark or "") + " [审核失败: 申请成员不存在]"
        app.save(update_fields=["status", "remark"])
        return redirect("/recruitment/applications/")

    role = Role.objects.filter(level=2).first() or Role.objects.first()
    member.club = club
    member.department = app.apply_department
    member.role = role
    member.save(update_fields=["club", "department", "role"])

    app.status = 2
    app.save(update_fields=["status"])
    return redirect("/recruitment/applications/")


def application_reject(req, nid):
    """拒绝报名（管理员/社长）"""
    role_type, club_id_role, _ = get_request_role(req)
    if role_type == "member":
        return redirect("/member/profile/")
    app = RecruitmentApplication.objects.filter(application_id=nid).first()
    if not app or app.status != 1:
        return redirect("/recruitment/applications/")
    if role_type == "president" and app.recruitment.club_id != club_id_role:
        return redirect("/recruitment/applications/")
    app.status = 3
    app.save(update_fields=["status"])
    return redirect("/recruitment/applications/")


def recruitment_apply(req, nid):
    """成员一键报名本社团招新批次"""
    role_type, _, member_id = get_request_role(req)
    if role_type != "member" or not member_id:
        return redirect("/recruitment/list")
    me = Member.objects.filter(member_id=member_id).first()
    rec = Recruitment.objects.filter(recruitment_id=nid).first()
    if not me or not rec:
        return redirect("/recruitment/list?apply_result=invalid")
    # 仅允许报名状态为报名中的批次
    if rec.status != 1:
        return redirect("/recruitment/list?apply_result=closed")
    # 如果成员已加入某个社团，不能报名其他社团（只能报名本社团）
    if me.club_id and me.club_id != rec.club_id:
        return redirect("/recruitment/list?apply_result=conflict")
    # 禁止同时申请多个社团（待审核或已通过都视为占用）
    conflict_app = RecruitmentApplication.objects.filter(
        student_id=me.member_id,
        status__in=[1, 2],
        recruitment__club_id__isnull=False,
    ).exclude(recruitment__club_id=rec.club_id).first()
    if conflict_app:
        return redirect("/recruitment/list?apply_result=conflict")
    old_app = RecruitmentApplication.objects.filter(
        recruitment=rec,
        student_id=me.member_id,
    ).first()
    if old_app:
        # 已拒绝可再次提交：重置为待审核，并刷新申请信息
        if old_app.status == 3:
            old_app.name = me.name
            old_app.gender = me.gender
            old_app.grade = me.grade
            old_app.major = me.major
            old_app.phone = me.phone
            old_app.email = me.email
            old_app.status = 1
            old_app.apply_time = datetime.datetime.now()
            old_app.save(update_fields=[
                "name", "gender", "grade", "major", "phone", "email", "status", "apply_time"
            ])
            return redirect("/recruitment/list?apply_result=reapplied")
        if old_app.status == 1:
            return redirect("/recruitment/list?apply_result=pending")
        if old_app.status == 2:
            return redirect("/recruitment/list?apply_result=approved")
        return redirect("/recruitment/list")
    try:
        RecruitmentApplication.objects.create(
            recruitment=rec,
            student_id=me.member_id,
            name=me.name,
            gender=me.gender,
            grade=me.grade,
            major=me.major,
            phone=me.phone,
            email=me.email,
            status=1,
            apply_time=datetime.datetime.now(),
        )
    except IntegrityError:
        return redirect("/recruitment/list?apply_result=pending")
    return redirect("/recruitment/list?apply_result=applied")
