# -*- coding: utf-8 -*-
"""登录角色：admin / president / member，用于视图与模板中判断视角"""
from functools import wraps
from django.shortcuts import redirect


def get_request_role(req):
    """
    返回当前请求的角色信息。
    return: (role_type, club_id, member_id)
    - role_type: "admin" | "president" | "member"
    - club_id: 社长/成员所属社团 id，管理员为 None
    - member_id: 社长/成员的学号，管理员为 None
    """
    info = req.session.get("info") or {}
    role_type = info.get("type", "admin")
    club_id = info.get("club_id")
    member_id = info.get("id") if role_type in ("president", "member") else None
    return role_type, club_id, member_id


def admin_required(view_func):
    """仅管理员可访问"""
    @wraps(view_func)
    def wrapper(req, *args, **kwargs):
        role_type, _, _ = get_request_role(req)
        if role_type != "admin":
            return redirect("/")
        return view_func(req, *args, **kwargs)
    return wrapper


def president_or_admin_required(view_func):
    """管理员或社长可访问（成员不可）"""
    @wraps(view_func)
    def wrapper(req, *args, **kwargs):
        role_type, _, _ = get_request_role(req)
        if role_type == "member":
            return redirect("/")
        return view_func(req, *args, **kwargs)
    return wrapper
