from django.shortcuts import render, redirect
from django.db.models import Count
from app01.models import Club, Member, Role
from app01.utils.page_nav import PageNav
from app01.srcs.forms.form import ClubModelForm
from app01.srcs.utils.export_excel import export_to_excel
from app01.srcs.utils.role_helper import get_request_role


def _sync_club_president_role(club_obj, president_member_obj):
    """同步社团社长：成员角色与社团社长姓名保持一致。"""
    if not club_obj:
        return
    
    role_president = Role.objects.filter(level=1).first()
    role_member = Role.objects.filter(level=2).first()
    if not role_president or not role_member:
        return

    # 确保 club_obj 有主键值
    if not club_obj.club_id:
        club_obj.refresh_from_db()
    
    club_id = club_obj.club_id
    if not club_id:
        return

    # 先把选中的成员设为社长（新社团没有现有社长需要降级）
    if president_member_obj:
        # 重新获取成员对象以确保最新状态
        member = Member.objects.filter(member_id=president_member_obj.member_id).first()
        if not member:
            return
        # 将成员移到本社团，并设为社长角色
        member.club_id = club_id
        member.role = role_president
        member.save(update_fields=["club_id", "role_id"])
        # 更新社团表的社长姓名
        if club_obj.president != member.name:
            club_obj.president = member.name
            club_obj.save(update_fields=["president"])


def club_list(req):
    """社团列表（社长仅见本社团）"""
    role_type, club_id_role, _ = get_request_role(req)
    if role_type == "member":
        return redirect("/member/profile/")
    search_data_dict = {}
    search_data = req.GET.get("q", "")
    if search_data:
        search_data_dict["name__contains"] = search_data
    if role_type == "president" and club_id_role:
        search_data_dict["club_id"] = club_id_role
    queryset = Club.objects.filter(**search_data_dict).annotate(
        member_count=Count("members")
    ).order_by("club_id")
    
    if req.GET.get("export") == "1":
        headers = ["社团ID", "名称", "简介", "成立日期", "社长", "创建时间", "成员人数"]
        rows = [[c.club_id, c.name, (c.description or "")[:50], c.established_date, c.president or "", c.create_time, c.member_count] for c in queryset]
        return export_to_excel(rows, headers, filename="社团列表.xlsx", sheet_name="社团")
    
    page_nav_obj = PageNav(req, queryset)
    content = {
        "queryset": page_nav_obj.page_queryset,
        "page_nav_string": page_nav_obj.get_html(),
        "search_data": search_data,
        "role_type": role_type,
    }
    return render(req, "club/club_list.html", content)


def club_add(req):
    """添加社团（仅管理员）"""
    if get_request_role(req)[0] != "admin":
        return redirect("/club/list")
    if req.method == "GET":
        form = ClubModelForm()
        return render(req, "club/club_add.html", {"form": form})
    else:
        form = ClubModelForm(data=req.POST)
        if form.is_valid():
            club_obj = form.save()
            _sync_club_president_role(club_obj, getattr(form, "_president_member_obj", None))
            return redirect("/club/list")
        else:
            return render(req, "club/club_add.html", {"form": form})


def club_delete(req):
    """删除社团（仅管理员）"""
    if get_request_role(req)[0] != "admin":
        return redirect("/club/list")
    nid = req.GET.get("nid")
    club_obj = Club.objects.filter(club_id=nid).first()
    if club_obj:
        # 仅清除成员的社团和角色关联，保留成员记录和状态
        from app01.models import Member
        Member.objects.filter(club_id=nid).update(club=None, role=None)
        club_obj.delete()
    return redirect("/club/list")


def club_edit(req, nid):
    """编辑社团（管理员或社长仅可编辑本社团）"""
    role_type, club_id_role, _ = get_request_role(req)
    if role_type == "member":
        return redirect("/member/profile/")
    row_obj = Club.objects.filter(club_id=nid).first()
    if row_obj and role_type == "president" and row_obj.club_id != club_id_role:
        return redirect("/club/list")
    if req.method == "GET":
        form = ClubModelForm(instance=row_obj)
        return render(req, "club/club_edit.html", {"form": form})
    
    form = ClubModelForm(data=req.POST, instance=row_obj)
    if form.is_valid():
        club_obj = form.save()
        _sync_club_president_role(club_obj, getattr(form, "_president_member_obj", None))
        return redirect("/club/list")
    return render(req, "club/club_edit.html", {"form": form})


def club_transfer(req):
    """社长转让：将社长身份转让给本社团另一成员（仅社长可操作）"""
    role_type, club_id_role, member_id = get_request_role(req)
    if role_type != "president" or not club_id_role or not member_id:
        return redirect("/")
    current = Member.objects.filter(member_id=member_id, club_id=club_id_role).first()
    club = Club.objects.filter(club_id=club_id_role).first()
    if not current or not club or not current.role or current.role.level != 1:
        return redirect("/club/list")
    # 本社团其他成员（排除自己）
    candidates = Member.objects.filter(
        club_id=club_id_role,
    ).exclude(member_id=member_id).order_by("member_id")
    if req.method == "GET":
        return render(req, "club/club_transfer.html", {
            "club": club,
            "candidates": candidates,
            "current_name": current.name,
        })
    to_member_id = req.POST.get("to_member_id", "").strip()
    if not to_member_id:
        return render(req, "club/club_transfer.html", {
            "club": club,
            "candidates": candidates,
            "current_name": current.name,
            "error": "请选择要转让的成员",
        })
    to_member = Member.objects.filter(member_id=to_member_id, club_id=club_id_role).first()
    if not to_member:
        return redirect("/club/transfer/")
    role_president = Role.objects.filter(level=1).first()
    role_member = Role.objects.filter(level=2).first()
    if not role_president or not role_member:
        return redirect("/club/list")
    # 新社长
    to_member.role = role_president
    to_member.save(update_fields=["role_id"])
    # 原社长改为普通成员
    current.role = role_member
    current.save(update_fields=["role_id"])
    # 更新社团表的社长姓名
    club.president = to_member.name
    club.save(update_fields=["president"])
    # 当前登录者变为普通成员视角
    req.session["info"]["type"] = "member"
    req.session["info"]["role_level"] = 2
    req.session.modified = True
    return redirect("/club/list")


