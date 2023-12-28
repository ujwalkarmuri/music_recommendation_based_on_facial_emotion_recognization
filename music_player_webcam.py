import time
import cv2
import label_image
import os
import random
import subprocess
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

size = 4
# We load the xml file
classifier = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')
global text
webcam = cv2.VideoCapture(0)  # Using default WebCam connected to the PC.
now = time.time()  # For calculate seconds of video
# here is second of time which taken by emotion recognition system ,you can change it
future = now + 8

print("Get Ready...")


def RunFile(path) -> str:
    if os.name == "nt":
        return os.startfile(path)
    else:
        exit


def getfilesR(path):
    files = []
    for r, d, f in os.walk(path):
        for file in f:
            files.append(os.path.join(r, file))
    return files


while True:
    (rval, im) = webcam.read()
    im = cv2.flip(im, 1, 0)  # Flip to act as a mirror
    # Resize the image to speed up detection
    mini = cv2.resize(im, (int(im.shape[1] / size), int(im.shape[0] / size)))
    # detect MultiScale / faces
    faces = classifier.detectMultiScale(mini)
    # Draw rectangles around each face

    for f in faces:
        (x, y, w, h) = [v * size for v in f]  # Scale the shapesize backup
        sub_face = im[y:y + h, x:x + w]
        # Saving the current image from the webcam for testing.
        FaceFileName = "uj.jpg"
        cv2.imwrite(FaceFileName, sub_face)
        # Getting the Result from the label_image file, i.e., Classification Result.
        text = label_image.main(FaceFileName)
        text = text.title()  # Title Case looks Stunning.
        font = cv2.FONT_HERSHEY_TRIPLEX

        if text == 'Angry':
            cv2.rectangle(im, (x, y), (x + w, y + h), (0, 25, 255), 7)
            cv2.putText(im, text, (x + h, y), font, 1, (0, 25, 255), 2)

        if text == 'Smile':
            cv2.rectangle(im, (x, y), (x + w, y + h), (0, 260, 0), 7)
            cv2.putText(im, text, (x + h, y), font, 1, (0, 260, 0), 2)

        if text == 'Fear':
            cv2.rectangle(im, (x, y), (x + w, y + h), (0, 255, 255), 7)
            cv2.putText(im, text, (x + h, y), font, 1, (0, 255, 255), 2)

        if text == 'Sad':
            cv2.rectangle(im, (x, y), (x + w, y + h), (0, 191, 255), 7)
            cv2.putText(im, text, (x + h, y), font, 1, (0, 191, 255), 2)

        print(text)

    # # Show the image/
    cv2.imshow('Music player with Emotion recognition', im)
    key = cv2.waitKey(10) & 0xff

    if time.time() > future:
        cv2.destroyAllWindows()
        print(text)
        print

        # if text in ["Angry", "Sad", "Fear", "Smile"]:
        #     randomfile = random.choice(os.listdir("Angry"))
        #     file = f"{os.getcwd()}\\{randomfile}"
        #     RunFile(file)
        if text == 'Angry':
            randomfile = random.choice(getfilesR("Angry"))
            print(
                'You are angry !!!! please calm down:) ,I will play song for you :' + randomfile)
            RunFile(randomfile)

        if text == 'Smile':
            randomfile = random.choice(getfilesR("Smile"))
            print('You are smiling :) ,I playing special song for you: ' + randomfile)
            RunFile(randomfile)

        if text == 'Fear':
            randomfile = random.choice(getfilesR("Fear"))
            print('You have fear of something ,I playing song for you: ' + randomfile)
            RunFile(randomfile)

        if text == 'Sad':
            randomfile = random.choice(getfilesR("Sad"))
            print('You are sad,dont worry:) ,I playing song for you: ' + randomfile)
            RunFile(randomfile)
        break

    if key == 27:  # The Esc key
        break
