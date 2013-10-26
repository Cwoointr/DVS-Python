import cv2.cv as cv
import cv2
import time
from PIL import Image
import sys
from Eye import *
import PIL
""" A class to perform actions on a photo of a face
    This class has two child classes:
      HorizonalPhoto
      VerticalPhoto
"""
# NOTE: photoImg is a photo of a face

DEBUG = False

class FacePhoto():
    """ This class has attributes:
        IplImage facePhoto - a photo of the whole face
        string path - the path to the photo of the whole face
        Eye left - the left eye object
        Eye right - the right eye object
    """

    #TODO: Error checking and raising is not accounted for in psudeoclasses

    def __init__(self, photoImg, photoPath):
        """ Initializes eye objects

        Calls findEyes() to initialize the eye attributes.

        Args:
            photo photoImg - an image of a face

        Return:
            None
        """
        # Initialize the face photo to the value passed in
        self.facePhoto = photoImg
        self.path = photoPath
        # Initialize the other attributes to None so that they exist
        self.left = None
        self.right = None
        """
        if DEBUG:
            print "In the facePhoto __init__"
        """
        # Set attributes intialized to None by finding them.
        self.findEyes()

################# Utility Methods ######################

    def findEyes(self):
        """ Detects eyes in a photo and initializes relevant attributes

        Uses opencv libarary methods to detect a face and then detect the
        eyes in that face. If there are exactly two eye regions found it
        populates the region attributes. If a face is not found or exactly two
        eye regions are not found the method returns false.

        Args:
            None

        Return:
            bool - True if there were no issues. False for any error
        """
        # eyeDetection.py logic goes here
        # if there's 2 regions
        #     construct left and right eye objects; set left and right
        # else
        #     don't set the left and right attributes or construct Eye objects
        # Load the image the user chose

        #NOTE: You may need to modify this path to point to the dir with your cascades
        faceCascade = cv.Load("/usr/local/Cellar/opencv/2.4.6.1/share/OpenCV/haarcascades/haarcascade_frontalface_default.xml")
        eyeCascade = cv.Load("/usr/local/Cellar/opencv/2.4.6.1/share/OpenCV/haarcascades/haarcascade_eye.xml")

        # Detect the eyes and make an image with bounding boxes on it
        image = self.DetectEyes(self.facePhoto, faceCascade, eyeCascade)
        return "findEyes successfully called"
    
    ## Load the face and eye cascade when the analysis is done ##
    def Load():
       return (faceCascade, eyeCascade)

    ## The actual eye detection logic ##
    def DetectEyes(self, image, faceCascade, eyeCascade):
        min_size = (20,20)
        image_scale = 2
        haar_scale = 1.2
        min_neighbors = 3
        haar_flags = cv.CV_HAAR_DO_CANNY_PRUNING

        # Allocate the temporary images
        gray = cv.CreateImage((image.width, image.height), 8, 1)
        smallImage = cv.CreateImage((cv.Round(image.width / image_scale),
                                    cv.Round (image.height / image_scale)), 8 ,1)

        # Convert color input image to grayscale
        cv.CvtColor(image, gray, cv.CV_BGR2GRAY)

        # Scale input image for faster processing
        cv.Resize(gray, smallImage, cv.CV_INTER_LINEAR)

        # Equalize the histogram
        cv.EqualizeHist(smallImage, smallImage)

        # Detect the faces
        faces = cv.HaarDetectObjects(smallImage, faceCascade, cv.CreateMemStorage(0),
                                    haar_scale, min_neighbors, haar_flags, min_size)


        # Saving the face region points so we can use them to calculate
        # non-relative eye points
        pt1 = (0,0)
        pt2 = (0,0)
        # If faces are found
        if faces:
            for ((x, y, w, h), n) in faces:
                # the input to cv.HaarDetectObjects was resized, so scale the
                # bounding box of each face and convert it to two CvPoints
                pt1 = (int(x * image_scale), int(y * image_scale))
                pt2 = (int((x + w) * image_scale), int((y + h) * image_scale))
                if DEBUG:
                    cv.Rectangle(image, pt1, pt2, cv.RGB(255, 0, 0), 3, 8, 0)
                face_region = cv.GetSubRect(image,(x,int(y + (h/4)),w,int(h/2)))
                cv.SetImageROI(image, (pt1[0], pt1[1], pt2[0] - pt1[0],
                                      int((pt2[1] - pt1[1]) * 0.7)))
            if DEBUG:
                print "First face point: " + str(pt1)
                print "Second face point: " + str(pt2)
                
        # If there are no faces found there's no reason to continue
        else:
            if DEBUG:
                print "No faces found, returning false"
            return False  
      

        # NOTE: This returns the eye regions we're interested in
        eyes = cv.HaarDetectObjects(image, eyeCascade, cv.CreateMemStorage(0),
                                   1.3, min_neighbors, haar_flags, (15,15))

        
        if DEBUG:
            print "Eyes: " + str(eyes)
            ## Draw rectangles around the eyes found ##
            
            if eyes:
                # For each eye found
                for eye in eyes:
                    print "In findEyes() we are drawing a rectangle around: " + \
                                 str((eye[0][0], eye[0][1],
                                 eye[0][0] + eye[0][2],eye[0][1] + eye[0][3]))
                    # Draw a rectangle around the eye
                    cv.Rectangle(image,(eye[0][0], eye[0][1]),
                                 (eye[0][0] + eye[0][2],eye[0][1] + eye[0][3]),
                                 cv.RGB(255, 0, 0), 1, 8, 0)
            # Display the image with bounding boxes
            cv.ShowImage("Face with Eyes before overdetection correction", image)

            # Destroy the window when the user presses any key
            cv.WaitKey(0)
            cv.DestroyWindow("Face with Eyes before overdetection correction")
            
            
        # loop through eyes to find rectangles inside one another and
        # eliminate the larger ones
        if len(eyes) >= 2:
            for thisEye in eyes:
                for thatEye in eyes:
                    if DEBUG:
                        print "thisEye: " + str((thisEye[0][0], thisEye[0][1],
                                 thisEye[0][0] + thisEye[0][2],
                                 thisEye[0][1] + thisEye[0][3]))
                        print "thatEye: " + str((thatEye[0][0], thatEye[0][1],
                                 thatEye[0][0] + thatEye[0][2],
                                 thatEye[0][1] + thatEye[0][3]))
                    if thisEye == thatEye:
                        if DEBUG:
                            print "breaking"
                        continue
                    elif thisEye[0][0] > thatEye[0][0] and \
                         thisEye[0][1] > thatEye[0][1] and \
                         (thisEye[0][0] + thisEye[0][2]) < \
                         (thatEye[0][0] + thatEye[0][2]) and \
                         (thisEye[0][1] + thisEye[0][3]) < \
                         (thatEye[0][1] + thatEye[0][3]):
                        # thisEye is inside thatEye
                        if DEBUG:
                            print "removing " + str(thatEye) + " from eyes"
                        eyes.remove(thatEye)
        if DEBUG:
            print "Eyes after looping: " + str(eyes)
        
        cv.ResetImageROI(image)
        #calls set eyes if two regions found, otherwise returns false
        if len(eyes) == 2:
            if DEBUG:
                print "There are two eyes - detectEyes"
            # x, y, w, h
            left = (eyes[0][0][0] + pt1[0] , eyes[0][0][1] +pt1[1],
                    eyes[0][0][0] + eyes[0][0][3] + pt1[0],
                    eyes[0][0][1] + eyes[0][0][2] + pt1[1])
            right = (eyes[1][0][0] + pt1[0] , eyes[1][0][1] +pt1[1],
                    eyes[1][0][0] + eyes[1][0][3] + pt1[0],
                    eyes[1][0][1] + eyes[1][0][2] + pt1[1])
            if DEBUG:
                print "left: " + str(left)
                print "right: " + str(right)
            self.setEyes(left, right)
            return True
        if DEBUG:
            print "Found more or less than 2 eyes, returning false"
        return False

    
    def eyeRemove(self, region):
        """ Crops an eye from the facePhoto and returns it as a seperate photo

        This method takes in a region which is interpreted to be a region representing
        and eye and crops the eye out. It then returns the cropped photo

        Args:
            region region - a region representing the eye

        Return:
            photo eyePhoto - a photo of just the eye
        """
        # really takes in four points per region
        # place eye region here
        #face = Image.open(self.path)
        crop = (region[0],region[1], region[2] - region[0], region[3] - region[1])
        if DEBUG:
            print "Region passed to eye remove: " + str(region)
            print "And here's crop: " + str(crop)
            print "Before crop we have type: " + str(type(self.facePhoto))
            print self.facePhoto
            cv.ShowImage("We're cropping", self.facePhoto)
            cv.WaitKey(0)
            cv.DestroyWindow("We're cropping")
        eye = cv.GetSubRect(self.facePhoto, crop)
        #eye = face.crop(region)
        if DEBUG:
            print "After crop we have type: " + str(type(eye))
        return eye

##################### Getters ############################

    def getEyes(self):
        """ Returns a tuple of the left and right eye objects """
        leftEye = self.getLeftEye()
        rightEye = self.getRightEye()
        return (leftEye, rightEye)

    def getLeftEye(self):
        """ Returns the left eye object """
        return self.left

    def getRightEye():
        """ Returns the right eye object """
        return self.right

##################### Setters ############################

    def setEyes(self, leftRegion, rightRegion):
        """ Sets or resets both eye objects """
        if DEBUG:
            print "We're here in setEyes now"
        self.setLeftEye(leftRegion)
        self.setRightEye(rightRegion)
        return "setEyes successfully called"
        
    def setLeftEye(self,region):
        """ Constructs a new Eye object and stores it in left """
        if DEBUG:
            print "And we're setting the left eye now"
        # Crop out a photo of the eye to pass the Eye constructor
        left_eyePhoto = self.eyeRemove(region)
        # Constructs the left eye
        self.left = Eye(left_eyePhoto, region)
        return "setLeftEye successfully called"

    def setRightEye(self,region):
        """ Constructs a new Eye object and stores it in right """
        if DEBUG:
            print "And we're setting the right eye now"
        # Crop out a photo of the eye to pass the Eye constructor
        right_eyePhoto = self.eyeRemove(region)
        # Constructs the right eye
        self.right = Eye(right_eyePhoto, region)
        return "setRightEye successfully called"



    
        
    
