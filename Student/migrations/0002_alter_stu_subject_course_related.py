# Generated by Django 4.0.4 on 2022-05-28 04:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Student', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stu_subject',
            name='course_related',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Student.modeluniversity'),
        ),
    ]
