import json 
import os

def load_experiments(FILE_PATH):
    if not os.path.exists(FILE_PATH):
        return []
    with open(FILE_PATH, "r") as f:
        if not f.read(): return []
    with open(FILE_PATH, "r") as f:
        return json.load(f)

def save_experiments(experiments, FILE_PATH):
    with open(FILE_PATH, "w") as f:
        json.dump(experiments, f, indent=4)