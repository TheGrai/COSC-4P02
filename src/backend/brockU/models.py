import uuid
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

class Subject(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=4, unique=True)
    name = models.CharField(max_length=64)
    url = models.URLField(blank=True)
    description = models.TextField(blank=True)

class Instructor(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)

def validate_course_code(value):
    course_code = value.split()
    credit_value = ['F', 'N', 'P', 'Q', 'Y']
    try:
        subject = Subject.objects.get(code = course_code[0])
        creditIndex = credit_value.index(course_code[1][1])
    except Subject.DoesNotExist:
        raise ValidationError(
            _('%(value)s is not a valid Subject.'),
            params = {'value': course_code[0]},
        )
    except:
        raise ValidationError(
            _('%(value)s is not a valid Course Code.'),
            params = {'value': value},
        )

class Course(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=9, validators=[validate_course_code])
    name = models.CharField(max_length=64)
    description = models.TextField(blank=True)
    format = models.TextField(blank=True)
    prerequesites = models.TextField(blank=True)
    exclusions = models.TextField(blank=True)
    restrictions = models.TextField(blank=True)
    notes = models.TextField(blank=True)

# Create your models here.
class CourseOffering(models.Model):
    class DeliveryType(models.TextChoices):
        ASYNCHRONOUS = 'ASY', _('Asynchronous Online')
        BLENDED = 'BLD', _('Blended')
        PRACTICUM = 'CLI', _('Practicum (Clinic)')
        FIELD_COURSE = 'FLD', _('Field Course')
        HYFLEX = 'HYF', _('Hyflex')
        INTERNATIONAL_FIELD_EXPERIENCE = 'IFT', _('International Field Experience')
        INTERNSHIP = 'INT', _('Internship')
        LABORATORY = 'LAB', _('Labortory')
        LECTURE = 'LEC', _('Lecture')
        ONLINE_MIXED = 'ONM', _('Online Mixed')
        PROJECT = 'PRO', _('Project')
        SEMINAR = 'SEM', _('Seminar')
        SYNCHRONOUS = 'SYN', _('Synchronus')
        TUTORIAL = 'TUT', _('Tutorial')

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    course_id = models.ForeignKey('Course', on_delete=models.CASCADE)
    delivery_type = models.CharField(choices=DeliveryType.choices, default=DeliveryType.LECTURE, max_length=3)
    instructor_id = models.ForeignKey('Instructor', null=True, on_delete=models.SET_NULL)
    duration = models.CharField(max_length=3)
    section = models.IntegerField()
    location = models.CharField(max_length=64, blank=True)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    schedule = models.JSONField(blank=True)

class Exam(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    course = models.ForeignKey('Course', on_delete=models.CASCADE)
    section = models.IntegerField()
    date = models.DateField(null=True)
    time = models.CharField(max_length=5, blank=True)
    location = models.CharField(max_length=64, blank=True)