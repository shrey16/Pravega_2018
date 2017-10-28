# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-23 19:09
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import registrations.models


class Migration(migrations.Migration):

    dependencies = [
        ('registrations', '0002_auto_20171022_0031'),
    ]

    operations = [
        migrations.CreateModel(
            name='LasyaParticipant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contact', models.CharField(blank=True, max_length=15, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{13}$|^$')])),
                ('email', models.EmailField(max_length=254)),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='LasyaRegistration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('institution', models.CharField(blank=True, max_length=200)),
                ('email', models.EmailField(max_length=254)),
                ('contact', models.CharField(blank=True, max_length=15, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{13}$|^$')])),
                ('prelims_video', models.FileField(max_length=255, upload_to=registrations.models.LasyaRegistration.upload_video_path, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['mp4', '3gp', 'mkv'])])),
            ],
        ),
        migrations.AlterField(
            model_name='bobparticipant',
            name='contact',
            field=models.CharField(blank=True, max_length=15, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{13}$|^$')]),
        ),
        migrations.AlterField(
            model_name='prosceniumstreetplayregistration',
            name='contact1',
            field=models.CharField(blank=True, max_length=15, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{13}$|^$')]),
        ),
        migrations.AlterField(
            model_name='prosceniumstreetplayregistration',
            name='contact2',
            field=models.CharField(blank=True, max_length=15, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{13}$|^$')]),
        ),
        migrations.AlterField(
            model_name='prosceniumtheatreregistration',
            name='contact1',
            field=models.CharField(blank=True, max_length=15, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{13}$|^$')]),
        ),
        migrations.AlterField(
            model_name='prosceniumtheatreregistration',
            name='contact2',
            field=models.CharField(blank=True, max_length=15, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{13}$|^$')]),
        ),
        migrations.AddField(
            model_name='lasyaparticipant',
            name='registration_entry',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='registrations.LasyaRegistration'),
        ),
    ]