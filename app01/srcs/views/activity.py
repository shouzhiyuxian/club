from django.shortcuts import render, redirect
from app01.models import Activity, Club, Member
from app01.utils.page_nav import PageNav
from app01.srcs.forms.form import ActivityModelForm
from app01.srcs.utils.export_excel import export_to_excel


def _activity_queryset(req):
    search_data_dict = {}
    if req.GET.get("q"):
        search_data_dict["title__contains"] = req.GET.get("q")
    if req.GET.get("club_id"):
        search_data_dict["club_id"] = req.GET.get("club_id")
    return Activity.objects.filter(**search_data_dict).order_by("-create_time")


def activity_list(req):
    """活动列表"""
    queryset = _activity_queryset(req)
    if req.GET.get("export") == "1":
        status_map = {1: "报名中", 2: "进行中", 3: "已结束", 4: "已取消"}
        headers = ["活动ID", "活动名称", "所属社团", "地点", "开始时间", "结束时间", "人数限制", "当前人数", "组织者", "状态", "创建时间"]
        rows = []
        for a in queryset:
            rows.append([
                a.activity_id, a.title, a.club.name if a.club else "", a.location or "",
                a.start_time, a.end_time, a.max_participants or "", a.current_participants,
                a.organizer.name if a.organizer else "", status_map.get(a.status, ""), a.create_time,
            ])
        return export_to_excel(rows, headers, filename="活动列表.xlsx", sheet_name="活动")
    
    page_nav_obj = PageNav(req, queryset)
    clubs = Club.objects.all()
    content = {
        "queryset": page_nav_obj.page_queryset,
        "page_nav_string": page_nav_obj.get_html(),
        "search_data": req.GET.get("q", ""),
        "clubs": clubs,
        "selected_club_id": req.GET.get("club_id", ""),
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

