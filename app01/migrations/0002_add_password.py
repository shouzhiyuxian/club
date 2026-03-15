# Generated manually to add password field

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='password',
            field=models.CharField(blank=True, max_length=64, null=True, verbose_name='登录密码'),
        ),
    ]