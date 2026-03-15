# -*- coding: utf-8 -*-
"""将角色合并为仅 社长、普通成员（系统仅三种身份：管理员、社长、成员）"""
from django.db import migrations


def consolidate_roles(apps, schema_editor):
    Role = apps.get_model("app01", "Role")
    Member = apps.get_model("app01", "Member")
    president, _ = Role.objects.get_or_create(name="社长", defaults={"level": 1, "description": "社团负责人"})
    president.level = 1
    president.save(update_fields=["level"])
    member_role, _ = Role.objects.get_or_create(name="普通成员", defaults={"level": 2, "description": "成员"})
    member_role.level = 2
    member_role.save(update_fields=["level"])
    for m in Member.objects.select_related("role").all():
        if m.role_id and m.role.level == 1:
            m.role_id = president.role_id
        else:
            m.role_id = member_role.role_id
        m.save(update_fields=["role_id"])
    Role.objects.exclude(name__in=["社长", "普通成员"]).delete()


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("app01", "0016_role_choices_two"),
    ]

    operations = [
        migrations.RunPython(consolidate_roles, noop),
    ]
