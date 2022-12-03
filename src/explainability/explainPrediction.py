from quantiseVideo import *
import sys
sys.path.append('../')
from evaluateModel import *
from tensorflow import keras
import cv2
import glob


def maskFrames(video_path, n):
    print("Quantising video...")
    ranges, fps, frameSize = getFrames(video_path, n)
    print(ranges)
    data = load_sample(video_path)
    result = predict(data, model)
    exciting_label = result[0]
    print("Original video result", result)

    frames = []
    differnces = {}

    for filename in glob.glob('../../data/frames/*.jpg'):
        filename = filename.split('/')[4].split('.')[0]
        frames.append(int(filename[5:]))
    frames = sorted(frames)

    for r in ranges:
        keyFrame = r[0]
        print("Building new video without", keyFrame)
        lowerBound = r[1]
        upperBound = r[2]
        out = cv2.VideoWriter(str(keyFrame) + '.mp4', cv2.VideoWriter_fourcc('m','p','4','v'), fps, frameSize)
        for frame in frames:
            if lowerBound <= frame <= upperBound:
                continue
            else:
                img = cv2.imread('../../data/frames/frame' +str(frame)+ '.jpg')
                out.write(img)

        out.release()

        data = load_sample(str(keyFrame) + '.mp4')
        result = predict(data, model)
        print(keyFrame)
        print(result)
        differnces.update({keyFrame:result[0]-exciting_label})

    sorted_frames = {k: v for k, v in sorted(differnces.items(), key=lambda item: item[1])}
    print(sorted_frames)

    prime_frame = sorted_frames.key()[0]
    print("prime frame", prime_frame)

    for r in ranges:
        if r[0]==prime_frame:
            lower_frame, upper_frame = r[1], r[2]
            break

    return prime_frame, lower_frame, upper_frame


def maskPixels(key_frame, lower_frame, upper_frame, box_size=5):
    f1 = cv2.imread('../../data/frames/frame' + str(lower_frame) + '.jpg')

    for i in range(box_size):
        for j in range(box_size)
            f1[i][j] = (0,0,0)

    cv2.imwrite('../../data/frames/frame'+str(lower_frame)+'.jpg', f1)




if __name__ == "__main__":
    # print("Loading model...")
    # model = keras.models.load_model('../../data/models/predict_model')
    # video_path = "../../data/videos/test_videos/2496.mp4"
    # print(maskFrames(video_path, 25))
    maskPixels(70,53,76)
