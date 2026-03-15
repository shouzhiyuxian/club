from django.shortcuts import render, redirect
from app01.models import ActivityRegistration, Activity, Member
from app01.utils.page_nav import PageNav
from app01.srcs.forms.form import ActivityRegistrationModelForm
from app01.srcs.utils.export_excel import export_to_excel
from app01.srcs.utils.role_helper import get_request_role


def _registration_queryset(req):
    search_data_dict = {}
    role_type, club_id_role, _ = get_request_role(req)
    if role_type == "president" and club_id_role:
        search_data_dict["activity__club_id"] = club_id_role
    if req.GET.get("activity_id"):
        search_data_dict["activity_id"] = req.GET.get("activity_id")
    if req.GET.get("member_id"):
        search_data_dict["member_id"] = req.GET.get("member_id")
    return ActivityRegistration.objects.filter(**search_data_dict).order_by("registration_id")


def registration_list(req):
    """活动报名列表（社长仅见本社团活动的报名）"""
    role_type, club_id_role, _ = get_request_role(req)
    if role_type == "member":
        return redirect("/member/my-registrations/")
    queryset = _registration_queryset(req)
    if req.GET.get("export") == "1":
        status_map = {1: "已报名", 2: "已参加", 3: "已取消", 4: "未参加"}
        headers = ["报名ID", "活动", "成员", "学号", "报名时间", "状态", "备注"]
        rows = [[r.registration_id, r.activity.title, r.member.name, r.member.member_id, r.register_time, status_map.get(r.status, ""), (r.remark or "")[:50]] for r in queryset]
        return export_to_excel(rows, headers, filename="活动报名列表.xlsx", sheet_name="活动报名")
    
    page_nav_obj = PageNav(req, queryset)
    activities = Activity.objects.all() if role_type == "admin" else Activity.objects.filter(club_id=club_id_role)
    members = Member.objects.all() if role_type == "admin" else Member.objects.filter(club_id=club_id_role)
    content = {
        "queryset": page_nav_obj.page_queryset,
        "page_nav_string": page_nav_obj.get_html(),
        "activities": activities,
        "members": members,
        "selected_activity_id": req.GET.get("activity_id", ""),
        "selected_member_id": req.GET.get("member_id", ""),
    }
    return render(req, "registration/registration_list.html", content)


def registration_add(req):
    """添加活动报名（社长仅能选本社团活动与成员）"""
    role_type, club_id_role, _ = get_request_role(req)
    if role_type == "member":
        return redirect("/member/my-registrations/")
    if req.method == "GET":
        form = ActivityRegistrationModelForm()
        if role_type == "president" and club_id_role:
            form.fields["activity"].queryset = Activity.objects.filter(club_id=club_id_role)
            form.fields["member"].queryset = Member.objects.filter(club_id=club_id_role)
        activity_id = req.GET.get("activity_id")
        if activity_id:
            try:
                activity = Activity.objects.get(activity_id=activity_id)
                if role_type != "president" or activity.club_id == club_id_role:
                    form.fields["activity"].initial = activity
            except Activity.DoesNotExist:
                pass
        return render(req, "registration/registration_add.html", {"form": form})
    else:
        form = ActivityRegistrationModelForm(data=req.POST)
        if form.is_valid():
            # 检查是否已经报名
            activity = form.cleaned_data.get("activity")
            member = form.cleaned_data.get("member")
            if ActivityRegistration.objects.filter(activity=activity, member=member).exists():
                form.add_error("member", "该成员已经报名此活动")
                return render(req, "registration/registration_add.html", {"form": form})
            
            # 更新活动的当前参与人数
            if form.instance.register_time is None:
                import datetime
                form.instance.register_time = datetime.datetime.now()
            
            form.save()
            
            # 更新活动的当前参与人数
            activity.current_participants = activity.registrations.filter(status__in=[1, 2]).count()
            activity.save()
            
            return redirect("/registration/list")
        else:
            return render(req, "registration/registration_add.html", {"form": form})


def registration_delete(req):
    """删除活动报名（社长仅能删本社团活动的报名）"""
    role_type, club_id_role, _ = get_request_role(req)
    if role_type == "member":
        return redirect("/member/my-registrations/")
    nid = req.GET.get("nid")
    registration = ActivityRegistration.objects.filter(registration_id=nid).first()
    if registration and role_type == "president" and registration.activity.club_id != club_id_role:
        return redirect("/registration/list")
    if registration:
        activity = registration.activity
        registration.delete()
        # 更新活动的当前参与人数
        activity.current_participants = activity.registrations.filter(status__in=[1, 2]).count()
        activity.save()
    return redirect("/registration/list")


def registration_edit(req, nid):
    """编辑活动报名（社长仅能编辑本社团活动的报名）"""
    role_type, club_id_role, _ = get_request_role(req)
    if role_type == "member":
        return redirect("/member/my-registrations/")
    row_obj = ActivityRegistration.objects.filter(registration_id=nid).first()
    if row_obj is None:
        return redirect("/registration/list")
    if role_type == "president" and row_obj.activity.club_id != club_id_role:
        return redirect("/registration/list")
    
    if req.method == "GET":
        form = ActivityRegistrationModelForm(instance=row_obj)
        return render(req, "registration/registration_edit.html", {"form": form})
    
    form = ActivityRegistrationModelForm(data=req.POST, instance=row_obj)
    if form.is_valid():
        form.save()
        # 更新活动的当前参与人数
        activity = form.instance.activity
        activity.current_participants = activity.registrations.filter(status__in=[1, 2]).count()
        activity.save()
        return redirect("/registration/list")
    return render(req, "registration/registration_edit.html", {"form": form})

