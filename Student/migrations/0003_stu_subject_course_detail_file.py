# Generated by Django 4.0.4 on 2022-05-28 04:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Student', '0002_alter_stu_subject_course_related'),
    ]

    operations = [
        migrations.AddField(
            model_name='stu_subject',
            name='course_detail_file',
            field=models.FileField(default='none', upload_to='files/'),
        ),
    ]
