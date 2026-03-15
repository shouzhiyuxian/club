# -*- coding: utf-8 -*-
"""普通成员视角：我的信息、我的报名、可报名活动"""
from django.shortcuts import render, redirect, get_object_or_404
from django import forms
from app01.models import Member, Activity, ActivityRegistration
from app01.utils.md5 import get_md5
from app01.srcs.utils.role_helper import get_request_role


def _member_required(req):
    """要求已登录且为成员或社长，返回 Member 或 None"""
    role_type, club_id, member_id = get_request_role(req)
    if role_type not in ("member", "president") or not member_id:
        return None
    return Member.objects.filter(member_id=member_id).first()


def member_profile(req):
    """我的信息：查看/编辑本人信息、修改密码"""
    me = _member_required(req)
    if not me:
        return redirect("/login/")

    if req.method == "GET":
        from app01.srcs.forms.form import MemberModelForm
        form = MemberModelForm(instance=me)
        # 成员只能改部分字段：姓名、手机、邮箱、备注；学号/社团/部门/角色等只读或隐藏
        for fname in ["member_id", "club", "department", "role", "join_time", "status"]:
            if fname in form.fields:
                form.fields[fname].disabled = True
        return render(req, "member_portal/profile.html", {"form": form, "member": me})

    from app01.srcs.forms.form import MemberModelForm
    form = MemberModelForm(data=req.POST, instance=me)
    # 不允许通过表单修改学号、社团、部门、角色、加入时间、状态
    form.fields.get("member_id") and form.fields["member_id"].disabled or None
    if form.is_valid():
        inst = form.save(commit=False)
        inst.member_id = me.member_id
        inst.club_id = me.club_id
        inst.department_id = me.department_id
        inst.role_id = me.role_id
        inst.join_time = me.join_time
        inst.status = me.status
        inst.save()
        return redirect("/member/profile/")
    for fname in ["member_id", "club", "department", "role", "join_time", "status"]:
        if fname in form.fields:
            form.fields[fname].disabled = True
    return render(req, "member_portal/profile.html", {"form": form, "member": me})


def member_change_password(req):
    """修改密码（成员端）"""
    me = _member_required(req)
    if not me:
        return redirect("/login/")

    class PwdForm(forms.Form):
        old_password = forms.CharField(label="原密码", widget=forms.PasswordInput(attrs={"class": "form-control"}))
        new_password = forms.CharField(label="新密码", min_length=6, widget=forms.PasswordInput(attrs={"class": "form-control"}))
        confirm = forms.CharField(label="确认新密码", widget=forms.PasswordInput(attrs={"class": "form-control"}))

        def clean_confirm(self):
            if self.cleaned_data.get("new_password") != self.cleaned_data.get("confirm"):
                raise forms.ValidationError("两次输入不一致")
            return self.cleaned_data["confirm"]

    if req.method == "GET":
        return render(req, "member_portal/change_password.html", {"form": PwdForm()})

    form = PwdForm(req.POST)
    if form.is_valid():
        old_md5 = get_md5(form.cleaned_data["old_password"])
        if me.password != old_md5:
            form.add_error("old_password", "原密码错误")
            return render(req, "member_portal/change_password.html", {"form": form})
        me.password = get_md5(form.cleaned_data["new_password"])
        me.save()
        return redirect("/member/profile/")
    return render(req, "member_portal/change_password.html", {"form": form})


def my_registrations(req):
    """我的报名：当前成员的活动报名列表"""
    me = _member_required(req)
    if not me:
        return redirect("/login/")

    queryset = ActivityRegistration.objects.filter(member=me).order_by("registration_id")
    return render(req, "member_portal/my_registrations.html", {"queryset": queryset, "member": me})


def activities_can_register(req):
    """可报名活动：本社团内状态为「报名中」且本人未报名的活动"""
    me = _member_required(req)
    if not me:
        return redirect("/login/")

    if not me.club_id:
        return render(req, "member_portal/activities_can_register.html", {"queryset": [], "member": me})

    my_activity_ids = set(
        ActivityRegistration.objects.filter(member=me).values_list("activity_id", flat=True)
    )
    # 本社团、报名中、未报名的
    queryset = Activity.objects.filter(
        club_id=me.club_id,
        status=1,
    ).exclude(activity_id__in=my_activity_ids).order_by("activity_id")
    return render(req, "member_portal/activities_can_register.html", {"queryset": queryset, "member": me})


def do_register(req, activity_id):
    """成员自助报名某活动"""
    me = _member_required(req)
    if not me:
        return redirect("/login/")

    activity = get_object_or_404(Activity, activity_id=activity_id)
    if activity.club_id != me.club_id or activity.status != 1:
        return redirect("/member/activities/")
    if ActivityRegistration.objects.filter(activity=activity, member=me).exists():
        return redirect("/member/my-registrations/")
    ActivityRegistration.objects.create(activity=activity, member=me, status=1)
    activity.current_participants = activity.registrations.filter(status__in=[1, 2]).count()
    activity.save()
    return redirect("/member/my-registrations/")
