from skimage import novice

class BloodDetector(object):
    def __init__(self):
        pass
    
    # Blood detect method
    def process(self):
        pass

class BloodColorDetector():
    def __init__(self, path, filename):
        self.img = novice.open(path + "/" + filename)
    
    def process(self):
        pass