import cv2
import time

# Read the image
# img = cv2.imread('shape.jpg')

cap = cv2.VideoCapture(0)
# to use camera add camera http
min_area = 5000 #it's too small

# Convert the image to grayscale
while 1:
        
    img = cap.read()
    _ , frame = img
    grey_img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Apply a binary threshold to the grayscale image
    ret, threshold_image = cv2.threshold(grey_img, 220, 255, cv2.THRESH_BINARY)

    # Find contours in the threshold image
    contours, hierarchy = cv2.findContours(threshold_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        #this code finds all contors and method determines how contors are found in relation with each other 
        
    # Loop through each contour
    for i, contour in enumerate(contours):
        if i == 0:
            continue  # Skip the first contour
        
        # Approximate the contour
        epsilon = 0.01 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)
        
        if cv2.contourArea(contour) > min_area:
            # Draw the contour on the original image
            cv2.drawContours(frame, [contour], 0, (0, 0, 0), 4)
            # Get bounding box coordinates
            x, y, w, h = cv2.boundingRect(approx)
            x_mid = int(x + w / 2)
            y_mid = int(y + h / 2)
            
            # Set text parameters
            coords = (x_mid, y_mid)
            colour = (0, 0, 0)
            font = cv2.FONT_HERSHEY_PLAIN
            
            # Identify and annotate the shape
            if len(approx) == 3 :
                cv2.putText(frame, 'triangle', coords, font, 1, colour, 1)
            if len(approx) == 4 :
                cv2.putText(frame, 'square', coords, font, 1, colour, 1)
            if len(approx) == 5:
                cv2.putText(frame, 'pentagon', coords, font, 1, colour, 1)
            print(cv2.contourArea(contour))
    

        
    cv2.imshow('window', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release
cv2.waitKey(0)
cv2.destroyAllWindows()
