import time
import os
import psutil
from queue import Queue
from sortedcontainers import SortedList
import numpy as np
from scipy.optimize import linear_sum_assignment


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


# đối tượng hướng, thiết lập theo chiều đồng hồ
L = Direction((-1, 0), 'L')
R = Direction((1, 0), 'R')
U = Direction((0, -1), 'U')
D = Direction((0, 1), 'D')
directions = [U, L, D, R]


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
            ## Using Manhattan distance
            # temp.append(abs(goal[0] - box[0]) + abs(goal[1] - box[1]))

            ## Using DistanceToGoal 2d-array
            temp.append(distanceToGoal[goal][box])

    arr = np.array(temp)
    # tạo matrix với row: goal và colum: box
    cost = arr.reshape(len(goals), len(boxes))
    row_ind, col_ind = linear_sum_assignment(cost)  # Hungarian Algorithm
    return cost[row_ind, col_ind].sum() + step  # f(n) = g(n) + h(n)


def set_available_moves(player, boxes):
    # thiết lập thuộc tính available_moves là list chứa move hợp lệ (là một tập con của list direction = [U,L,R,D])
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
    res = True
    boxes = set(boxes)
    if temp in boxes:
        boxes.remove(temp)
        boxes.add((player[0] + 2 * direction.vector[0], player[1] + 2 * direction.vector[1]))

        if (player[0] + 2 * direction.vector[0], player[1] + 2 * direction.vector[1]) in dead_squares:
            res = False
    boxes = tuple(boxes)
    player = temp
    return res, player, boxes


def is_win(goals, boxes):
    return goals.issubset(boxes)


def set_value(filename):
    walls = set()  # set of Point()
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
    return walls, goals, tuple(boxes), paths, player


map_list = ['MINI COSMOS', 'MICRO COSMOS']
itemMemory = psutil.Process(os.getpid()).memory_info().rss / (1024 * 1024)


def A_star(curr_player, curr_boxes):
    node_generated = 0
    frontier = SortedList(key=lambda x: minimum_cost(x[2], x[1]))
    explored = set()
    frontier.add((curr_player, curr_boxes, 0, []))

    node_generated += 1
    explored.add((curr_player, curr_boxes))
    startTime = time.time()
    while True:
        (now_player, now_boxes, step, actions) = frontier.pop(0)
        moves = set_available_moves(now_player, now_boxes)
        for m in moves:
            res, new_player, new_boxes = move(now_player, now_boxes, m)
            if (new_player, new_boxes) not in explored and res == True:
                explored.add((new_player, new_boxes))
                if is_win(goals, new_boxes):
                    end = time.time() - startTime
                    memo_info = psutil.Process(os.getpid()).memory_info().rss / (1024 * 1024) - itemMemory
                    return (node_generated + 1, step + 1, end, memo_info)
                frontier.add((new_player, new_boxes, step + 1, actions + [m]))
            node_generated += 1


if __name__ == '__main__':
    i = -1
    if not os.path.exists("A_star.csv"):
        f = open("A_star.csv", 'w+')
        f.write("Map,Level,Algorithm,Node generated,Step,Time (s),Memory (MB)\n")
        f.close()
        i = 0
    else:
        # load file
        f = open("A_star.csv", "r")
        contents = f.read()
        i = len(contents.split('\n')) - 2
        f.close()

    print("Loading A-star algorithm results from testcase {}".format(i + 1))

    for j in range(i, 80):
        walls, goals, boxes, paths, player = set_value(
            "./Testcases/{}/{}.txt".format(map_list[int(j / 40)], j % 40 + 1))
        distanceToGoal, dead_squares = set_distance()
        print("\nSolving testcase {}: ".format(j + 1))
        (node_created, step, times, memo) = A_star(player, boxes)

        f = open("A_star.csv", 'a+')
        f.write(
            "{},{},A_star,{},{},{:0.6f},{:0.6f}\n".format(map_list[int(j / 40)], j % 40 + 1, node_created, step, times,
                                                          memo))
        print("Results testcase {}. Node generated: {}, Step: {}, Time: {:0.6f} s, Memory: {:0.6f} MB\n".format(j + 1,
                                                                                                                node_created,
                                                                                                                step,
                                                                                                                times,
                                                                                                                memo))
        f.close()

    print("\nSolving A-star algorithm results Completed")