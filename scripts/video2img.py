from pathlib import Path
import cv2

vidcap = cv2.VideoCapture('calibration/IMG_0714.MOV')
img_path = "calibration/IMG_0714/"
Path(img_path).mkdir(parents=True, exist_ok=True)

success,image = vidcap.read()
count = 0
while success:
  cv2.imwrite("{0}frame_{1:05d}.png".format(img_path, count), image)     # save frame as JPEG file      
  success,image = vidcap.read()
  print(f'Read a new frame: {count} {success}')
  count += 1