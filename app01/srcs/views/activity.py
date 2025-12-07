from django.shortcuts import render, redirect
from app01.models import Activity, Club, Member
from app01.utils.page_nav import PageNav
from app01.srcs.forms.form import ActivityModelForm


def activity_list(req):
    """活动列表"""
    search_data_dict = {}
    search_data = req.GET.get("q", "")
    club_id = req.GET.get("club_id", "")
    
    if search_data:
        search_data_dict["title__contains"] = search_data
    
    if club_id:
        search_data_dict["club_id"] = club_id
    
    queryset = Activity.objects.filter(**search_data_dict).order_by("-create_time")
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
    return render(req, "activity/activity_list.html", content)


def activity_add(req):
    """添加活动"""
    if req.method == "GET":
        form = ActivityModelForm()
        return render(req, "activity/activity_add.html", {"form": form})
    else:
        form = ActivityModelForm(data=req.POST)
        if form.is_valid():
            form.save()
            return redirect("/activity/list")
        else:
            return render(req, "activity/activity_add.html", {"form": form})


def activity_delete(req):
    """删除活动"""
    nid = req.GET.get("nid")
    Activity.objects.filter(activity_id=nid).delete()
    return redirect("/activity/list")


def activity_edit(req, nid):
    """编辑活动"""
    row_obj = Activity.objects.filter(activity_id=nid).first()
    if row_obj is None:
        return redirect("/activity/list")
    
    if req.method == "GET":
        form = ActivityModelForm(instance=row_obj)
        return render(req, "activity/activity_edit.html", {"form": form})
    
    form = ActivityModelForm(data=req.POST, instance=row_obj)
    if form.is_valid():
        form.save()
        return redirect("/activity/list")
    return render(req, "activity/activity_edit.html", {"form": form})


def activity_detail(req, nid):
    """活动详情（包含报名列表）"""
    activity = Activity.objects.filter(activity_id=nid).first()
    if activity is None:
        return redirect("/activity/list")
    
    # 获取该活动的所有报名记录
    registrations = activity.registrations.all().order_by("-register_time")
    
    content = {
        "activity": activity,
        "registrations": registrations,
    }
    return render(req, "activity/activity_detail.html", content)

