import matplotlib.pyplot as plt
import matplotlib.animation as anim
import os
from PIL import Image
import argparse
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument('-r', type=int)
parser.add_argument('-a', action='store_true')
args = parser.parse_args()

plt.axis('off')
pars = os.listdir('runs')
if args.a:
    pars[-1] = np.random.choice(pars)
elif args.r is not None:
    pars[-1] = f"{args.r:0=5}"
par = os.path.join('runs',pars[-1])
plt.title(pars[-1])
pics = os.listdir(par)
pics = [os.path.join(par,i) for i in pics]
def draw(i):
    return [plt.imshow(Image.open(i).transpose(Image.ROTATE_90))]

anime = anim.FuncAnimation(
    plt.gcf(),
    draw,
    pics,
    blit=True,
    interval=200,
    repeat_delay=400
)

plt.show()
