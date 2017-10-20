import blood
import cv2

img = cv2.imread("img/test.jpg")
detector = blood.BloodColorDetector()
print(detector.process(img))