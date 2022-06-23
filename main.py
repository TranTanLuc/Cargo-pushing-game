import pygame
import time
from pygame.locals import *
import os
import psutil
from queue import Queue
from datetime import datetime
from sortedcontainers import SortedList
import numpy as np
from scipy.optimize import linear_sum_assignment

#thiet lap cac bien pygame
fps = 60
width = 700 #chieu rong console
height = 1100 #chieu cao console
successes, failures = pygame.init()
print("{0} successes and {1} failures".format(successes, failures))
pygame.display.set_caption("day thung")
surface = pygame.display.set_mode((height, width))
clock = pygame.time.Clock()

#thiet lap mau sac
BLACK = '#283747'
YELLOW = '#F7DC6F'
THEME = '#567BF1'
ORANGE = '#FA4304'
BLUE_LIGHT = '#440862'
RED = '#F0094F'
GRAY_LIGHT = '#E9D8DD'



#thiet lap font chu
menuFont = pygame.font.SysFont("arial", 60, bold = True)
helpFont = pygame.font.SysFont("arial", 25)
wordFont = pygame.font.SysFont("arial", 25)
recordFont = pygame.font.SysFont("arial", 17)
mapFont = pygame.font.SysFont("arial", 20, bold = True)
levelFont = pygame.font.SysFont("arial", 25, bold = True)
buttonFont = pygame.font.SysFont("arial", 18, bold = True)

#cac bien toan cuc
numsRow = 8
numsCol = 8

numsUnit = max(numsCol, numsRow)
lengthSquare = int(width / numsUnit)

offsetX = lengthSquare * (numsUnit - numsCol) / 2
offsetY = lengthSquare * (numsUnit - numsRow) / 2

map_list = ['MINI COSMOS', 'MICRO COSMOS']
map_index = 0
level = 0
mode = 0
win = 0
step = 1
timeTook = 0
pushed = 0
startTime = 0
stepNode = 0
visualized = 0
moves = []
history = 0
name = ''
actions = []
ptr = -1
itemMemory = psutil.Process(os.getpid()).memory_info().rss / (1024 * 1024)

#thiet lap hinh anh trong game
bg = pygame.image.load("imgs/bg.png")
bg = pygame.transform.scale(bg, (width, width))

wall = pygame.image.load('imgs/wall.png')
wall = pygame.transform.scale(wall, (lengthSquare, lengthSquare))

box = pygame.image.load('imgs/box.png')
box = pygame.transform.scale(box, (lengthSquare, lengthSquare))

goal = pygame.image.load('imgs/goal.png')
goal = pygame.transform.scale(goal, (lengthSquare, lengthSquare))

player_ = pygame.image.load('imgs/player.png')
player_ = pygame.transform.scale(player_, (lengthSquare, lengthSquare))

up_arrow = pygame.image.load("imgs/up_arrow.png")
up_arrow = pygame.transform.scale(up_arrow, (20, 20))

down_arrow = pygame.image.load("imgs/down_arrow.png")
down_arrow = pygame.transform.scale(down_arrow, (20, 20))

pick_button = pygame.image.load("imgs/choose.png")
pick_button = pygame.transform.scale(pick_button, (70, 35))

change = pygame.image.load("imgs/change.png")
change = pygame.transform.scale(change, (32, 32))

visualizebtn = pygame.image.load("imgs/visualizebutton.png")
visualizebtn = pygame.transform.scale(visualizebtn, (100, 100))

restartbtn = pygame.image.load("imgs/restart.png")
restartbtn = pygame.transform.scale(restartbtn, (105, 40))

undobtn = pygame.image.load("imgs/undo.png")
undobtn = pygame.transform.scale(undobtn, (35, 35))

redo_button = pygame.image.load("imgs/redo.png")
redo_button = pygame.transform.scale(redo_button, (35, 35))


#thiet lap Rectangles

up_arrow_rect = Rect(600 + 245, 0 + 200, 20, 20)
down_arrow_rect = Rect(600 + 245, 0 + 220, 20, 20)
change_rect = Rect(600 + 340, 0 + 150, 32, 32)
pick_rect = Rect(600 + 305, 0 + 198, 98, 41)
self_rect = Rect(700 + 40, 305, 110, 48)
bfs_rect = Rect(700 + 165, 305, 95, 48)
A_rect = Rect(700 + 275, 305, 95, 48)
restart_rect = Rect(700 + 160, 0 + 410, 105, 40)
visualize_rect = Rect(700 + 155, 0 + 650, 161, 34)
undo_rect = Rect(700 + 90, 0 + 410, 50, 40)
redo_rect = Rect(700 + 285, 0 + 410, 50, 40)


#thiet lap hien thi
def display_bg():
    surface.blit(bg, [0, 0])
    
def display_title():
    menuText = menuFont.render("PUSH PUSH", True, YELLOW)
    surface.blit(menuText, [700 + 60, 0 + 20])

def display_title_1(color=THEME):
    step1Text = helpFont.render("1 DO KHO", True, color)
    surface.blit(step1Text, [700 + 10, 0 + 105])


def display_up_arrow():
    surface.blit(up_arrow, [600 + 245, 0 + 200])


def display_down_arrow():
    surface.blit(down_arrow, [600 + 245, 0 + 220])


def display_change():
    surface.blit(change, [600 + 340, 0 + 150])


def display_pick_button():
    surface.blit(pick_button, [600 + 305, 0 + 198])


def display_title_content_1(color=THEME):
    statusText = helpFont.render("Map:", True, color)
    attemptedText = helpFont.render("Level:", True, color)
    surface.blit(statusText, [700 + 30, 0 + 152])
    surface.blit(attemptedText, [700 + 30, 0 + 200])


def display_map(color=GRAY_LIGHT):
    mapText = mapFont.render(f"{map_list[map_index]}", True, color)
    surface.blit(mapText, [700 + 95, 0 + 155])

def display_level(color=GRAY_LIGHT):
    levelText = levelFont.render(f"{level + 1}", True, color)
    surface.blit(levelText, [700 + 105, 0 + 200])


def display_title_2(color=THEME):
    step2Text = helpFont.render("2 CHON CHE DO CHOI", True, color)
    surface.blit(step2Text, [700 + 10, 0 + 252])


def display_button_self():
    pygame.draw.rect(surface, YELLOW, pygame.Rect(700 + 40, 305, 110, 48), 0, 6)
    step7Text = buttonFont.render("CHOI LUON", True, THEME)
    surface.blit(step7Text, [700 + 45, 318])


def display_button_BFS():
    pygame.draw.rect(surface, YELLOW, pygame.Rect(700 + 165, 305, 95, 48), 0, 6)
    step7Text = buttonFont.render("BFS", True, THEME)
    surface.blit(step7Text, [700 + 190, 318])


def display_button_A():
    pygame.draw.rect(surface, YELLOW, pygame.Rect(700 + 275, 305, 95, 48), 0, 6)
    step7Text = buttonFont.render("A*", True, THEME)
    surface.blit(step7Text, [700 + 313, 318])


def display_record():
    recordText = recordFont.render("loi giai duoc ghi o folder Results", True, RED)
    surface.blit(recordText, [700 + 10, 0 + 612])


def display_title_3(color=THEME):
    step3Text = helpFont.render("3 CHUC VUIII!!!", True, color)
    surface.blit(step3Text, [700 + 10, 0 + 365])


def display_title_content_step_3(color=ORANGE):
    statusText = helpFont.render("Status:", True, color)
    surface.blit(statusText, [700 + 26, 0 + 455])

    if not (mode >= 2 and win == 0):
        attemptedText = helpFont.render("Time:", True, color)
        stepText = helpFont.render("Step:", True, color)
        pushedText = helpFont.render("Pushed:", True, color)

        surface.blit(attemptedText, [700 + 30, 0 + 493])
        surface.blit(stepText, [700 + 30, 0 + 530])
        surface.blit(pushedText, [700 + 30, 0 + 570])


def display_content_step_3():
    status_str = ""
    if win == -1:
        status_str = ""
        status_col = ORANGE
    if win == 0:
        status_str = "Solving . . ."
        status_col = ORANGE
    elif win == 2:
        status_str = "hic khong giai duoc :<"
        status_col = ORANGE
    elif win == 1:
        status_str = "GOOD JOB =))"
        status_col = ORANGE

    statusText = wordFont.render(f"{status_str}", True, status_col)
    surface.blit(statusText, [700 + 127, 0 + 458])

    if not (mode >= 2 and win == 0):
        timeText = helpFont.render("{:0.6f} s".format(timeTook), True, ORANGE)
        stepText = helpFont.render(f"{stepNode}", True, ORANGE)
        pushedText = helpFont.render(f"{pushed}", True, ORANGE)

        surface.blit(timeText, [700 + 110, 0 + 493])
        surface.blit(stepText, [700 + 135, 0 + 530])
        surface.blit(pushedText, [700 + 135, 0 + 570])


def display_restart():
    surface.blit(restartbtn, [700 + 160, 0 + 410])


def display_visualize():
    surface.blit(visualizebtn, [700 + 150, 0 + 620])


def display_undo():
    pygame.draw.rect(surface, RED, pygame.Rect(700 + 90, 0 + 410, 50, 40), 0, 20)
    surface.blit(undobtn, [700 + 95, 0 + 410])


def display_redo():
    pygame.draw.rect(surface, RED, pygame.Rect(700 + 285, 0 + 410, 50, 40), 0, 20)
    surface.blit(redo_button, [700 + 292, 0 + 410])


def display_step_1(col=RED, mode=-1):
    display_title_1(color=col)
    if mode == -1:
        display_up_arrow()
        display_down_arrow()
        display_change()
        display_pick_button()
        display_title_content_1()
        display_map()
        display_level()
    else:
        display_title_content_1()
        display_map(GRAY_LIGHT)
        display_level(GRAY_LIGHT)


def display_step_2(col=THEME, mode=0):
    display_title_2(color=col)
    if mode == 0:
        display_button_self()
        display_button_BFS()
        display_button_A()
    elif mode == 1:
        display_button_self()
    elif mode == 2:
        display_button_BFS()
    elif mode == 3:
        display_button_A()

# xem lai
def display_step_3(col=THEME, mode=0):
    display_title_3(color=col)
    if step == 3:
        display_undo()
        display_redo()
        display_restart()
        display_title_content_step_3()
        display_content_step_3()

        if mode > 1 and win == 1:
            display_visualize()


def draw_menu():
    pygame.draw.rect(surface, BLUE_LIGHT, [700, 0, 1050, 700])
    display_bg()

    if step == 1:
        display_step_1(THEME, -1)
        display_step_2(mode=-1)
        display_step_3()
    elif step == 2:
        display_step_1(THEME, 0)
        display_step_2(THEME, mode=0)
        display_step_3()
    elif step == 3:
        display_step_1(THEME, 0)
        display_step_2(THEME, mode=mode)
        if win == 0:
            display_step_3(THEME, mode=mode)
        elif win == 1:
            display_step_3(THEME, mode=mode)
            display_record()

def draw_board():
    draw_menu()

    for point in walls:
        surface.blit(wall, [offsetX + lengthSquare * point[0], offsetY + lengthSquare * point[1]])

    for point in paths:
        pygame.draw.rect(surface, BLACK,
                         [offsetX + lengthSquare * point[0], offsetY + lengthSquare * point[1], lengthSquare,
                          lengthSquare])

    # # Debug dead_squares
    # for point in dead_squares:
    # 	pygame.draw.rect(surface, RED, [offsetX + lengthSquare * point[0], offsetY + lengthSquare * point[1], lengthSquare, lengthSquare])

    for point in goals:
        surface.blit(goal, [offsetX + lengthSquare * point[0], offsetY + lengthSquare * point[1]])

    point = player
    surface.blit(player_, [offsetX + lengthSquare * point[0], offsetY + lengthSquare * point[1]])

    for point in boxes:
        surface.blit(box, [offsetX + lengthSquare * point[0], offsetY + lengthSquare * point[1]])

    display_title()
    pygame.display.flip()


#reset data
def reset_data():
    global numsCol, numsRow, numsUnit, lengthSquare, offsetX, offsetY, wall, box, goal, player_, walls, goals, boxes, paths, player, name, distanceToGoal, dead_squares, actions, ptr

    wall = pygame.image.load('imgs/wall.png')
    box = pygame.image.load('imgs/box.png')
    goal = pygame.image.load('imgs/goal.png')
    player_ = pygame.image.load('imgs/player.png')
    name = "./Testcases/{}/{}.txt".format(map_list[map_index], level + 1)
    walls, goals, boxes, paths, player, numsRow, numsCol = set_value(name)
    distanceToGoal, dead_squares = set_distance()
    actions = []
    ptr = -1

    numsUnit = max(numsCol, numsRow)
    lengthSquare = int(width / numsUnit)

    offsetX = lengthSquare * (numsUnit - numsRow) / 2
    offsetY = lengthSquare * (numsUnit - numsCol) / 2

    wall = pygame.transform.scale(wall, (lengthSquare, lengthSquare))
    box = pygame.transform.scale(box, (lengthSquare, lengthSquare))
    goal = pygame.transform.scale(goal, (lengthSquare, lengthSquare))
    player_ = pygame.transform.scale(player_, (lengthSquare, lengthSquare))


def init_data():
    global move, win, step, timeTook, pushed, startTime, stepNode, map_index, level, board, numsRow, numsCol, numsUnit, lengthSquare, offsetX, offsetY, visualized, actions

    mode = 0
    win = 0
    step = 1
    timeTook = 0
    pushed = 0
    startTime = 0
    stepNode = 0
    visualized = 0
    actions = []
    reset_data()


#thiet lap cac cau truc du lieu va cac ham
class Direction:
    '''
    gồm một vector chỉ hướng, và ký tự đại diện cho vector đó để
    lưu kết quả ra file .txt
    '''

    def __init__(self, vector, char):
        self.vector = vector
        self.char = char

    def get_char(self):
        return self.char


# đối tượng chỉ hướng
L = Direction((-1, 0), 'L')
R = Direction((1, 0), 'R')
U = Direction((0, -1), 'U')
D = Direction((0, 1), 'D')
directions = [U, L, D, R]  # thiết lập theo chiều đồng hồ




# $$ Luật di chuyển trong bản đồ: luật bên duới áp dụng cho 4 hướng: UP, DOWN, LEFT, RIGHT
# Rule 1: nếu ô tiếp theo trống chúng ta có thể di chuyển
# Rule 2: nếu ô tiếp theo có tường, không thể di chuyển
# Rule 3: nếu ô tiếp theo có hộp:
# Rule 3.1: nếu ô tiếp theo của tiếp theo có hộp hoặc tường, không thể di chuyển
# Rule 3.2: nếu ô tiếp theo của tiếp theo không có hộp hoặc tường, chúng ta có thể di chuyển và đẩy hộp thêm 1 ô

def set_available_moves(player, boxes):
    # Setup attribute available_moves như một list chứa moves hợp lệ, là tập con của directions list (<= 4)
    # Available moves : Rule 1 + Rule 3.2
    available_moves = []
    for direction in directions:
        # ô tiếp theo có thể trống hoặc có hộp
        if (player[0] + direction.vector[0], player[1] + direction.vector[1]) not in walls:
            # ô tiếp theo là hộp
            if (player[0] + direction.vector[0], player[1] + direction.vector[1]) in boxes:
                # 3.1 và 3.2
                if ((player[0] + 2 * direction.vector[0], player[1] + 2 * direction.vector[1]) not in walls) and (
                        (player[0] + 2 * direction.vector[0], player[1] + 2 * direction.vector[1]) not in boxes):
                    available_moves.append(direction)
            else:
                # ô tiếp theo trống
                available_moves.append(direction)
    return available_moves


# di chuyển người chơi với direction, direction này phải nằm trong avaiable_moves
def move(player, boxes, direction):
    temp = (player[0] + direction.vector[0], player[1] + direction.vector[1])
    is_pushed = 0
    res = True
    boxes = set(boxes)
    if temp in boxes:
        is_pushed = 1
        boxes.remove(temp)
        boxes.add((player[0] + 2 * direction.vector[0], player[1] + 2 * direction.vector[1]))

        if (player[0] + 2 * direction.vector[0], player[1] + 2 * direction.vector[1]) in dead_squares:
            res = False
    boxes = tuple(boxes)
    player = temp
    return res, is_pushed, player, boxes


def is_win(goals, boxes):
    return goals.issubset(boxes)


def undo():
    global player, boxes, ptr, stepNode, pushed
    if ptr > -1:
        move = actions[ptr]
        boxes = set(boxes)
        if move[1] == 1:
            pushed -= 1
            boxes.remove((player[0] + move[0].vector[0], player[1] + move[0].vector[1]))
            boxes.add(player)
        boxes = tuple(boxes)
        player = (player[0] - move[0].vector[0], player[1] - move[0].vector[1])
        stepNode -= 1
        ptr -= 1


def redo():
    global player, boxes, ptr, stepNode, pushed
    if ptr < len(actions) - 1:
        _, is_pushed, player, boxes = move(player, boxes, actions[ptr + 1][0])
        ptr += 1
        stepNode += 1
        pushed += is_pushed


def set_distance():
    distanceToGoal = dict()
    dead_squares = set()
    for goal in goals:
        distanceToGoal[goal] = dict()
        for path in paths:
            distanceToGoal[goal][path] = 1e9
    queue = Queue()
    for goal in goals:
        distanceToGoal[goal][goal] = 0
        queue.put(goal)
        while not queue.empty():
            position = queue.get()
            for direction in directions:
                boxPosition = (position[0] + direction.vector[0], position[1] + direction.vector[1])
                playerPosition = (position[0] + 2 * direction.vector[0], position[1] + 2 * direction.vector[1])
                if boxPosition in paths:
                    if distanceToGoal[goal][boxPosition] == 1e9:
                        if (boxPosition not in walls) and (playerPosition not in walls):
                            distanceToGoal[goal][boxPosition] = distanceToGoal[goal][position] + 1
                            queue.put(boxPosition)
    # dead squares, để giảm không gian trạng thái
    for path in paths:
        ok = 1
        for goal in goals:
            if distanceToGoal[goal][path] != 1e9:
                ok = 0
                break
        if ok == 1:
            dead_squares.add(path)
    return distanceToGoal, dead_squares


def minimum_cost(step, boxes):
    # ghép tất cả các khoảng cách từ tất cả các đích đến các boxes để cho tổng là nhỏ nhất: Hungarian Algorithm
    temp = []
    for goal in goals:
        for box in boxes:
            # # Manhattan distance
            # temp.append(abs(goal[0] - box[0]) + abs(goal[1] - box[1]))

            # Using DistanceToGoal 2d-array
            temp.append(distanceToGoal[goal][box])

    arr = np.array(temp)
    # tạo matrix với row: goal và colum: box
    cost = arr.reshape(len(goals), len(boxes))
    row_ind, col_ind = linear_sum_assignment(cost)  # Hungarian Algorithm
    return cost[row_ind, col_ind].sum() + step  # f(n) = g(n) + h(n)


def set_value(filename):
    walls = set()  # tập hợp các tọa độ
    goals = set()
    boxes = []
    paths = set()
    player = None
    x = 0
    y = 0
    with open(filename, 'r') as f:
        read_data = f.read()
        lines = read_data.split('\n')
        for line in lines:
            x = 0
            for char in line:
                if char == '#':  # Wall
                    walls.add((x, y))
                elif char == 'x':  # Box
                    boxes.append((x, y))
                    paths.add((x, y))
                elif char == '?':  # Goal
                    goals.add((x, y))
                    paths.add((x, y))
                elif char == '@':  # Player
                    player = (x, y)
                    paths.add((x, y))
                elif char == '-':  # Player and Goal
                    goals.add((x, y))
                    player = (x, y)
                    paths.add((x, y))
                elif char == '+':  # Box and Goal
                    goals.add((x, y))
                    boxes.append((x, y))
                    paths.add((x, y))
                elif char == '.':  # Path - avaiable move
                    paths.add((x, y))
                x += 1
            y += 1
    return walls, goals, tuple(boxes), paths, player, x, y





def line_prepender(filename, algo, sol, ste, gen, rep, expl, memo, dur):
    if not os.path.exists('Results'):
        os.mkdir('Results')
    if not os.path.exists(filename):
        open(filename, 'w+')
    with open(filename, 'r+') as f:
        content = f.read()
        f.seek(0, 0)
        dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S %p")
        f.write(dt_string + '\n')
        f.write("test case: " + name.split('./')[-1] + '\n')
        f.write("algorithm: " + algo + '\n')
        f.write("loi giai: " + sol + '\n')
        f.write("so buoc: " + str(ste) + '\n')
        f.write("so node duoc sinh: " + str(gen) + '\n')
        f.write("so node lap: " + str(rep) + '\n')
        f.write("so node mo rong: " + str(expl) + '\n')
        f.write("bo nho: " + str(memo) + ' MB' + '\n')
        f.write("thoi gian: " + str(dur) + " secs" + '\n')
        f.write("\n\n")
        f.write("===================================================" + '\n')
        f.write("===================================================" + '\n')
        f.write("\n\n")
        f.write(content)


def add_history(algo, sol, ste, gen, rep, expl, memo, dur):
    line_prepender('Results/history_log.txt', algo, sol, ste, gen, rep, expl, memo, dur)
    line_prepender('Results/Solution_{}_test {}'.format(name.split('/')[2], name.split('/')[3]), algo, sol, ste, gen,
                   rep, expl, memo, dur)


def get_history_moves(actions):
    return ", ".join(list(map(lambda move: move[0].char, actions)))


#thiet lap thuat toan
def bfs(curr_player, curr_boxes):
    global win, timeTook, startTime
    node_repeated = 0
    node_generated = 0
    frontier = Queue()
    explored = set()
    frontier.put((curr_player, curr_boxes, 0, 0, []))

    node_generated += 1
    explored.add((curr_player, curr_boxes))
    startTime = time.time()
    while True:
        if frontier.empty():
            print("Solution not found\n")
            return (0, 0, 0, 0, [])

        (now_player, now_boxes, steps, push, actions) = frontier.get()
        moves = set_available_moves(now_player, now_boxes)
        for m in moves:
            res, is_pushed, new_player, new_boxes = move(now_player, now_boxes, m)
            if (new_player, new_boxes) not in explored and res == True:
                explored.add((new_player, new_boxes))
                if is_win(goals, new_boxes):
                    timeTook = time.time() - startTime
                    win = 1
                    memo_info = psutil.Process(os.getpid()).memory_info().rss / (1024 * 1024) - itemMemory
                    add_history("Breadth First Search", get_history_moves(actions + [(m, is_pushed)]), steps + 1,
                                node_generated, node_repeated, len(explored), memo_info, timeTook)
                    return (node_generated + 1, steps + 1, timeTook, memo_info, actions + [(m, is_pushed)])
                frontier.put((new_player, new_boxes, steps + 1, push + is_pushed, actions + [(m, is_pushed)]))
            else:
                node_repeated += 1
            node_generated += 1


def A_star(curr_player, curr_boxes):
    global win, timeTook, startTime
    node_repeated = 0
    node_generated = 0
    frontier = SortedList(key=lambda x: minimum_cost(x[2], x[1]))
    explored = set()
    frontier.add((curr_player, curr_boxes, 0, 0, []))
    node_generated += 1
    explored.add((curr_player, curr_boxes))
    startTime = time.time()
    while True:
        if len(frontier) == 0:
            print("Solution not found\n")
            return (0, 0, 0, 0, [])

        (now_player, now_boxes, steps, push, actions) = frontier.pop(0)
        moves = set_available_moves(now_player, now_boxes)
        for m in moves:
            res, is_pushed, new_player, new_boxes = move(now_player, now_boxes, m)
            if (new_player, new_boxes) not in explored and res == True:
                explored.add((new_player, new_boxes))
                if is_win(goals, new_boxes):
                    timeTook = time.time() - startTime
                    win = 1
                    memo_info = psutil.Process(os.getpid()).memory_info().rss / (1024 * 1024) - itemMemory
                    add_history("A star", get_history_moves(actions + [(m, is_pushed)]), steps + 1, node_generated,
                                node_repeated, len(explored), memo_info, timeTook)
                    return (node_generated + 1, steps + 1, timeTook, memo_info, actions + [(m, is_pushed)])
                frontier.add((new_player, new_boxes, steps + 1, push + is_pushed, actions + [(m, is_pushed)]))
            else:
                node_repeated += 1
            node_generated += 1


#main
if __name__ == '__main__':
    name = "./Testcases/{}/{}.txt".format(map_list[0], 1)
    walls, goals, boxes, paths, player, _, _ = set_value(name)
    distanceToGoal, dead_squares = set_distance()

    while True:
        clock.tick(fps)
        if is_win(goals, boxes) == True and mode == 1:
            win = 1
            # This result has been recorded in Results folder
            if history == 0:
                add_history("manually", get_history_moves(actions), stepNode, 0, 0, 0, 0, timeTook)
                history = 1

        if step == 3 and win == 0 and mode == 1:
            timeTook = time.time() - startTime

        if step == 3 and mode == 2 and win == 0:
            (node_created, steps, times, memo, moves) = bfs(player, boxes)

        if step == 3 and mode == 3 and win == 0:
            (node_created, steps, times, memo, moves) = A_star(player, boxes)

        if len(moves) > 0 and visualized == 1:
            (_, is_pushed, player, boxes) = move(player, boxes, moves[0][0])
            actions.append(moves[0])
            moves.pop(0)
            stepNode += 1
            pushed += is_pushed
            ptr += 1
            time.sleep(0.3)

        for event in pygame.event.get():
            keys_pressed = pygame.key.get_pressed()
            if event.type == pygame.QUIT or keys_pressed[pygame.K_q]:
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if step == 3:
                    if mode == 1 and win == 0:
                        if event.key == pygame.K_w or event.key == pygame.K_UP:
                            if U in set_available_moves(player, boxes):
                                if ptr + 1 < len(actions):
                                    actions = actions[0:(ptr + 1)]
                                (_, is_pushed, player, boxes) = move(player, boxes, U)
                                stepNode += 1
                                pushed += is_pushed
                                ptr += 1
                                actions.append((U, is_pushed))
                        elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                            if D in set_available_moves(player, boxes):
                                if ptr + 1 < len(actions):
                                    actions = actions[0:(ptr + 1)]
                                (_, is_pushed, player, boxes) = move(player, boxes, D)
                                stepNode += 1
                                pushed += is_pushed
                                ptr += 1
                                actions.append((D, is_pushed))
                        elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                            if L in set_available_moves(player, boxes):
                                if ptr + 1 < len(actions):
                                    actions = actions[0:(ptr + 1)]
                                (_, is_pushed, player, boxes) = move(player, boxes, L)
                                stepNode += 1
                                pushed += is_pushed
                                ptr += 1
                                actions.append((L, is_pushed))
                        elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                            if R in set_available_moves(player, boxes):
                                if ptr + 1 < len(actions):
                                    actions = actions[0:(ptr + 1)]
                                (_, is_pushed, player, boxes) = move(player, boxes, R)
                                stepNode += 1
                                pushed += is_pushed
                                ptr += 1
                                actions.append((R, is_pushed))

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos

                if step == 1:
                    if up_arrow_rect.collidepoint(x, y):
                        level = (level + 1) % 40
                        reset_data()
                    if down_arrow_rect.collidepoint(x, y):
                        level = (level + 39) % 40
                        reset_data()
                    if change_rect.collidepoint(x, y):
                        map_index = 1 - map_index
                        reset_data()
                    if pick_rect.collidepoint(x, y):
                        step = 2

                if step == 2:
                    if self_rect.collidepoint(x, y):
                        mode = 1
                        step = 3
                        startTime = time.time()
                    if bfs_rect.collidepoint(x, y):
                        mode = 2
                        step = 3
                        continue
                    if A_rect.collidepoint(x, y):
                        mode = 3
                        step = 3
                        continue

                if step == 3:
                    if mode == 1:
                        if restart_rect.collidepoint(x, y):
                            init_data()
                            step = 1
                        if undo_rect.collidepoint(x, y):
                            undo()
                        if redo_rect.collidepoint(x, y):
                            redo()
                    if mode == 2:
                        # Bfs
                        if restart_rect.collidepoint(x, y):
                            init_data()
                            step = 1
                        if win == 1:
                            if visualized == 0:
                                if visualize_rect.collidepoint(x, y):
                                    visualized = 1
                            else:
                                if undo_rect.collidepoint(x, y):
                                    undo()
                                if redo_rect.collidepoint(x, y):
                                    redo()
                    if mode == 3:
                        # A_star
                        if restart_rect.collidepoint(x, y):
                            init_data()
                            step = 1
                        if win == 1:
                            if visualized == 0:
                                if visualize_rect.collidepoint(x, y):
                                    visualized = 1
                            else:
                                if undo_rect.collidepoint(x, y):
                                    undo()
                                if redo_rect.collidepoint(x, y):
                                    redo()

        draw_board()
        pygame.display.update()