import json
import os
from tkinter import filedialog
from tkinter import messagebox

def transfer_to_json():

    source_file = filedialog.askopenfilename(title="Select TXT file as data source", filetypes=[("TXT file", "*txt")])
    target_file = filedialog.asksaveasfilename(title="Select JSON file for the SB", defaultextension=".json", filetypes=[("JSON file", "*json")])


    panels = {}
    panel_names = set()
    newtarget_file = source_file[:-4] + ".json"
    
    # Read the text file and store the lines in a list
    try:
        with open(source_file, 'r', encoding='utf-8') as file:
            lines = file.readlines()
    except UnicodeDecodeError:
        with open(source_file, 'r', encoding='latin-1') as file:
            lines = file.readlines()
    
    # Check if the text file is in the correct format
    line_number=1
    for line in lines:
        parts = line.strip().split('\t')
        if len(parts) != 2:  
            messagebox.showerror("Error", f"The text file is not as it supposed to be in line number {line_number}")
            return
        line_number += 1

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





#transfer_to_json()