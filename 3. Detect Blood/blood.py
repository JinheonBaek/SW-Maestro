import cv2
import numpy as np

class BloodDetector(object):
    def __init__(self):
        pass

    # Blood detect method
    def process(self):
        pass

class BloodColorDetector(BloodDetector):
    def __init__(self, BR_threshold = None, DR_threshold = None):
        self.img = None
        self.img_height = None
        self.img_width = None
        self.img_channels = None

        # Bright Red Blood Range
        if BR_threshold == None:
            self.BR_threshold = {'red': (80, 170), 'green': (0, 5), 'blue': (0, 5)}
        else:
            self.BR_threshold = BR_threshold
        
        # Dark Red Blood Range
        if DR_threshold == None:
            self.DR_threshold = {'red': (120, 200), 'green': (0, 90), 'blue': (0, 90)}
        else:
            self.DR_threshold = DR_threshold

    def process(self, img):
        self.img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.img_height, self.img_width, self.img_channels = img.shape
        count_test = 0
        count = 0
        print("Process Image", self.img.size)
        
        # Iterate pixel of image
        for i in range(self.img_height):
            for j in range(self.img_width):
                red, green, blue = self.img[i, j]
                
                if (
                    (red >= self.BR_threshold['red'][0]) & 
                    (red <= self.BR_threshold['red'][1]) &
                    (green >= self.BR_threshold['green'][0]) &
                    (green <= self.BR_threshold['green'][1]) &
                    (blue >= self.BR_threshold['blue'][0]) &
                    (blue <= self.BR_threshold['blue'][1]) ) :
                    if (self.check_color_distribution_depth(i, j)) :
                        count += 1
                elif (
                    (red >= self.DR_threshold['red'][0]) & 
                    (red <= self.DR_threshold['red'][1]) &
                    (green >= self.DR_threshold['green'][0]) &
                    (green <= self.DR_threshold['green'][1]) &
                    (blue >= self.DR_threshold['blue'][0]) &
                    (blue <= self.DR_threshold['blue'][1]) &
                    (abs(int(green) - int(blue)) <= 8) ) :
                    if (self.check_color_distribution_depth(i, j)) :
                        count += 1
        
        return count / (self.img_width * self.img_height)

    def check_color_distribution_depth(self, x, y):
        count = 0

        for j in range(-2, 3):
            for i in range(-2, 3):
                if (x + i < 0 | y + j < 0):
                    break
                elif ((x + i >= self.img_width) | (y + j >= self.img_height)):
                    break
                if (np.all(self.img[x, y]) == np.all(self.img[x + i, y + j])):
                    count += 1

            if count >= 25:
                return False

        return True
