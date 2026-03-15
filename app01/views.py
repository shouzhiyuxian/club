import datetime
import json
from django.shortcuts import render, redirect, HttpResponse
from django.db.models import Count
from django.db.models.functions import TruncMonth
from app01.models import Club, Member, Activity, ActivityRegistration, Department, Role


# Create your views here.

def index(req):
    """仪表盘首页：统计卡片 + 图表数据"""
    # 基础统计
    club_count = Club.objects.count()
    member_count = Member.objects.count()
    activity_count = Activity.objects.count()
    registration_count = ActivityRegistration.objects.count()

    # 各社团成员数（柱状图）
    members_per_club = list(
        Club.objects.annotate(c=Count("members"))
        .values_list("name", "c")
        .order_by("-c")[:10]
    )
    club_labels = [x[0] for x in members_per_club]
    club_member_counts = [x[1] for x in members_per_club]

    # 活动状态分布（饼图）
    status_map = {1: "报名中", 2: "进行中", 3: "已结束", 4: "已取消"}
    activity_status_qs = (
        Activity.objects.values("status")
        .annotate(c=Count("activity_id"))
        .order_by("status")
    )
    activity_status_labels = [status_map.get(r["status"], str(r["status"])) for r in activity_status_qs]
    activity_status_counts = [r["c"] for r in activity_status_qs]

    # 近6个月活动数量趋势（折线图，按创建月份）
    six_months_ago = datetime.datetime.now() - datetime.timedelta(days=180)
    per_month = (
        Activity.objects.filter(create_time__gte=six_months_ago)
        .annotate(month=TruncMonth("create_time"))
        .values("month")
        .annotate(c=Count("activity_id"))
        .order_by("month")
    )
    month_labels = []
    month_counts = []
    for r in per_month:
        month_labels.append(r["month"].strftime("%Y-%m") if r["month"] else "")
        month_counts.append(r["c"])

    # 成员年级分布（柱状图）
    grade_map = {1: "大一", 2: "大二", 3: "大三", 4: "大四", 5: "研究生"}
    grade_qs = (
        Member.objects.filter(grade__isnull=False)
        .values("grade")
        .annotate(c=Count("member_id"))
        .order_by("grade")
    )
    grade_labels = [grade_map.get(r["grade"], str(r["grade"])) for r in grade_qs]
    grade_counts = [r["c"] for r in grade_qs]

    content = {
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
    return render(req, "index.html", content)


def dbop(req):
    import random
    from app01.models import UserInfo, PhoneNumbers
    for i in range(100, 300):
            number = random.randint(1000000000, 9999999999)
            UserInfo.objects.create(user_id=str(i))
            PhoneNumbers.objects.create(mobile=number)
    return HttpResponse("done")









