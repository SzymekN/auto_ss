import time
import win32gui
import win32ui
from pyautogui import size as screen_size
from numpy import asarray
from ctypes import windll
from PIL import Image as Image
import atexit

def goodbye(counter):
    try:
        with open("counter.txt", 'w') as file:
            file.write(counter)
    except:
        print("couldn't save")


def simple_error(imageA, imageB):

    im1_arr = asarray(imageA)
    im2_arr = asarray(imageB)
    
    width, height = imageA.size
    pixel_count = width * height
    similarities = pixel_count

    for y in range(height):

        for x in range(width):

            if im1_arr[y][x][0] != im2_arr[y][x][0]:

                similarities -= 1

        if similarities / pixel_count < 0.95:

            print(similarities / pixel_count)
            global image_count
            image_count += 1
            atexit.register(goodbye, image_count)
            imageB.save("ss"+str(image_count)+".png")
            return

toplist, winlist = [], []
def enum_cb(hwnd, results):
    winlist.append((hwnd, win32gui.GetWindowText(hwnd)))

image_count = 0

if __name__ == "__main__":

    # hwnd = win32gui.FindWindow(None, 'Michał Twaróg | Microsoft Teams')

    win32gui.EnumWindows(enum_cb, toplist)
    teams = [(hwnd, title) for hwnd, title in winlist if '| microsoft teams' in title.lower()]

    # for window in teams:
    #     print(window)

    # just grab the hwnd for first window matching teams
    print(len(teams))
    teams = teams[0]
    print(teams)
    hwnd = teams[0]

    # get screen size
    w, h = screen_size()

    hwndDC = win32gui.GetWindowDC(hwnd)
    mfcDC  = win32ui.CreateDCFromHandle(hwndDC)
    saveDC = mfcDC.CreateCompatibleDC()

    saveBitMap = win32ui.CreateBitmap()
    saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)

    saveDC.SelectObject(saveBitMap)

    # Change the line below depending on whether you want the whole window
    # or just the client area. 
    result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 3)

    # win32gui.SetForegroundWindow(hwnd)
    bmpinfo = saveBitMap.GetInfo()
    bmpstr = saveBitMap.GetBitmapBits(True)

    im1 = Image.frombuffer(
        'RGB',
        (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
        bmpstr, 'raw', 'BGRX', 0, 1)

    try:
        with open("counter.txt", 'r') as file:
            image_count = int(file.read())
    except:
        image_count = 0

    # try:
    #     counter_file = open("counter.txt", "w")
    # except:
    #     print("Couldn't open file")

    if result == 1:
        #PrintWindow Succeeded
        im1.save("ss0.png")


    run = True

    while run:

        time.sleep(1)
        start = time.time()
        
        saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)
        saveDC.SelectObject(saveBitMap)

        # Change the line below depending on whether you want the whole window
        # or just the client area. 
        result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 3)

        # win32gui.SetForegroundWindow(hwnd)
        bmpinfo = saveBitMap.GetInfo()
        bmpstr = saveBitMap.GetBitmapBits(True)

        im2 = Image.frombuffer(
            'RGB',
            (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
            bmpstr, 'raw', 'BGRX', 0, 1)

        # win32gui.DeleteObject(saveBitMap.GetHandle())
        # saveDC.DeleteDC()
        # mfcDC.DeleteDC()
        # win32gui.ReleaseDC(hwnd, hwndDC)

        if result == 1:
            #PrintWindow Succeeded
            simple_error(im1, im2)
            im1 = im2



        # im2 = ImageGrab.grab()  # X1,Y1,X2,Y2
        # simple_error(im1, im2)

        # im1 = im2  # X1,Y1,X2,Y2
        end = time.time()
        print("time: ", end - start)

    win32gui.DeleteObject(saveBitMap.GetHandle())
    saveDC.DeleteDC()
    mfcDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, hwndDC)



