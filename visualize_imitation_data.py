import matplotlib.pyplot as plt
import os
from matplotlib.axes import Axes
import matplotlib.animation as anim
import PIL.Image as img
from tqdm import tqdm
import argparse
from PIL import ImageOps

pics = os.listdir("data_imitation")
fig, ax = plt.subplots()
ax: Axes = ax

parser = argparse.ArgumentParser()
parser.add_argument('-o', default='visual.mp4')
parser.add_argument('-c', action='store_true')
args = parser.parse_args()

def draw(p):
    ax.clear()
    name = f"data_imitation\\{p}"
    im = img.open(name)
    if not args.c:
        im = ImageOps.grayscale(im)
    ax.imshow(im, 'gray')
    xy = [int(i) for i in p[11:-4].split('x')]
    x = im.width/2
    y = im.height/2
    dx = xy[0] - x
    dy = xy[1] - y
    ax.arrow(x,y,dx,dy, length_includes_head=True, head_width=10)
    ax.set_title(name)


anime = anim.FuncAnimation(
    fig,
    draw,
    tqdm(pics)
)

output = args.o
if output[-4:] != '.mp4':
    output += ".mp4"
anime.save(output)

# draw(pics[1])

# plt.show()
# print(pics)