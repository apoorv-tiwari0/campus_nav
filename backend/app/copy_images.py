import shutil
import os

src = r"C:\DIP\campus_nav\dataset_raw"
dst = r"C:\DIP\campus_nav\backend\data\images"

shutil.copytree(src, dst, dirs_exist_ok=True)

print("Copied all images")
