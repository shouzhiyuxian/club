# -*- coding: utf-8 -*-
"""公告管理"""
from django.shortcuts import render, redirect
from django.http import HttpResponse
from app01.models import Announcement
from app01.utils.page_nav import PageNav
from app01.srcs.forms.form import AnnouncementModelForm
from app01.srcs.utils.role_helper import get_request_role


def announcement_list(request):
    """公告列表 - 管理员看全部，社长看全局+本社团，成员看全局+本社团"""
    role, club_id, member_id = get_request_role(request)
    if not role:
        return redirect("/account/login")

    # 根据角色筛选公告
    if role == "admin":
        # 管理员看全部公告
        queryset = Announcement.objects.all()
    elif role == "president":
        # 社长看全局公告 + 本社团公告
        from django.db.models import Q
        queryset = Announcement.objects.filter(Q(club_id__isnull=True) | Q(club_id=club_id))
    else:
        # 普通成员看已发布的全局公告 + 本社团公告
        from django.db.models import Q
        queryset = Announcement.objects.filter(
            (Q(club_id__isnull=True) | Q(club_id=club_id)),
            status=1
        )

    # 搜索
    search = request.GET.get("search", "")
    if search:
        queryset = queryset.filter(title__icontains=search)

    # 分页
    page_nav = PageNav(request, queryset, page_size=10)
    page_queryset = page_nav.page_queryset
    page_nav_html = page_nav.get_html()

    context = {
        "page_queryset": page_queryset,
        "page_nav_html": page_nav_html,
        "search": search,
        "role": role,
        "club_id": club_id,
    }
    return render(request, "announcement/list.html", context)


def announcement_add(request):
    """添加公告 - 管理员发全局公告，社长发本社团公告"""
    role, club_id, member_id = get_request_role(request)
    if role not in ("admin", "president"):
        return HttpResponse("权限不足")

    if request.method == "GET":
        form = AnnouncementModelForm()
        # 社长只能发本社团公告，传递club_id给模板
        return render(request, "announcement/add.html", {"form": form, "role": role, "club_id": club_id})

    form = AnnouncementModelForm(data=request.POST)
    if form.is_valid():
        # 发布者：仅管理员有 MyAdmin 账号，社长的 session id 是成员 id 不能填到 publisher
        if role == "admin":
            admin_id = request.session.get("info", {}).get("id")
            if admin_id:
                form.instance.publisher_id = admin_id
        else:
            form.instance.publisher_id = None  # 社长发布不填发布者（publisher 外键是 MyAdmin）

        # 社长发布的公告自动绑定到本社团
        if role == "president":
            form.instance.club_id = club_id

        form.save()
        return redirect("/announcement/list")
    return render(request, "announcement/add.html", {"form": form, "role": role, "club_id": club_id})


def announcement_edit(request, nid):
    """编辑公告 - 管理员编辑所有公告，社长只能编辑本社团的"""
    role, club_id, member_id = get_request_role(request)
    if role not in ("admin", "president"):
        return HttpResponse("权限不足")

    obj = Announcement.objects.filter(announcement_id=nid).first()
    if not obj:
        return HttpResponse("公告不存在")

    # 权限检查：社长只能编辑本社团的公告
    if role == "president" and obj.club_id != club_id:
        return HttpResponse("权限不足")

    if request.method == "GET":
        form = AnnouncementModelForm(instance=obj)
        return render(request, "announcement/edit.html", {"form": form, "role": role})

    form = AnnouncementModelForm(data=request.POST, instance=obj)
    if form.is_valid():
        form.save()
        return redirect("/announcement/list")
    return render(request, "announcement/edit.html", {"form": form, "role": role})


def announcement_delete(request, nid):
    """删除公告 - 管理员删除所有公告，社长只能删除本社团的"""
    role, club_id, member_id = get_request_role(request)
    if role not in ("admin", "president"):
        return HttpResponse("权限不足")

    obj = Announcement.objects.filter(announcement_id=nid).first()
    if not obj:
        return HttpResponse("公告不存在")

    # 权限检查：社长只能删除本社团的公告
    if role == "president" and obj.club_id != club_id:
        return HttpResponse("权限不足")

    obj.delete()
    return redirect("/announcement/list")


def announcement_detail(request, nid):
    """公告详情"""
    role, club_id, member_id = get_request_role(request)
    if not role:
        return redirect("/account/login")

    obj = Announcement.objects.filter(announcement_id=nid).first()
    if not obj:
        return HttpResponse("公告不存在")

    # 只有管理员或发布的公告才能查看
    if role != "admin" and obj.status != 1:
        return HttpResponse("权限不足")

    return render(request, "announcement/detail.html", {"obj": obj})