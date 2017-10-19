from skimage import novice
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
        self.img = img
        count = 0
        print("Process Image", self.img.size)
        # Iterate pixel of image
        for p in self.img:
            if (
                (p.red >= self.BR_threshold['red'][0]) & 
                (p.red <= self.BR_threshold['red'][1]) &
                (p.green >= self.BR_threshold['green'][0]) &
                (p.green <= self.BR_threshold['green'][1]) &
                (p.blue >= self.BR_threshold['blue'][0]) &
                (p.blue <= self.BR_threshold['blue'][1]) ) :
                if (self.check_color_distribution_depth(p.x, p.y)) :
                    count += 1
                    self.make_mark(p)

            elif (
                (p.red >= self.DR_threshold['red'][0]) & 
                (p.red <= self.DR_threshold['red'][1]) &
                (p.green >= self.DR_threshold['green'][0]) &
                (p.green <= self.DR_threshold['green'][1]) &
                (p.blue >= self.DR_threshold['blue'][0]) &
                (p.blue <= self.DR_threshold['blue'][1]) &
                (abs(p.green - p.blue) <= 8) ) :
                if (self.check_color_distribution_depth(p.x, p.y)) :
                    count += 1
                    self.make_mark(p)
        
        self.img.show()

        return count / (img.width * img.height)

    def check_color_distribution_depth(self, x, y):
        count = 0

        for j in range(-2, 3):
            for i in range(-2, 3):
                if (x + i < 0 | y + j < 0):
                    break
                elif ((x + i >= self.img.height) | (y + j >= self.img.width)):
                    break
                if (np.all(self.img.xy_array[x][y]) == np.all(self.img.xy_array[x + i][y + j])):
                    count += 1

            if count >= 25:
                return False

        return True

    def make_mark(self, p):
        p.red = 255
        p.green = 255
        p.blue = 255
