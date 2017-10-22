import cv2
import csv
import math
from PIL import Image
import numpy as np

_path = './video/fi1_xvid.avi'
cap = cv2.VideoCapture()
cap.open(_path)

set_video_width = 1280
set_video_height = 720
frame_num = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
print(frame_num)
# number of features = sub_row * sub_col
sub_row, sub_col = int(set_video_height/15), int(set_video_width/15)

frames = np.zeros((frame_num, int(set_video_height), int(set_video_width)))
print(frames.shape)

# Load all frames of video & convert frame to extract flows
for i in range(frame_num):
    (ret_val, im_cap) = cap.read()
    
    # frame reshape
    frame = np.array(Image.fromarray(im_cap).resize((set_video_width, set_video_height)))
    frames[i] = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

# Extract flows from the two frames
flows = np.zeros((frame_num-1, set_video_height, set_video_width, 2))
for i in range(frame_num-1):
    flows[i] = cv2.calcOpticalFlowFarneback(frames[i],frames[i+1], None, 0.5, 3, 15, 3, 5, 1.2, 0) 

# mags, angs
mags = np.zeros((frame_num-1, set_video_height, set_video_width))
angs = np.zeros((frame_num-1, set_video_height, set_video_width))
for i in range(frame_num-1):
    mags[i], angs[i] = cv2.cartToPolar(flows[i, :, :, 0], flows[i, :, :, 1])

# Variation of the mags & angs
Ds = np.zeros((frame_num-2, set_video_height, set_video_width))
sub_mags = np.zeros((frame_num-1, 15, 15))
sub_angs = np.zeros((frame_num-1, 15, 15))

# weight
w = 0.4

# Calculate Movement Descriptor
for i in range(sub_row):
    for j in range(sub_col):
        for k in range(frame_num-1):
            sub_mags[k, :, :] = mags[k, 15*i : 15*(i+1), 15*j : 15*(j+1)]
            sub_angs[k, :, :] = angs[k, 15*i : 15*(i+1), 15*j : 15*(j+1)]

        M = sub_mags[:, 7, 7]
        V = sub_angs[:, 7, 7]

        for k in range(len(M) - 1):
            Ds[k, i, j] = (w*abs(M[k+1]-M[k]))+((1-w)*math.acos(V[k+1]*V[k]/abs(V[k+1]*V[k])))/math.radians(180) 
        Ds[np.isnan(Ds)] = 0

# Motion Binary Map : extract high motion
threshold = 2.5
MBM = np.zeros_like(Ds)
MBM[Ds > threshold] = 1

# Mean
MBM_mean = MBM.mean(axis=2)

f = open('HockeyTraining.csv', 'w', encoding='utf-8', newline='')
wr = csv.writer(f)
li = list(MBM_mean.reshape(MBM_mean.shape[0] * MBM_mean.shape[1]))
wr.writerow(li)
f.close()
cap.release()