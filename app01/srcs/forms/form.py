from django import forms
from app01.utils.bootstrap_modelform import BootstrapModelForm
from app01.models import (
    MyAdmin, Club, Role, Member, Activity, ActivityRegistration,
    Recruitment, RecruitmentApplication, Announcement,
    ActivityComment, ActivityPhoto, ActivityLike,
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
    account = forms.CharField(required=True, label="登录账号",
                              widget=forms.TextInput(attrs={"class": "form-control", }))
    user_name = forms.CharField(required=False, label="管理员姓名",
                                widget=forms.TextInput(attrs={"class": "form-control", }))
    password = forms.CharField(required=True, label="输入密码", min_length=8,
                                  widget=forms.PasswordInput(attrs={"class": "form-control", }))
    confirm_pwd = forms.CharField(required=True, label="确认密码", min_length=8,
                                widget=forms.PasswordInput(attrs={"class": "form-control", }))
    class Meta:
        model = MyAdmin  # 这里必须是model字母，不能错
        fields = ["account", "user_name", "password", "confirm_pwd", "id"]  # 这里必须是fields字母，不能错
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

    def clean_account(self):
        account = self.cleaned_data.get("account")
        if MyAdmin.objects.filter(account=account).exists():
            raise ValidationError("该账号已存在")
        return account


class MyadminFormEdit(BootstrapModelForm):
    account = forms.CharField(required=True, label="登录账号",
                              widget=forms.TextInput(attrs={"class": "form-control", }))
    class Meta:
        model = MyAdmin  # 这里必须是model字母，不能错
        fields = ["account", "user_name"]  # 这里必须是fields字母，不能错

    def clean_account(self):
        account = self.cleaned_data.get("account")
        # 排除当前实例，检查其他记录是否有相同账号
        instance_id = self.instance.id if self.instance else None
        if MyAdmin.objects.filter(account=account).exclude(id=instance_id).exists():
            raise ValidationError("该账号已存在")
        return account


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
                                       label="成立日期",
                                       widget=forms.DateInput(attrs={"class": "form-control", "type": "date"}))
    president = forms.ChoiceField(
        required=False,
        label="社长",
        choices=[],
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    
    class Meta:
        model = Club
        fields = ["name", "description", "established_date", "president"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].label = "社团名称"
        self.fields['description'].label = "社团简介"
        # 编辑时优先限制为该社团成员；新增时只显示未加入社团的人
        # 判断是新增还是编辑：有 pk 说明是编辑
        is_edit = self.instance and self.instance.pk
        if is_edit:
            # 编辑时只显示本社团成员
            members_qs = Member.objects.filter(club_id=self.instance.club_id).order_by("member_id")
        else:
            # 新增时只显示未加入任何社团的成员
            members_qs = Member.objects.filter(club__isnull=True).order_by("member_id")
        choices = [("", "请选择社长")] + [
            (m.member_id, f"{m.name}（{m.member_id}）")
            for m in members_qs
        ]
        self.fields["president"].choices = choices
        self._president_member_obj = None

        # 回显当前社长：按本社团 + 姓名反查到成员学号
        if self.instance and self.instance.club_id and self.instance.president:
            current = Member.objects.filter(
                club_id=self.instance.club_id,
                name=self.instance.president,
            ).order_by("member_id").first()
            if current:
                self.initial["president"] = current.member_id

    def clean_president(self):
        member_id = (self.cleaned_data.get("president") or "").strip()
        if not member_id:
            self._president_member_obj = None
            return ""
        member_obj = Member.objects.filter(member_id=member_id).select_related("club").first()
        if not member_obj:
            raise ValidationError("所选社长成员不存在")
        self._president_member_obj = member_obj
        # 模型字段仍存社长姓名
        return member_obj.name
    
# 角色相关表单
class RoleModelForm(BootstrapModelForm):
    class Meta:
        model = Role
        fields = ["name", "level"]


# 成员相关表单
class MemberModelForm(BootstrapModelForm):
    """成员表单 - 添加时使用（包含member_id）"""
    join_time = forms.DateField(required=False, label="加入日期",
                                widget=forms.DateInput(attrs={"class": "form-control", "type": "date"}))
    
    class Meta:
        model = Member
        fields = ["member_id", "name", "avatar", "gender", "grade", "major", "phone", "email",
                 "club", "role", "join_time"]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 添加模式：所有字段必填，除了 club、role、avatar
        if not (self.instance and self.instance.pk):
            for field_name in self.fields:
                if field_name not in ('club', 'role', 'avatar'):
                    self.fields[field_name].required = True
                else:
                    self.fields[field_name].required = False
        # 如果是编辑模式（存在instance），禁用member_id字段
        if self.instance and self.instance.pk:
            self.fields['member_id'].disabled = True
            self.fields['member_id'].help_text = "学号（主键）不可修改"
            
            # 将禁用字段的原始值注入 data，防止提交时被清空
            if self.data and hasattr(self.instance, 'club_id'):
                data = self.data.copy()
                if 'club' not in self.data:
                    data['club'] = self.instance.club_id or ''
                if 'role' not in self.data:
                    data['role'] = self.instance.role_id or ''
                if 'join_time' not in self.data:
                    data['join_time'] = str(self.instance.join_time) if self.instance.join_time else ''
                self.data = data
        # 存储旧的 role_id 和 club_id，用于检测变更
        if self.instance and self.instance.pk:
            self._old_role_id = self.instance.role_id
            self._old_club_id = self.instance.club_id
        else:
            self._old_role_id = None
            self._old_club_id = None
    
    def save(self, commit=True):
        """重写 save 方法，同步 Club.president 字段和原社长降级"""
        instance = super().save(commit=False)
        
        # 检测角色是否变为社长
        is_now_president = False
        if instance.role_id:
            try:
                role = Role.objects.get(role_id=instance.role_id)
                if role.level == 1 and instance.club_id:
                    is_now_president = True
            except Role.DoesNotExist:
                pass
        
        # 如果变为社长，同步 Club.president 并降级原社长
        if is_now_president and instance.club_id:
            # 更新社团表的社长姓名
            Club.objects.filter(club_id=instance.club_id).update(president=instance.name)
            
            # 将原社长（如果有）降级为普通成员
            role_member = Role.objects.filter(level=2).first()
            if role_member:
                Member.objects.filter(
                    club_id=instance.club_id,
                    role__level=1
                ).exclude(member_id=instance.member_id).update(role=role_member)
        
        # 如果之前是社长但现在不是，清除 Club.president
        if self._old_role_id and instance.role_id:
            try:
                old_role = Role.objects.get(role_id=self._old_role_id)
                new_role = Role.objects.get(role_id=instance.role_id)
                if old_role.level == 1 and new_role.level != 1:
                    # 清除社团的社长信息（如果此成员是该社团的社长）
                    if self._old_club_id:
                        Club.objects.filter(
                            club_id=self._old_club_id, 
                            president=instance.name
                        ).update(president="")
            except Role.DoesNotExist:
                pass
        
        if commit:
            instance.save()
            # 更新旧值
            self._old_role_id = instance.role_id
            self._old_club_id = instance.club_id
        
        return instance
    
    def clean_phone(self):
        phone = self.cleaned_data.get("phone")
        if phone and len(phone) != 11:
            raise ValidationError("手机号格式错误，应为11位数字")
        return phone
    
    def clean_member_id(self):
        member_id = self.cleaned_data.get("member_id")
        if not member_id:
            raise ValidationError("学号不能为空")
        # 编辑时跳过重复检查（自己本身就是已存在的）
        if not self.instance or not self.instance.pk:
            if Member.objects.filter(member_id=member_id).exists():
                raise ValidationError("该学号已存在")
        return member_id
    
    def clean(self):
        cleaned_data = super().clean()
        club = cleaned_data.get("club")
        role = cleaned_data.get("role")
        
        # 如果没加入社团，角色必须为NULL（未设置）
        if not club:
            cleaned_data["role"] = None
        # 如果加入了社团但没有选角色，默认设为普通成员
        elif club and not role:
            from app01.models import Role
            role_member = Role.objects.filter(level=2).first()
            if role_member:
                cleaned_data["role"] = role_member
        
        return cleaned_data


# 活动相关表单
class ActivityModelForm(BootstrapModelForm):
    start_time = forms.DateTimeField(required=False,
                                     label="开始时间",
                                     widget=forms.DateTimeInput(attrs={"class": "form-control", "type": "datetime-local"}))
    end_time = forms.DateTimeField(required=False,
                                   label="结束时间",
                                   widget=forms.DateTimeInput(attrs={"class": "form-control", "type": "datetime-local"}))

    class Meta:
        model = Activity
        fields = ["title", "club", "description", "location", "start_time", "end_time", 
                 "max_participants", "organizer", "status"]

    def __init__(self, *args, club_id=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].label = "活动标题"
        self.fields['club'].label = "所属社团"
        self.fields['description'].label = "活动描述"
        self.fields['location'].label = "活动地点"
        self.fields['max_participants'].label = "最大参与人数"
        self.fields['organizer'].label = "组织者"
        self.fields['status'].label = "状态"
        # 限制组织者只能选择本社团的成员
        if club_id:
            self.fields["organizer"].queryset = Member.objects.filter(club_id=club_id, club__isnull=False)
        elif self.instance and self.instance.club_id:
            self.fields["organizer"].queryset = Member.objects.filter(club_id=self.instance.club_id, club__isnull=False)
        else:
            # 如果没有指定社团，显示所有在团成员
            self.fields["organizer"].queryset = Member.objects.filter(club__isnull=False)
    
    def clean(self):
        """验证组织者是否属于选中的社团"""
        cleaned_data = super().clean()
        club = cleaned_data.get("club")
        organizer = cleaned_data.get("organizer")
        
        if club and organizer:
            if organizer.club_id != club.club_id:
                raise forms.ValidationError("组织者必须是该社团的成员")
        
        return cleaned_data


# 活动报名相关表单
class ActivityRegistrationModelForm(BootstrapModelForm):
    class Meta:
        model = ActivityRegistration
        fields = ["activity", "member", "status"]


# 招新批次相关表单
class RecruitmentModelForm(BootstrapModelForm):
    start_date = forms.DateField(required=False,
                                 label="开始日期",
                                 widget=forms.DateInput(attrs={"class": "form-control", "type": "date"}))
    end_date = forms.DateField(required=False,
                               label="结束日期",
                               widget=forms.DateInput(attrs={"class": "form-control", "type": "date"}))

    class Meta:
        model = Recruitment
        fields = ["club", "title", "start_date", "end_date", "status"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['club'].label = "所属社团"
        self.fields['title'].label = "招新批次标题"
        self.fields['status'].label = "状态"


# 招新报名相关表单
class RecruitmentApplicationModelForm(BootstrapModelForm):
    apply_time = forms.DateTimeField(required=False,
                                     label="申请时间",
                                     widget=forms.DateTimeInput(attrs={"class": "form-control", "type": "datetime-local"}))

    class Meta:
        model = RecruitmentApplication
        fields = ["recruitment", "student_id", "name", "gender", "grade", "major", "phone", "email",
                  "status", "apply_time", "remark"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['recruitment'].label = "招新批次"
        self.fields['student_id'].label = "学号"
        self.fields['name'].label = "姓名"
        self.fields['gender'].label = "性别"
        self.fields['grade'].label = "年级"
        self.fields['major'].label = "专业"
        self.fields['phone'].label = "手机号"
        self.fields['email'].label = "邮箱"
        self.fields['status'].label = "状态"
        self.fields['remark'].label = "备注"

    def clean_phone(self):
        phone = self.cleaned_data.get("phone")
        if phone and len(phone) != 11:
            raise ValidationError("手机号格式错误，应为11位数字")
        return phone


class AnnouncementModelForm(BootstrapModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 置顶用开关样式，不用 form-control
        self.fields["is_top"].widget.attrs["class"] = "form-check-input"

    class Meta:
        model = Announcement
        fields = ["title", "content", "status", "is_top"]


# 活动评论相关表单
class ActivityCommentForm(BootstrapModelForm):
    class Meta:
        model = ActivityComment
        fields = ["content"]
        widgets = {
            "content": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "写下你的评论..."}),
        }


# 活动照片相关表单
class ActivityPhotoForm(BootstrapModelForm):
    class Meta:
        model = ActivityPhoto
        fields = ["photo", "description"]
        widgets = {
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 2, "placeholder": "照片描述（可选）"}),
        }
