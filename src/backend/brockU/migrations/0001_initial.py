# Generated by Django 3.2.13 on 2022-04-15 21:59

import brockU.models
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('code', models.CharField(max_length=9, validators=[brockU.models.validate_course_code])),
                ('name', models.CharField(max_length=64)),
                ('description', models.TextField(blank=True)),
                ('format', models.TextField(blank=True)),
                ('prerequesites', models.TextField(blank=True)),
                ('exclusions', models.TextField(blank=True)),
                ('restrictions', models.TextField(blank=True)),
                ('notes', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Instructor',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=25)),
                ('last_name', models.CharField(max_length=25)),
            ],
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('code', models.CharField(max_length=4, unique=True)),
                ('name', models.CharField(max_length=64)),
                ('url', models.URLField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='CourseOffering',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('delivery_type', models.CharField(choices=[('ASY', 'Asynchronous Online'), ('BLD', 'Blended'), ('CLI', 'Practicum (Clinic)'), ('FLD', 'Field Course'), ('HYF', 'Hyflex'), ('IFT', 'International Field Experience'), ('INT', 'Internship'), ('LAB', 'Labortory'), ('LEC', 'Lecture'), ('ONM', 'Online Mixed'), ('PRO', 'Project'), ('SEM', 'Seminar'), ('SYN', 'Synchronus'), ('TUT', 'Tutorial')], default='LEC', max_length=3)),
                ('duration', models.CharField(max_length=3)),
                ('section', models.IntegerField()),
                ('location', models.CharField(blank=True, max_length=64)),
                ('start_date', models.DateField(null=True)),
                ('end_date', models.DateField(null=True)),
                ('schedule', models.JSONField(blank=True)),
                ('course_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='brockU.course')),
                ('instructor_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='brockU.instructor')),
            ],
        ),
    ]
