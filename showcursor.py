from Xlib.display import Display
import time

def main():
    display = Display()

    print(display.screen())
    if not display.has_extension('XFIXES'):
        if display.query_extension('XFIXES') is None:
            print('XFIXES extension not supported')


    screen = display.screen()

    screen.root.xfixes_hide_cursor()
    display.sync()

    time.sleep(1)

    screen.root.xfixes_show_cursor()
    display.sync()

main()