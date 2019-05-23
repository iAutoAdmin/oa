# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-10-28 03:00
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('process', '0001_initial'),
        ('account', '0003_auto_20181028_1032'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='applicant',
            field=models.ForeignKey(help_text='用户对应的申请流程', null=True, on_delete=django.db.models.deletion.CASCADE, to='process.Process', verbose_name='用户对应的申请流程'),
        ),
        migrations.AddField(
            model_name='user',
            name='approver',
            field=models.ForeignKey(help_text='用户对应的审批表', null=True, on_delete=django.db.models.deletion.CASCADE, to='process.ApprovalProcess', verbose_name='用户对应的审批表'),
        ),
    ]
