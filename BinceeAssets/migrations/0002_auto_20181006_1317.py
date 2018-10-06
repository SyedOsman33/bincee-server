# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-10-06 08:17
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('BinceeAssets', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RealTimeLocationData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(db_index=True)),
                ('latitude', models.DecimalField(blank=True, decimal_places=10, max_digits=20, null=True)),
                ('longitude', models.DecimalField(blank=True, decimal_places=10, max_digits=20, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='binceeentities',
            name='created_datetime',
            field=models.DateTimeField(auto_now_add=True, db_index=True, default=datetime.datetime(2018, 10, 6, 8, 17, 6, 416806, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='binceeentities',
            name='description',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='binceeentities',
            name='dob',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='binceeentities',
            name='modified_by',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='binceeentities',
            name='modified_datetime',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='binceeentities',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='static/media/'),
        ),
        migrations.AddField(
            model_name='realtimelocationdata',
            name='bince_entity',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='location_data_entity_id', to='BinceeAssets.BinceeEntities'),
        ),
    ]