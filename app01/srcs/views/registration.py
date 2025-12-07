from django.shortcuts import render, redirect
from app01.models import ActivityRegistration, Activity, Member
from app01.utils.page_nav import PageNav
from app01.srcs.forms.form import ActivityRegistrationModelForm
from django.http import JsonResponse


def registration_list(req):
    """活动报名列表"""
    search_data_dict = {}
    activity_id = req.GET.get("activity_id", "")
    member_id = req.GET.get("member_id", "")
    
    if activity_id:
        search_data_dict["activity_id"] = activity_id
    
    if member_id:
        search_data_dict["member_id"] = member_id
    
    queryset = ActivityRegistration.objects.filter(**search_data_dict).order_by("-register_time")
    page_nav_obj = PageNav(req, queryset)
    page_queryset = page_nav_obj.page_queryset
    page_nav_string = page_nav_obj.get_html()
    
    # 获取所有活动和成员用于筛选
    activities = Activity.objects.all()
    members = Member.objects.all()
    
    content = {
        "queryset": page_queryset,
        "page_nav_string": page_nav_string,
        "activities": activities,
        "members": members,
        "selected_activity_id": activity_id,
        "selected_member_id": member_id,
    }
    return render(req, "registration/registration_list.html", content)


def registration_add(req):
    """添加活动报名"""
    if req.method == "GET":
        form = ActivityRegistrationModelForm()
        # 如果从活动详情页传递了activity_id，则预填充
        activity_id = req.GET.get("activity_id")
        if activity_id:
            try:
                activity = Activity.objects.get(activity_id=activity_id)
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
    """删除活动报名"""
    nid = req.GET.get("nid")
    registration = ActivityRegistration.objects.filter(registration_id=nid).first()
    if registration:
        activity = registration.activity
        registration.delete()
        # 更新活动的当前参与人数
        activity.current_participants = activity.registrations.filter(status__in=[1, 2]).count()
        activity.save()
    return redirect("/registration/list")


def registration_edit(req, nid):
    """编辑活动报名"""
    row_obj = ActivityRegistration.objects.filter(registration_id=nid).first()
    if row_obj is None:
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

