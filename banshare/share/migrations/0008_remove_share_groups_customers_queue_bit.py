# Generated by Django 3.0.4 on 2020-04-22 06:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('share', '0007_auto_20200422_1020'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='share_groups_customers',
            name='queue_bit',
        ),
    ]