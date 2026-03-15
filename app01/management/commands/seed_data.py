# -*- coding: utf-8 -*-
"""
填充假数据：社团、部门、角色、成员、活动、报名记录。
执行：python manage.py seed_data
"""
import random
import datetime
from django.core.management.base import BaseCommand
from django.utils import timezone
from app01.models import Club, Department, Role, Member, Activity, ActivityRegistration


class Command(BaseCommand):
    help = "填充社团、部门、角色、成员、活动及报名假数据，用于仪表盘展示"

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear",
            action="store_true",
            help="先清空除管理员外的所有相关数据再填充",
        )

    def handle(self, *args, **options):
        if options["clear"]:
            self._clear_data()
        self._ensure_roles()
        clubs = self._create_clubs()
        departments = self._create_departments(clubs)
        roles = list(Role.objects.all().order_by("level"))
        members = self._create_members(clubs, departments, roles)
        activities = self._create_activities(clubs, members)
        self._create_registrations(activities, members)
        self._update_activity_participants()
        self.stdout.write(self.style.SUCCESS("假数据填充完成。可访问首页查看仪表盘。"))

    def _clear_data(self):
        ActivityRegistration.objects.all().delete()
        Activity.objects.all().delete()
        Member.objects.all().delete()
        Department.objects.all().delete()
        Club.objects.all().delete()
        self.stdout.write("已清空活动报名、活动、成员、部门、社团数据。")

    def _ensure_roles(self):
        """仅两种角色：社长、普通成员（系统身份为管理员/社长/成员）"""
        for name, level, desc in [("社长", 1, "社团负责人"), ("普通成员", 2, "成员")]:
            Role.objects.get_or_create(name=name, defaults={"level": level, "description": desc})

    def _create_clubs(self):
        data = [
            ("科技创新协会", "开展编程、竞赛、项目实践等活动。", "张伟", "13800001001", "tech@club.edu.cn"),
            ("书法社", "传承书法艺术，定期练笔与展览。", "李芳", "13800001002", "calligraphy@club.edu.cn"),
            ("篮球社", "组织训练与院系篮球赛。", "王强", "13800001003", "basketball@club.edu.cn"),
            ("摄影协会", "外拍、讲座、作品分享。", "刘洋", "13800001004", "photo@club.edu.cn"),
            ("英语角", "口语练习、观影、四六级互助。", "陈敏", "13800001005", "english@club.edu.cn"),
        ]
        clubs = []
        for name, desc, president, phone, email in data:
            c, _ = Club.objects.get_or_create(
                name=name,
                defaults={
                    "description": desc,
                    "established_date": timezone.now().date() - datetime.timedelta(days=random.randint(200, 800)),
                    "president": president,
                    "contact_phone": phone,
                    "contact_email": email,
                    "status": 1,
                },
            )
            clubs.append(c)
        return clubs

    def _create_departments(self, clubs):
        dept_templates = ["策划部", "宣传部", "外联部", "技术部", "办公室"]
        created = []
        for club in clubs:
            n = random.randint(2, 4)
            for name in random.sample(dept_templates, n):
                Department.objects.get_or_create(
                    club=club,
                    name=f"{club.name[:2]}{name}",
                    defaults={"description": f"{name}日常事务"},
                )
            created.extend(list(club.departments.all()))
        return created

    def _create_members(self, clubs, departments, roles):
        # 姓名池（可重复使用学号唯一即可）
        first_names = "伟芳强洋敏静丽军杰磊明华鹏飞鑫斌勇艳玲涛超秀英".strip()
        last_names = "张李王刘陈杨黄赵周吴徐孙马朱胡郭何高林罗郑梁谢宋唐韩曹许邓冯曹曾彭吕苏卢蒋蔡贾丁魏薛叶阎余潘杜戴夏钟汪田任姜范方石姚谭廖邹熊金陆郝孔白崔康毛邱秦江史顾侯邵孟龙万段漕钱汤尹黎易常武乔贺赖龚文".strip()
        majors = ["计算机科学与技术", "软件工程", "电子信息", "机械工程", "工商管理", "汉语言文学", "英语", "数学与应用数学", "金融学", "法学"]

        members = []
        used_ids = set()
        member_id_start = 2021001

        for i, club in enumerate(clubs):
            depts = list(club.departments.all())
            n_members = random.randint(5, 12)
            for j in range(n_members):
                mid = str(member_id_start + len(used_ids))
                if mid in used_ids:
                    member_id_start += 1000
                    mid = str(member_id_start + len(used_ids))
                used_ids.add(mid)
                name = random.choice(last_names) + random.choice(first_names)
                gender = random.choice([1, 2])
                grade = random.choice([1, 2, 3, 4, 5])
                major = random.choice(majors)
                phone = "138" + "".join([str(random.randint(0, 9)) for _ in range(8)])
                email = f"{mid}@student.edu.cn"
                dept = random.choice(depts) if depts else None
                # 每社团一名社长，其余为普通成员
                if j == 0 and not Member.objects.filter(club=club, role__level=1).exists():
                    role = next((r for r in roles if r.level == 1), roles[-1])
                else:
                    role = next((r for r in roles if r.level == 2), roles[-1])
                join_delta = datetime.timedelta(days=random.randint(30, 400))
                join_time = timezone.now() - join_delta
                m = Member.objects.create(
                    member_id=mid,
                    name=name,
                    gender=gender,
                    grade=grade,
                    major=major,
                    phone=phone,
                    email=email,
                    club=club,
                    department=dept,
                    role=role,
                    join_time=join_time,
                    status=1,
                )
                members.append(m)

        return members

    def _create_activities(self, clubs, members):
        activities = []
        titles = [
            "招新宣讲会", "技术分享会", "周末训练", "书法体验课", "摄影外拍",
            "英语角晨读", "院系友谊赛", "换届大会", "年终总结会", "主题讲座",
            "团建活动", "作品展览", "线上竞赛", "迎新晚会", "读书会",
        ]
        locations = ["学生活动中心", "教学楼A101", "体育馆", "图书馆报告厅", "操场", "线上会议", "校门口集合"]
        now = timezone.now()
        status_choices = [1, 1, 2, 3, 3, 3, 4]  # 多些已结束

        for i in range(12):
            club = random.choice(clubs)
            club_members = [m for m in members if m.club_id == club.club_id]
            organizer = random.choice(club_members) if club_members else None
            title = random.choice(titles) + f"（{club.name}）"
            start_delta = datetime.timedelta(days=random.randint(-120, 30))
            start_time = now + start_delta
            end_time = start_time + datetime.timedelta(hours=random.randint(2, 5))
            create_time = start_time - datetime.timedelta(days=random.randint(1, 20))
            status = random.choice(status_choices)
            act = Activity.objects.create(
                title=title,
                club=club,
                description=f"活动说明：{title}的详细安排与注意事项。",
                location=random.choice(locations),
                start_time=start_time,
                end_time=end_time,
                max_participants=random.choice([30, 50, 80, 100]),
                current_participants=0,
                organizer=organizer,
                status=status,
            )
            # 让 create_time 影响“近6个月趋势”
            Activity.objects.filter(activity_id=act.activity_id).update(create_time=create_time)
            act.create_time = create_time
            activities.append(act)
        return activities

    def _create_registrations(self, activities, members):
        for act in activities:
            club_members = [m for m in members if m.club_id == act.club_id]
            n_reg = random.randint(0, min(15, len(club_members), act.max_participants or 99))
            chosen = random.sample(club_members, n_reg) if club_members else []
            for m in chosen:
                status = random.choice([1, 1, 2, 2, 3, 4])  # 已报名、已参加为主
                ActivityRegistration.objects.get_or_create(
                    activity=act,
                    member=m,
                    defaults={"status": status},
                )

    def _update_activity_participants(self):
        for act in Activity.objects.all():
            count = act.registrations.filter(status__in=[1, 2]).count()  # 已报名、已参加
            Activity.objects.filter(activity_id=act.activity_id).update(current_participants=count)
