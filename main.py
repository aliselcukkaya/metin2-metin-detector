from cv2 import cv2 as cv
import numpy as np
import os
from time import time,sleep
from windowcapture import WindowCapture
from vision_metin import VisionMetin
import pyautogui
from threading import Thread
import admin
from detection_metin import DetectionMetin
from machine import MetinMachine, MachineState
import keyboard
import pydirectinput

# this is for sending keystrokes to the app
if not admin.isUserAdmin():
    admin.runAsAdmin()

os.chdir(os.path.dirname(os.path.abspath(__file__)))

DEBUG_MODE = False


# initialize the WindowCapture class
wincap = WindowCapture('this_is_your_metin2_client_name')# you can get it from Task Manager
# initialize the detection class
detector_metin = DetectionMetin('tu_young_metin.png')
# initialize the Vision class
vision_metin = VisionMetin()
# initialize the Machine class
machine = MetinMachine((wincap.offset_x, wincap.offset_y), (wincap.w, wincap.h))


wincap.start()
detector_metin.start()
machine.start()

counter = 0

loop_time = time()
flag = True
while(flag):
    if wincap.screenshot is None:
        continue

    # get an updated image of the game
    screenshot = wincap.screenshot
    detector_metin.update(screenshot)
    
    
    # update the machine with the data it needs right now
    #print(machine.state)
    #print(machine.counter)
    
    if machine.state == MachineState.SLAY:
        machine.update_screenshot(screenshot)
        targets = vision_metin.get_click_points(detector_metin.rectangles)
        machine.update_targets(targets)
        #keyboard.press_and_release('z')
        
    elif machine.state == MachineState.BUFF:
        """
        sleep(1)
        pydirectinput.keyDown('ctrl')
        pydirectinput.press('g')
        pydirectinput.keyUp('ctrl')
        pydirectinput.press('1')
        pydirectinput.keyDown('ctrl')
        pydirectinput.press('g')
        pydirectinput.keyUp('ctrl')
        pydirectinput.keyDown('ctrl')
        pydirectinput.press('g')
        pydirectinput.keyUp('ctrl')
        pydirectinput.press('3')
        pydirectinput.keyDown('ctrl')
        pydirectinput.press('g')
        pydirectinput.keyUp('ctrl')
        sleep(1)
        """
    



    #debug the loop rate
    if DEBUG_MODE:
        screenshot_img = vision_metin.draw_rectangle(detector_metin.rectangles, screenshot)
        #screenshot_img = vision_sandik.draw_rectangle(detector_sandik.rectangles, screenshot)
        cv.imshow('Matches', screenshot_img)
        print('FPS {}'.format(1 / (time() - loop_time)))
        loop_time = time()

    # press 'q' with the output window focused to exit.
    # waits 1 ms every loop to process key presses
    if cv.waitKey(1) == ord('q'):
        wincap.stop()
        detector_metin.stop()
        machine.stop()
        cv.destroyAllWindows()
        flag = False
        break

print('Done.')