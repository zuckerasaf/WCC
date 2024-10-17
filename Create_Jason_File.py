import json
import os
from tkinter import filedialog

def transfer_to_json(source_file,target_file):
    panels = {}
    panel_names = set()
    newtarget_file = source_file[:-4] + ".json"

    try:
        with open(source_file, 'r', encoding='utf-8') as file:
            lines = file.readlines()
    except UnicodeDecodeError:
        with open(source_file, 'r', encoding='latin-1') as file:
            lines = file.readlines()
        

    # Parse the lines and organize them into the desired structure
    for line in lines:
        key, value = line.strip().split('\t')
        if key not in panels:
            panels[key] = {"panel_name": key, "Items": {}}
        item_key = f"item_{len(panels[key]['Items']) + 1}"
        panels[key]["Items"][item_key] = value
        panel_names.add(key)

    # Convert the dictionary to a list
    panels_list = list(panels.values())

    # Create the final structure
    final_data = {
        "panels": panels_list,
        "panel_names": list(panel_names)
    }

    # Write the final structure to the target JSON file
    with open(target_file, 'w', encoding='utf-8') as file:
        json.dump(final_data, file, indent=2)
    with open(newtarget_file, 'w', encoding='utf-8') as file:
        json.dump(final_data, file, indent=2)




source_file = filedialog.askopenfilename(filetypes=[("TXT file", "*txt")])
directory = r'C:\projectPython\WCC\DB'
target_file = os.path.basename(source_file)[:-4] + '.json'
target_file = os.path.join(directory, target_file)
transfer_to_json(source_file,target_file)