from django.shortcuts import render, redirect, HttpResponse
from app01.models import Club, Member, Activity, ActivityRegistration


# Create your views here.

def index(req):
    # 获取统计数据
    club_count = Club.objects.count()
    member_count = Member.objects.count()
    activity_count = Activity.objects.count()
    registration_count = ActivityRegistration.objects.count()
    
    content = {
        "club_count": club_count,
        "member_count": member_count,
        "activity_count": activity_count,
        "registration_count": registration_count,
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









