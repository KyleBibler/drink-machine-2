# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import drink_maker.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DrinkRequest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time_stamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Liquid',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
                ('density', models.DecimalField(default=1.0, max_digits=6, decimal_places=2)),
            ],
        ),
        migrations.CreateModel(
            name='LiquidAmount',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('volume', drink_maker.models.IntegerRangeField(default=45)),
                ('liquid', models.ForeignKey(to='drink_maker.Liquid')),
            ],
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
                ('components', models.ManyToManyField(to='drink_maker.Liquid', through='drink_maker.LiquidAmount')),
            ],
        ),
        migrations.CreateModel(
            name='Valve',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('servo_pin', models.IntegerField(unique=True)),
                ('angle_closed', models.IntegerField()),
                ('angle_open', models.IntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='liquidamount',
            name='recipe',
            field=models.ForeignKey(to='drink_maker.Recipe'),
        ),
        migrations.AddField(
            model_name='liquid',
            name='valve',
            field=models.OneToOneField(null=True, blank=True, to='drink_maker.Valve'),
        ),
        migrations.AddField(
            model_name='drinkrequest',
            name='recipe',
            field=models.ForeignKey(to='drink_maker.Recipe'),
        ),
    ]
