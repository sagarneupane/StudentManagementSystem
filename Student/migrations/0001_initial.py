# Generated by Django 4.0.4 on 2022-05-28 03:40

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_name', models.CharField(max_length=255)),
                ('course_code', models.CharField(max_length=5, unique=True)),
                ('course_description', models.TextField()),
                ('course_url', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='University',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('university_name', models.CharField(max_length=150)),
                ('university_code', models.CharField(max_length=5)),
                ('university_description', models.TextField()),
                ('university_url', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='Stu_Subject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject_name', models.CharField(max_length=150)),
                ('subject_code', models.CharField(max_length=10)),
                ('subject_details', models.TextField()),
                ('full_marks', models.IntegerField(validators=[django.core.validators.MaxValueValidator(101), django.core.validators.MinValueValidator(0)])),
                ('theory_marks', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('theory_pass_marks', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('practical_marks', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('practical_pass_marks', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('semester', models.CharField(choices=[('First Sem', 'First Semster'), ('Second Sem', 'Second Semester'), ('Third Sem', 'Third Semester'), ('Fourth Sem', 'Fourth Semester'), ('Fifth Sem', 'Fifth Semester'), ('Sixth Sem', 'Sixth Semester'), ('Seventh Sem', 'Seventh Semester'), ('Eighth Sem', 'Eighth Semester')], max_length=20)),
                ('course_related', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Student.course')),
            ],
        ),
        migrations.CreateModel(
            name='ModelUniversity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Student.course')),
                ('university', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Student.university')),
            ],
        ),
        migrations.AddField(
            model_name='course',
            name='university_affiliation',
            field=models.ManyToManyField(related_name='university', through='Student.ModelUniversity', to='Student.university'),
        ),
    ]
