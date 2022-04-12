from django.contrib import admin
from import_export import fields, resources
from import_export.admin import ImportExportModelAdmin
from import_export.widgets import ForeignKeyWidget, JSONWidget
from .models import Subject, Course, CourseComponent, Instructor

# Register your models here.
class SubjectResource(resources.ModelResource):
    class Meta:
        model = Subject

class SubjectAdmin(ImportExportModelAdmin):
    resource_class = SubjectResource

admin.site.register(Subject, SubjectAdmin)

class InstructorResource(resources.ModelResource):
    class Meta:
        model = Instructor

class InstructorAdmin(ImportExportModelAdmin):
    resource_class = InstructorResource

admin.site.register(Instructor, InstructorAdmin)

class CourseResource(resources.ModelResource):
    class Meta:
        model = Course

class CourseAdmin(ImportExportModelAdmin):
    resource_class = CourseResource

admin.site.register(Course, CourseAdmin)

class CourseComponentResource(resources.ModelResource):
    course_id = fields.Field(
        column_name='code',
        attribute='code',
        widget=ForeignKeyWidget(Course, field='code')
    )
    schedule = fields.Field(
        column_name='schedule',
        attribute='schedule',
        widget=JSONWidget()
    )
    class Meta:
        model = CourseComponent

class CourseComponentAdmin(ImportExportModelAdmin):
    resource_class = CourseComponentResource

admin.site.register(CourseComponent, CourseComponentAdmin)