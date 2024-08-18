import random
from pytesseract import pytesseract
import cv2
import pyautogui
import mss
import numpy
from playsound import playsound
import keyboard
from config import *

pytesseract.tesseract_cmd = path_to_tesseract
POSITION = "RANDOM"
PRESSED_SHIFT = False
cluster_pos = {"x1": 1100, "x2": 1400, "y1": 450, "y2": 590}
cluster_pos_img = {"top": 400, "left": 1000, "width": 600, "height": 187}
alteration_pos_img = {"top": 242, "left": 87, "width": 35, "height": 30}
items_rarity = {1: "normal", 2: "magic", 3: "rare"}
amount_clusters = clusters_in_your_inventory
pos_xy = 52
current_cluster = 1
expensive_passives = [["BLADES", "FURY"]]


class Inventory:
    def __init__(self):
        self.inventory = [[0, 0, 0, 0, 0] for _ in range(12)]
        for i in range(amount_clusters):
            self.inventory[i // 5][i % 5] = 1


class Cluster:
    def __init__(self):
        self.passives = 0
        self.rarity = items_rarity[1]
        self.modifiers = 0

    def scouring(self):
        self.__init__()


inv = Inventory()
cluster = Cluster()


def time_delay():
    if imitation_people:
        return round(random.uniform(0.1, 1), 2)
    return 0


def pos_slot_1():
    return random.randint(1293, 1297), random.randint(613, 619)


def dpos_slot(slot):
    return random.randint(1293, 1297) + pos_xy * ((slot - 1) // 5), random.randint(613, 619) + pos_xy * ((slot - 1) % 5)


def pos_alteration():
    return random.randint(107, 113), random.randint(267, 273)


def pos_augmentation():
    return random.randint(223, 229), random.randint(325, 331)


def pos_transmutation():
    return random.randint(51, 57), random.randint(270, 276)


def pos_regal():
    return random.randint(435, 441), random.randint(266, 272)


def pos_scouring():
    return random.randint(435, 441), random.randint(503, 509)


def move_to_item(x=0, y=0):
    global POSITION
    if x == 0 and y == 0:
        pyautogui.moveTo(*pos_slot_1(), time_delay())
    else:
        pyautogui.moveTo(x, y, time_delay())


def move_to_alteration():
    global POSITION
    if POSITION != "ALTERATION":
        POSITION = "ALTERATION"
        pyautogui.moveTo(*pos_alteration(), time_delay())
        
        
def move_to_augmentation():
    global POSITION
    if POSITION != "AUGMENTATION":
        POSITION = "AUGMENTATION"
        pyautogui.moveTo(*pos_augmentation(), time_delay())


def move_to_transmutation():
    global POSITION
    pyautogui.moveTo(*pos_transmutation(), time_delay())


def move_to_regal():
    global POSITION
    if POSITION != "REGAL":
        POSITION = "REGAL"
        pyautogui.moveTo(*pos_regal(), time_delay())


def move_to_scouring():
    global POSITION
    if POSITION != "SCOURING":
        POSITION = "SCOURING"
        pyautogui.moveTo(*pos_scouring(), time_delay())


def check_expensive_passives(text):
    for word in text.split():
        if ("B1ADES" in word or "BLADES" in word) and ("FURY" in word):
            return True


def main():
    global current_cluster, POSITION, PRESSED_SHIFT
    with mss.mss() as sct:
        while "Screen capturing":
            move_to_item()
            cluster_img = numpy.array(sct.grab(cluster_pos_img))
            text = pytesseract.image_to_string(cluster_img)
            if keyboard.is_pressed('q'):
                if PRESSED_SHIFT:
                    pyautogui.keyUp("shift")
                break
            count_passives = 0
            modifiers = 0
            tsplit = text.split()
            for i in range(len(tsplit)):
                if (not (i+1 >= len(tsplit))) and (not (i+5 >= len(tsplit))) and "1" == tsplit[i] and "DDED" in tsplit[i+1] and "A" != tsplit[i+5]:
                    count_passives += 1
                    modifiers += 1
            for i in range(len(tsplit)):
                if ("ALSO" in tsplit[i] or "AlSO" in tsplit[i] or "A1SO" in tsplit[i]) or (tsplit[i] == "SKILLS" and tsplit[i+1] == "HAVE"):
                    modifiers += 1
            cluster.modifiers = modifiers
            cluster.passives = count_passives
            if debug:
                print(cluster.modifiers, cluster.passives, cluster.rarity, current_cluster)
            if cluster.rarity == items_rarity[1]:
                if debug:
                    print("transmutation")
                move_to_transmutation()
                pyautogui.rightClick()
                move_to_item()
                pyautogui.leftClick()
                cluster.rarity = items_rarity[2]
                continue
            if cluster.passives == 1 and cluster.modifiers == 1:
                if debug:
                    print("augmentation")
                if PRESSED_SHIFT:
                    pyautogui.keyUp("shift")
                    PRESSED_SHIFT = False
                move_to_augmentation()
                pyautogui.rightClick()
                move_to_item()
                pyautogui.leftClick()
                continue
            if cluster.passives == 2 and cluster.rarity == items_rarity[2]:
                if debug:
                    print("regal")
                if PRESSED_SHIFT:
                    pyautogui.keyUp("shift")
                    PRESSED_SHIFT = False
                move_to_regal()
                pyautogui.rightClick()
                move_to_item()
                pyautogui.leftClick()
                cluster.rarity = items_rarity[3]
                continue
            if cluster.passives == 2 and cluster.rarity == items_rarity[3]:
                if debug:
                    print("scouring")
                move_to_scouring()
                pyautogui.rightClick()
                move_to_item()
                pyautogui.leftClick()
                cluster.scouring()
                continue
            if (cluster.passives < 2 and cluster.rarity == items_rarity[2]) or (cluster.modifiers <= 2 and cluster.rarity == items_rarity[2]):
                if debug:
                    print("alteration")
                if not PRESSED_SHIFT:
                    pyautogui.keyDown("shift")
                    PRESSED_SHIFT = True
                    move_to_alteration()
                    pyautogui.rightClick()
                    move_to_item()
                    pyautogui.leftClick()
                    continue
                else:
                    pyautogui.leftClick()
                    continue
            if (cluster.passives == 3) or check_expensive_passives(text):
                if debug:
                    print(f"done {current_cluster} cluster")
                if sounds:
                    playsound('sounds/uwu.mp3')
                move_to_item()
                pyautogui.leftClick()
                move_to_item(*dpos_slot(61-current_cluster))
                pyautogui.leftClick()
                current_cluster += 1
                cluster.scouring()
                if current_cluster == (amount_clusters+1):
                    if sounds:
                        playsound("sounds/omg.mp3")
                    break
                move_to_item(*dpos_slot(current_cluster))
                pyautogui.leftClick()
                move_to_item()
                pyautogui.leftClick()
                if debug:
                    print("relocated")
                continue
            if (cv2.waitKey(0) & 0xFF) == 27:
                if PRESSED_SHIFT:
                    pyautogui.keyUp("shift")
                cv2.destroyAllWindows()
                break


main()
