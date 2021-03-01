from cv2 import cv2 as cv
from threading import Thread, Lock
from vision_metin import VisionMetin


class DetectionMetin:

    # threading properties
    stopped = True
    lock = None
    rectangles = []
    # properties
    screenshot = None
    vision = VisionMetin()

    def __init__(self, metin_file_path):
        # create a thread lock object
        self.lock = Lock()
        self.vision.get_img_shape(metin_file_path)

    def update(self, screenshot):
        self.lock.acquire()
        self.screenshot = screenshot
        self.lock.release()

    def start(self):
        self.stopped = False
        t = Thread(target=self.run)
        t.start()

    def stop(self):
        self.stopped = True

    def run(self):
        while not self.stopped:
            if not self.screenshot is None:
                # do object detection
                rectangles = self.vision.find_rectangle(self.screenshot)
                # lock the thread while updating the results
                self.lock.acquire()
                self.rectangles = rectangles
                self.lock.release()