import pyscreenshot as ImageGrab
from numpy import asarray
import time


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

        if similarities / pixel_count < 0.98:

            print(similarities / pixel_count)
            global image_count
            image_count += 1
            imageB.save("ss"+str(image_count)+".png")
            return

if __name__ == "__main__":

    im1 = ImageGrab.grab()  # X1,Y1,X2,Y2
    im1.save("ss0.png")
    image_count = 0

    while True:

        time.sleep(0.1)
        start = time.time()

        im2 = ImageGrab.grab()  # X1,Y1,X2,Y2
        simple_error(im1, im2)

        im1 = im2  # X1,Y1,X2,Y2
        end = time.time()
        print("time: ", end - start)

