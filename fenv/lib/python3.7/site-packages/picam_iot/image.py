from picamera import PiCamera
from time import sleep
from storage import *
import numpy as np
import io
import cv2

class image:
    """
    Manages all image operations. Allows capturing and storage of images, 
    setting up of camera image characteristics and interfacing images with face detection
    """

    def __init__(self, local = "./images/"):
        """
        Initializes the image manegement module 
        
        """
        self.camera = PiCamera()
        self.local = local
    
    def capture(self, name, res = (960, 600)):
        """ Captures and returns and image object.

        The image is saved to local storage by default but can be set to other storages.

        :param name: name of the image to be captured
        :param res: image resolution, 
        :returns: An image object
        :rtype: jpg
        """
        self.camera.resolution = res
        self.camera.start_preview()
        sleep(5)
        self.camera.capture(self.local + name + ".jpg")
        self.camera.stop_preview()

    def set_resolution(self, res = (1024, 768), width = False, height = False ):
        """ Sets the resolution of the images
        :param res: A tupple with the resolution as (width, height). Default is (1024, 768)
        :param width: Sets the camera width to the provided width. Default is 1024 pixels.
        :param height: Sets camera heigh to the specified height. Default is 768.
        """
        self.camera.resolution = res
    
    def face_capture(self, name = "image"):
        """ Captures an image and Draws a box around the frame with a face.
        :param name: name of the image to be saved, default is "image".
        """
        stream = io.BytesIO()
        self.camera.resolution = (320, 240)
        self.camera.capture(stream, format = 'jpeg')
        buffer = np.fromstring(stream.getvalue(), dtype = np.uint8)

        img = cv2.imdecode(buffer, 1)
        cascade = cv2.CascadeClassifier('./res/faces.xml')
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = cascade.detectMultiScale(gray_img, 1.1, 5)

        for (x,y,w,h) in faces:
            cv2.rectangle(img, (x,y), (x + w, y + h), (0, 255, 255), 2)
        
        cv2.imwrite( self.local + name + ".jpg", img )
        self.set_resolution()
    
    def face_detect(self, image, show = False):
        """ Takes an image and detects faces from the image, and draw boxes around where there are faces
        :param image: location of the image.
        :param show: whether or not the image should be diplayed to the screen, default is false.
        
        """
        cascade = cv2.CascadeClassifier("./res/faces.xml")
        img = cv2.imread(image)
        img = cv2.resize(img, (320, 240))
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        faces = cascade.detectMultiScale(gray_img, 1.1, 4)

        print("found " + str(len(faces)) + " faces")
        
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
        
        cv2.imwrite(image, img)

        if show:
            cv2.imshow(image, img)
    
if __name__ == "__main__":
    pass