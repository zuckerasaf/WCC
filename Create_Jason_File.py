import json

def transfer_to_json(source_file, target_file):
    panels = {}
    panel_names = set()

    # Read the source file with utf-8 encoding
    with open(source_file, 'r', encoding='utf-8') as file:
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


transfer_to_json('source_jason.txt', 'Panel_Switch_DB.json')