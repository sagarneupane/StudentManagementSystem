# Generated by Django 4.0.4 on 2022-06-12 10:26

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Student', '0020_correctanswer'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignment',
            name='submission_deadline',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
