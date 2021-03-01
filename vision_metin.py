from cv2 import cv2 as cv
import numpy as np
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

class VisionMetin:

    # properties
    metin_img = None
    metin_w = 0
    metin_h = 0
    method = None
    
    def get_img_shape(self, metin_img_path, method=cv.TM_CCOEFF_NORMED):
        # load the image we're trying to match
        # https://docs.opencv.org/4.2.0/d4/da8/group__imgcodecs.html
        self.metin_img = cv.imread(metin_img_path, cv.IMREAD_UNCHANGED)

        # Save the dimensions of the metin image
        self.metin_w = self.metin_img.shape[1]
        self.metin_h = self.metin_img.shape[0]

        # There are 6 methods to choose from:
        # TM_CCOEFF, TM_CCOEFF_NORMED, TM_CCORR, TM_CCORR_NORMED, TM_SQDIFF, TM_SQDIFF_NORMED
        self.method = method
    
    # given a list of [x, y, w, h] rectangles returned by find(), convert those into a list of
    # [x, y] positions in the center of those rectangles where we can click on those found items
    def get_click_points(self, rectangles):
        points = []

        # Loop over all the rectangles
        for (x, y, w, h) in rectangles:
            # Determine the center position
            center_x = x + int(w/2)
            center_y = y + int(h/2)
            # Save the points
            points.append((center_x, center_y))

        return points


    def find_rectangle(self, screenshot_img, threshold=0.55):
        # run the OpenCV algorithm
        result = cv.matchTemplate(screenshot_img, self.metin_img, self.method)

        # Get the all the positions from the match result that exceed our threshold
        locations = np.where(result >= threshold)
        locations = list(zip(*locations[::-1]))
        #print(locations)

        # You'll notice a lot of overlapping rectangles get drawn. We can eliminate those redundant
        # locations by using groupRectangles().
        # First we need to create the list of [x, y, w, h] rectangles
        rectangles = []
        for loc in locations:
            rect = [int(loc[0]), int(loc[1]), self.metin_w, self.metin_h]
            # Add every box to the list twice in order to retain single (non-overlapping) boxes
            rectangles.append(rect)
            rectangles.append(rect)
        # Apply group rectangles.
        # The groupThreshold parameter should usually be 1. If you put it at 0 then no grouping is
        # done. If you put it at 2 then an object needs at least 3 overlapping rectangles to appear
        # in the result. I've set eps to 0.5, which is:
        # "Relative difference between sides of the rectangles to merge them into a group."
        rectangles, weights = cv.groupRectangles(rectangles, groupThreshold=1, eps=0.5)
        #print(rectangles)

        return rectangles
    
    def draw_rectangle (self,rectangles, screenshot_img):
        #print('Found metin.')

        line_color = (0, 255, 0)
        line_type = cv.LINE_4
        
        # Loop over all the rectangles
        for (x, y, w, h) in rectangles:
                # Determine the box position
                top_left = (x, y)
                bottom_right = (x + w, y + h)
                # Draw the box
                cv.rectangle(screenshot_img, top_left, bottom_right, color=line_color, 
                            lineType=line_type, thickness=2)
        
        return screenshot_img