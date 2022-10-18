#!/usr/bin/python3

import os
import signal
import keyboard
import time
import random

widthandheight = str(os.popen("stty size").read())
widthandheightS = widthandheight.strip().rsplit(" ")
WIDTH = int(widthandheightS[1])
HEIGHT = int(widthandheightS[0]) - 3

snake_head = "o" #YOU CAN CHANGE THIS
snake_body = "o" #YOU CAN CHANGE THIS
snake_food = "*" #YOU CAN CHANGE THIS
wallUD = "#" #YOU CAN CHANGE THIS
wallLR = "#" #YOU CAN CHANGE THIS
DIRECTION = "RIGHT"

CORDS = {
    "snake_head" : {
        "snake_x" : 5,
        "snake_y" : 5
    },
    "snake_food" : {
        "snake_food_x" : random.randint(0, WIDTH - 4),
        "snake_food_y" : random.randint(0, HEIGHT - 4)
    },
}

def clear(): os.system("clear")
snake_body_list = []
score = []

def main_page():
    clear()
    BANNER = r"""    
       _____ _   _          _  ________ 
      / ____| \ | |   /\   | |/ /  ____|
     | (___ |  \| |  /  \  | ' /| |__   
      \___ \| . ` | / /\ \ |  < |  __|  
      ____) | |\  |/ ____ \| . \| |____ 
     |_____/|_| \_/_/    \_\_|\_\______|                                       
                MADE BY DAHNI
    ____________________________________________
    """
    print(BANNER)
    print("\nPress space to start")
    while True:
        if keyboard.is_pressed("space"):
            break

def game_over():
    clear()
    BANNER = r"""
           _____          __  __ ______    ______      ________ _____  
          / ____|   /\   |  \/  |  ____|  / __ \ \    / /  ____|  __ \ 
         | |  __   /  \  | \  / | |__    | |  | \ \  / /| |__  | |__) |
         | | |_ | / /\ \ | |\/| |  __|   | |  | |\ \/ / |  __| |  _  / 
         | |__| |/ ____ \| |  | | |____  | |__| | \  /  | |____| | \ \ 
          \_____/_/    \_\_|  |_|______|  \____/   \/   |______|_|  \_\
                                CREATED BY DAHNI
    _________________________________________________________________________
                                -> Your score is {}
    """.format(len(score))
    print(BANNER)
    exit(1)

def handler(sing,frame): game_over()
signal.signal(signal.SIGINT, handler)

def add(cords_list, direction, head_x, head_y):
    if len(cords_list) == 0:
        if direction == "RIGHT": cords_list.append([head_x - 1,head_y])
        elif direction == "LEFT": cords_list.append([head_x + 1, head_y])
        elif direction == "UP": cords_list.append([head_x,head_y + 1])
        elif direction == "DOWN": cords_list.append([head_x, head_y - 1])
    elif len(cords_list) == 1:
        element = cords_list[0]
        element_x = element[0]
        element_y = element[1]
        if direction == "RIGHT": cords_list.append([element_x - 1,element_y])
        elif direction == "LEFT": cords_list.append([element_x + 1, element_y])
        elif direction == "UP": cords_list.append([element_x,element_y + 1])
        elif direction == "DOWN": cords_list.append([element, element_y - 1])
    else:
        last_element = cords_list[len(cords_list) - 1]
        last_element_x = last_element[0]
        last_element_y = last_element[1]
        if cords_list[len(cords_list) - 2][1] > last_element_y: cords_list.append([last_element_x,last_element_y - 1])
        elif cords_list[len(cords_list) - 2][1] < last_element_y: cords_list.append([last_element_x,last_element_y + 1])
        elif cords_list[len(cords_list) - 2][0] > last_element_x: cords_list.append([last_element_x - 1,last_element_y])
        elif cords_list[len(cords_list) - 2][0] < last_element_x: cords_list.append([last_element_x + 1,last_element_y])

def moveX(head_x,head_y,cord_list):
    if len(cord_list) >= 2:
        for x in range(1, len(cord_list)):
            cord_list[len(cord_list) - x] = cord_list[(len(cord_list) - x) - 1]
        cord_list[0] = [head_x,head_y]
    elif len(cord_list) == 1:
        cord_list[0][0] = head_x
        cord_list[0][1] = head_y
    else:
        pass
    
def drawBoard(grid):
    for _ in range(WIDTH): grid.append(wallUD)
    for y in range(0, HEIGHT):
        grid.append(wallLR)
        for x in range(0, WIDTH - 1):
            if x == CORDS["snake_head"]["snake_x"] and y == CORDS["snake_head"]["snake_y"]: grid.append(snake_head)
            elif [CORDS["snake_head"]["snake_x"], CORDS["snake_head"]["snake_y"]] in snake_body_list: game_over()
            elif x == CORDS["snake_food"]["snake_food_x"] and y == CORDS["snake_food"]["snake_food_y"]: grid.append(snake_food)
            elif [x,y] in snake_body_list: grid.append(snake_body)
            elif CORDS["snake_head"]["snake_x"] == -1: game_over()
            elif CORDS["snake_head"]["snake_x"] == WIDTH - 2: game_over()
            elif CORDS["snake_head"]["snake_y"] == -1: game_over()
            elif CORDS["snake_head"]["snake_y"] == HEIGHT: game_over()
            elif CORDS["snake_head"]["snake_x"] == CORDS["snake_food"]["snake_food_x"] and CORDS["snake_head"]["snake_y"] == CORDS["snake_food"]["snake_food_y"]:
                CORDS["snake_food"]["snake_food_x"] = random.randint(0, WIDTH - 4)
                CORDS["snake_food"]["snake_food_y"] = random.randint(0, HEIGHT - 4)
                add(snake_body_list, DIRECTION, CORDS["snake_head"]["snake_x"], CORDS["snake_head"]["snake_y"])
                score.append("point")
            else:
                if x == WIDTH - 2:
                    grid.append(wallLR)
                else:
                    grid.append(" ")
    
    for _ in range(WIDTH): grid.append(wallUD)

def updateScreen():
    grid = []
    drawBoard(grid)
    screen = "".join(grid)
    print(screen)
    time.sleep(0.1) #YOU CAN CHANGE THIS
    clear()    

if __name__ == "__main__":
    main_page()
    while True:
        updateScreen()
        if keyboard.is_pressed("a"):
            if DIRECTION != "RIGHT":
                CORDS["snake_head"]["snake_x"] -= 1
                moveX(CORDS["snake_head"]["snake_x"] + 1,CORDS["snake_head"]["snake_y"],snake_body_list)
                DIRECTION = "LEFT"
        elif keyboard.is_pressed("d"):
            if DIRECTION != "LEFT":
                CORDS["snake_head"]["snake_x"] += 1
                moveX(CORDS["snake_head"]["snake_x"] - 1,CORDS["snake_head"]["snake_y"],snake_body_list)
                DIRECTION = "RIGHT"
        elif keyboard.is_pressed("w"): 
            if DIRECTION != "DOWN":
                CORDS["snake_head"]["snake_y"] -= 1
                moveX(CORDS["snake_head"]["snake_x"],CORDS["snake_head"]["snake_y"] + 1,snake_body_list)
                DIRECTION = "UP"
        elif keyboard.is_pressed("s"):
            if DIRECTION != "UP":
                CORDS["snake_head"]["snake_y"] += 1
                moveX(CORDS["snake_head"]["snake_x"],CORDS["snake_head"]["snake_y"] - 1,snake_body_list)
                DIRECTION = "DOWN"
        else:
            if DIRECTION == "RIGHT":
                CORDS["snake_head"]["snake_x"] += 1
                moveX(CORDS["snake_head"]["snake_x"] - 1,CORDS["snake_head"]["snake_y"],snake_body_list)
            elif DIRECTION == "LEFT":
                CORDS["snake_head"]["snake_x"] -= 1
                moveX(CORDS["snake_head"]["snake_x"] + 1,CORDS["snake_head"]["snake_y"],snake_body_list)
            elif DIRECTION == "UP":
                CORDS["snake_head"]["snake_y"] -= 1
                moveX(CORDS["snake_head"]["snake_x"],CORDS["snake_head"]["snake_y"] + 1,snake_body_list)
            elif DIRECTION == "DOWN":
                CORDS["snake_head"]["snake_y"] += 1
                moveX(CORDS["snake_head"]["snake_x"],CORDS["snake_head"]["snake_y"] - 1,snake_body_list)
