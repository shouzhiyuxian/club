# Created manually to ensure Announcement table exists

from django.db import migrations, models
import django.db.models.deletion
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0003_alter_activity_table_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Announcement',
            fields=[
                ('announcement_id', models.BigAutoField(primary_key=True, serialize=False, verbose_name='公告ID')),
                ('title', models.CharField(max_length=200, verbose_name='公告标题')),
                ('content', models.TextField(verbose_name='公告内容')),
                ('publish_time', models.DateTimeField(blank=True, default=datetime.datetime.now, null=True, verbose_name='发布时间')),
                ('status', models.SmallIntegerField(choices=[(1, '发布'), (2, '草稿'), (3, '删除')], default=1, verbose_name='状态')),
                ('is_top', models.BooleanField(default=False, verbose_name='置顶')),
                ('publisher', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='announcements', to='app01.myadmin', verbose_name='发布者')),
            ],
            options={
                'verbose_name': '公告',
                'db_table': 'announcement',
                'ordering': ['-is_top', '-publish_time'],
            },
        ),
    ]
