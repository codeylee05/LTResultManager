# Generated by Django 4.2.4 on 2025-04-11 16:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subjects',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('grade', models.CharField(choices=[('US', 'US'), ('IGCSE_1', 'IGCSE 1'), ('IGCSE_2', 'IGCSE 2'), ('AS_1', 'AS Level 1'), ('AS_2', 'AS Level 2'), ('GED', 'GED')], max_length=10)),
                ('subjects', models.ManyToManyField(related_name='subject_teachers', to='main.subjects')),
            ],
        ),
        migrations.AddField(
            model_name='subjects',
            name='teacher',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='teacher_subjects', to='main.teacher'),
        ),
        migrations.AddField(
            model_name='student',
            name='class_teacher',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='class_students', to='main.teacher'),
        ),
        migrations.AddField(
            model_name='student',
            name='subjects',
            field=models.ManyToManyField(related_name='subject_students', to='main.subjects'),
        ),
    ]
