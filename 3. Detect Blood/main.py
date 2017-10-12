import blood
from skimage import novice

img = novice.open('img/test.jpg')
detector = blood.BloodColorDetector()
print(detector.process(img))