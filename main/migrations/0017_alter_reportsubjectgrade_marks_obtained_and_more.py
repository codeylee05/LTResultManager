# Generated by Django 4.2.4 on 2025-06-22 11:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0016_alter_reportsubjectgrade_class_average_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reportsubjectgrade',
            name='marks_obtained',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='reportsubjectgrade',
            name='total_marks',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
