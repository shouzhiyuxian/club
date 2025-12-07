from django.db import models
# Create your models here.
import datetime


class MyAdmin(models.Model):
    """管理员表"""
    id = models.CharField(verbose_name="管理员账号", primary_key=True, max_length=32)
    user_name = models.CharField(verbose_name="管理员名", max_length=32)
    password = models.CharField(verbose_name="管理员密码", max_length=64)

    class Meta:
        verbose_name = "管理员"
        db_table = "管理员表"

    def __str__(self):
        return self.user_name


class Club(models.Model):
    """社团表"""
    club_id = models.BigAutoField(primary_key=True, verbose_name="社团ID")
    name = models.CharField(verbose_name="社团名称", max_length=100, null=False, blank=False)
    description = models.TextField(verbose_name="社团简介", null=True, blank=True)
    established_date = models.DateField(verbose_name="成立日期", null=True, blank=True, default=datetime.date.today)
    president = models.CharField(verbose_name="社长姓名", max_length=30, null=True, blank=True)
    contact_phone = models.CharField(verbose_name="联系电话", max_length=11, null=True, blank=True)
    contact_email = models.EmailField(verbose_name="联系邮箱", null=True, blank=True)
    status_choices = (
        (1, "正常"),
        (2, "暂停"),
        (3, "解散"),
    )
    status = models.SmallIntegerField(verbose_name="状态", choices=status_choices, default=1)
    create_time = models.DateTimeField(verbose_name="创建时间", null=True, blank=True, default=datetime.datetime.now)

    class Meta:
        verbose_name = "社团"
        db_table = "社团表"

    def __str__(self):
        return self.name


class Department(models.Model):
    """部门表（社团内的部门）"""
    department_id = models.BigAutoField(primary_key=True, verbose_name="部门ID")
    name = models.CharField(verbose_name="部门名称", max_length=100, null=False, blank=False)
    club = models.ForeignKey(to="Club", to_field="club_id", related_name="departments",
                            verbose_name="所属社团", null=True, blank=True, on_delete=models.CASCADE)
    description = models.TextField(verbose_name="部门简介", null=True, blank=True)
    create_time = models.DateTimeField(verbose_name="创建时间", null=True, blank=True, default=datetime.datetime.now)

    class Meta:
        verbose_name = "部门"
        db_table = "部门表"

    def __str__(self):
        return self.name


class Role(models.Model):
    """角色表（成员在社团中的角色）"""
    role_id = models.BigAutoField(primary_key=True, verbose_name="角色ID")
    name = models.CharField(verbose_name="角色名称", max_length=50, null=False, blank=False)
    level_choices = (
        (1, "社长"),
        (2, "副社长"),
        (3, "部长"),
        (4, "副部长"),
        (5, "普通成员"),
    )
    level = models.SmallIntegerField(verbose_name="级别", choices=level_choices, default=5)
    description = models.TextField(verbose_name="角色描述", null=True, blank=True)

    class Meta:
        verbose_name = "角色"
        db_table = "角色表"

    def __str__(self):
        return self.name


class Member(models.Model):
    """成员表"""
    member_id = models.CharField(verbose_name="学号", primary_key=True, max_length=30)
    name = models.CharField(verbose_name="姓名", max_length=30, null=False, blank=False)
    gender_choices = ((1, "男"), (2, "女"))
    gender = models.SmallIntegerField(verbose_name="性别", choices=gender_choices, null=True, blank=True)
    grade_choices = (
        (1, "大一"),
        (2, "大二"),
        (3, "大三"),
        (4, "大四"),
        (5, "研究生"),
    )
    grade = models.SmallIntegerField(verbose_name="年级", choices=grade_choices, null=True, blank=True)
    major = models.CharField(verbose_name="专业", max_length=100, null=True, blank=True)
    phone = models.CharField(verbose_name="手机号", max_length=11, null=True, blank=True)
    email = models.EmailField(verbose_name="邮箱", null=True, blank=True)
    club = models.ForeignKey(to="Club", to_field="club_id", related_name="members",
                            verbose_name="所属社团", null=True, blank=True, on_delete=models.SET_NULL)
    department = models.ForeignKey(to="Department", to_field="department_id", related_name="members",
                                   verbose_name="所属部门", null=True, blank=True, on_delete=models.SET_NULL)
    role = models.ForeignKey(to="Role", to_field="role_id", related_name="members",
                             verbose_name="角色", null=True, blank=True, on_delete=models.SET_NULL)
    join_time = models.DateTimeField(verbose_name="加入时间", null=True, blank=True, default=datetime.datetime.now)
    status_choices = (
        (1, "正常"),
        (2, "请假"),
        (3, "退社"),
    )
    status = models.SmallIntegerField(verbose_name="状态", choices=status_choices, default=1)
    remark = models.TextField(verbose_name="备注", null=True, blank=True)

    class Meta:
        verbose_name = "成员"
        db_table = "成员表"

    def __str__(self):
        return self.name


class Activity(models.Model):
    """活动表"""
    activity_id = models.BigAutoField(primary_key=True, verbose_name="活动ID")
    title = models.CharField(verbose_name="活动名称", max_length=100, null=False, blank=False)
    club = models.ForeignKey(to="Club", to_field="club_id", related_name="activities",
                            verbose_name="所属社团", null=True, blank=True, on_delete=models.CASCADE)
    description = models.TextField(verbose_name="活动描述", null=True, blank=True)
    location = models.CharField(verbose_name="活动地点", max_length=200, null=True, blank=True)
    start_time = models.DateTimeField(verbose_name="开始时间", null=True, blank=True)
    end_time = models.DateTimeField(verbose_name="结束时间", null=True, blank=True)
    max_participants = models.IntegerField(verbose_name="最大参与人数", null=True, blank=True, default=0)
    current_participants = models.IntegerField(verbose_name="当前参与人数", default=0)
    organizer = models.ForeignKey(to="Member", to_field="member_id", related_name="organized_activities",
                                 verbose_name="组织者", null=True, blank=True, on_delete=models.SET_NULL)
    status_choices = (
        (1, "报名中"),
        (2, "进行中"),
        (3, "已结束"),
        (4, "已取消"),
    )
    status = models.SmallIntegerField(verbose_name="状态", choices=status_choices, default=1)
    create_time = models.DateTimeField(verbose_name="创建时间", null=True, blank=True, default=datetime.datetime.now)

    class Meta:
        verbose_name = "活动"
        db_table = "活动表"

    def __str__(self):
        return self.title


class ActivityRegistration(models.Model):
    """活动报名表"""
    registration_id = models.BigAutoField(primary_key=True, verbose_name="报名ID")
    activity = models.ForeignKey(to="Activity", to_field="activity_id", related_name="registrations",
                                verbose_name="活动", null=False, blank=False, on_delete=models.CASCADE)
    member = models.ForeignKey(to="Member", to_field="member_id", related_name="registrations",
                              verbose_name="成员", null=False, blank=False, on_delete=models.CASCADE)
    register_time = models.DateTimeField(verbose_name="报名时间", null=True, blank=True, default=datetime.datetime.now)
    status_choices = (
        (1, "已报名"),
        (2, "已参加"),
        (3, "已取消"),
        (4, "未参加"),
    )
    status = models.SmallIntegerField(verbose_name="状态", choices=status_choices, default=1)
    remark = models.TextField(verbose_name="备注", null=True, blank=True)

    class Meta:
        verbose_name = "活动报名"
        db_table = "活动报名表"
        unique_together = [['activity', 'member']]  # 防止重复报名

    def __str__(self):
        return f"{self.member.name} - {self.activity.title}"

