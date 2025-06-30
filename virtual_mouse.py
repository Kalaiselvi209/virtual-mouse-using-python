import cv2
import pyautogui
import numpy as np
import time

cap = cv2.VideoCapture(0)
screen_w, screen_h = pyautogui.size()

prev_x, prev_y = 0, 0
still_start_time = 0
click_delay = 1  # seconds to wait before clicking

while True:
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Blue color range (change to red if needed)
    lower_color = np.array([100, 100, 100])
    upper_color = np.array([140, 255, 255])

    mask = cv2.inRange(hsv, lower_color, upper_color)
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 1000:
            x, y, w, h = cv2.boundingRect(contour)
            cx = x + w // 2
            cy = y + h // 2

            cv2.circle(frame, (cx, cy), 10, (0, 255, 0), -1)

            # Move the real mouse
            screen_x = np.interp(cx, [0, frame.shape[1]], [0, screen_w])
            screen_y = np.interp(cy, [0, frame.shape[0]], [0, screen_h])
            pyautogui.moveTo(screen_x, screen_y)

            # Check if object is still (for clicking)
            if abs(cx - prev_x) < 10 and abs(cy - prev_y) < 10:
                if still_start_time == 0:
                    still_start_time = time.time()
                elif time.time() - still_start_time > click_delay:
                    pyautogui.click()
                    print("Clicked!")
                    still_start_time = 0  # Reset after click
            else:
                still_start_time = 0

            prev_x, prev_y = cx, cy

    cv2.imshow("Virtual Mouse (Color Tracker + Click)", frame)

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()
