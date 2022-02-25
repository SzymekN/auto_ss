import time
import win32gui
import win32ui
import atexit
from pyautogui import size as screen_size
from numpy import asarray
from ctypes import windll
from PIL import Image as Image

def goodbye():
    # try:
    #     with open("counter.txt", 'w') as file:
    #         file.write(str(image_count))
    # except:
    #     print("couldn't save")

    # win32gui.DeleteObject(saveBitMap.GetHandle())
    # saveDC.DeleteDC()
    # mfcDC.DeleteDC()
    # win32gui.ReleaseDC(hwnd, hwndDC)
    pass
        

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
        hwndDC = win32gui.GetWindowDC(self.hwnd)
        self.mfcDC  = win32ui.CreateDCFromHandle(hwndDC)
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



if __name__ == "__main__":

    atexit.register(goodbye)
    auto_ss = Auto_ss()

    image1 = auto_ss.take_screenshot()
    image1.save("ss0.png")

    while True:

        time.sleep(1)
        start = time.time()

        image2 = auto_ss.take_screenshot()
        auto_ss.simple_error(image1, image2)
        image1 = image2

        end = time.time()
        print("time: ", end - start)




