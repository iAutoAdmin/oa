# Generated by Django 2.2.1 on 2019-07-09 07:07

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('name', models.CharField(help_text='姓名', max_length=32, null=True, verbose_name='姓名')),
                ('tel', models.CharField(help_text='电话', max_length=15, null=True, verbose_name='电话')),
            ],
            options={
                'verbose_name': '用户扩展表',
                'db_table': 'auth_user',
                'ordering': ['id'],
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('department_name', models.CharField(help_text='部门名称', max_length=64, verbose_name='部门名称')),
                ('level', models.CharField(choices=[('syb', '事业部'), ('one', '一级部门'), ('two', '二级部门')], default='syb', help_text='事业部，一级部门，还是二级部门', max_length=32, verbose_name='部门级别')),
                ('is_deleted', models.IntegerField(choices=[(0, '启用'), (1, '禁用')], default=0, help_text='请选择新建部门的状态', verbose_name='部门状态')),
                ('leader', models.ForeignKey(help_text='领导', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='department_leader', to=settings.AUTH_USER_MODEL, verbose_name='部门领导')),
                ('parent_dept', models.ForeignKey(help_text='子部门门', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='account.Department', verbose_name='子部门')),
            ],
            options={
                'verbose_name': '用户部门表',
                'db_table': 'auth_user_department',
                'ordering': ['id'],
            },
        ),
        migrations.AddField(
            model_name='user',
            name='department',
            field=models.ForeignKey(help_text='部门', null=True, on_delete=django.db.models.deletion.CASCADE, to='account.Department', verbose_name='部门'),
        ),
        migrations.AddField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
    ]
