from __future__ import print_function
import argparse
import glob
import os
import json
import cv2
import random


def plot_one_box(c1, c2, img, color=None, label=None, line_thickness=3):
    # Plots one bounding box on image img
    tl = line_thickness or round(0.002 * (img.shape[0] + img.shape[1]) / 2) + 1  # line/font thickness
    color = color or [random.randint(0, 255) for _ in range(3)]
    cv2.rectangle(img, c1, c2, color, thickness=1, lineType=cv2.LINE_AA)
    if label:
        tf = max(tl - 1, 1)  # font thickness
        t_size = cv2.getTextSize(label, 0, fontScale=tl / 3, thickness=tf)[0]
        c2 = c1[0] + t_size[0], c1[1] - t_size[1] - 3
        cv2.rectangle(img, c1, c2, color, -1, cv2.LINE_AA)  # filled
        cv2.putText(img, label, (c1[0], c1[1] - 2), 0, tl / 3, [225, 255, 255], thickness=tf, lineType=cv2.LINE_AA)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("image_directory", help='Path of images inside yolo folder that will used for training/testing (will be appended to the begining of imagename in all images names txt)')
    args = parser.parse_args()
    os.mkdir("labels")
    count = 0
    labels = ['person','bike','car','motor','bus','train','truck','light','dog','scooter','other vehicle']


    with open("index.json") as f:
        data = json.load(f)
        frames = data['frames']
        width = 640.0
        height = 512.0
        image_names = []

        for frame in frames:
            image_name = "video-" + frame["videoMetadata"]["videoId"] + "-frame-" + str(frame["videoMetadata"]["frameIndex"]).zfill(6) + "-" + frame["datasetFrameId"] + ".jpg"
            image_names.append(args.image_directory + image_name)
            count += 1
            img = cv2.imread("data/"+image_name)
            converted_results = []  

            for anno in frame["annotations"]:
                label = anno['labels'][0]
                if label in labels:
                    bbox_height = anno["boundingBox"]["h"]
                    bbox_width = anno["boundingBox"]["w"]
                    x = anno["boundingBox"]["x"]
                    y = anno["boundingBox"]["y"]
                    cat_id = labels.index(label)

                    x_center, y_center = (x + bbox_width / 2, y + bbox_height / 2)
                    x_rel, y_rel = (x_center / width, y_center / height)
                    w_rel, h_rel = (bbox_width / width, bbox_height / height)
                    converted_results.append((cat_id, x_rel, y_rel, w_rel, h_rel))

                    c1 = (x,y)
                    c2 = (x+bbox_width, y+bbox_height)
                    plot_one_box(c1, c2, img, label= label)

            cv2.imshow("labeled", img)
            cv2.waitKey(1)
            print(args.image_directory + image_name)
            file = open("labels/" + str(image_name)[:-4] + '.txt', 'w+')
            file.write('\n'.join('%d %.6f %.6f %.6f %.6f' % res for res in converted_results))
            file.close()
        file = open('all_image_names.txt', 'w+')
        file.write('\n'.join('%s' % name for name in image_names))
        file.close()
        print("DONE!!")
        print("Processed", str(count), "images....")


                        



