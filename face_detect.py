
# import the necessary packages
import argparse
import cv2
import glob
import json
from firebase import firebase 

# construct the argument parse and parse the arguments

ap = argparse.ArgumentParser()
#ap.add_argument("-i", "--image", required=True,
#	help="path to the input image")
ap.add_argument("-c", "--cascade",
	default="haarcascade_frontalface_default.xml",
	help="path to cat detector haar cascade")
args = vars(ap.parse_args())

# load the input folder contaning image 

image = cv2.imread("1.jpg")


 
# first show original size and then perform the actual resizing of the image
print image.shape
r = 600.0 / image.shape[1]
dim = (600, int(image.shape[0] * r))
image = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)

#convert it to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# load detector Haar cascade, then detect faces
# in the input image
detector = cv2.CascadeClassifier(args["cascade"])
rects = detector.detectMultiScale(gray, scaleFactor=1.3,
	minNeighbors=10, minSize=(75, 75))

j=0
# loop over the  faces and draw a rectangle surrounding each
for (i, (x, y, w, h)) in enumerate(rects):
        j=j+1
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cv2.putText(image, "Face #{}".format(i + 1), (x, y - 10),
		cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 0, 255), 2)

print j

# show the detected faces
cv2.imshow("Faces", image)
cv2.waitKey(0)
firebase=firebase.FirebaseApplication('https://iot12-8370b.firebaseio.com/')
data={'faces':j}
firebase =firebase.put('https://iot12-8370b.firebaseio.com/','/count',data)
