import keyboard
from os import system
from auto_ss import *
from loop_control import *
from atexit import register
from time import sleep, time


def print_menu(auto_ss):
    '''Print hotkeys and stats'''
    system("cls")
    print("Window name: "+auto_ss.window_name_found)
    print('''Hotkeys:
* ctrl+p to pause/continue
* ctrl+s to take screenshot manually
* ctrl++ to increase sensitivity
* ctrl+- to decrease sensitivity
    ''')
    print("Screenshot count: "+str(auto_ss.image_count))
    print("Current sensitivity: "+str(auto_ss.min_similarity*100)+"%")


if __name__ == "__main__":

    system('cls')

    auto_ss = Auto_ss()
    control = LoopControl()
    register(goodbye, auto_ss)

    keyboard.add_hotkey('space', auto_ss.reset_counter, args=[control, -1])
    keyboard.add_hotkey('0', auto_ss.reset_counter, args=[control, 0])
    print("Press 0 to start naming from 0, space to continue from previous run")
    print("Default: continue numeration\n")

    for sec in range(5, 0, -1):
        if control.key_pressed:
            control.key_pressed = False
            break
        print(sec, end=".. ", flush=True)
        sleep(1)

    keyboard.unregister_all_hotkeys()

    print("\nCounting from "+str(auto_ss.image_count))

    image1 = auto_ss.take_screenshot()
    auto_ss.save_screenshot(image1)

    keyboard.add_hotkey('ctrl+p', control.pause)
    keyboard.add_hotkey('ctrl+s', auto_ss.manual_screenshot)
    keyboard.add_hotkey('ctrl+plus', auto_ss.change_sensitivity, args=[True, ])
    keyboard.add_hotkey('ctrl+-', auto_ss.change_sensitivity, args=[False, ])

    while True:

        while control.run:

            # sleep to ignore animations
            sleep(1)
            print_menu(auto_ss)

            image2 = auto_ss.take_screenshot()
            # start = time()

            # compare images
            saved = auto_ss.simple_error(image1, image2)

            # end = time()
            # print("time: ", end - start)

            if saved:
                image1 = image2

        print("PAUSE")
        while control.paused:
            sleep(0.2)

        print("CONTINUE")
