import os

import numpy as np
import cv2
from mss import mss
from PIL import Image

from agario_bot import parse_score
from window_utils import find_agario

bb = find_agario()
print(bb)
# bounding_box = {'top': 100, 'left': 631, 'width': 1285, 'height': 960}

sct = mss()
template = cv2.imread('play_bt_smol.png')
w, h = template.shape[:-1]
os.environ['TESSDATA_PREFIX'] = os.curdir

while True:
    xmargin = int(bb['width'] // 2.5)
    ymargin = bb['height'] // 8
    _bb = {
        'top':      bb['top'] + ymargin,
        'left':     bb['left'] + xmargin,
        'width':    bb['width'] - 2*xmargin,
        'height':   bb['height'] - 4*ymargin,
    }
    cropped_img = sct.grab(_bb)
    img_rgb = np.array(cropped_img)[:, :, :-1]
    try:
        sfood, scells = parse_score(np.array(cropped_img)[:, :, :-1])
    except Exception as e:
        print(e)
    cv2.imshow('screen', img_rgb)

    if (cv2.waitKey(1) & 0xFF) == ord('q'):
        cv2.destroyAllWindows()
        break