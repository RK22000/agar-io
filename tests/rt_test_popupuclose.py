import os

import numpy as np
import cv2
from mss import mss
from PIL import Image

from agario_bot import parse_score, find_img
from window_utils import find_agario

bb = find_agario()
print(bb)
# bounding_box = {'top': 100, 'left': 631, 'width': 1285, 'height': 960}

sct = mss()
template = cv2.imread('popupweakspot.png')
w, h = template.shape[:-1]
os.environ['TESSDATA_PREFIX'] = os.curdir

while True:
    cropped_img = sct.grab(bb)
    img_rgb = np.array(cropped_img)[:, :, :-1]
    loc = find_img(img_rgb, template)
    # if loc is not None:
    m = np.ascontiguousarray(img_rgb, dtype=np.uint8)
    cv2.rectangle(m, loc, (loc[0]+w, loc[1]+h), (0, 255, 0), 2)
    print(loc)
    # cv2.circle(np.array(cropped_img), loc, 10, (0, 255, 0), 2)
    cv2.imshow('screen', m)

    if (cv2.waitKey(1) & 0xFF) == ord('q'):
        cv2.destroyAllWindows()
        break