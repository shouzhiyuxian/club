from django import forms
from app01.utils.bootstrap_modelform import BootstrapModelForm
from app01.models import (
    MyAdmin, Club, Department, Role, Member, Activity, ActivityRegistration
)

from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator


# ============ 已废弃的表单类（保留用于向后兼容） ============
# 注意：UserInfo 和 PhoneNumbers 模型已被移除，以下表单类已不再使用
# 如需使用成员管理功能，请使用 MemberModelForm

# class UserModelForm(BootstrapModelForm):
#     """已废弃：请使用 MemberModelForm"""
#     pass

# class NumModelForm(BootstrapModelForm):
#     """已废弃：此功能已移除"""
#     pass

# class NumModelFormEdit(BootstrapModelForm):
#     """已废弃：此功能已移除"""
#     pass


from app01.utils.md5 import get_md5
class MyadminForm(BootstrapModelForm):
    user_name = forms.CharField(required=False, label="管理员姓名",
                                widget=forms.TextInput(attrs={"class": "form-control", }))
    password = forms.CharField(required=True, label="输入密码", min_length=8,
                                  widget=forms.PasswordInput(attrs={"class": "form-control", }))
    confirm_pwd = forms.CharField(required=True, label="确认密码", min_length=8,
                                widget=forms.PasswordInput(attrs={"class": "form-control", }))
    class Meta:
        model = MyAdmin  # 这里必须是model字母，不能错
        fields = "__all__"  # 这里必须是fields字母，不能错
        # exclude = ["mobile"]

    def clean_confirm_pwd(self):
        pwd = self.cleaned_data.get("password")
        c_pwd = get_md5(self.cleaned_data.get("confirm_pwd"))
        if pwd != c_pwd:
            raise ValidationError("密码不一致")
        # 返回什么数据库里存什么
        return c_pwd

    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        # 返回什么数据库里存什么
        return get_md5(pwd)


class MyadminFormEdit(BootstrapModelForm):
    class Meta:
        model = MyAdmin  # 这里必须是model字母，不能错
        fields = ["user_name"]  # 这里必须是fields字母，不能错


class MyadminFormReset(BootstrapModelForm):
    password = forms.CharField(required=True, label="输入密码", min_length=8,
                               widget=forms.PasswordInput(attrs={"class": "form-control", }))
    confirm_pwd = forms.CharField(required=True, label="确认密码", min_length=8,
                                  widget=forms.PasswordInput(attrs={"class": "form-control", }))
    class Meta:
        model = MyAdmin  # 这里必须是model字母，不能错
        fields = ["password","confirm_pwd"]  # 这里必须是fields字母，不能错
    def clean_confirm_pwd(self):
        pwd = self.cleaned_data.get("password")
        c_pwd = get_md5(self.cleaned_data.get("confirm_pwd"))
        if pwd != c_pwd:
            raise ValidationError("密码不一致")
        # 返回什么数据库里存什么
        return c_pwd

    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        # 返回什么数据库里存什么
        return get_md5(pwd)


# ============ 社团管理系统表单 ============

# 社团相关表单
class ClubModelForm(BootstrapModelForm):
    established_date = forms.DateField(required=False,
                                       widget=forms.DateInput(attrs={"class": "form-control", "type": "date"}))
    
    class Meta:
        model = Club
        fields = ["name", "description", "established_date", "president", "contact_phone", "contact_email", "status"]
    
    def clean_contact_phone(self):
        phone = self.cleaned_data.get("contact_phone")
        if phone and len(phone) != 11:
            raise ValidationError("手机号格式错误，应为11位数字")
        return phone


# 部门相关表单
class DepartmentModelForm(BootstrapModelForm):
    class Meta:
        model = Department
        fields = ["name", "club", "description"]


# 角色相关表单
class RoleModelForm(BootstrapModelForm):
    class Meta:
        model = Role
        fields = ["name", "level", "description"]


# 成员相关表单
class MemberModelForm(BootstrapModelForm):
    join_time = forms.DateTimeField(required=False,
                                    widget=forms.DateTimeInput(attrs={"class": "form-control", "type": "datetime-local"}))
    
    class Meta:
        model = Member
        fields = ["member_id", "name", "gender", "grade", "major", "phone", "email", 
                 "club", "department", "role", "join_time", "status", "remark"]
    
    def clean_phone(self):
        phone = self.cleaned_data.get("phone")
        if phone and len(phone) != 11:
            raise ValidationError("手机号格式错误，应为11位数字")
        return phone
    
    def clean_member_id(self):
        member_id = self.cleaned_data.get("member_id")
        if not member_id:
            raise ValidationError("学号不能为空")
        return member_id


# 活动相关表单
class ActivityModelForm(BootstrapModelForm):
    start_time = forms.DateTimeField(required=False,
                                     widget=forms.DateTimeInput(attrs={"class": "form-control", "type": "datetime-local"}))
    end_time = forms.DateTimeField(required=False,
                                   widget=forms.DateTimeInput(attrs={"class": "form-control", "type": "datetime-local"}))
    
    class Meta:
        model = Activity
        fields = ["title", "club", "description", "location", "start_time", "end_time", 
                 "max_participants", "organizer", "status"]


# 活动报名相关表单
class ActivityRegistrationModelForm(BootstrapModelForm):
    register_time = forms.DateTimeField(required=False,
                                       widget=forms.DateTimeInput(attrs={"class": "form-control", "type": "datetime-local"}))
    
    class Meta:
        model = ActivityRegistration
        fields = ["activity", "member", "status", "remark"]
