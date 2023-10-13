from manim import *
import os

class Visualize(Scene):
    def construct(self):
        img = ImageMobject(os.path.join("dataset","1_1997X78_1737X381.png"))
        scale = 0.85
        img.height*=scale
        img.width*=scale
        self.add(img)
        cursor = Circle(1).move_to(img.get_left()+RIGHT*img.length_over_dim(1)*1997/2240, img.get_top()+DOWN*img.length_over_dim(0)*78/1400)
        self.play(Create(cursor))