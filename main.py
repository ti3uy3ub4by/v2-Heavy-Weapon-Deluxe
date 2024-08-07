from gui.mod_menu import ModMenu
from threading import Thread
from memory.memory_reader import PymemHandler
import keyboard as kb
from configs.config import OPEN
from time import sleep
import atexit
import psutil

def keybinds(modmenu):
    isopen = True
    while True:
        if kb.is_pressed(OPEN):
            if isopen:
                modmenu.win.withdraw()
                isopen = False
            else:
                modmenu.update_position()
                modmenu.win.deiconify()
                isopen = True
                modmenu.win.focus_force()
            sleep(0.5)  # Add a delay to prevent the key press from being registered multiple times

def check_game_running(modmenu):
    while True:
        game_running = any(proc.name() == "HeavyWeapon.exe" for proc in psutil.process_iter())
        if not game_running:
            modmenu.game_running = False
            modmenu.stop_hacks()
            modmenu.win.destroy()
            break
        sleep(1)

def cleanup(modmenu, mem_handler):
    modmenu.stop_hacks()
    mem_handler.close()

if __name__ == "__main__":
    mem_handler = PymemHandler("HeavyWeapon.exe")
    modmenu = ModMenu("Heavy Weapon Hack", 400, 600, mem_handler)  # Adjusted window size for tabs

    keybinds_thread = Thread(target=keybinds, args=(modmenu,))
    keybinds_thread.daemon = True
    keybinds_thread.start()

    check_game_running_thread = Thread(target=check_game_running, args=(modmenu,))
    check_game_running_thread.daemon = True
    check_game_running_thread.start()

    atexit.register(cleanup, modmenu, mem_handler)

    modmenu.win.mainloop()
