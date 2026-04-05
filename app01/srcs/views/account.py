# -*- coding: utf-8 -*-
"""统一登录：管理员（user_name+密码）、社长/成员（学号+密码）"""
from django.shortcuts import render, redirect
from django import forms
from app01.utils.md5 import get_md5
from app01.models import MyAdmin, Member


class LoginForm(forms.Form):
    """账号：管理员填用户名，成员填学号"""
    account = forms.CharField(
        label="账号",
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "管理员填用户名，成员填学号"}),
    )
    password = forms.CharField(
        label="密码",
        required=True,
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "密码"}, render_value=True),
    )

    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        return get_md5(pwd)


def login(req):
    if req.method == "GET":
        return render(req, "account/login.html", {"form": LoginForm()})

    form = LoginForm(data=req.POST)
    if not form.is_valid():
        return render(req, "account/login.html", {"form": form})

    account = form.cleaned_data.get("account").strip()
    pwd_md5 = form.cleaned_data.get("password")

    # 1. 先尝试管理员（user_name + 密码）
    adm = MyAdmin.objects.filter(user_name=account, password=pwd_md5).first()
    if adm:
        req.session["info"] = {
            "type": "admin",
            "id": adm.id,
            "name": adm.user_name,
        }
        return redirect("/")

    # 2. 再尝试成员（学号 + 密码）
    member = Member.objects.filter(member_id=account, password=pwd_md5).first()
    if member:
        role_level = member.role.level if member.role else 2
        # 社长：role.level==1；其余为普通成员视角
        view_type = "president" if role_level == 1 else "member"
        req.session["info"] = {
            "type": view_type,
            "id": member.member_id,
            "name": member.name,
            "club_id": member.club_id,
            "role_level": role_level,
            "avatar": member.avatar.url if member.avatar else None,
        }
        return redirect("/")

    form.add_error("password", "账号或密码错误")
    return render(req, "account/login.html", {"form": form})


def logout(req):
    req.session.clear()
    return redirect("/login/")
