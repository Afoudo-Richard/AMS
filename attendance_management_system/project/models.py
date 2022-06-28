import email
import profile
from unicodedata import name
from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class University(models.Model):
    name = models.CharField(max_length=300)
    email = models.CharField(max_length=200)
    location = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.name

class Department(models.Model):
    name = models.CharField(max_length=200)
    short_name = models.CharField(max_length=200, unique=True)

    def total_course(self):
        return self.course_set.all().count()
    def total_student(self):
        return self.student_set.all().count()

    def __str__(self) -> str:
        return self.name

class Course(models.Model):
    department = models.ForeignKey(Department, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=200)

    def total_students(self):
        return self.student_set.all().count()
        
    def total_course_topics(self):
        return self.coursetopic_set.all().count()

    def __str__(self) -> str:
        return self.name
class CourseTopic(models.Model):
    course = models.ForeignKey(Course, null=True, on_delete=models.SET_NULL)
    topic = models.CharField(max_length=200)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    comment = models.CharField(max_length=300, null=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.topic

class Student(models.Model):
    SEX = (
        ("Male", "Male"),
        ('Female', "Female"),
    )
    #user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    firstname = models.CharField(max_length=200)
    lastname = models.CharField(max_length=200)
    phone = models.CharField(max_length=200)
    sex = models.CharField(max_length=200, choices=SEX)
    email = models.CharField(max_length=200)
    date_created = models.DateTimeField(auto_now_add=True)
    profile_pic = models.ImageField(null=True, blank=True, upload_to='students')
    courses = models.ManyToManyField(Course)


    def all_student_images(self):
        return self.studentimages_set.all()


    def __str__(self) -> str:
        return self.firstname

class StudentImages(models.Model):
    picture = models.CharField(max_length=200)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

class Attendance(models.Model):
    course= models.ForeignKey(Course, null=True ,on_delete=models.SET_NULL)
    course_topic = models.ForeignKey(CourseTopic, null=True ,on_delete=models.SET_NULL)
    student = models.ForeignKey(Student, null=True, on_delete=models.SET_NULL)
    date_created = models.DateTimeField(auto_now_add=True)

    
    