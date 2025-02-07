import os

import re

from datetime import datetime

def create_folders(results_path, ue=""):
    # Specify the path where you want to create the folder

    problem = os.getenv('EOH_PROBLEM')
    model = os.getenv('MODEL_NAME')
    model = re.sub('[^A-Za-z0-9]+', '', model)

    current = f'results_{datetime.now().strftime("%Y%m%d_%H%M%S")}_{problem}_{model}_ue{ue}'
    folder_path = os.path.join(results_path, current)

    print(f'Folder Path: {folder_path}')

    # Check if the folder already exists
    if not os.path.exists(folder_path):
        # Create the main folder "results"
        os.makedirs(folder_path)

    # Create subfolders inside "results"
    subfolders = ["history", "pops", "pops_best", "all_programs", "visualization"]
    for subfolder in subfolders:
        subfolder_path = os.path.join(folder_path, subfolder)
        if not os.path.exists(subfolder_path):
            os.makedirs(subfolder_path)

    os.environ["CURRENT_EXPERIMENT"] = folder_path
