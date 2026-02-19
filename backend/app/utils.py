import os
import pickle
from PIL import Image
from app.model import get_embedding

CACHE_FILE = "data/embeddings/cache.pkl"

import cv2
import numpy as np

def preprocess_for_dip(pil_image):
    img = np.array(pil_image)
    # convert RGB → LAB for CLAHE
    lab = cv2.cvtColor(img, cv2.COLOR_RGB2LAB)
    l, a, b = cv2.split(lab)
    # CLAHE contrast enhancement
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    l = clahe.apply(l)
    lab = cv2.merge((l,a,b))
    img = cv2.cvtColor(lab, cv2.COLOR_LAB2RGB)
    # Gaussian blur
    img = cv2.GaussianBlur(img, (3,3), 0)
    return Image.fromarray(img)


def build_or_load_cache(image_root):

    if os.path.exists(CACHE_FILE):
        print("\nLoading cached embeddings...\n")
        with open(CACHE_FILE, "rb") as f:
            embeddings, ids = pickle.load(f)
        return embeddings, ids

    print("\nBuilding embeddings cache...\n")

    embeddings = []
    ids = []

    for root, _, files in os.walk(image_root):
        for file in files:
            if file.lower().endswith((".jpg", ".jpeg", ".png")):
                path = os.path.join(root, file)
                rel = os.path.relpath(path, image_root)
                try:
                    img = Image.open(path).convert("RGB")
                    from app.utils import preprocess_for_dip
                    img = preprocess_for_dip(img)

                    emb = get_embedding(img)
                    embeddings.append(emb)
                    ids.append(rel.replace("\\","/"))

                    print("Embedded:", rel)

                except Exception as e:
                    print("Failed:", rel, e)

    os.makedirs("data/embeddings", exist_ok=True)

    with open(CACHE_FILE, "wb") as f:
        pickle.dump((embeddings, ids), f)

    print("\nCache saved.\n")

    return embeddings, ids
import json

def load_landmarks():
    with open("data/landmarks.json") as f:
        return json.load(f)


def path_to_instructions(path, landmarks):

    if not path:
        return []

    # build reverse lookup:
    # "BHT5B" → "Boys Hostel"
    folder_to_name = {}

    for name, frame in landmarks.items():
        folder = frame.split("/")[0]
        folder_to_name[folder] = name

    instructions = []

    prev_folder = path[0].split("/")[0]
    prev_name = folder_to_name.get(prev_folder, prev_folder)

    instructions.append(f"Start at {prev_name}")

    for p in path[1:]:

        folder = p.split("/")[0]

        if folder != prev_folder:

            name = folder_to_name.get(folder, folder)
            instructions.append(f"Move towards {name}")

            prev_folder = folder

    instructions.append("You have arrived")

    return instructions
