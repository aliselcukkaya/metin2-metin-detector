from cv2 import cv2 as cv
import pyautogui
from time import sleep, time
from threading import Thread, Lock
from math import sqrt
import os
import keyboard
import pydirectinput

os.chdir(os.path.dirname(os.path.abspath(__file__)))
class MachineState:
    SLAY = 0
    COLLECT = 1
    BUFF = 3


class MetinMachine:
    # threading properties
    stopped = True
    lock = None
    
    # properties
    state = None
    targets = []
    screenshot = None
    window_offset = (0,0)
    window_w = 0
    window_h = 0
    clicked = False
    metin_count = 0
    counter = 3600



    def __init__(self, window_offset, window_size):
        # create a thread lock object
        self.lock = Lock()

        # for translating window positions into screen positions, it's easier to just
        # get the offsets and window size from WindowCapture rather than passing in 
        # the whole object
        self.window_offset = window_offset
        self.window_w = window_size[0]
        self.window_h = window_size[1]


        # start Machine in the initializing mode to allow us time to get setup.
        # mark the time at which this started so we know when to complete it
        self.state = MachineState.SLAY

    def click_next_target(self):
        # 1. order targets by distance from center
        # loop:
        #   2. hover over the nearest target
        #   3. confirm that it's limestone via the tooltip
        #   4. if it's not, check the next target
        # endloop
        # 5. if no target was found return false
        # 6. click on the found target and return true
        targets = self.targets_ordered_by_distance(self.targets)

        # load up the next target in the list and convert those coordinates
        # that are relative to the game screenshot to a position on our
        # screen
        #print(targets)
        if len(targets) > 0:
            target_pos = targets[0]
            screen_x, screen_y = self.get_screen_position(target_pos)
            print('Moving mouse to x:{} y:{}'.format(screen_x, screen_y))

            # move the mouse
            pyautogui.moveTo(x=screen_x, y=screen_y)
            # short pause to let the mouse movement complete and allow
            # time for the tooltip to appear
            #sleep(1)
            self.metin_count += 1
            pyautogui.click()
            print("\Slayed metin count: " + str(self.metin_count) + "\n")
            self.clicked = True



    def targets_ordered_by_distance(self, targets):
        # our character is always in the center of the screen
        my_pos = (self.window_w / 2, self.window_h / 2)
        # searched "python order points by distance from point"
        # simply uses the pythagorean theorem
        # https://stackoverflow.com/a/30636138/4655368
        def pythagorean_distance(pos):
            return sqrt((pos[0] - my_pos[0])**2 + (pos[1] - my_pos[1])**2)
        targets.sort(key=pythagorean_distance)

        # print(my_pos)
        # print(targets)
        # for t in targets:
        #    print(pythagorean_distance(t))
        return targets


    # translate a pixel position on a screenshot image to a pixel position on the screen.
    # pos = (x, y)
    # WARNING: if you move the window being captured after execution is started, this will
    # return incorrect coordinates, because the window position is only calculated in
    # the WindowCapture __init__ constructor.
    def get_screen_position(self, pos):
        return (pos[0] + self.window_offset[0], pos[1] + self.window_offset[1])

    # threading methods

    def update_targets(self, targets):
        self.lock.acquire()
        self.targets = targets
        self.lock.release()

    def update_screenshot(self, screenshot):
        self.lock.acquire()
        self.screenshot = screenshot
        self.lock.release()

    def start(self):
        self.stopped = False
        t = Thread(target=self.run)
        t.start()

    def stop(self):
        self.stopped = True

    # main logic controller
    def run(self):
        while not self.stopped:
            if self.state == MachineState.SLAY:
                self.click_next_target()
                #this sleep time is depend on how much time is your character need to slay a metin
                sleep(7.7)
                # z for collecting items on the ground
                pydirectinput.press('z')

                # this is needed if character stuck with mobs
                if self.counter % 100 == 0:
                    pydirectinput.press('space')
                    pydirectinput.press('space')
                    pydirectinput.press('space')

                # this part is actually made for warrior class
                # 1 is for Aura of the Sword, 3 is for Berserk
                # you can adjust this for your character and skill positions
                # the counter increases approximately every 8 seconds
                # you can calculate for when your skills are expired
                elif self.counter >= 2000:
                    self.lock.acquire()
                    sleep(1)
                    pydirectinput.keyDown('ctrl')
                    pydirectinput.press('g')
                    pydirectinput.keyUp('ctrl')
                    sleep(1)
                    pydirectinput.press('1')
                    sleep(1)
                    pydirectinput.keyDown('ctrl')
                    pydirectinput.press('g')
                    pydirectinput.keyUp('ctrl')
                    sleep(1)
                    pydirectinput.keyDown('ctrl')
                    pydirectinput.press('g')
                    pydirectinput.keyUp('ctrl')
                    sleep(1)
                    pydirectinput.press('3')
                    sleep(1)
                    pydirectinput.keyDown('ctrl')
                    pydirectinput.press('g')
                    pydirectinput.keyUp('ctrl')
                    sleep(1)
                    self.counter = 0
                    self.lock.release()

                # this counter needed for the above actions
                self.lock.acquire()
                self.counter += 10
                self.lock.release()

            elif self.state == MachineState.BUFF:
                self.lock.acquire()
                """
                sleep(1.5)
                pydirectinput.keyDown('ctrl')
                pydirectinput.press('g')
                pydirectinput.keyUp('ctrl')
                keyboard.press_and_release('1')
                pydirectinput.keyDown('ctrl')
                pydirectinput.press('g')
                pydirectinput.keyUp('ctrl')
                pydirectinput.keyDown('ctrl')
                pydirectinput.press('g')
                pydirectinput.keyUp('ctrl')
                keyboard.press_and_release('3')
                pydirectinput.keyDown('ctrl')
                pydirectinput.press('g')
                pydirectinput.keyUp('ctrl')
                sleep(1.5)
                """
                self.counter = 0
                self.state = MachineState.SLAY
                self.lock.release()

                """
                if self.clicked == True:
                    self.lock.acquire()
                    self.state = MachineState.COLLECT
                    self.lock.release()
                """
                """
                if not success:
                    success = self.click_next_target()
                """

                # if successful, switch state to moving
                # if not, backtrack or hold the current position
                """
                if success:
                    self.lock.acquire()
                    self.state = MachineState.MOVING
                    self.lock.release()
                elif len(self.click_history) > 0:
                    self.click_backtrack()
                    self.lock.acquire()
                    self.state = MachineState.BACKTRACKING
                    self.lock.release()
                else:
                    # stay in place and keep searching
                    pass
                """
