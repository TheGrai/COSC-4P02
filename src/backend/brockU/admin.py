from django.contrib import admin
from import_export import fields, resources
from import_export.admin import ImportExportModelAdmin
from import_export.widgets import ForeignKeyWidget, JSONWidget
from .models import Subject, Course, CourseOffering, Instructor

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

class CourseOfferingResource(resources.ModelResource):
    def before_import_row(self, row, row_number=None, **kwargs):
        first_name = row["instructor_first_name"]
        last_name = row["instructor_last_name"]
        instructorQuery =  Instructor.objects.filter(first_name=first_name, last_name=last_name)
        if instructorQuery:
            instructor_id = instructorQuery[0].id
            row['instructor_id'] = instructor_id

    course_id = fields.Field(
        column_name='code',
        attribute='course_id',
        widget=ForeignKeyWidget(Course, field='code')
    )
    schedule = fields.Field(
        column_name='schedule',
        attribute='schedule',
        widget=JSONWidget()
    )
    class Meta:
        model = CourseOffering
        exclude = ('code', )

class CourseComponentAdmin(ImportExportModelAdmin):
    resource_class = CourseOfferingResource

admin.site.register(CourseOffering, CourseComponentAdmin)