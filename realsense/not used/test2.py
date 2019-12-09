import cv2

cap = cv2.VideoCapture(3)
#cap = cv2.imread("/home/ashley/index.jpeg")
cap.set(3,640)
cap.set(4,480)

while(True):
	ret,frame = cap.read()	
	#frame = cap
	
	cv2.imshow('video', frame)

	k = cv2.waitKey(30) & 0xff
	if k == 27:
		break

cap.release()
cv2.destroyAllWindows()
