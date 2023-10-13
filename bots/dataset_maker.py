import pyautogui
import os
import time
import threading

class DatasetMaker:
    def __init__(self, root="dataset", nextPosDelaySec=1) -> None:
        if not os.path.isdir(root):
            os.makedirs(root)
        self.root = root
        def updatePic(pic):
            time.sleep(nextPosDelaySec)
            x, y = pyautogui.position()
            picUpdated = pic.split(".")[0] + f"_{x}X{y}.png"
            # print(f"{pic} --> {picUpdated}")
            os.rename(pic, picUpdated)
        self.updatePic = updatePic
        


    def snap(self, id):
        x, y = pyautogui.position()
        cur_pos = f"{id}_{x}X{y}.png"
        img_name = os.path.join(self.root, cur_pos)
        image = pyautogui.screenshot(img_name)
        
        update = threading.Thread(target=self.updatePic, args=(img_name,))
        update.start()

def newDatasetMaker():
    return DatasetMaker("dataset")
