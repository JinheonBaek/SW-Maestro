import blood
import cv2

img = cv2.imread("img/test2.jpg")
detector = blood.BloodColorDetector()
print(detector.process(img))