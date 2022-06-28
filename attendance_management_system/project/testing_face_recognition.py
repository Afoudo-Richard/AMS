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
