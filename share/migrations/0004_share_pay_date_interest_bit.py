# Generated by Django 3.0.4 on 2020-04-21 08:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('share', '0003_auto_20200421_1343'),
    ]

    operations = [
        migrations.AddField(
            model_name='share_pay_date',
            name='interest_bit',
            field=models.IntegerField(default=0),
        ),
    ]
