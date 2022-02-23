from PIL import ImageGrab
from numpy import asarray
import time
import win32gui
import win32api
import win32ui
import win32com
from ctypes import windll
import ctypes
from PIL import Image as Image
import pyautogui


# def mse(imageA, imageB):
# 	# the 'Mean Squared Error' between the two images is the
# 	# sum of the squared difference between the two images;
# 	# NOTE: the two images must have the same dimension
# 	err = sum((imageA.astype("float") - imageB.astype("float")) ** 2)
# 	err /= float(imageA.shape[0] * imageA.shape[1])
	
# 	# return the MSE, the lower the error, the more "similar"
# 	# the two images are
# 	return err

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
    w, h = pyautogui.size()

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

    # win32gui.DeleteObject(saveBitMap.GetHandle())
    # saveDC.DeleteDC()
    # mfcDC.DeleteDC()
    # win32gui.ReleaseDC(hwnd, hwndDC)

    if result == 1:
        #PrintWindow Succeeded
        im1.save("ss0.png")


    # im1 = ImageGrab.grab()  # X1,Y1,X2,Y2
    # im1.save("ss0.png")
    # image_count = 0

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

