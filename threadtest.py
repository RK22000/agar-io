import threading
import time

def main():
    boolean = [False]
    threading.Thread(target=boolCheck, args=(boolean, )).start()
    time.sleep(0.5)
    boolEdit(boolean)
    pass


def boolCheck(boolToCheck):
    count=0
    while not boolToCheck[0] and count < 100:
        print(f"nope {count}")
        count+=1
        time.sleep(0.1)
    print("Yes!!!")

def boolEdit(boolToEdit):
    boolToEdit[0]=True


if __name__=='__main__':
    main()