from pathlib import Path
from argparse import ArgumentParser
from datetime import datetime
import os
import vlc
import cv2
import numpy as np
import re
import ipdb

def read_video(video_path):
    if not Path(video_path).is_file():
        print(f'video path {video_path} not a file')
        exit(-1)
    cap = cv2.VideoCapture(video_path, cv2.CAP_FFMPEG)
    if not cap.isOpened():
        print(f'video {video_path} open failed')
        exit(-1)
    
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print(f"The total number of frames in video {video_path} is {total_frame_count}")

    success_count = 0
    imgs = []
    for i in range(total_frame_count+1):
        success, image = cap.read()
        #print(f'Read a new frame: {i} {success}')
        if success:
            imgs.append(image)
            success_count += 1

    cap.release()
    print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Read {success_count} of {total_frame_count} frames finished!")

    return imgs, fps

def resize_images(imgs, dim):
    resized_imgs = []
    w, h = dim
    for img in imgs:
        interpolation = cv2.INTER_LINEAR
        height, width, channels = img.shape
        if width < w or height < h:
            interpolation=cv2.INTER_AREA
        resized_img = cv2.resize(img, dim, interpolation=interpolation)
        resized_imgs.append(resized_img)
    
    return resized_imgs


def crop_images(imgs, scale, size):
    interpolation = cv2.INTER_LINEAR
    if scale < 1.0:
        interpolation=cv2.INTER_AREA
    x, y, w, h = size

    crop_imgs = []
    for img in imgs:
        #ipdb.set_trace()
        scale_img = cv2.resize(img, None, fx=scale, fy=scale, interpolation=interpolation)
        assert y+h < scale_img.shape[0] and x+w < scale_img.shape[1]
        crop_img = scale_img[y:y+h, x:x+w]
        crop_imgs.append(crop_img)
    
    return crop_imgs

def write_images(imgs, img_path):
    Path(img_path).mkdir(parents=True, exist_ok=True)
    for i in range(len(imgs)):
        cv2.imwrite("{0}/frame_{1:05d}.png".format(img_path, i), imgs[i])

def vlc_show_video(video_name):
    media = vlc.MediaPlayer(video_name)
    media.play()

def cv_show_video(imgs, video_name):
    video_name = os.path.basename(video_name)
    for img in imgs:
        cv2.imshow(video_name, img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()

def write_video(imgs, video_filename, size, fps, fourcc=cv2.VideoWriter_fourcc(*'XVID')):
    w, h = size
    Path(video_filename).parent.mkdir(parents=True, exist_ok=True)
    out = cv2.VideoWriter(video_filename, fourcc, fps, (w,h))
    for img in imgs:
        out.write(img)
    
    out.release()
    print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Wirte {len(imgs)} frames video to file {video_filename} success!")

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument('-i', '--video', default="", help='input path_of_video')
    parser.add_argument('-s', '--show', type=bool, default=False, help='show video')
    parser.add_argument('-o', '--images', default="", help='output path_for images')
    parser.add_argument('-r', '--resize', default="", help='output path_for video')
    parser.add_argument('-c', '--crop', default="", help='output path_for video')
    parser.add_argument('-d', '--diff', default="", help='diff videos')

    opts = parser.parse_args()
    #ipdb.set_trace()
    
    if opts.diff:
        print("diff")
        names = ["synthesia_elon.mp4", "synthesia2_elon.mp4", "synthesia3_elon.mp4", "synthesia_bbc.mp4", "synthesia2_bbc.mp4", "synthesia3_bbc.mp4"]
        imgs_dict, fps_dict = {}, {}
        imgs_frames = []
        for name in names:
            imgs_dict[name], fps_dict[name] = read_video(name)
            h, w, c = imgs_dict[name][0].shape
            crop_size = (w//2, 0, w//2-1, h-1)
            if re.match('synthesia3_', name):
                print('dddddddddddd')
                crop_size = (w//4, 0, w//2-1, h-1)
            imgs_dict[name] = crop_images(imgs_dict[name], 1, crop_size)
            imgs_frames.append(len(imgs_dict[name]))

        '''
        diffs = []
        for i in range(min(len_1, len_2)):
            diff = np.abs(imgs_1[i] - imgs_2[i])
            gray1 = cv2.cvtColor(imgs_1[i], cv2.COLOR_BGR2GRAY)
            gray2 = cv2.cvtColor(imgs_2[i], cv2.COLOR_BGR2GRAY)
            diff_g = np.abs(gray1 - gray2)
            diff_g = cv2.cvtColor(diff_g, cv2.COLOR_GRAY2BGR)
            c1 = np.concatenate((imgs_1[i], imgs_2[i]), axis=1)
            c2 = np.concatenate((diff, diff_g), axis=1)
            c = np.concatenate((c1,c2), axis=0)
            diffs.append(c)
        h, w, c = imgs_1[0].shape
        diffs = resize_images(diffs, dim=(w,h))
        write_video(diffs, "synthesia_diff.mp4", (w,h), fps)
        '''
        #ipdb.set_trace()
        result = []
        for i in range(min(imgs_frames)):
            c1 = np.concatenate((imgs_dict[names[0]][i], imgs_dict[names[1]][i], imgs_dict[names[2]][i]), axis=1)
            c2 = np.concatenate((imgs_dict[names[3]][i], imgs_dict[names[4]][i], imgs_dict[names[5]][i]), axis=1)
            c = np.concatenate((c1,c2), axis=0)
            result.append(c)
        h, w, c = result[0].shape
        write_video(result, "synthesia_c.mp4", (w,h), fps_dict[names[0]])
        exit(0)

    if opts.show is True:
        vlc_show_video(opts.video)
        exit(0)

    imgs, fps = read_video(opts.video)
    
    if opts.images:
        write_images(imgs, opts.images)
        exit(0)
    
    if opts.resize:
        w, h = 256, 256
        imgs = resize_images(imgs, dim=(w,h))
        write_video(imgs, opts.resize, (w, h), fps)
        exit(0)

    if opts.crop:
        w, h = 256, 256
        size = 30, 150, w, h
        scale = 0.3

        #scale = 0.24
        #size = 0, 80, w, h

        scale = 0.73
        size = 0, 0, w, h

        #scale = 0.5
        #size = 30, 25, w, h
        
        imgs = crop_images(imgs, scale, size)
        write_video(imgs, opts.crop, (w, h), fps)
        exit(0)
