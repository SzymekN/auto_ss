import time
import win32gui
import win32ui
import atexit
import keyboard
from pyautogui import size as screen_size
from numpy import asarray
from ctypes import windll
from PIL import Image as Image

def goodbye(auto_ss):

    try:
        with open("counter.txt", 'w') as file:
            file.write(str(auto_ss.image_count))
    except:
        print("couldn't save")
            

class Auto_ss():

    def enum_cb(self, hwnd, results):
        self.winlist.append((hwnd, win32gui.GetWindowText(hwnd)))

    def _get_window_handle(self):
        win32gui.EnumWindows(self.enum_cb, self.toplist)
        teams = [(hwnd, title) for hwnd, title in self.winlist if self.window_name in title.lower()]
        teams = teams[0]
        print(teams)
        self.hwnd = teams[0]

    def _get_display_handle(self):
        self.hwndDC = win32gui.GetWindowDC(self.hwnd)
        self.mfcDC  = win32ui.CreateDCFromHandle(self.hwndDC)
        self.saveDC = self.mfcDC.CreateCompatibleDC()

    def take_screenshot(self):

        self.saveBitMap.CreateCompatibleBitmap(self.mfcDC, self.w, self.h)
        self.saveDC.SelectObject(self.saveBitMap)

        # Change the line below depending on whether you want the whole window
        # or just the client area. 
        result = windll.user32.PrintWindow(self.hwnd, self.saveDC.GetSafeHdc(), 3)

        # win32gui.SetForegroundWindow(hwnd)
        bmpinfo = self.saveBitMap.GetInfo()
        bmpstr = self.saveBitMap.GetBitmapBits(True)

        im = Image.frombuffer(
            'RGB',
            (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
            bmpstr, 'raw', 'BGRX', 0, 1)
        
        if result == 1:
            return im
        else:
            print("WARNING! Couldn't take screenshot")
            exit()

    def _get_counter(self):
        try:
            with open("counter.txt", 'r') as file:
                self.image_count = int(file.read())
        except:
            self.image_count = 0

    def __init__(self) -> None:

        # window_name = '| microsoft teams'
        self.window_name = "opera"
        self.toplist, self.winlist = [], []
        self.w, self.h = screen_size()

        self._get_window_handle()
        self._get_display_handle()
        self.saveBitMap = win32ui.CreateBitmap()
        self._get_counter()

    def simple_error(self, imageA, imageB):

        im1_arr = asarray(imageA)
        im2_arr = asarray(imageB)
        
        width, height = imageA.size
        pixel_count = width * height
        similarities = pixel_count

        for y in range(height):

            for x in range(width):

                # check pixel by pixel if R channels are same
                if im1_arr[y][x][0] != im2_arr[y][x][0]:
                    similarities -= 1

            # if similarity is lesser than given % same img and return
            if similarities / pixel_count < 0.95:

                print(similarities / pixel_count)
                self.image_count += 1
                imageB.save("ss"+str(self.image_count)+".png")
                return

    def __del__(self):

        win32gui.DeleteObject(self.saveBitMap.GetHandle())
        self.saveDC.DeleteDC()
        self.mfcDC.DeleteDC()
        win32gui.ReleaseDC(self.hwnd, self.hwndDC)

    def set_counter(self, control, number):
        
        control.key_pressed = True
        if number > -1:
            self.image_count = number   
        
class LoopControl():

    def __init__(self) -> None:
        self.key_pressed = False
        self.paused = False
        self.run = True

    def pause(self):
        self.paused = not self.paused
        self.run = not self.run

if __name__ == "__main__":

    auto_ss = Auto_ss()
    control = LoopControl()
    atexit.register(goodbye, auto_ss)

    keyboard.add_hotkey('space', auto_ss.set_counter, args=[control, -1])
    keyboard.add_hotkey('0', auto_ss.set_counter, args=[control, 0])
    print("Press 0 to start naming from 0, space to continue from previous run")
    print("Default: continue numeration\n")

    for sec in range(5,0,-1):
        if control.key_pressed:
            control.key_pressed = False
            break
        print(sec, end=".. ", flush=True)
        time.sleep(1)

    keyboard.unregister_all_hotkeys()

    print("\nCounting from "+str(auto_ss.image_count))

    image1 = auto_ss.take_screenshot()
    image1.save("ss"+str(auto_ss.image_count)+".png")

    print("Press ctrl+p to pause/continue")
    keyboard.add_hotkey('ctrl+p', control.pause)

    while True:

        while control.run:
            time.sleep(1)
            start = time.time()

            image2 = auto_ss.take_screenshot()
            auto_ss.simple_error(image1, image2)
            image1 = image2

            end = time.time()
            print("time: ", end - start)

        print("PAUSE")
        while control.paused:
            time.sleep(0.2)

        print("CONTINUE")
        




