# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-12-20 06:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('influencers', '0027_auto_20161216_2223'),
    ]

    operations = [
        migrations.AlterField(
            model_name='noisemakerprofile',
            name='bank_name',
            field=models.CharField(choices=[('Access Bank Plc', 'Access Bank Plc'), ('Diamond Bank Limited', 'Diamond Bank Limited'), ('Ecobank Nigeria Plc', 'Ecobank Nigeria Plc'), ('Fidelity Bank Plc', 'Fidelity Bank Plc'), ('First Bank of Nigeria Plc', 'First Bank of Nigeria Plc'), ('First City Monument Bank Ltd', 'First City Monument Bank Ltd'), ('Guaranty Trust Bank Plc', 'Guaranty Trust Bank Plc'), ('StanbicIBTC Bank', 'StanbicIBTC Bank'), ('Skye Bank', 'Skye Bank'), ('Standard Chartered Bank Nigeria Ltd', 'Standard Chartered Bank Nigeria Ltd'), ('Sterling Bank Plc', 'Sterling Bank Plc'), ('Union Bank of Nigeria Plc', 'Union Bank of Nigeria Plc'), ('United Bank for Africa Plc', 'United Bank for Africa Plc'), ('Unity Bank', 'Unity Bank'), ('Wema Bank Plc', 'Wema Bank Plc'), ('Zenith International Bank Ltd', 'Zenith International Bank Ltd')], default=0, max_length=250),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='noisemakerprofile',
            name='preferences',
            field=models.CharField(default=3, max_length=6500),
            preserve_default=False,
        ),
    ]