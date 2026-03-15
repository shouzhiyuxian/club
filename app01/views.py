import datetime
import json
from django.shortcuts import render, redirect, HttpResponse
from django.db.models import Count
from django.db.models.functions import TruncMonth
from app01.models import Club, Member, Activity, ActivityRegistration, Department, Role
from app01.srcs.utils.role_helper import get_request_role


def _dashboard_for_club(club_id):
    """按社团 ID 汇总仪表盘数据（供社长单社团或管理员查看某社团）"""
    base_members = Member.objects.filter(club_id=club_id)
    base_activities = Activity.objects.filter(club_id=club_id)
    member_count = base_members.count()
    activity_count = base_activities.count()
    registration_count = ActivityRegistration.objects.filter(activity__club_id=club_id).count()
    status_map = {1: "报名中", 2: "进行中", 3: "已结束", 4: "已取消"}
    activity_status_qs = base_activities.values("status").annotate(c=Count("activity_id")).order_by("status")
    activity_status_labels = [status_map.get(r["status"], str(r["status"])) for r in activity_status_qs]
    activity_status_counts = [r["c"] for r in activity_status_qs]
    six_months_ago = datetime.datetime.now() - datetime.timedelta(days=180)
    per_month = (
        base_activities.filter(create_time__gte=six_months_ago)
        .annotate(month=TruncMonth("create_time"))
        .values("month")
        .annotate(c=Count("activity_id"))
        .order_by("month")
    )
    month_labels = [r["month"].strftime("%Y-%m") if r["month"] else "" for r in per_month]
    month_counts = [r["c"] for r in per_month]
    grade_map = {1: "大一", 2: "大二", 3: "大三", 4: "大四", 5: "研究生"}
    grade_qs = base_members.filter(grade__isnull=False).values("grade").annotate(c=Count("member_id")).order_by("grade")
    grade_labels = [grade_map.get(r["grade"], str(r["grade"])) for r in grade_qs]
    grade_counts = [r["c"] for r in grade_qs]
    club = Club.objects.filter(club_id=club_id).first()
    club_name = club.name if club else ""
    return {
        "club_id": club_id,
        "club_name": club_name,
        "member_count": member_count,
        "activity_count": activity_count,
        "registration_count": registration_count,
        "club_labels": json.dumps([club_name], ensure_ascii=False),
        "club_member_counts": json.dumps([member_count]),
        "activity_status_labels": json.dumps(activity_status_labels, ensure_ascii=False),
        "activity_status_counts": json.dumps(activity_status_counts),
        "month_labels": json.dumps(month_labels, ensure_ascii=False),
        "month_counts": json.dumps(month_counts),
        "grade_labels": json.dumps(grade_labels, ensure_ascii=False),
        "grade_counts": json.dumps(grade_counts),
    }


def _dashboard_full():
    """全平台仪表盘（仅管理员）"""
    club_count = Club.objects.count()
    member_count = Member.objects.count()
    activity_count = Activity.objects.count()
    registration_count = ActivityRegistration.objects.count()
    members_per_club = list(
        Club.objects.annotate(c=Count("members")).values_list("name", "c").order_by("-c")[:10]
    )
    club_labels = [x[0] for x in members_per_club]
    club_member_counts = [x[1] for x in members_per_club]
    status_map = {1: "报名中", 2: "进行中", 3: "已结束", 4: "已取消"}
    activity_status_qs = Activity.objects.values("status").annotate(c=Count("activity_id")).order_by("status")
    activity_status_labels = [status_map.get(r["status"], str(r["status"])) for r in activity_status_qs]
    activity_status_counts = [r["c"] for r in activity_status_qs]
    six_months_ago = datetime.datetime.now() - datetime.timedelta(days=180)
    per_month = (
        Activity.objects.filter(create_time__gte=six_months_ago)
        .annotate(month=TruncMonth("create_time"))
        .values("month")
        .annotate(c=Count("activity_id"))
        .order_by("month")
    )
    month_labels = [r["month"].strftime("%Y-%m") if r["month"] else "" for r in per_month]
    month_counts = [r["c"] for r in per_month]
    grade_map = {1: "大一", 2: "大二", 3: "大三", 4: "大四", 5: "研究生"}
    grade_qs = Member.objects.filter(grade__isnull=False).values("grade").annotate(c=Count("member_id")).order_by("grade")
    grade_labels = [grade_map.get(r["grade"], str(r["grade"])) for r in grade_qs]
    grade_counts = [r["c"] for r in grade_qs]
    return {
        "club_count": club_count,
        "member_count": member_count,
        "activity_count": activity_count,
        "registration_count": registration_count,
        "club_labels": json.dumps(club_labels, ensure_ascii=False),
        "club_member_counts": json.dumps(club_member_counts),
        "activity_status_labels": json.dumps(activity_status_labels, ensure_ascii=False),
        "activity_status_counts": json.dumps(activity_status_counts),
        "month_labels": json.dumps(month_labels, ensure_ascii=False),
        "month_counts": json.dumps(month_counts),
        "grade_labels": json.dumps(grade_labels, ensure_ascii=False),
        "grade_counts": json.dumps(grade_counts),
    }


def index(req):
    """仪表盘：未登录不可见；管理员看全局或某社团，社长看本社团，成员看个人概览"""
    role_type, club_id_role, member_id = get_request_role(req)
    # 未登录（理论上中间件已拦截，此处兜底）
    if not req.session.get("info"):
        return redirect("/login/")

    # 普通成员：仅显示个人相关概览，无全局/社团数据
    if role_type == "member":
        me = Member.objects.filter(member_id=member_id).first()
        my_reg_count = ActivityRegistration.objects.filter(member_id=member_id).count()
        can_register = 0
        if me and me.club_id:
            my_activity_ids = ActivityRegistration.objects.filter(member_id=member_id).values_list("activity_id", flat=True)
            can_register = Activity.objects.filter(club_id=me.club_id, status=1).exclude(activity_id__in=my_activity_ids).count()
        return render(req, "index.html", {
            "role_type": "member",
            "member": me,
            "my_registration_count": my_reg_count,
            "can_register_count": can_register,
        })

    # 社长：仅本社团仪表盘
    if role_type == "president" and club_id_role:
        data = _dashboard_for_club(club_id_role)
        data["role_type"] = "president"
        data["club_count"] = 1
        return render(req, "index.html", data)

    # 管理员：支持“查看某社团”或全局
    club_id_param = req.GET.get("club_id", "").strip()
    if club_id_param:
        try:
            cid = int(club_id_param)
            if Club.objects.filter(club_id=cid).exists():
                data = _dashboard_for_club(cid)
                data["role_type"] = "admin"
                data["club_count"] = 1
                data["clubs"] = Club.objects.all().order_by("club_id")
                data["selected_club_id"] = cid
                return render(req, "index.html", data)
        except ValueError:
            pass
    data = _dashboard_full()
    data["role_type"] = "admin"
    data["clubs"] = Club.objects.all().order_by("club_id")
    data["selected_club_id"] = None
    return render(req, "index.html", data)


def dbop(req):
    import random
    from app01.models import UserInfo, PhoneNumbers
    for i in range(100, 300):
            number = random.randint(1000000000, 9999999999)
            UserInfo.objects.create(user_id=str(i))
            PhoneNumbers.objects.create(mobile=number)
    return HttpResponse("done")
