import cv2

import scenedetect
import scenedetect.detectors
import scenedetect.manager
from blooddetect.blood import BloodColorDetector
from sensationalismdetect import vision
from movementdescriptor import MBM

def scene_detect(filename = None):

    print("PySceneDetect version being used: %s" % str(scenedetect.__version__))

    # Set mode of detector
    content_detector = scenedetect.detectors.ContentDetector()
    threshold_detector = scenedetect.detectors.ThresholdDetector()

    # Set SceneManager
    smgr = scenedetect.manager.SceneManager(detector = content_detector, save_images = False, frame_skip = 0)
    #smgr = scenedetect.manager.SceneManager(detector = content_detector, save_images = False)

    # Above this is setting scenedetect

    # Scene detect
    scenedetect.detect_scenes_file("./video/" + filename, smgr)

    # Print
    print("Detected %d scenes in video %s (algorithm = content, threshold = default)." % (len(smgr.scene_list), filename))
    return smgr.scene_list

def blood_detect(img = None, detector = None):
    print(detector.process(img))

def sensationalism_detect(img = None):
    print(vision.process(img))

def main():
    filename = "my_video.mp4"
    scene_list = scene_detect(filename = filename)
    
    for i in scene_list:
        for 

    #blood_detect(img, detector)

#sensationalism_detect(img)
#blood_detect(img = img, detector = BloodColorDetector())


main()