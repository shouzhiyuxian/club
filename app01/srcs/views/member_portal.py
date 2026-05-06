# -*- coding: utf-8 -*-
"""普通成员视角：我的信息、我的报名、可报名活动"""
from django.shortcuts import render, redirect, get_object_or_404
from django import forms
from app01.models import Member, Activity, ActivityRegistration, ActivityComment, ActivityPhoto, ActivityLike, Follow, ClubDiscussion, RecruitmentApplication
from app01.utils.md5 import get_md5
from app01.srcs.utils.role_helper import get_request_role
from django.contrib import messages


def _member_required(req):
    """要求已登录且为成员或社长，返回 Member 或 None"""
    role_type, club_id, member_id = get_request_role(req)
    if role_type not in ("member", "president") or not member_id:
        return None
    return Member.objects.filter(member_id=member_id).select_related('role', 'club').first()


def member_profile(req):
    """我的信息：查看/编辑本人信息、修改密码"""
    me = _member_required(req)
    if not me:
        return redirect("/login/")

    if req.method == "GET":
        from app01.srcs.forms.form import MemberModelForm
        form = MemberModelForm(instance=me)
        # 成员只能改部分字段：姓名、手机、邮箱；学号/社团/角色等只读或隐藏
        for fname in ["member_id", "club", "role", "join_time"]:
            if fname in form.fields:
                form.fields[fname].disabled = True
        
        avatar_url = me.avatar.url if me.avatar else None
        print(f"DEBUG: member={me.name}, avatar={me.avatar}, avatar_url={avatar_url}")
        context = {
            "form": form, 
            "member": me,
            "avatar_url": avatar_url,
        }
        return render(req, "member_portal/profile.html", context)

    from app01.srcs.forms.form import MemberModelForm
    form = MemberModelForm(data=req.POST, files=req.FILES, instance=me)
    if form.is_valid():
        inst = form.save(commit=False)
        # 强制保留不允许修改的字段，防止 disabled 字段在提交时被清空
        inst.member_id = me.member_id
        inst.club_id = me.club_id
        inst.role_id = me.role_id
        inst.join_time = me.join_time
        inst.save()
        # 同步 session 中的用户信息，确保导航栏头像和姓名更新
        if req.session.get("info"):
            req.session["info"]["name"] = inst.name
            req.session["info"]["avatar"] = inst.avatar.url if inst.avatar else None
            req.session.modified = True
        messages.success(req, "个人信息更新成功！")
        return redirect("/member/profile/")
    for fname in ["member_id", "club", "role", "join_time"]:
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
    """可报名活动：本社团内状态为「报名中」且本人未报名的活动（成员和社长都可用）"""
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
    
    # 获取角色类型用于模板显示
    role_type, _, _ = get_request_role(req)
    
    return render(req, "member_portal/activities_can_register.html", {
        "queryset": queryset, 
        "member": me,
        "role_type": role_type,
    })


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


def leave_club(req):
    """成员退出社团（社长必须先转让社长身份）"""
    me = _member_required(req)
    if not me:
        return redirect("/login/")
    
    # 检查是否是社长（role.level == 1）
    if me.role and me.role.level == 1:
        # 社长必须先转让身份才能退出，重定向到转让页面
        return redirect("/club/transfer/")
    
    if req.method == "POST":
        # 获取当前社团ID（用于更新招新申请）
        old_club_id = me.club_id
        
        # 清除成员的社团关联
        me.club = None
        me.role = None
        me.save()
        
        # 更新 session 信息
        if req.session.get("info"):
            req.session["info"]["club_id"] = None
            # 将角色类型从 president 改为 member
            # 因为退出后不再是社长
            if req.session["info"].get("type") == "president":
                req.session["info"]["type"] = "member"
            req.session.modified = True
        
        # 将该成员在该社团的所有"已通过"招新申请状态改为"已拒绝"
        # 这样成员可以重新报名该社团或其他社团
        if old_club_id:
            RecruitmentApplication.objects.filter(
                student_id=me.member_id,
                status=2,  # 已通过
                recruitment__club_id=old_club_id
            ).update(status=3)  # 改为已拒绝
            
            # 同时将该成员对其他社团的"待审核"申请也改为"已拒绝"
            # 避免退出后无法报名其他社团
            RecruitmentApplication.objects.filter(
                student_id=me.member_id,
                status=1,  # 待审核
                recruitment__club_id__isnull=False
            ).exclude(recruitment__club_id=old_club_id).update(status=3)  # 改为已拒绝
        
        return redirect("/member/profile/")
    
    return redirect("/member/profile/")


def club_discussion(req):
    """社团内部讨论页面"""
    me = _member_required(req)
    if not me:
        return redirect("/login/")
    
    # 获取当前成员关注的人（无论是否有社团都需要）
    following_ids = set(Follow.objects.filter(follower=me).values_list('followed_id', flat=True))
    
    if not me.club:
        return render(req, "member_portal/discussion.html", {
            "error": "您尚未加入任何社团",
            "member": me,
            "following_ids": following_ids,
            "discussions": [],
        })
    
    if req.method == "POST":
        content = req.POST.get("content", "").strip()
        if content:
            ClubDiscussion.objects.create(
                club=me.club,
                member=me,
                content=content
            )
        return redirect("/member/discussion/")
    
    # 获取社团所有讨论
    discussions = ClubDiscussion.objects.filter(
        club=me.club,
        is_deleted=False
    ).select_related('member', 'member__role').order_by("-create_time")
    
    # 获取当前成员关注的人
    following_ids = set(Follow.objects.filter(follower=me).values_list('followed_id', flat=True))
    
    context = {
        "discussions": discussions,
        "member": me,
        "following_ids": following_ids,
    }
    return render(req, "member_portal/discussion.html", context)


def delete_discussion(req, discussion_id):
    """删除自己的讨论"""
    me = _member_required(req)
    if not me:
        return redirect("/login/")
    
    discussion = get_object_or_404(ClubDiscussion, discussion_id=discussion_id)
    
    # 只能删除自己的发言，社长可以删除任何人的
    if discussion.member == me or (me.role and me.role.level == 1):
        discussion.is_deleted = True
        discussion.save()
    
    return redirect("/member/discussion/")


def activity_detail(req, activity_id):
    """活动详情页面（成员端，包含评论、照片、点赞功能）"""
    me = _member_required(req)
    if not me:
        return redirect("/login/")

    activity = get_object_or_404(Activity, activity_id=activity_id)
    if activity.club_id != me.club_id:
        return redirect("/member/activities/")

    # 获取活动相关数据
    registrations = ActivityRegistration.objects.filter(activity=activity).select_related('member')
    comments = ActivityComment.objects.filter(activity=activity).select_related('member').order_by('create_time')
    photos = ActivityPhoto.objects.filter(activity=activity).select_related('member').order_by('-upload_time')
    
    # 检查当前用户是否已报名、已点赞
    is_registered = ActivityRegistration.objects.filter(activity=activity, member=me).exists()
    is_liked = ActivityLike.objects.filter(activity=activity, member=me).exists()
    
    # 获取点赞数量
    likes_count = ActivityLike.objects.filter(activity=activity).count()
    
    # 处理POST请求（评论、点赞等）
    if req.method == "POST":
        if req.POST.get("action") == "comment":
            # 添加评论
            content = req.POST.get("content", "").strip()
            if content:
                ActivityComment.objects.create(activity=activity, member=me, content=content)
                return redirect(f"/member/activity/{activity_id}/")
        
        elif req.POST.get("action") == "like":
            # 点赞/取消点赞
            if is_liked:
                ActivityLike.objects.filter(activity=activity, member=me).delete()
            else:
                ActivityLike.objects.create(activity=activity, member=me)
            return redirect(f"/member/activity/{activity_id}/")
        
        elif req.POST.get("action") == "upload_photo":
            # 上传照片
            from app01.srcs.forms.form import ActivityPhotoForm
            form = ActivityPhotoForm(req.POST, req.FILES)
            if form.is_valid():
                photo = form.save(commit=False)
                photo.activity = activity
                photo.member = me
                photo.save()
                return redirect(f"/member/activity/{activity_id}/")

    context = {
        "activity": activity,
        "registrations": registrations,
        "comments": comments,
        "photos": photos,
        "is_registered": is_registered,
        "is_liked": is_liked,
        "likes_count": likes_count,
        "member": me,
    }
    return render(req, "member_portal/activity_detail.html", context)
