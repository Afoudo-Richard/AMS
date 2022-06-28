from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('user_dashboard/', views.user_dashboard, name="user_dashboard"),
    path('departments/', views.departments, name="departments"),
    path('department/add/', views.add_department, name="add_department"),
    path('students/', views.students, name="students"),
    path('student/<str:pk>/', views.view_student, name="view_student"),
    path('add_student/', views.add_student, name="add_student"),
    path('add_student_images/<str:pk>', views.add_student_image, name="add_student_images"),
    path('delete_student_image/<str:pk>', views.delete_student_image, name="delete_student_image"),
    path('take_attendance/<str:course_id>/<str:course_topic_id>', views.take_attendance, name="attendance"),
    path('take_attendance/<str:course_id>/<str:course_topic_id>/use_face_recognition', views.use_face_recognition, name="use_face_recognition"),
    path('courses/', views.courses, name="courses"),
    path('view_attendance/<str:course_topic_id>', views.view_attendance, name="view_attendance"),
    path('courses/add/', views.add_courses, name="add_courses"),
    path('course_topics/<str:pk>', views.course_topic, name="course_topics"),
    path('course_topics/<str:pk>/add/', views.add_course_topic, name="add_course_topic"),
]