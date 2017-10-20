import cv2
import csv
import os

import scenedetect
import scenedetect.detectors
import scenedetect.manager
from blooddetect.blood import BloodColorDetector
from sensationalismdetect import vision
from movementdescriptor import extract_movementDescriptor

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

def blood_detect(movie_name = None, images = None, detector = None, scene_num = None, cut_num = None):
    data_dir_path = "./blood_data/" + movie_name
    if not os.path.exists(str(data_dir_path)):
        os.makedirs(str(data_dir_path))
    output_name = "Movie-%sScene-%04dCut-%04d.csv" % (movie_name, scene_num, cut_num)
    data_path_prefix = data_dir_path + '\\' + output_name

    f = open(data_path_prefix, 'w', encoding='utf-8', newline='')
    wr = csv.writer(f)
    
    wr.writerow(['scene_num', 'cut_num', 'result'])
    for i in range(cut_num):
        result = detector.process(images[i])
        wr.writerow([scene_num, i, result])
    
    f.close()
    
def sensationalism_detect(movie_name = None, images = None, scene_num = None, cut_num = None):
    data_dir_path = "./sensationalism_data/" + movie_name
    if not os.path.exists(str(data_dir_path)):
        os.makedirs(str(data_dir_path))
    output_name = "Movie-%sScene-%04dCut-%04d.csv" % (movie_name, scene_num, cut_num)
    data_path_prefix = data_dir_path + '\\' + output_name

    f = open(data_path_prefix, 'w', encoding='utf-8', newline='')
    wr = csv.writer(f)

    wr.writerow(['scene_num', 'cut_num', 'result'])
    for i in range(cut_num):
        result = vision.process(images[i])['adult']
        wr.writerow([scene_num, i, result])

    f.close()
    

def main():
    cap = cv2.VideoCapture()
    
    movie_name = "my_video.mp4"
    #scene_list = scene_detect(filename = filename)
    scene_list = [84, 140, 288]
    scene_list.insert(0, 0)

    cap.open("./video/" + movie_name)
    
    for scene_num in range(len(scene_list) - 1):
        images = []
        cut_num = scene_list[scene_num + 1] - scene_list[scene_num]
        
        for j in range(cut_num):
            (ret_val, im_cap) = cap.read()
            images.append(im_cap)

        blood_detect(movie_name = movie_name, images = images, detector = BloodColorDetector(), scene_num = scene_num, cut_num = cut_num)
        sensationalism_detect(movie_name = movie_name, images = images, scene_num = scene_num, cut_num = cut_num)
        #MBM()
        break

main()
