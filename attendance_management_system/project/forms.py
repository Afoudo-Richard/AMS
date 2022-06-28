from django.forms import ModelForm
from .models import *

class StudentForm(ModelForm):
    class Meta:
        model = Student
        fields = '__all__'


class DepartmentForm(ModelForm):
    class Meta:
        model = Department
        fields = '__all__'

class CourseForm(ModelForm):
    class Meta:
        model = Course
        fields = '__all__'

class CourseTopicForm(ModelForm):
    class Meta:
        model = CourseTopic
        fields = '__all__'

