import cv2 as cv
import os
import pygifsicle
from pygifsicle import optimize
import time
import imutils
import keyboard
from colorama import Fore, Back, Style
from rembg.bg import remove
import numpy as np
import io
import imageio
from PIL import Image
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True


nume_rembg = 1

def setVid():
    vid=cv.VideoCapture('http://192.168.0.3:8080/video')
    vid.set(cv.CAP_PROP_BUFFERSIZE, 2)
    livefeed(vid)


def poza():
    os.system("adb shell input keyevent 224")
    time.sleep(1)
 
     # Unlock the screen (The premise needs to turn off the mobile phone login password in the settings)
    os.system("adb shell input keyevent 82")
    time.sleep(1)
 
     # Start camera
    os.system("adb shell am start -a android.media.action.STILL_IMAGE_CAMERA")
    time.sleep(3) #Leave more time to auto focus
 
     # camera key to take pictures
    os.system("adb shell input keyevent 80") #focus picture
    time.sleep(1)


     # Luam ultima poza facuta
    myfilename = os.popen("adb shell ls -t /storage/emulated/0/DCIM/Camera/").read()
    print(myfilename)
    print("--")
    sep="\n"   
    myfilename=myfilename.split(sep,1)[0] #trim la myfile extrage toate numele de fisiere din folder
    print(myfilename)

    print("--")
    time.sleep(1)
 
     # doscarca poza
    pentrudelete="/storage/emulated/0/DCIM/Camera/"+str(myfilename)
    adbcode = "adb pull /storage/emulated/0/DCIM/Camera/"+str(myfilename)+" AlbumPoze"
    os.system(adbcode)
    time.sleep(1)
 
     # back key to temporarily back the camera
    os.system("adb shell input keyevent 4")
    time.sleep(1)

    deletepicture="adb shell rm -f "+pentrudelete
    print(deletepicture)
    os.system(deletepicture)
    time.sleep(3)
 
     # Power key black screen
    os.system("adb shell input keyevent 26")
    #return myfilename
    show_edit(myfilename)
    setVid()

def show_edit(nume): 
    img=cv.imread("AlbumPoze/"+nume)
    scale_percent=20
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dsize = (width, height)
    imgs=cv.resize(img,dsize,interpolation= cv.INTER_LINEAR)
    cv.imshow("image",imgs)
    cv.waitKey(1)
    rembg(nume)

def rembg(file_name):
    global nume_rembg
    input_path="AlbumPoze/"+file_name
    file_name=str(nume_rembg)+".jpg"
    output_path="rembg/"+file_name

    f = np.fromfile(input_path)
    result = remove(f)
    img = Image.open(io.BytesIO(result)).convert("RGBA") ## RGBA pentru transparenta, imagini png

    width=img.width
    height=img.height
    image = Image.new('RGB', size=(width, height), color=(255, 255, 255))
    image.paste(img, (0, 0), mask=img)
    img=image
    img.save(output_path)
    print (Fore.GREEN + "Coversie Reusita")
    nume_rembg=nume_rembg+1

    image=cv.imread("rembg/"+file_name)
    scale_percent=20
    width = int(image.shape[1] * scale_percent / 100)
    height = int(image.shape[0] * scale_percent / 100)
    dsize = (width, height)
    imgs=cv.resize(image,dsize,interpolation= cv.INTER_LINEAR)

    cv.imshow("image rembg",imgs)
    cv.waitKey(1)

    setVid()

def create_gif():
    print("Saving GIF in progress")
    gif= []
    directory= os.listdir("rembg")
    for x in directory:
        file_path="rembg/"+x
        gif.append(imageio.imread(file_path))
    imageio.mimsave("gifs/test.gif",gif,duration=0.2)
    ##optimize("gifs/test.gif") de rezolvat
    print("succes?")

    



def livefeed(vid):
    while(True):
      
        # Capture the video frame
        # by frame
        ret, frame = vid.read()
        if ret:
            scale_percentw=60
            scale_percenth=40
            width = int(frame.shape[1] * scale_percentw / 100)
            height = int(frame.shape[0] * scale_percenth / 100)
            dsize = (width, height)
            frame=cv.resize(frame,dsize,interpolation= cv.INTER_LINEAR)

            # Display the resulting frame
            cv.imshow('frame', frame)

            if keyboard.is_pressed("p"):
               poza()

            if keyboard.is_pressed("g"):
               create_gif()
            if keyboard.is_pressed("q"):
               vid.release()
               cv.destroyAllWindows()
               break

            if cv.waitKey(1) & 0xFF == ord('q'):
                break
        else:
                print("Nu exista video")
                print("Apasa T pentru a incerca inca o data")
                vid.release()
                cv.destroyAllWindows()
                while(True):
                    time.sleep(0.2)
                    if keyboard.is_pressed("t"):
                       print("Se Incearca")
                       setVid()
                


           

        

setVid()
cv.destroyAllWindows()
