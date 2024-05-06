# from pynput import keyboard
# from pynput.keyboard import Key

# def on_key_release(key):
#     if key == Key.right:
#         print("Right key clicked")

#     elif key == Key.esc:
#         exit()

# with keyboard.Listener(on_release=on_key_release) as listener:
#     listener.join()

import keyboard

def print_right(event):
    print("right")

keyboard.on_press_key("right", print_right)

keyboard.wait()

# while True:
#     try:
#         if keyboard.is_pressed('left'):
#             print("left")
#         time.sleep(0.1)
#     except:
#         break