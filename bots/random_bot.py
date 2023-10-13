import pyautogui
import numpy

class RandomBot:
    def nextMove(self):
        width, height = pyautogui.size()
        x, y = numpy.random.random(2) * [width, height]
        pyautogui.moveTo(x, y, 0.1)

def newBot():
    return RandomBot()
