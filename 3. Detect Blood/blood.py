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

        # Iterate pixel of image
        for p in self.img:
            if (
                p.red >= self.BR_threshold['red'][0] & 
                p.red <= self.BR_threshold['red'][1] &
                p.green >= self.BR_threshold['green'][0] &
                p.green <= self.BR_threshold['green'][1] &
                p.blue >= self.BR_threshold['blue'][0] &
                p.blue <= self.BR_threshold['blue'][1] ) :
                if (self.check_color_distribution_depth(p.x, p.y)) :
                    count += 1

            elif (
                p.red >= self.DR_threshold['red'][0] & 
                p.red <= self.DR_threshold['red'][1] &
                p.green >= self.DR_threshold['green'][0] &
                p.green <= self.DR_threshold['green'][1] &
                p.blue >= self.DR_threshold['blue'][0] &
                p.blue <= self.DR_threshold['blue'][1] ) :
                if (self.check_color_distribution_depth(p.x, p.y)) :
                    count += 1
        
        return count / (img.width * img.height)

    def check_color_distribution_depth(self, x, y):
        count = 0
        for i in range(-2, 3):
            for j in range(-2, 3):
                if (x + i < 0 | y + i < 0):
                    break
                elif ((x + i >= self.img.height - 1) | (y + j >= self.img.width - 1)):
                    break
                if (np.all(self.img.xy_array[x][y]) == np.all(self.img.xy_array[x + i][y + j])):
                    count += 1
        
        if count >= 3:
            return False
        
        return True
                
