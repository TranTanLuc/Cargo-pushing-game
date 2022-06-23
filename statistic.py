import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

BFS = pd.read_csv("BFS.csv", na_values=["???", "??? "])
Astar = pd.read_csv("A_star.csv", na_values=["???", "??? "])


def drawChart(factor, map):
    stepBFS = []
    stepAstar = []
    if (map == "MINI COSMOS"):
        stepBFS = BFS[factor][1:41]
        stepAstar = BFS[factor][1:41]
    else:
        stepBFS = BFS[factor][40:len(BFS)]
        stepAstar = BFS[factor][40:len(BFS)]


    barWidth = 0.25
    fig = plt.subplots(figsize=(12, 8))

    index = []
    for i in range(0, len(stepBFS)):
        index.append(i + 1)



    # Set position of bar on X axis
    br1 = np.arange(len(stepBFS))
    br2 = [x + barWidth for x in br1]


    # Make the plot
    plt.bar(br1, stepBFS, color='r', width=barWidth,
            edgecolor='grey', label='BFS')
    plt.bar(br2, stepAstar, color='g', width=barWidth,
            edgecolor='grey', label='A_star')


    # Adding Xticks
    ylab = ""
    if (factor == "Step"):
        ylab = "Step"
    elif (factor == "Time (s)"):
        ylab = "sec"
    elif (factor == "Node generated"):
        ylab = "Node"
    else:
        ylab = "MB"

    plt.xlabel('TC', fontweight='bold', fontsize=15)
    plt.ylabel(ylab, fontweight='bold', fontsize=15)


    plt.xticks([barWidth / 2 + r for r in range(len(stepBFS))], index)
    if (factor == "Memory (MB)"):
        plt.title("bộ nhớ sử dụng trong " + map + " Testcases")
    elif (factor == "Time (s)"):
        plt.title("thời gian chạy của thuật toán trong " + map + " Testcases")
    elif (factor == "Node generated"):
        plt.title("số node được tạo trong " + map + " Testcases")
    else:
        plt.title("số " + factor + " trong " + map + " Testcases")
    plt.legend()

    save = ""
    if (factor == "Memory (MB)"):
        save = "memory"
    elif (factor == "Step"):
        save = "step"
    elif (factor == "Node generated"):
        save = "nodeGenerated"
    else:
        save = "time"
    plt.savefig("./Charts/" + save + "_" + map + ".png")


drawChart("Step", "MINI COSMOS")
drawChart("Step", "MICRO COSMOS")
drawChart("Time (s)", "MINI COSMOS")
drawChart("Time (s)", "MICRO COSMOS")
drawChart("Memory (MB)", "MINI COSMOS")
drawChart("Memory (MB)", "MICRO COSMOS")
drawChart("Node generated", "MINI COSMOS")
drawChart("Node generated", "MICRO COSMOS")


