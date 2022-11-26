import os
import subprocess
import sys
import cv2
import numpy as np
import glob
from skimage.metrics import structural_similarity
from PIL import Image


def frameSimilarity(frame1, frame2):
    frame1 = cv2.imread('../../data/frames/frame' + str(frame1) + '.jpg')
    frame2 = cv2.imread('../../data/frames/frame' + str(frame2) + '.jpg')
    before = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    after = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
    (score, diff) = structural_similarity(before, after, full=True)
    return score


def getFrames(video_path, n):
    print("Removing files from last video...")
    files = glob.glob('../../data/frames/*')
    for f in files:
        os.remove(f)

    print("Frame extraction for new video")

    cap = cv2.VideoCapture(video_path)
    frame_num = cap.get(cv2.CAP_PROP_FRAME_COUNT)
	fps = video.get(cv2.cv.CV_CAP_PROP_FPS)
    print("Number of frames:", frame_num)
	print("Frames per second:", fps)

    # assume dependence between frames
    for i in range(int(frame_num)):
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.imwrite('../../data/frames/frame'+str(i)+'.jpg', frame)

    cap.release()
    cv2.destroyAllWindows()
    return getRanges(frame_num, n), fps


def getRanges(frame_num, n):
    frames = {}
    for i in range(0, int(frame_num-5), 10):
        score = frameSimilarity(i, i+10)
        if score < 0.5:
            frames.update({i: score})
    frames = {k: v for k, v in sorted(
        frames.items(), key=lambda item: item[1])}
    frames = [k for k in frames.keys()][:n]

    ranges = []

    for frame in frames:
        r = [frame]
        for i in range(1, int(frame_num)):
            try:
                if (frameSimilarity(frame, frame-i)) < 0.5:
                    r.append(frame-i)
                    break
            except:
                r.append(1)
                break
        for i in range(1, int(frame_num)):
            try:
                if (frameSimilarity(frame, frame+i)) < 0.5:
                    r.append(frame+i)
                    break
            except:
                r.append(frame_num)
                break
        ranges.append(r)
    return ranges
