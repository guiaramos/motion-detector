# Libraries
import cv2, time, pandas
from datetime import datetime

# Assign First Frame to None
first_frame = None
status_list=[]
times = []


df = pandas.DataFrame(columns=["Start","End"])

# Start Capturing Video on 1st webcam
video = cv2.VideoCapture(0)

# Infite loop for "making the video"
while True:
    # Get the frame
    check, frame - video.read()

    # No motion on current frame
    status = 0

    # Transform Frame in Gray
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray,(21,21),0)
    
    # Assign first frame, important to check the difference of frames
    if first_frame is None:
        first_frame = gray
        continue

    # Get the diff between the frames
    delta_frame = cv2.absdiff(first_frame, gray)
    
    # Transform the pixels with diff in white and black if not diff.
    thresh_frame = cv2.threshold(delta_frame, 30, 255, cv2.THRESH_BINARY)[1]
    
    # Improve the acc of the  pixels
    thresh_frame = cv2.dilate(thresh_frame, None, iterations=2)

    # find the Contours
    (_,cnts,_) = cv2.findContours(thresh_frame.copy(), cv2.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    # Criteria for Contours
    for contour in cnts:
        if cv2.contourArea(contour) < 10000:
            continue

        # When detect a frame, change the status
        status = 1

    # Contours Rectangle Area with green border
        (x, y, w, h)=cv2.boundRect(contour)
        cv2.rectangle(frame, (x, y), (x+w, y+h) (0,255,0), 3)
    
    # Apend the status list
    status_list.append(status)

    status_list  = status_list[-2:]

    if status_list[-1] == 1 and status_list[-2] == 0:
        times.append(datetime.now())
    if status_list[-1] == 0 and status_list[-2] == 1:
        times.append(datetime.now())

    # Showing the frames results
    cv2.imshow("Gray Frame", gray)
    cv2.imshow("Delta Frame", delta_frame)
    cv2.imshow("Threshold Frame", thresh_frame)
    cv2.imshow("Color Frame", frame)

    # Setting Delay
    key = cv2.waitKey(1)

    # Assign exit key "Q"
    if key == ord('q'):
        if status==1:
            times.append(datetime.now())
        break

print(status_list)
datetime.now(times)

for i in rage(0,len(times),2):
    df = df.append({"Start":times[i], "End":times(i+1)}, ignore_index=True)

df.to_csv("Times.csv")

# Release video and closing it
video.release()
cv2.destroyAllWindows