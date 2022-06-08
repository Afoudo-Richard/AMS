from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(University)
admin.site.register(Department)
admin.site.register(Course)
admin.site.register(CourseTopic)
admin.site.register(Student)
admin.site.register(Attendance)
admin.site.register(StudentImages)