from os import path
from pathlib import Path
from argparse import ArgumentParser
from glob import glob
import cv2

def parse():
    """Parse command line
    :returns: options
    """
    parser = ArgumentParser()
    parser.add_argument('input', help='input folder with images')
    return parser.parse_args()

def rotate_image(image_name):
    img = cv2.imread(image_name)
    img = cv2.rotate(img, cv2.ROTATE_180)
    cv2.imwrite(image_name, img)

def rotate_all(image_path):
    images = glob(image_path)
    images.sort()
    for _, fname in enumerate(images):
        print(f'rotate image {fname} finished!')
        rotate_image(fname)
        

if __name__ == "__main__":
    opts = parse()
    rotate_all(opts.input)