# Generated by Django 4.0.4 on 2022-06-12 02:45

import Student.formatchecker
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Student', '0019_delete_correctanswer'),
    ]

    operations = [
        migrations.CreateModel(
            name='CorrectAnswer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('correct_answer', Student.formatchecker.ContentRestrictiononFileField(blank=True, null=True, upload_to='answers/')),
                ('assignment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Student.assignment')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='Student.stu_subject')),
            ],
        ),
    ]
