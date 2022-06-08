from multiprocessing import context
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from attendance_management_system.settings import MEDIA_ROOT
from .models import *
from .forms import *

import face_recognition
import os
import cv2
from uuid import uuid4

KNOWN_FACES_DIR = '/static/images/students/known_images'
UNKNOWN_FACES_DIR = '/static/images/students/unknown_images'
PATH_OF_KNOWN_FACES = os.path.dirname(os.path.realpath(__file__)) + KNOWN_FACES_DIR
PATH_OF_UNKNOWN_FACES = os.path.dirname(os.path.realpath(__file__)) + UNKNOWN_FACES_DIR
TOLERANCE = 0.6
FRAME_THICHNESS = 3
FONT_THICKNESS =2
MODEL = "cnn" #hog 


# Create your views here.

def index(request):
    return render(request, 'project/login.html')

def dashboard(request):
    departments = Department.objects.all()
    context = {
        'departments': departments
    }
    return render(request, 'project/dashboard.html', context)

def logout(request):
    logout(request)
    return redirect('login')

def take_attendance(request, course_id, course_topic_id):
    # course = Course.objects.get(id = course_id)
    # all_students_in_course = course.student_set.all()

    # this is thesame as the code above but in one line.
    all_students_in_course = Student.objects.filter(courses__id = course_id)
    
    context = {
        'students': all_students_in_course,
    }

    return render(request, 'project/take_attendance.html', context)

def attendance(request, course_id, course_topic_id):
    all_students_in_course = Student.objects.filter(courses__id = course_id)
    
    context = {
        'students': all_students_in_course,
    }


    return render(request, 'project/attendance.html', context)

def courses(request):
    courses = Course.objects.all()
    context = {
        'courses': courses
    }
    return render(request, 'project/courses.html', context)

def course_topic(request, pk):
    course = Course.objects.get(id=pk)
    course_topics = course.coursetopic_set.all()
    student_taking_course = Student.objects.filter(courses__id=course.id)
    
    context = {
        'course': course,
        'course_topics': course_topics,
        'total_students_taking_course' : student_taking_course.count()
    }

    return render(request, 'project/course_topics.html', context)

def students(request):
    students = Student.objects.all()
    context = {
        'students': students
    }

    return render(request, 'project/students.html', context)

def view_student(request, pk):
    student = Student.objects.get(id=pk)

    context = {
        "student":student
    }

    return render(request, 'project/view_student.html', context)

def add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            student = form.save()
            return redirect(f'/student/{student.id}')
    else:
        form = StudentForm()
        context = {
            'form': form
        }
    return render(request, 'project/forms/student_form.html', context)

def face_count(imagelocation):
    image = face_recognition.load_image_file(imagelocation)
    face_locations = face_recognition.face_locations(image)

    return len(face_locations)


def add_student_image(request, pk):
    context = {
        'id': pk
    }


    if request.method == 'POST':
        imgs = request.FILES.getlist('student_images')
        errors = {
            'no_image_in_picture': [],
            'more_that_one_image': [],
        }
        
        # img_extension = os.path.splitext(imgs[0].name)[1]

        student = Student.objects.get(id=pk)

        user_folder = MEDIA_ROOT + "/students/"+ student.firstname + "-" +str(student.id)

        if not os.path.exists(user_folder):
            os.mkdir(user_folder)


        for img in imgs:
            img_count = face_count(img)

            if img_count == 0:
                errors['no_image_in_picture'].append(img)
                continue
            
            elif img_count > 1:
                errors['more_that_one_image'].append(img)
                continue

            img_extension = os.path.splitext(img.name)[1]
            id = str(uuid4())
            img_save_path = f"{user_folder}/{id}{img_extension}"
            
            # while os.path.exists(img_save_path):
            #     i = i+1
            #     img_save_path = f"{user_folder}/{i}{img_extension}"
            
            with open(img_save_path, 'wb+') as f:
                for chunk in img.chunks():
                    f.write(chunk)
            image_path = f"students/{student.firstname}-{str(student.id)}/{id}{img_extension}"
            image = StudentImages(student=student, picture=image_path)
            image.save()

        if len(errors['no_image_in_picture']) + len(errors['more_that_one_image']) > 0 :
            messages.info(request, "Error uploading user image")
            if len(errors['no_image_in_picture']) != 0:
                messages.info(request,f"images with no user picture: {len(errors['no_image_in_picture'])}")
            if len(errors['more_that_one_image']) != 0:
                messages.info(request,f"images with more that one picture: {len(errors['more_that_one_image'])}")
        else :
            messages.info(request, "Successfully uploaded images")

        #messages.info(request, f"Total errors uploading image: {len(errors['no_image_in_picture']) + len(errors['more_that_one_image'])} \n images with no user picture: {len(errors['no_image_in_picture'])} \n images with more that one picture: {len(errors['more_that_one_image'])}" )
        return redirect(f'/student/{student.id}')
        
        
    return render(request, 'project/forms/add_student_image.html',context)

def delete_student_image(request, pk):
    if request.method == "POST":
        student = Student.objects.get(id=pk)
        student_image = StudentImages.objects.get(id=request.POST.get('image_id'))
        
        file_location = request.POST.get('image_location')

        full_path = os.path.join(MEDIA_ROOT,file_location)
        
        os.chmod(full_path, 0o777)
        if os.path.exists(full_path):
            os.remove(full_path)
            student_image.delete()
        else:
            print("Could not delete file")
        return redirect(f'/student/{student.id}')
        
    


def face_recog(request):
    print(os.listdir(os.path.dirname(os.path.realpath(__file__)) + KNOWN_FACES_DIR))
    known_faces = []
    known_names = []

    for name in os.listdir(PATH_OF_KNOWN_FACES):
        for filename in os.listdir(f"{PATH_OF_KNOWN_FACES}/{name}"):
            image = face_recognition.load_image_file(f"{PATH_OF_KNOWN_FACES}/{name}/{filename}")
            print(f"{PATH_OF_KNOWN_FACES}/{name}/{filename}")
            encoding = face_recognition.face_encodings(image)[0]
            known_faces.append(encoding)
            known_names.append(name)
    
    print("Processing unkwonw faces")

    for filename in os.listdir(PATH_OF_UNKNOWN_FACES):
        image = face_recognition.load_image_file(f"{PATH_OF_UNKNOWN_FACES}/{filename}")
        # locations = face_recognition.face_locations(image, model=MODEL)
        locations = face_recognition.face_locations(image)

        encoding = face_recognition.face_encodings(image, locations)

        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        for face_encoding, face_location in zip(encoding, locations):
            results = face_recognition.compare_faces(known_faces, face_encoding, TOLERANCE)

            match = None

            if True in results:
               match =  known_names[results.index(True)]
               print(f"Match found: {match}")

               top_left = (face_location[3], face_location[0])
               bottom_right =(face_location[1], face_location[2])

               color = [0, 255, 0]

               cv2.rectangle(image, top_left, bottom_right, color, FRAME_THICHNESS)

               top_left = (face_location[3], face_location[2])
               bottom_right =(face_location[1], face_location[2]+22)

               cv2.rectangle(image, top_left, bottom_right, color, cv2.FILLED)
               cv2.putText(image, match, (face_location[3]+10, face_location[2]+15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200,200,200),FONT_THICKNESS) 

        cv2.imshow(filename, image)
        cv2.waitKey(1000)
        #cv2.destroyWindow(filename)



    print("Hello world")
    return HttpResponse()

def face_recog2(request):
    video = cv2.VideoCapture(2)
    known_faces = []
    known_names = []

    for name in os.listdir(PATH_OF_KNOWN_FACES):
        for filename in os.listdir(f"{PATH_OF_KNOWN_FACES}/{name}"):
            image = face_recognition.load_image_file(f"{PATH_OF_KNOWN_FACES}/{name}/{filename}")
            print(f"{PATH_OF_KNOWN_FACES}/{name}/{filename}")
            encoding = face_recognition.face_encodings(image)[0]
            known_faces.append(encoding)
            known_names.append(name)
    
    print("Processing unknown faces")
    while True:
        # image = face_recognition.load_image_file(f"{PATH_OF_UNKNOWN_FACES}/{filename}")
        # locations = face_recognition.face_locations(image, model=MODEL)

        ret, image = video.read()
        locations = face_recognition.face_locations(image)

        encoding = face_recognition.face_encodings(image, locations)

        # image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)


        for face_encoding, face_location in zip(encoding, locations):
            results = face_recognition.compare_faces(known_faces, face_encoding, TOLERANCE)

            match = None

            if True in results:
               match =  known_names[results.index(True)]
               print(f"Match found: {match}")

               top_left = (face_location[3], face_location[0])
               bottom_right =(face_location[1], face_location[2])

               color = [0, 255, 0]

               cv2.rectangle(image, top_left, bottom_right, color, FRAME_THICHNESS)

               top_left = (face_location[3], face_location[2])
               bottom_right =(face_location[1], face_location[2]+22)

               cv2.rectangle(image, top_left, bottom_right, color, cv2.FILLED)
               cv2.putText(image, match, (face_location[3]+10, face_location[2]+15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200,200,200),FONT_THICKNESS) 

        cv2.imshow(filename, image)
        #cv2.waitKey(1000)
        #cv2.destroyWindow(filename)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break


    print("Hello world")
    return HttpResponse()

def face_recog3(request):

    known_face_encodings = [
        
    ]
    known_face_names = [
        
    ]

    path_to_unknown_faces =  MEDIA_ROOT + "/students/"

    # This is a demo of running face recognition on live video from your webcam.
    video_capture = cv2.VideoCapture(0)

    # change the name of the video frame
    cv2.namedWindow("Face Recognition")

    # Load a sample picture and learn how to recognize it.
    for name in os.listdir(path_to_unknown_faces):
        for filename in os.listdir(f"{path_to_unknown_faces}/{name}"):
            image = face_recognition.load_image_file(f"{path_to_unknown_faces}/{name}/{filename}")
            encoding = face_recognition.face_encodings(image)[0]
            known_face_encodings.append(encoding)
            known_face_names.append(name)

    

    # Initialize some variables
    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True

    while True:
        # Grab a single frame of video
        ret, frame = video_capture.read()

        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]

        # Only process every other frame of video to save time
        if process_this_frame:
            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(
                rgb_small_frame, face_locations)

            face_names = []
            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(
                    known_face_encodings, face_encoding, tolerance=0.55)
                name = "Unknown"

                # # If a match was found in known_face_encodings, just use the first one.
                if True in matches:
                    first_match_index = matches.index(True)
                    name = known_face_names[first_match_index]

                    # video_capture.release()
                    # cv2.destroyAllWindows()

                    # return True

                face_names.append(name)

        process_this_frame = not process_this_frame

        # Display the results
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35),
                          (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6),
                        font, 1.0, (255, 255, 255), 1)

        # Display the resulting image
        cv2.imshow('Face Recognition', frame)

        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release handle to the webcam
    video_capture.release()
    cv2.destroyAllWindows()

    print("Hello world")
    return HttpResponse()
