import cv2
import pickle
import cvzone
import numpy as np

cap=cv2.VideoCapture('carPark.mp4') #captures video

width,height=107,48 #width=157-50 height=240-192


with open('CarParkPos','rb') as f: #opening saved file that we are saving in maim
        posList=pickle.load(f)


def CheckParkingSpace(imgProcess): 
    
    spacecounter=0
     
    for pos in posList:
        x,y=pos
      
        img_crop=imgProcess [y:y+height,x:x+width] #cropping image form reactange bos
        cv2.imshow("str(x*y)",img_crop) #displaying the cropped image
    
        count=cv2.countNonZero(img_crop)
        
        cvzone.putTextRect(img,str(count),(x,y+height-5),scale=1.5,thickness=2,offset=0,colorR=(0,0,255))
  
        if count<900:
            color=(0,255,0) #green color
            thickness=4
            spacecounter+=1
        else:
            color=(0,0,255) #red color
            thickness=2
        cv2.rectangle(img,pos,(pos[0]+width,pos[1]+height),color,thickness)
    cvzone.putTextRect(img,f'Space Availiable :{spacecounter}/{len(posList)}',(100,50),scale=2.5,thickness=2,offset=0,colorR=(0,180,0))


while True:
    
     # used to run video in loop
    if cap.get(cv2.CAP_PROP_POS_FRAMES)==cap.get(cv2.CAP_PROP_FRAME_COUNT):
         cap.set(cv2.CAP_PROP_POS_FRAMES,0)


    success,img=cap.read()


    imgGray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY) #graying the image
    imgBlur=cv2.GaussianBlur(imgGray,(3,3),1) #adding blur to image

    imgThreshold=cv2.adaptiveThreshold(imgBlur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,25,16)
   
    imgMedianblur=cv2.medianBlur(imgThreshold,5)
    
    kernel=np.ones((3,3),np.uint8)
    
    imgDilate=cv2.dilate(imgMedianblur,kernel,iterations=1)


    CheckParkingSpace(imgDilate)
    # for pos in posList:
    #       cv2.rectangle(img,pos,(pos[0]+width,pos[1]+height),(255,0,255),2)



    cv2.imshow("Carparking",img) #shows video

    # cv2.imshow("GrayImg",imgGray)
    # cv2.imshow("BlurredImage",imgBlur)
    # cv2.imshow("THRESHOLDImage",imgThreshold)
    # cv2.imshow("MedianBlurredImage",imgMedianblur) 
    # cv2.imshow("DilatedImage",imgDilate)
    cv2.waitKey(10)
    