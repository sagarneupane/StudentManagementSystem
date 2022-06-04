# Generated by Django 4.0.4 on 2022-06-03 02:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Student', '0013_delete_submitassignment'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubmitAssignment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('submitted_date', models.DateField(auto_now_add=True)),
                ('submitted_time', models.TimeField(auto_now_add=True)),
                ('submitted_data', models.FileField(upload_to='assignmentsubmitted/')),
                ('edited', models.IntegerField(default=0)),
                ('check_status', models.BooleanField(default=False)),
                ('assignment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Student.assignment')),
                ('submitted_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='AssignmentCheck',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('checked_date', models.DateTimeField(auto_now_add=True)),
                ('correct_status', models.BooleanField()),
                ('assignment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Student.submitassignment')),
            ],
        ),
    ]