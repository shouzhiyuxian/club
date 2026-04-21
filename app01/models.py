from django.db import models
# Create your models here.
import datetime


class MyAdmin(models.Model):
    """管理员表"""
    id = models.CharField(verbose_name="ID", primary_key=True, max_length=32)
    account = models.CharField(verbose_name="登录账号", max_length=32, unique=True, null=True, blank=True)
    user_name = models.CharField(verbose_name="管理员名", max_length=32)
    password = models.CharField(verbose_name="管理员密码", max_length=64)

    class Meta:
        verbose_name = "管理员"
        db_table = "myadmin"

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
        db_table = "club"

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
        db_table = "department"

    def __str__(self):
        return self.name


class Role(models.Model):
    """角色表（成员在社团中的角色）"""
    role_id = models.BigAutoField(primary_key=True, verbose_name="角色ID")
    name = models.CharField(verbose_name="角色名称", max_length=50, null=False, blank=False)
    level_choices = (
        (1, "社长"),
        (2, "普通成员"),
    )
    level = models.SmallIntegerField(verbose_name="级别", choices=level_choices, default=2)
    description = models.TextField(verbose_name="角色描述", null=True, blank=True)

    class Meta:
        verbose_name = "角色"
        db_table = "role"

    def __str__(self):
        return self.name


class Member(models.Model):
    """成员表"""
    member_id = models.CharField(verbose_name="学号", primary_key=True, max_length=30)
    name = models.CharField(verbose_name="姓名", max_length=30, null=False, blank=False)
    nickname = models.CharField(verbose_name="昵称", max_length=50, null=True, blank=True)
    avatar = models.ImageField(verbose_name="头像", upload_to='avatars/', null=True, blank=True)
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
    password = models.CharField(verbose_name="登录密码", max_length=64, null=True, blank=True)

    class Meta:
        verbose_name = "成员"
        db_table = "member"

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
        db_table = "activity"

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
        db_table = "activity_registration"
        unique_together = [['activity', 'member']]  # 防止重复报名

    def __str__(self):
        return f"{self.member.name} - {self.activity.title}"


class Recruitment(models.Model):
    """招新批次表"""
    recruitment_id = models.BigAutoField(primary_key=True, verbose_name="招新ID")
    club = models.ForeignKey(to="Club", to_field="club_id", related_name="recruitments",
                            verbose_name="所属社团", null=False, blank=False, on_delete=models.CASCADE)
    title = models.CharField(verbose_name="批次名称", max_length=100, null=False, blank=False)
    start_date = models.DateField(verbose_name="开始日期", null=True, blank=True)
    end_date = models.DateField(verbose_name="结束日期", null=True, blank=True)
    status_choices = (
        (1, "报名中"),
        (2, "已结束"),
    )
    status = models.SmallIntegerField(verbose_name="状态", choices=status_choices, default=1)
    create_time = models.DateTimeField(verbose_name="创建时间", null=True, blank=True, default=datetime.datetime.now)

    class Meta:
        verbose_name = "招新批次"
        db_table = "recruitment"

    def __str__(self):
        return f"{self.club.name} - {self.title}"


class RecruitmentApplication(models.Model):
    """招新报名表"""
    application_id = models.BigAutoField(primary_key=True, verbose_name="报名ID")
    recruitment = models.ForeignKey(to="Recruitment", to_field="recruitment_id", related_name="applications",
                                    verbose_name="招新批次", null=False, blank=False, on_delete=models.CASCADE)
    student_id = models.CharField(verbose_name="学号", max_length=30, null=False, blank=False)
    name = models.CharField(verbose_name="姓名", max_length=30, null=False, blank=False)
    gender_choices = ((1, "男"), (2, "女"))
    gender = models.SmallIntegerField(verbose_name="性别", choices=gender_choices, null=True, blank=True)
    grade_choices = (
        (1, "大一"), (2, "大二"), (3, "大三"), (4, "大四"), (5, "研究生"),
    )
    grade = models.SmallIntegerField(verbose_name="年级", choices=grade_choices, null=True, blank=True)
    major = models.CharField(verbose_name="专业", max_length=100, null=True, blank=True)
    phone = models.CharField(verbose_name="手机号", max_length=11, null=True, blank=True)
    email = models.EmailField(verbose_name="邮箱", null=True, blank=True)
    apply_department = models.ForeignKey(to="Department", to_field="department_id", related_name="recruitment_applications",
                                         verbose_name="申请部门", null=True, blank=True, on_delete=models.SET_NULL)
    status_choices = (
        (1, "待审核"),
        (2, "已通过"),
        (3, "已拒绝"),
    )
    status = models.SmallIntegerField(verbose_name="状态", choices=status_choices, default=1)
    apply_time = models.DateTimeField(verbose_name="申请时间", null=True, blank=True, default=datetime.datetime.now)
    remark = models.TextField(verbose_name="备注", null=True, blank=True)

    class Meta:
        verbose_name = "招新报名"
        db_table = "recruitment_application"
        unique_together = [["recruitment", "student_id"]]

    def __str__(self):
        return f"{self.name}({self.student_id}) - {self.recruitment.title}"


class Announcement(models.Model):
    """公告表"""
    announcement_id = models.BigAutoField(primary_key=True, verbose_name="公告ID")
    title = models.CharField(verbose_name="公告标题", max_length=200, null=False, blank=False)
    content = models.TextField(verbose_name="公告内容", null=False, blank=False)
    club = models.ForeignKey(to="Club", to_field="club_id", related_name="announcements",
                            verbose_name="所属社团", null=True, blank=True, on_delete=models.CASCADE)
    publisher = models.ForeignKey(to="MyAdmin", to_field="id", related_name="announcements",
                                  verbose_name="发布者", null=True, blank=True, on_delete=models.SET_NULL)
    publish_time = models.DateTimeField(verbose_name="发布时间", null=True, blank=True, default=datetime.datetime.now)
    status_choices = (
        (1, "发布"),
        (2, "草稿"),
        (3, "删除"),
    )
    status = models.SmallIntegerField(verbose_name="状态", choices=status_choices, default=1)
    is_top = models.BooleanField(verbose_name="置顶", default=False)

    class Meta:
        verbose_name = "公告"
        db_table = "announcement"
        ordering = ["-is_top", "-publish_time"]

    def __str__(self):
        return self.title


class Follow(models.Model):
    """关注表"""
    follow_id = models.BigAutoField(primary_key=True, verbose_name="关注ID")
    follower = models.ForeignKey(to="Member", to_field="member_id", related_name="following",
                                 verbose_name="关注者", null=False, blank=False, on_delete=models.CASCADE)
    followed = models.ForeignKey(to="Member", to_field="member_id", related_name="followers",
                                 verbose_name="被关注者", null=False, blank=False, on_delete=models.CASCADE)
    follow_time = models.DateTimeField(verbose_name="关注时间", null=True, blank=True, default=datetime.datetime.now)

    class Meta:
        verbose_name = "关注"
        db_table = "follow"
        unique_together = [['follower', 'followed']]  # 防止重复关注

    def __str__(self):
        return f"{self.follower.name} 关注 {self.followed.name}"


class ActivityComment(models.Model):
    """活动评论表"""
    comment_id = models.BigAutoField(primary_key=True, verbose_name="评论ID")
    activity = models.ForeignKey(to="Activity", to_field="activity_id", related_name="comments",
                                verbose_name="活动", null=False, blank=False, on_delete=models.CASCADE)
    member = models.ForeignKey(to="Member", to_field="member_id", related_name="activity_comments",
                              verbose_name="评论者", null=False, blank=False, on_delete=models.CASCADE)
    content = models.TextField(verbose_name="评论内容", null=False, blank=False)
    create_time = models.DateTimeField(verbose_name="评论时间", null=True, blank=True, default=datetime.datetime.now)

    class Meta:
        verbose_name = "活动评论"
        db_table = "activity_comment"
        ordering = ["create_time"]

    def __str__(self):
        return f"{self.member.name} 对 {self.activity.title} 的评论"


class ActivityPhoto(models.Model):
    """活动照片表"""
    photo_id = models.BigAutoField(primary_key=True, verbose_name="照片ID")
    activity = models.ForeignKey(to="Activity", to_field="activity_id", related_name="photos",
                                verbose_name="活动", null=False, blank=False, on_delete=models.CASCADE)
    member = models.ForeignKey(to="Member", to_field="member_id", related_name="activity_photos",
                              verbose_name="上传者", null=False, blank=False, on_delete=models.CASCADE)
    photo = models.ImageField(verbose_name="照片", upload_to='activity_photos/', null=False, blank=False)
    description = models.TextField(verbose_name="照片描述", null=True, blank=True)
    upload_time = models.DateTimeField(verbose_name="上传时间", null=True, blank=True, default=datetime.datetime.now)

    class Meta:
        verbose_name = "活动照片"
        db_table = "activity_photo"
        ordering = ["-upload_time"]

    def __str__(self):
        return f"{self.member.name} 上传的 {self.activity.title} 照片"


class ActivityLike(models.Model):
    """活动点赞表"""
    like_id = models.BigAutoField(primary_key=True, verbose_name="点赞ID")
    activity = models.ForeignKey(to="Activity", to_field="activity_id", related_name="likes",
                                verbose_name="活动", null=False, blank=False, on_delete=models.CASCADE)
    member = models.ForeignKey(to="Member", to_field="member_id", related_name="activity_likes",
                              verbose_name="点赞者", null=False, blank=False, on_delete=models.CASCADE)
    like_time = models.DateTimeField(verbose_name="点赞时间", null=True, blank=True, default=datetime.datetime.now)

    class Meta:
        verbose_name = "活动点赞"
        db_table = "activity_like"
        unique_together = [['activity', 'member']]  # 防止重复点赞

    def __str__(self):
        return f"{self.member.name} 点赞 {self.activity.title}"


class ClubDiscussion(models.Model):
    """社团内部讨论表"""
    discussion_id = models.BigAutoField(primary_key=True, verbose_name="讨论ID")
    club = models.ForeignKey(to="Club", to_field="club_id", related_name="discussions",
                            verbose_name="所属社团", null=False, blank=False, on_delete=models.CASCADE)
    member = models.ForeignKey(to="Member", to_field="member_id", related_name="discussions",
                              verbose_name="发言者", null=False, blank=False, on_delete=models.CASCADE)
    content = models.TextField(verbose_name="讨论内容", null=False, blank=False)
    create_time = models.DateTimeField(verbose_name="发言时间", null=True, blank=True, default=datetime.datetime.now)
    is_deleted = models.BooleanField(verbose_name="是否删除", default=False)

    class Meta:
        verbose_name = "社团讨论"
        db_table = "club_discussion"
        ordering = ["-create_time"]

    def __str__(self):
        return f"{self.member.name} 在 {self.club.name} 的发言"

