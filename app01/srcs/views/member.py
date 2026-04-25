from django.shortcuts import render, redirect
from django import forms
from app01.models import Member, Club, Department, Role, Follow
from app01.srcs.views.profile import _can_view_profile
from app01.utils.page_nav import PageNav
from app01.srcs.forms.form import MemberModelForm
from app01.srcs.utils.export_excel import export_to_excel
from app01.srcs.utils.role_helper import get_request_role
from app01.utils.md5 import get_md5
from datetime import date


class MemberResetPwdForm(forms.Form):
    """管理员重置成员登录密码"""
    password = forms.CharField(label="新密码", min_length=6, widget=forms.PasswordInput(attrs={"class": "form-control"}))
    confirm = forms.CharField(label="确认密码", widget=forms.PasswordInput(attrs={"class": "form-control"}))

    def clean_confirm(self):
        if self.cleaned_data.get("password") != self.cleaned_data.get("confirm"):
            raise forms.ValidationError("两次输入不一致")
        return self.cleaned_data["confirm"]


def _member_queryset(req):
    search_data_dict = {}
    if req.GET.get("q"):
        search_data_dict["name__contains"] = req.GET.get("q")
    club_id = req.GET.get("club_id")
    role_type, club_id_role, _ = get_request_role(req)
    
    # 强制权限控制：非管理员只能看到自己社团的成员
    if role_type == "admin":
        # 管理员可以查看所有成员，或按club_id过滤
        if club_id:
            search_data_dict["club_id"] = club_id
        # 管理员不传 club_id 时，显示所有成员（包括无社团的）
    else:
        # 社长和普通成员只能看到自己社团的成员
        if club_id_role:
            search_data_dict["club_id"] = club_id_role
        else:
            # 如果没有社团ID，返回空查询集
            return Member.objects.none()
    
    queryset = Member.objects.filter(**search_data_dict)
    
    # 自动修复1：在社团中但角色为NULL的成员，设置为普通成员
    role_member = Role.objects.filter(level=2).first()
    if role_member:
        queryset.filter(club__isnull=False, role__isnull=True).update(role=role_member)
    
    # 自动修复2：未加入社团但角色不为NULL的成员，清除角色
    queryset.filter(club__isnull=True, role__isnull=False).update(role=None)
    
    return queryset.order_by("member_id")


def member_list(req):
    """成员列表（社长仅见本社团成员，普通成员仅见同一社团成员）"""
    role_type, club_id_role, member_id = get_request_role(req)
    
    if req.GET.get("export") == "1":
        queryset = _member_queryset(req)
        headers = ["学号", "姓名", "性别", "年级", "专业", "手机", "邮箱", "所属社团", "角色", "加入时间"]
        rows = []
        for m in queryset:
            rows.append([
                m.member_id,
                m.name,
                m.get_gender_display() if m.gender else "",
                m.get_grade_display() if m.grade else "",
                m.major or "",
                m.phone or "",
                m.email or "",
                m.club.name if m.club else "",
                m.role.name if m.role else "",
                m.join_time,
            ])
        return export_to_excel(rows, headers, filename="成员列表.xlsx", sheet_name="成员")
    
    queryset = _member_queryset(req)
    page_nav_obj = PageNav(req, queryset)
    clubs = Club.objects.all() if role_type == "admin" else Club.objects.filter(club_id=club_id_role)
    
    # 获取当前用户member对象（用于关注状态检查）
    current_member = None
    if member_id:
        current_member = Member.objects.filter(member_id=member_id).first()
    
    # 为每个成员添加关注状态和是否可关注状态
    members_with_follow_status = []
    if current_member:
        following_ids = set(Follow.objects.filter(follower=current_member).values_list('followed_id', flat=True))
        for member in page_nav_obj.page_queryset:
            member.is_following = member.member_id in following_ids
            member.can_follow = current_member != member and _can_view_profile(current_member, member)
            members_with_follow_status.append(member)
    else:
        for member in page_nav_obj.page_queryset:
            member.can_follow = False
            members_with_follow_status.append(member)
    
    content = {
        "queryset": members_with_follow_status,
        "page_nav_string": page_nav_obj.get_html(),
        "search_data": req.GET.get("q", ""),
        "clubs": clubs,
        "selected_club_id": str(club_id_role) if role_type in ("president", "member") else req.GET.get("club_id", ""),
        "can_manage": role_type in ("admin", "president"),  # 是否可以管理成员
        "current_member": current_member,
    }
    return render(req, "member/member_list.html", content)


def member_add(req):
    """添加成员（社长仅能添加到本社团）"""
    role_type, club_id_role, _ = get_request_role(req)
    if role_type == "member":
        return redirect("/member/profile/")
    if req.method == "GET":
        form = MemberModelForm()
        if role_type == "president" and club_id_role:
            form.fields["club"].queryset = Club.objects.filter(club_id=club_id_role)
            form.fields["club"].initial = Club.objects.filter(club_id=club_id_role).first()
        return render(req, "member/member_add.html", {"form": form})
    form = MemberModelForm(data=req.POST)
    if form.is_valid():
        if role_type == "president" and club_id_role:
            form.instance.club_id = club_id_role
        if form.instance.join_time is None:
            form.instance.join_time = date.today()
        instance = form.save()
        # 保存后刷新实例，确保密码字段正确设置
        instance.refresh_from_db()
        if not instance.password:
            instance.password = get_md5("123456")
            instance.save(update_fields=["password"])
        return redirect("/member/list")
    return render(req, "member/member_add.html", {"form": form})


def member_delete(req):
    """删除成员（社长仅能删本社团成员）"""
    role_type, club_id_role, _ = get_request_role(req)
    if role_type == "member":
        return redirect("/member/profile/")
    nid = req.GET.get("nid")
    obj = Member.objects.filter(member_id=nid).first()
    if not obj:
        return redirect("/member/list")
    if role_type == "president" and obj.club_id != club_id_role:
        return redirect("/member/list")
    
    # 删除前，清除对应社团的社长信息（如果该成员是社长或社长字段匹配）
    if obj.club_id and obj.name:
        Club.objects.filter(
            club_id=obj.club_id, 
            president=obj.name
        ).update(president="")
    
    Member.objects.filter(member_id=nid).delete()
    return redirect("/member/list")


def member_edit(req, nid):
    """编辑成员（社长仅能编辑本社团成员）"""
    role_type, club_id_role, _ = get_request_role(req)
    if role_type == "member":
        return redirect("/member/profile/")
    row_obj = Member.objects.filter(member_id=nid).first()
    if row_obj is None:
        return redirect("/member/list")
    if role_type == "president" and row_obj.club_id != club_id_role:
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


def member_reset_pwd(req, nid):
    """重置成员登录密码（仅管理员）"""
    if get_request_role(req)[0] != "admin":
        return redirect("/member/list")
    row_obj = Member.objects.filter(member_id=nid).first()
    if not row_obj:
        return redirect("/member/list")
    if req.method == "GET":
        form = MemberResetPwdForm()
        return render(req, "member/member_reset_pwd.html", {"form": form, "member": row_obj})
    form = MemberResetPwdForm(data=req.POST)
    if form.is_valid():
        row_obj.password = get_md5(form.cleaned_data["password"])
        row_obj.save(update_fields=["password"])
        return redirect("/member/list")
    return render(req, "member/member_reset_pwd.html", {"form": form, "member": row_obj})

