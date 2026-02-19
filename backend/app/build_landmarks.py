import os
import json

IMAGE_ROOT = r"C:\DIP\campus_nav\backend\data\images"
OUT = r"C:\DIP\campus_nav\backend\data\landmarks.json"

landmarks = {}

# mapping folder → human name
names = {
    "GTKNS": "Gate",
    "KNSTFB": "KN Canteen",
    "FBTSB": "First Block",
    "SBTOA": "Second Block",
    "OATTB": "Open Auditorium",
    "TBTGH": "Girls Hostel",
    "GHTSC": "South Canteen",
    "SCTJW": "Juice World",
    "JWT6B": "Sixth Block",
    "6BTCCD": "Cafe Coffee Day",
    "CCDTARCHI": "Architecture Block",
    "ARCHITNC": "North Canteen",
    "BHT5B": "Boys Hostel",
    "5BTOA": "Fifth Block"
}

for folder in names:

    path = os.path.join(IMAGE_ROOT, folder)

    if not os.path.exists(path):
        continue

    files = sorted([
        f for f in os.listdir(path)
        if f.lower().endswith(".jpg")
    ])

    if not files:
        continue

    # pick middle frame
    mid = files[len(files)//2]

    landmarks[names[folder]] = f"{folder}/{mid}"

with open(OUT, "w") as f:
    json.dump(landmarks, f, indent=2)

print("Landmarks built:", len(landmarks))
