import win32gui
import win32ui
from pyautogui import size as screen_size
from numpy import asarray, count_nonzero
from ctypes import windll
from PIL import Image as Image


def goodbye(auto_ss):
    '''Function executed at exit, saves counter to file'''
    try:
        with open("counter.txt", 'w') as file:
            file.write(str(auto_ss.image_count))
    except:
        print("couldn't save")


class Auto_ss():
    '''Main class in script, handles finding wanted window and making screen shots'''

    def enum_cb(self, hwnd, results):
        '''Function getting information about all procesess and it's handles'''

        self.winlist.append((hwnd, win32gui.GetWindowText(hwnd)))

    def _get_window_handle(self):
        '''Function gets handle to wanted window, and saves it'''

        # get all windows
        win32gui.EnumWindows(self.enum_cb, self.toplist)

        # get windows with matching title
        windows = [(hwnd, title) for hwnd,
                   title in self.winlist if self.window_name_to_search in title.lower()]

        # error if couldn't find any window
        if not windows:
            print("ERROR! No windows found")
            exit()

        # choose first found window with matching title
        window = windows[0]
        print(window)

        # handle to wanted window
        self.hwnd = window[0]
        self.window_name_found = window[1]

    def _create_context(self):
        '''Create new context from window handle'''

        self.hwndDC = win32gui.GetWindowDC(self.hwnd)
        self.mfcDC = win32ui.CreateDCFromHandle(self.hwndDC)
        self.saveDC = self.mfcDC.CreateCompatibleDC()

    def take_screenshot(self):
        '''Take screenshot of an app'''

        # Create bitmap compatibile with window DC
        self.saveBitMap.CreateCompatibleBitmap(self.mfcDC, self.w, self.h)
        self.saveDC.SelectObject(self.saveBitMap)

        # if screen taken succesfully, result == 1
        result = windll.user32.PrintWindow(
            self.hwnd, self.saveDC.GetSafeHdc(), 3)

        # put window on foreground
        # win32gui.SetForegroundWindow(hwnd)
        bmpinfo = self.saveBitMap.GetInfo()
        bmpstr = self.saveBitMap.GetBitmapBits(True)

        # Create image
        im = Image.frombuffer(
            'RGB',
            (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
            bmpstr, 'raw', 'BGRX', 0, 1)

        # if screenshot taken succesfully return image, else exit script
        if result == 1:
            return im
        else:
            print("WARNING! Couldn't take screenshot")
            exit()

    def save_screenshot(self, image):
        '''Save image and counter'''

        print("saving ss"+str(self.image_count)+".png...")
        image.save("ss"+str(self.image_count)+".png")
        self.image_count += 1

        try:
            with open("counter.txt", 'w') as file:
                file.write(str(self.image_count))

        except:
            print("couldn't save")

    def manual_screenshot(self):
        '''Take screenshot manually, without checking similarities'''

        image = self.take_screenshot()
        self.save_screenshot(image)

    def _get_counter(self):
        '''Read counter value saved to file'''

        try:
            with open("counter.txt", 'r') as file:
                self.image_count = int(file.read())
        except:
            self.image_count = 0

    def __init__(self) -> None:
        '''Get all needed data to make screenshots of one app'''

        self.window_name_to_search = '| microsoft teams'
        # self.window_name_to_search = "opera"
        self.toplist, self.winlist = [], []

        # uncomment when you have your app on main screen
        # self.w, self.h = screen_size()
        self.w, self.h = 1920, 1080
        self.min_similarity = 0.95

        self._get_window_handle()
        self._create_context()
        self.saveBitMap = win32ui.CreateBitmap()
        self._get_counter()

    def simple_error(self, imageA, imageB):
        '''Calculate how many differences are in particular pixels on two images'''

        im1_arr = asarray(imageA)
        im2_arr = asarray(imageB)

        differences = count_nonzero(im1_arr != im2_arr)

        width, height = self.w, self.h
        all_subpixels = width * height * 3
        print("Similarity: " + str((1 - (differences / (all_subpixels))) * 100)+"%")

        if self.min_similarity == 1:
            self.save_screenshot(imageB)
            return True

        # if similarity is lesser than given % save img and return
        if (differences / all_subpixels) >= (1 - self.min_similarity):
            self.save_screenshot(imageB)
            return True

        return False

    def __del__(self):
        '''Delete used contexts'''

        win32gui.DeleteObject(self.saveBitMap.GetHandle())
        self.saveDC.DeleteDC()
        self.mfcDC.DeleteDC()
        win32gui.ReleaseDC(self.hwnd, self.hwndDC)

    def reset_counter(self, control, number):
        '''Force setting image count to 0'''

        control.key_pressed = True
        if number > -1:
            self.image_count = number

    def change_sensitivity(self, value):
        '''Change needed similarity between two images'''

        if (self.min_similarity >= 1 and value) or (self.min_similarity <= 0 and not value):
            if self.min_similarity >= 1:
                print("Max sensitivity")
            else:
                print("Min sensitivity")
            return

        if value:
            if self.min_similarity >= 0.99:
                self.min_similarity += 0.001
            else:
                self.min_similarity += 0.01
        else:
            if self.min_similarity >= 0.99:
                self.min_similarity -= 0.001
            else:
                self.min_similarity -= 0.01

        self.min_similarity = round(self.min_similarity, 3)

        print("Current needed similarity: "+str(self.min_similarity*100)+"%")
