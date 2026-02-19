import os
import json

DATASET_ROOT = r"C:\DIP\campus_nav\dataset_raw"   # adjust if needed
OUTPUT = r"C:\DIP\campus_nav\backend\data\graph.json"

graph = {}

folders = [
    "GTKNS",
    "KNSTFB",
    "FBTSB",
    "SBTOA",
    "OATTB",
    "TBTGH",
    "GHTSC",
    "SCTJW",
    "JWT6B",
    "6BTCCD",
    "CCDTARCHI",
    "ARCHITNC",
    "BHT5B",
    "5BTOA"
]

previous_last = None

for folder in folders:

    path = os.path.join(DATASET_ROOT, folder)

    if not os.path.exists(path):
        print("Missing:", path)
        continue

    images = sorted([
        f"{folder}/{x}"
        for x in os.listdir(path)
        if x.lower().endswith(".jpg")
    ])

    if not images:
        continue

    # connect sequential frames
    for i in range(len(images)):

        current = images[i]

        if current not in graph:
            graph[current] = []

        # connect to previous frame
        if i > 0:
            prev = images[i-1]
            graph[current].append(prev)

        # connect to next frame
        if i < len(images)-1:
            nxt = images[i+1]
            graph[current].append(nxt)

    # connect folder boundary
    first = images[0]
    last = images[-1]

    if previous_last:
        graph[first].append(previous_last)
        graph[previous_last].append(first)

    previous_last = last


# SPECIAL CONNECTION: North Canteen ↔ Boys Hostel

def connect_folders(folderA, folderB):

    A = sorted(os.listdir(os.path.join(DATASET_ROOT, folderA)))
    B = sorted(os.listdir(os.path.join(DATASET_ROOT, folderB)))

    if not A or not B:
        return

    a = f"{folderA}/{A[-1]}"
    b = f"{folderB}/{B[0]}"

    graph.setdefault(a, []).append(b)
    graph.setdefault(b, []).append(a)


connect_folders("ARCHITNC", "BHT5B")


with open(OUTPUT, "w") as f:
    json.dump(graph, f)

print("Graph built with", len(graph), "nodes")
