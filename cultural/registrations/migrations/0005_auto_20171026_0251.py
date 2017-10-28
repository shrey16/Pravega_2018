# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-25 21:21
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import registrations.models


class Migration(migrations.Migration):

    dependencies = [
        ('registrations', '0004_auto_20171024_0055'),
    ]

    operations = [
        migrations.CreateModel(
            name='SInECParticipant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('institution', models.CharField(max_length=200)),
                ('name', models.CharField(max_length=200)),
                ('city', models.CharField(max_length=200)),
                ('student_type', models.CharField(choices=[('ug', 'UG'), ('masters', 'Masters'), ('phd', 'Ph.D.'), ('postdoc', 'Post Doc')], default='ug', max_length=7)),
            ],
        ),
        migrations.CreateModel(
            name='SInECRegistration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('team_name', models.CharField(max_length=200)),
                ('project_name', models.CharField(max_length=200)),
                ('email', models.EmailField(max_length=254)),
                ('contact', models.CharField(blank=True, max_length=15, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+91----------'. 12 digits allowed.", regex='^\\+?1?\\d{12}$|^$')])),
                ('address', models.CharField(max_length=400)),
                ('project_abstract', models.TextField()),
                ('project_field', models.CharField(max_length=200)),
                ('project_patented', models.BooleanField()),
                ('registered_company', models.BooleanField()),
                ('privacy_preference', models.CharField(choices=[('public_awareness', 'I would like my project to be presented and evaluated in a closed room and would not like to display it to the general public.'), ('closed_room_evaluation', 'I would like to display my project to the general public to improve awareness about my project.')], default='closed_room_evaluation', max_length=22)),
                ('project_file', models.FileField(max_length=255, upload_to=registrations.models.SInECRegistration.upload_video_path)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='sinecregistration',
            unique_together=set([('team_name', 'project_name')]),
        ),
        migrations.AddField(
            model_name='sinecparticipant',
            name='registration_entry',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='registrations.SInECRegistration'),
        ),
    ]