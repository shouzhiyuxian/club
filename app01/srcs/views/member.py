from django.shortcuts import render, redirect
from app01.models import Member, Club, Department, Role
from app01.utils.page_nav import PageNav
from app01.srcs.forms.form import MemberModelForm


def member_list(req):
    """成员列表"""
    search_data_dict = {}
    search_data = req.GET.get("q", "")
    club_id = req.GET.get("club_id", "")
    
    if search_data:
        search_data_dict["name__contains"] = search_data
    
    if club_id:
        search_data_dict["club_id"] = club_id
    
    queryset = Member.objects.filter(**search_data_dict).order_by("-join_time")
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

