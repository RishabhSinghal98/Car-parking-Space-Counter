import cv2
import pickle


width,height=107,48 #width=157-50 height=240-192

try:
    with open('CarParkPos','rb') as f:
        posList=pickle.load(f)
except:
    posList=[]


        


def mouseClick(events,x,y,flags,parameters):
    if events == cv2.EVENT_LBUTTONDOWN: #if left mouse is clicked then we will appened the pos in posList
        posList.append((x,y))
        #below logic to delete rectangle box if box in between previous box
    if events == cv2.EVENT_RBUTTONDOWN: 
        for i, pos in enumerate(posList):
            x1,y1=pos
            if x1<x<x1+width and y1<y<y1+height:
                posList.pop(i)
    
    with open('CarParkPos','wb') as f:
        pickle.dump(posList,f)




while True:

    #cv2.rectangle(img,(50,192),(157,240),(255,0,255),2)
    
    img=cv2.imread('CarParkImg.png')
    for pos in posList:
        cv2.rectangle(img,pos,(pos[0]+width,pos[1]+height),(255,0,255),2)

   
    cv2.imshow("Car Parking",img) #shows image imshow takes two parameters one title for the image and another variable defined above
    cv2.setMouseCallback("Car Parking",mouseClick) #used to click mouse
    cv2.waitKey(1)
