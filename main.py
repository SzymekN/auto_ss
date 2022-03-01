import keyboard
from auto_ss import *
from loop_control import *
from atexit import register
from time import sleep, time


if __name__ == "__main__":

    auto_ss = Auto_ss()
    control = LoopControl()
    register(goodbye, auto_ss)

    keyboard.add_hotkey('space', auto_ss.reset_counter, args=[control, -1])
    keyboard.add_hotkey('0', auto_ss.reset_counter, args=[control, 0])
    print("Press 0 to start naming from 0, space to continue from previous run")
    print("Default: continue numeration\n")

    for sec in range(5,0,-1):
        if control.key_pressed:
            control.key_pressed = False
            break
        print(sec, end=".. ", flush=True)
        sleep(1)

    keyboard.unregister_all_hotkeys()

    print("\nCounting from "+str(auto_ss.image_count))

    image1 = auto_ss.take_screenshot()
    image1.save("ss"+str(auto_ss.image_count)+".png")

    print("Press ctrl+p to pause/continue")
    keyboard.add_hotkey('ctrl+p', control.pause)

    while True:

        while control.run:
            sleep(1)
            start = time()

            image2 = auto_ss.take_screenshot()

            #compare images
            auto_ss.simple_error(image1, image2)

            image1 = image2

            end = time()
            print("time: ", end - start)

        print("PAUSE")
        while control.paused:
            sleep(0.2)

        print("CONTINUE")
        




