# Generated by Django 4.2.4 on 2025-07-03 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0022_alter_termreport_days_absent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='termreport',
            name='days_absent',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
