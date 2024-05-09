import cv2
import numpy as np
import pyautogui
import keyboard
import time

# ColorBot made by lkx0 for AimBooster.com | Might work in other aim trainers, only tried on AimBooster.

# Color in RGB & reaction time in ms.

selected_color = (255, 208, 0)  
reaction_time = 0.15  

def detect_and_click_color():
    global selected_color, reaction_time
    screenshot = pyautogui.screenshot()
    screenshot = np.array(screenshot)
    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)
    selected_color_hsv = cv2.cvtColor(np.uint8([[selected_color]]), cv2.COLOR_RGB2HSV)[0][0]
    lower_bound = np.array([selected_color_hsv[0] - 10, 50, 50])
    upper_bound = np.array([selected_color_hsv[0] + 10, 255, 255])

    hsv = cv2.cvtColor(screenshot, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_bound, upper_bound)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        area = cv2.contourArea(contour)
        perimeter = cv2.arcLength(contour, True)
        
        if perimeter > 0:
            circularity = 4 * np.pi * area / (perimeter ** 2)

            if circularity > 0.8:
                M = cv2.moments(contour)
                if M["m00"] != 0:
                    cx = int(M["m10"] / M["m00"])
                    cy = int(M["m01"] / M["m00"])
                    pyautogui.click(x=cx, y=cy)
                    time.sleep(reaction_time)

print(" F2 to Init | F10 to Stop * Might take a couple F10 clicks to stop, take care.*")

running = False

# Color detection
while True:
    if keyboard.is_pressed('f2'):
        if not running:
            running = True
            print("Init.")
    if keyboard.is_pressed('f10'):
        if running:
            running = False
            print('Stop.')

    if running:
        detect_and_click_color()

    time.sleep(0.1)
