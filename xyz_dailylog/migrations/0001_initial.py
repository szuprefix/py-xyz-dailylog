# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2020-06-27 14:05
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import xyz_util.modelutils


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DailyLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('the_date', models.DateField(db_index=True, verbose_name='\u65e5\u671f')),
                ('context', xyz_util.modelutils.JSONField(blank=True, default={}, verbose_name='\u8be6\u60c5')),
                ('create_time', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='dailylog_dailylogs', to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
                'verbose_name': '\u65e5\u5fd7',
                'verbose_name_plural': '\u65e5\u5fd7',
            },
        ),
        migrations.CreateModel(
            name='Performance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('owner_id', models.PositiveIntegerField(blank=True, db_index=True, null=True, verbose_name='\u5c5e\u4e3b\u7f16\u53f7')),
                ('owner_name', models.CharField(blank=True, default='', max_length=256, verbose_name='\u5c5e\u4e3b\u540d\u79f0')),
                ('owner_group', models.CharField(blank=True, default='', max_length=256, verbose_name='\u5c5e\u4e3b\u5206\u7ec4')),
                ('user_name', models.CharField(blank=True, default='', max_length=256, verbose_name='\u7528\u6237\u59d3\u540d')),
                ('user_group', models.CharField(blank=True, default='', max_length=256, verbose_name='\u7528\u6237\u5206\u7ec4')),
                ('detail', xyz_util.modelutils.JSONField(blank=True, default={}, verbose_name='\u8be6\u60c5')),
                ('target', models.PositiveIntegerField(blank=True, default=0, verbose_name='\u76ee\u6807')),
                ('accomplish', models.PositiveIntegerField(blank=True, default=0, verbose_name='\u5b8c\u6210')),
                ('accumulate', models.PositiveIntegerField(blank=True, default=0, verbose_name='\u7d2f\u8ba1\u5b8c\u6210')),
                ('percent', models.PositiveSmallIntegerField(default=0, verbose_name='\u5b8c\u6210\u767e\u5206\u6bd4')),
                ('times', models.PositiveSmallIntegerField(default=0, verbose_name='\u6b21\u6570')),
                ('score', models.PositiveSmallIntegerField(blank=True, default=0, null=True, verbose_name='\u5f97\u5206')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('update_time', models.DateTimeField(auto_now=True, db_index=True, verbose_name='\u66f4\u65b0\u65f6\u95f4')),
                ('owner_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='contenttypes.ContentType', verbose_name='\u5f52\u7c7b')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='dailylog_performances', to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
                'ordering': ('-update_time',),
                'verbose_name': '\u8868\u73b0',
                'verbose_name_plural': '\u8868\u73b0',
            },
        ),
        migrations.CreateModel(
            name='Record',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('the_date', models.DateField(db_index=True, verbose_name='\u65e5\u671f')),
                ('owner_id', models.PositiveIntegerField(blank=True, db_index=True, null=True, verbose_name='\u5c5e\u4e3b\u7f16\u53f7')),
                ('owner_name', models.CharField(blank=True, default='', max_length=256, verbose_name='\u5c5e\u4e3b\u540d\u79f0')),
                ('owner_group', models.CharField(blank=True, default='', max_length=256, verbose_name='\u5c5e\u4e3b\u5206\u7ec4')),
                ('metics', models.CharField(max_length=128, verbose_name='\u6307\u6807')),
                ('user_name', models.CharField(blank=True, default='', max_length=256, verbose_name='\u7528\u6237\u59d3\u540d')),
                ('user_group', models.CharField(blank=True, default='', max_length=256, verbose_name='\u7528\u6237\u5206\u7ec4')),
                ('value', models.PositiveIntegerField(default=0, verbose_name='\u6570\u503c')),
                ('owner_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='contenttypes.ContentType', verbose_name='\u5f52\u7c7b')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='dailylog_records', to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
                'verbose_name': '\u8bb0\u5f55',
                'verbose_name_plural': '\u8bb0\u5f55',
            },
        ),
        migrations.CreateModel(
            name='Stat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('the_date', models.DateField(db_index=True, verbose_name='\u65e5\u671f')),
                ('owner_id', models.PositiveIntegerField(blank=True, db_index=True, null=True, verbose_name='\u5c5e\u4e3b\u7f16\u53f7')),
                ('metics', models.CharField(max_length=128, verbose_name='\u6307\u6807')),
                ('value', models.PositiveIntegerField(default=0, verbose_name='\u6570\u503c')),
                ('user_count', models.PositiveIntegerField(default=0, verbose_name='\u7528\u6237\u6570')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('owner_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='contenttypes.ContentType', verbose_name='\u5f52\u7c7b')),
            ],
            options={
                'verbose_name': '\u7edf\u8ba1',
                'verbose_name_plural': '\u7edf\u8ba1',
            },
        ),
        migrations.AlterUniqueTogether(
            name='stat',
            unique_together=set([('the_date', 'owner_type', 'owner_id', 'metics')]),
        ),
        migrations.AlterUniqueTogether(
            name='record',
            unique_together=set([('the_date', 'owner_type', 'owner_id', 'metics', 'user')]),
        ),
        migrations.AlterUniqueTogether(
            name='dailylog',
            unique_together=set([('the_date', 'user')]),
        ),
    ]