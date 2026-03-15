# -*- coding: utf-8 -*-
import hashlib
from django.conf import settings
from django.db import migrations


def set_default_password(apps, schema_editor):
    Member = apps.get_model("app01", "Member")
    obj = hashlib.md5((settings.SECRET_KEY or "").encode("utf-8"))
    obj.update("123456".encode("utf-8"))
    default_pwd = obj.hexdigest()
    Member.objects.filter(password__isnull=True).update(password=default_pwd)
    Member.objects.filter(password="").update(password=default_pwd)


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0014_member_password'),
    ]

    operations = [
        migrations.RunPython(set_default_password, noop),
    ]
