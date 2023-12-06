import matplotlib.pyplot as plt
import matplotlib.animation as anim
import os
from PIL import Image
import argparse
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument('-r', type=int)
parser.add_argument('-a', action='store_true')
parser.add_argument('-d', default='runs')
parser.add_argument('--pov', action='store_true')
parser.add_argument('-o')
args = parser.parse_args()

plt.axis('off')
pars = os.listdir(args.d)
if args.a:
    pars[-1] = np.random.choice(pars)
elif args.r is not None:
    pars[-1] = f"{args.r:0=5}"
par = os.path.join(args.d,pars[-1])
plt.title(pars[-1])
pics = os.listdir(par)
if '.fullpic' in pics and not args.pov:
    par = os.path.join(par, '.fullpic')
    pics = os.listdir(par)
pics = list(filter(lambda i: i[0]!='.', pics))
pics = [os.path.join(par,i) for i in pics]
pics = zip(pics[:-1], pics[1:])
interpolations = [0,0.5,1]
pics = sum([[(p,i) for i in interpolations] for p in pics], [])
def draw(i):
    (a, b), frac = i
    a = Image.open(a)
    b = Image.open(b)
    im = Image.blend(a,b,frac)
    # if args.pov:
    #     im = im.transpose(Image.ROTATE_90)
    return [plt.imshow(im)]

from tqdm import tqdm
anime = anim.FuncAnimation(
    plt.gcf(),
    draw,
    tqdm(pics),
    blit=True,
    interval=200,
    repeat_delay=400
)

if args.o is None:
    plt.gcf().canvas.manager.full_screen_toggle()
    plt.show()
else:
    anime.save(args.o)
