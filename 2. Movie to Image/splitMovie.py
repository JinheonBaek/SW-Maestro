
#
# PySceneDetect v0.5 API Test Script
#
# NOTE: This file can only be used with development versions of PySceneDetect,
#       and gives a high-level overview of how the new API will look and work.
#       This file is for development and testing purposes mostly, although it
#       also serves as a base for further example and test programs.
#

from __future__ import print_function

import scenedetect
import scenedetect.detectors
import scenedetect.manager


def main():

    print("Running PySceneDetect API test...")

    print("PySceneDetect version being used: %s" % str(scenedetect.__version__))

    # Set mode of detector
    content_detector = scenedetect.detectors.ContentDetector()
    threshold_detector = scenedetect.detectors.ThresholdDetector()

    # Set SceneManager
    smgr = scenedetect.manager.SceneManager(detector = content_detector, save_images = True, frame_skip = 0)
    #smgr = scenedetect.manager.SceneManager(detector = content_detector, save_images = False)

    # Above this is setting scenedetect

    # Scene detect
    scenedetect.detect_scenes_file("./video/fi1_xvid.avi", smgr)

    # Print
    print("Detected %d scenes in video (algorithm = content, threshold = default)." % (len(smgr.scene_list)))
    print(smgr.scene_list)

    '''
    content_detector = scenedetect.detectors.ContentDetector(threshold = 27)
    smgr = scenedetect.manager.SceneManager(detector = content_detector, downscale_factor = 2)
    scenedetect.detect_scenes_file("goldeneye.mp4", smgr)
    print("Detected %d scenes in video (algorithm = content, threshold = 27)." % (len(smgr.scene_list)))

    threshold = scenedetect.detectors.ThresholdDetector(threshold = 100)
    smgr = scenedetect.manager.SceneManager(detector = threshold, perf_update_rate = 5)
    scenedetect.detect_scenes_file("goldeneye.mp4", smgr)
    print("Detected %d scenes in video (algorithm = threshold, threshold = 100)." % (len(smgr.scene_list)))
    '''

if __name__ == "__main__":
    main()

