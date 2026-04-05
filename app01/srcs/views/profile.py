# -*- coding: utf-8 -*-
"""用户个人主页"""
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from app01.models import Member, ActivityRegistration, Follow
from app01.srcs.utils.role_helper import get_request_role


def _can_view_profile(viewer, target):
    """检查viewer是否可以查看target的个人主页"""
    if not viewer:
        return False
    # 管理员可以查看所有人
    role_type, _, _ = get_request_role_from_member(viewer)
    if role_type == "admin":
        return True
    # 同一社团成员可以查看
    if viewer.club and target.club and viewer.club == target.club:
        return True
    # 自己可以查看自己
    if viewer == target:
        return True
    return False


def get_request_role_from_member(member):
    """从member对象获取角色信息"""
    if not member:
        return "guest", None, None
    # 简单判断：如果role.level==1，则社长，否则成员
    # 但管理员不是member，所以需要特殊处理
    # 这里假设member不是admin，admin通过session判断
    if member.role and member.role.level == 1:
        return "president", member.club.club_id if member.club else None, member.member_id
    else:
        return "member", member.club.club_id if member.club else None, member.member_id


def profile_view(req, member_id):
    """个人主页"""
    role_type, club_id, my_member_id = get_request_role(req)
    if not my_member_id and role_type != "admin":
        return redirect("/login/")

    # 检查是否是管理员的个人主页
    from app01.models import MyAdmin
    admin_obj = None
    member_obj = None
    
    # 尝试查找Member
    member_obj = Member.objects.filter(member_id=member_id).first()
    if not member_obj:
        # 尝试查找MyAdmin
        admin_obj = MyAdmin.objects.filter(id=member_id).first()
    
    if not member_obj and not admin_obj:
        return render(req, "error.html", {"error": "用户不存在"})

    # 权限检查
    viewer_role = role_type
    viewer_member = None
    if my_member_id:
        viewer_member = Member.objects.filter(member_id=my_member_id).first()

    # 管理员可以查看所有人
    if viewer_role == "admin":
        can_view = True
    elif member_obj:
        # 对于成员，检查同一社团
        can_view = _can_view_profile(viewer_member, member_obj)
    else:
        # 对于管理员，只有管理员自己能看
        can_view = (viewer_role == "admin" and my_member_id == member_id)

    if not can_view:
        return render(req, "error.html", {"error": "无权限查看此用户主页"})

    if member_obj:
        # 成员个人主页
        joined_clubs = [member_obj.club] if member_obj.club else []
        participated_activities = ActivityRegistration.objects.filter(
            member=member_obj,
            status__in=[1, 2]  # 已报名或已参加
        ).select_related('activity').order_by('-register_time')

        following_count = Follow.objects.filter(follower=member_obj).count()
        followers_count = Follow.objects.filter(followed=member_obj).count()

        is_following = False
        if viewer_member and viewer_member != member_obj:
            is_following = Follow.objects.filter(follower=viewer_member, followed=member_obj).exists()

        common_activities = []
        if viewer_member and viewer_member.club and member_obj.club and viewer_member.club == member_obj.club and viewer_member != member_obj:
            viewer_registrations = set(ActivityRegistration.objects.filter(
                member=viewer_member, status__in=[1, 2]
            ).values_list('activity_id', flat=True))
            target_registrations = set(ActivityRegistration.objects.filter(
                member=member_obj, status__in=[1, 2]
            ).values_list('activity_id', flat=True))
            common_activity_ids = viewer_registrations & target_registrations
            from app01.models import Activity
            common_activities = Activity.objects.filter(activity_id__in=common_activity_ids).order_by('-create_time')

        context = {
            "target_member": member_obj,
            "joined_clubs": joined_clubs,
            "participated_activities": participated_activities,
            "following_count": following_count,
            "followers_count": followers_count,
            "is_following": is_following,
            "common_activities": common_activities,
            "is_own_profile": viewer_member == member_obj if viewer_member else False,
            "is_admin_profile": False,
        }
    else:
        # 管理员个人主页
        context = {
            "target_admin": admin_obj,
            "is_own_profile": viewer_role == "admin" and my_member_id == member_id,
            "is_admin_profile": True,
        }

    return render(req, "profile.html", context)


def follow_toggle(req, member_id):
    """关注/取消关注"""
    if req.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    role_type, club_id, my_member_id = get_request_role(req)
    if not my_member_id:
        return JsonResponse({"error": "Not logged in"}, status=401)

    viewer = get_object_or_404(Member, member_id=my_member_id)
    target = get_object_or_404(Member, member_id=member_id)

    if viewer == target:
        return JsonResponse({"error": "Cannot follow yourself"}, status=400)

    if not _can_view_profile(viewer, target):
        return JsonResponse({"error": "No permission"}, status=403)

    follow, created = Follow.objects.get_or_create(
        follower=viewer,
        followed=target,
        defaults={'follow_time': None}
    )
    if not created:
        # 取消关注
        follow.delete()
        return JsonResponse({"action": "unfollow", "following": False})
    else:
        # 关注
        return JsonResponse({"action": "follow", "following": True})