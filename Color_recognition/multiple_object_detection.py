
import cv2
import time

# Define the lower and upper bounds of the yellow color in BGR format
# blue green red 
red_lower = (120, 140, 118) #0 - 255
red_upper = (179, 240, 210)

green_lower = (50, 100, 0)
green_upper = (100, 230, 102)

min_area = 150  #minimum area used to prevent camera from detecting really small color gaps


        
def objectDetection (frame , color_lower , color_upper,min_area = min_area):
    
    # Convert the frame from BGR to HSV color space
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Threshold the frame to detect yellow-colored objects
    color_mask = cv2.inRange(hsv_frame, color_lower, color_upper)

    # Find contours of yellow-colored objects
    color_contours , _ = cv2.findContours(color_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

   # Filter contours based on minimum area
    filtered_contours = [contour for contour in color_contours if cv2.contourArea(contour) > min_area]

    
    # Draw bounding boxes around detected yellow-colored objects
    for contour in filtered_contours:
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 2)
        
    return filtered_contours
    
def isSomethingThere(frame , part_type):

    green_contours = objectDetection(frame , green_lower , green_upper)
    red_contours = objectDetection(frame , red_lower , red_upper)
    # Display the frame with bounding boxes
    cv2.imshow(f'Object Detection {part_type}', frame)

    # print(len(red_contours),len(green_contours)) # determine objects
    if len(green_contours) > 0: # red 
        
        # print(f"green {part_type} detected!")
        return "green" # adjust colors later
    elif len(red_contours) >0:
        
        # print(f"red {part_type} detected!")
        return "red" # adjust colors later
    else:
        # print(f"No {part_type} detected.")
        return "no object"




# Open the camera stream using mobile ip adress to access camera
cap = cv2.VideoCapture(0)
#'http://192.168.121.153:8080/video'
#program allows controlling quality
#using: ip webcam


messsage_time = time.time()+1
while True:
    # Read a frame from the camera stream
    ret, frame = cap.read()
        
    l,w = frame.shape[:2]

    center_x = w//2
        
    left_frame = frame[0:l, 0:center_x]       #frame[y,x]

    right_frame = frame[0:l, center_x:]

    right_area = isSomethingThere(right_frame,"base")


    left_area = isSomethingThere(left_frame,"right_area")
    if time.time() > messsage_time:
        messsage_time = time.time()+1
        print(f"found {right_area} on right_side")
        print(f"found {left_area} on left_side")
    cv2.imshow(f'Object Detection full', frame)

    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


# Release the camera stream
cap.release()
# Close OpenCV windows
