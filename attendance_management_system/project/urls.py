from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='login'),
    path('logout/', views.logout, name='logout'),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('students/', views.students, name="students"),
    path('student/<str:pk>/', views.view_student, name="view_student"),
    path('add_student/', views.add_student, name="add_student"),
    path('add_student_images/<str:pk>', views.add_student_image, name="add_student_images"),
    path('delete_student_image/<str:pk>', views.delete_student_image, name="delete_student_image"),
    path('take_attendance/<str:course_id>/<str:course_topic_id>', views.take_attendance, name="attendance"),
    path('courses/', views.courses, name="courses"),
    path('course_topics/<str:pk>', views.course_topic, name="course_topics"),
    path('face_rec/', views.face_recog),
    path('face_rec2/', views.face_recog2),
    path('face_rec3/', views.face_recog3),
]