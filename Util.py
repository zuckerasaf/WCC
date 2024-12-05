import tkinter as tk
from tkinter import filedialog, Toplevel, Label, Entry, Button, StringVar, OptionMenu, ttk
from tkinter import messagebox
from PIL import ImageTk, Image, ImageDraw, ImageFont
import json
from lxml import etree

def Update_switch_Picture():
    pass


def Update_Data_FromDBSIM(picture, root,tempData,DBSIM_Mapping_entry,DBSIM_Element_entry,DBSIM_Element_Type_entry):
    global DBSimElementValues_Display_update_var
    DBSimElementValues_Display_update_var = []
    if tempData.DBSIM_Default_file != "No DBSIM selected yet": 
        if not(tempData.DBSIM_panel == "none" or tempData.DBSIM_panel == "No DBSIM panel selected"or tempData.DBSIM_panel == ""):
            tree = etree.parse(tempData.DBSIM_Default_file)
            switch_type = tree.xpath(f'//MessageDefinitions/MessageDefinition [@Name="{tempData.DBSIM_panel}"]/Elements/Element/TypeDefinition')[0].text
            elements = tree.xpath(f'//Types/TypeDefinition[@Name="{switch_type}"]/Elements/Element/@Name')
        else:
            elements = ["none"] 
            messagebox.showwarning("Warning", "No Panel from DBSIM selected yet \n first update DBSIM panel name in main window")
            return
    else :
         messagebox.showwarning("Warning", "No DBSIM file selected yet")
         return
    
    print (elements)   
#     # Sort the switch names alphabetically
#     switch_names_sorted = sorted(switch_names)
    elements_sorted = sorted(elements)

    # Create a new window for switch name selection
    switch_window_Updtae = tk.Toplevel(root)
    switch_window_Updtae.title("update DBSIM value for the current wwitch")

    # Set the width of the switch_window to twice its default width
    default_width = 200  # Example default width, adjust as needed
    switch_window_Updtae.geometry(f"{default_width * 2}x120")  # Adjust height as needed

    # Create a StringVar to track the selected switch name
    selected_switch_name_DBSIM_Update = tk.StringVar()

            # Create a label and combobox for panel name selection
    Switch_label_DBSIM = ttk.Label(switch_window_Updtae, text="Select switch Name DBSIM:")
    Switch_label_DBSIM.pack(padx=10, pady=5)

    Switch_combobox_DBSIM_Update = ttk.Combobox(switch_window_Updtae, textvariable=selected_switch_name_DBSIM_Update, values=elements_sorted, width=40)
    Switch_combobox_DBSIM_Update.pack(padx=10, pady=5)


    # Function to proceed after switch name is selected
    def proceed(DBSIM_Mapping_entry,DBSIM_Element_entry,DBSIM_Element_Type_entry):
        i = 0
        if selected_switch_name_DBSIM_Update.get():
            if selected_switch_name_DBSIM_Update.get() != "" or selected_switch_name_DBSIM_Update.get() == "none":
                elemtypDef  = tree.xpath(f'//Types/TypeDefinition/Elements/Element[@Name="{selected_switch_name_DBSIM_Update.get()}"]/TypeDefinition')
                listnameelme = tree.xpath(f'//Types/TypeDefinition[@Name="{elemtypDef[0].text}"]/Enumerators/Enumerator/@Name')
                listEngValueelme = tree.xpath(f'//Types/TypeDefinition[@Name="{elemtypDef[0].text}"]/Enumerators/Enumerator/EngValue')
                #elementType = tree.xpath(f'//Types/TypeDefinition[@Name="{elemtypDef[0].text}"]/ElementType')[0].text
                elementType = tree.xpath(f'//Types/TypeDefinition[@Name="{elemtypDef[0].text}"]/EngType')[0].text
                for i in range(len(listEngValueelme)):
                    DBSimElementValues_Display_update_var.append(listnameelme[i] + " = " + listEngValueelme[i].text + "\n")

                DBSIM_Mapping_entry.delete("1.0", tk.END)  # Clear the Text widget
                DBSIM_Mapping_entry.insert(tk.END, "".join(DBSimElementValues_Display_update_var))
                num_lines = "".join(DBSimElementValues_Display_update_var).count('\n') + 1
                DBSIM_Mapping_entry.config(height=num_lines)

                DBSIM_Element_entry.delete(0, tk.END)  # Clear the Text widget
                DBSIM_Element_entry.insert(0, selected_switch_name_DBSIM_Update.get())

                DBSIM_Element_Type_entry.delete(0, tk.END)  # Clear the Text widget
                DBSIM_Element_Type_entry.insert(0, elementType)

            switch_window_Updtae.destroy()
            
    

    # Create a button to proceed
    # command=lambda: browse_DB(db_name_var)
    proceed_button = ttk.Button(switch_window_Updtae, text="Proceed", command=lambda: proceed(DBSIM_Mapping_entry,DBSIM_Element_entry,DBSIM_Element_Type_entry))
    #proceed_button = ttk.Button(switch_window_Updtae, text="Proceed", command=proceed)
    proceed_button.pack(padx=10, pady=10)

    switch_window_Updtae.wait_window()

# # Function to select a panel name


def str2DBSIMelement (elemnets):
    str2DBsim = ""
    for elment in elemnets:
        pass

    return str2DBsim

def load_parameters_from_Jason(param):
    try:
        with open("InitValues.json", "r", encoding='utf-8') as file:
            data = json.load(file)
            if isinstance(data, list):
                return data[0].get(param, [])
            else:
                raise TypeError("Expected a list of dictionaries in the JSON file")
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []
    except TypeError as e:
        print(f"Error: {e}")
        return []

def load_backend_names():
    try:
        with open("alpha_data.json", "r") as file:
            data = json.load(file)
            backend_names = [item["backendName"] for item in data]
            return backend_names
    except FileNotFoundError:
        return []

def Switch_name_listbox(root):
    # Load backend names from the JSON file
    backend_names = load_backend_names()

    Switch_List = tk.Label(root, text=f" the avaliable swtich for this panel ")
    Switch_List.grid(row=3, column=1, padx=5, pady=5,sticky="w")

    # Create a listbox to display the backend names
    Switch_name_listbox = tk.Listbox(root,selectmode=tk.SINGLE, width=20, height=5)
    # Create a Scrollbar widget
    scrollbar = tk.Scrollbar(root, orient=tk.VERTICAL, command=Switch_name_listbox.yview)
    Switch_name_listbox.config(yscrollcommand=scrollbar.set)
    Switch_name_listbox.grid(row=2, column=1, padx=5, pady=5,sticky="w")#, sticky="nsew")
    scrollbar.grid(row=2, column=2, sticky="w")

    # update the backend names to the listbox
    Switch_name_listbox.delete(0, tk.END)
    for name in backend_names:
        Switch_name_listbox.insert(tk.END, name)
            
    # Configure grid to expand the listbox
    root.grid_rowconfigure(5, weight=1)
    root.grid_columnconfigure(0, weight=1)

def update_image_position_entry(tempData):
    global image_position_entry
    if image_position_entry:
        image_position_entry.delete(0, tk.END)
        image_position_entry.insert(0, str(tempData.new_image_position))

def update_rotation_entry(tempData):
    global rotation_entry
    if rotation_entry:
        rotation_entry.delete(0, tk.END)
        rotation_entry.insert(0, str(tempData.disp_rotation_angle))

def update_scale_image(switch):
    global image_scale_entry
    if image_scale_entry:
        image_scale_entry.delete(0, tk.END)
        image_scale_entry.insert(0, f"{switch.scale:.2f}")

        

def Bring_File_path ():
    global file_path
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.gif")])
    return file_path

def load_panel_names(DB_file_path):
    with open(DB_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        return data["panel_names"]
    
def load_switch_names(DB_file_path,panel_name):

    print("panel_name", panel_name)
    with open(DB_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        panels = data.get("panels", [])
        for panel in panels:
            if panel.get("panel_name") == panel_name:
                return list(panel.get("Items", {}).values())
        return []

def open_alpha_form(root,add_Switch,tempData, picture):

    global image_position_entry, rotation_entry, image_scale_entry

    print("new_scale - open_alpha_form",tempData.new_scale)
    def on_bring_file_path(var):
        file_path = Bring_File_path()
        if file_path:
            var.set(file_path)

    # Function to create label and entry pair
    def create_label_entry_pair(parent, label_text, row, column, default_value):
        label = Label(parent, text=label_text,width=15)
        label.grid(row=row, column=column)
        
        entry_var = StringVar()
        entry = Entry(parent, textvariable=entry_var,width=10)
        entry.grid(row=row, column=column + 1)
        entry_var.set(default_value)
    
        return entry_var
    
    def create_file_path_entry(frame, row, column, default_value):
        # Create the label
        Label(frame, text="File Path:").grid(row=row, column=column)
        
        # Create the StringVar
        file_path_var = StringVar()
        
        # Create the entry widget with right-aligned text
        file_path_entry = Entry(frame, textvariable=file_path_var, justify="right")
        file_path_entry.grid(row=row, column=column+1)
        file_path_var.set(default_value)
        
        # Set the cursor to the end of the text and scroll to the end
        file_path_entry.icursor(tk.END)
        file_path_entry.xview_moveto(1)
        
        # Create the button
        file_path_button = Button(frame, text="file", command=lambda: on_bring_file_path(file_path_var))
        file_path_button.grid(row=row, column=column+2)
        
        return file_path_var
    
    def toggle_frame(frame, button):
        if frame.winfo_viewable():
            frame.grid_remove()
            button.config(text=f" {button.cget('text').split(' ')[1]} Commands")
        else:
            frame.grid()
            button.config(text=f" {button.cget('text').split(' ')[1]} Commands")

    def save_alpha_data(add_Switch,picture, root,tempData):

        
        global rotation_angle

        backend_name = switch_name_entry.get()
        image_size = image_size_entry.get()
        image_position = image_position_entry.get()
        image_scale = image_scale_entry.get()
        type_value = type_var.get()

        DBSimElementValues = DBSIM_Mapping_entry.get("1.0", tk.END)
        enumMapping_list = [line for line in DBSimElementValues.split('\n') if line]
        enumMapping_dict = {}
        for item in enumMapping_list:
            key, value = item.split(' = ')
            enumMapping_dict[key.strip()] = int(value.strip())

        offset_on_value = offset_on_var.get()
        offset_off_value = offset_off_var.get()
        debugMode_value = debugMode_var.get()
        is_clickable_value = is_clickable_var.get()
        imageDefault_value = imageDefault_var.get()
        click_bounds_height_factor_value = click_bounds_height_factor_var.get()
        click_bounds_width_factor_value = click_bounds_width_factor_var.get()
        top = top_var.get()
        right = right_var.get()
        bottom = bottom_var.get()
        left = left_var.get()
        press_pull1 = press_pull1_var.get()
        press_pull2 = press_pull2_var.get()
        color_value = color_var.get()
        rotation_1_Key = rotation_1_Key_Var.get()
        rotation_1_angle = rotation_1_angle_Var.get()
        rotation_2_Key = rotation_2_Key_Var.get()
        rotation_2_angle = rotation_2_angle_Var.get()
        rotation_3_Key = rotation_3_Key_Var.get()
        rotation_3_angle = rotation_3_angle_Var.get()
        rotation_4_Key = rotation_4_Key_Var.get()
        rotation_4_angle = rotation_4_angle_Var.get()
        rotation_5_Key = rotation_5_Key_Var.get()
        rotation_5_angle = rotation_5_angle_Var.get()
        rotation_6_Key = rotation_6_Key_Var.get()
        rotation_6_angle = rotation_6_angle_Var.get()
        rotation_7_Key = rotation_7_Key_Var.get()
        rotation_7_angle = rotation_7_angle_Var.get()
        rotation_8_Key = rotation_8_Key_Var.get()
        rotation_8_angle = rotation_8_angle_Var.get()
        rotation_9_Key = rotation_9_Key_Var.get()
        rotation_9_angle = rotation_9_angle_Var.get()
        rotation_10_Key = rotation_10_Key_Var.get()
        rotation_10_angle = rotation_10_angle_Var.get()
        conversion_1_Key = conversion_1_Key_Var.get()
        conversion_1_file_path = conversion_1_file_path_Var.get()
        conversion_2_Key = conversion_2_Key_Var.get()
        conversion_2_file_path = conversion_2_file_path_Var.get()
        conversion_3_Key = conversion_3_Key_Var.get()
        conversion_3_file_path = conversion_3_file_path_Var.get()
        conversion_4_Key = conversion_4_Key_Var.get()
        conversion_4_file_path = conversion_4_file_path_Var.get()
        conversion_5_Key = conversion_5_Key_Var.get()
        conversion_5_file_path = conversion_5_file_path_Var.get()
        conversion_6_Key = conversion_6_Key_Var.get()
        conversion_6_file_path = conversion_6_file_path_Var.get()
        conversion_7_Key = conversion_7_Key_Var.get()
        conversion_7_file_path = conversion_7_file_path_Var.get()
        conversion_8_Key = conversion_8_Key_Var.get()
        conversion_8_file_path = conversion_8_file_path_Var.get()
        conversion_9_Key = conversion_9_Key_Var.get()
        conversion_9_file_path = conversion_9_file_path_Var.get()
        conversion_10_Key = conversion_10_Key_Var.get()
        conversion_10_file_path = conversion_10_file_path_Var.get()
        Value_conversion_1_Key = Value_conversion_1_Key_Var.get()
        Value_conversion_1_angle = Value_conversion_1_angle_Var.get()
        Value_conversion_2_Key = Value_conversion_2_Key_Var.get()
        Value_conversion_2_angle = Value_conversion_2_angle_Var.get()
        Value_conversion_3_Key = Value_conversion_3_Key_Var.get()
        Value_conversion_3_angle = Value_conversion_3_angle_Var.get()
        Value_conversion_4_Key = Value_conversion_4_Key_Var.get()
        Value_conversion_4_angle = Value_conversion_4_angle_Var.get()
        Value_conversion_5_Key = Value_conversion_5_Key_Var.get()
        Value_conversion_5_angle = Value_conversion_5_angle_Var.get()
        String_Length = String_Length_Var.get()
        Loggerstate = Logger_var.get()
        Z_Index = Z_index_var.get()
        ElementType = DBSIM_Element_Type_entry.get()


        debugMode_value = True if debugMode_value == "True" else False
        is_clickable_value = True if is_clickable_value == "True" else False

        data = {
            "type": type_value,
            "backendName": backend_name,
            #"panelName": picture.panelName,
            "panelName":tempData.DBSIM_panel,
            "panelNameORS": picture.panelNameORS,
            "panelNamePath": tempData.panel_Image_Path,
            "backend": {
                "key": backend_name + "_IN",
                "dbsimProps": {
                    "stationName": "",
                    #"blockName": "IOToHost." + picture.panelName,
                    "blockName": "IOToHost." + tempData.DBSIM_panel,
                    "elementName": "Data." + backend_name,
                    "elementType": ElementType,
                    #"enumMapping": enumMapping_list,
                    "enumMapping": enumMapping_dict,
                }
            },
            "component": {
                "debugMode": debugMode_value,
                "isClickable": is_clickable_value,
                "position": {
                    "imgWidth": picture.width,
                    "imgHeight": picture.height,
                    "posLeft": picture.x,  # image_position[0],
                    "posTop": picture.y,  # image_position[1],
                    "zIndex": int(Z_Index),
                    "imgScale": float(image_scale),
                },
                "imageProps": {
                    "imageDefault": imageDefault_value,  # picture.file_path,
                    "additionalImageData": {
                        conversion_1_Key: conversion_1_file_path,
                        conversion_2_Key: conversion_2_file_path,
                        conversion_3_Key: conversion_3_file_path,
                        conversion_4_Key: conversion_4_file_path,
                        conversion_5_Key: conversion_5_file_path,
                        conversion_6_Key: conversion_6_file_path,
                        conversion_7_Key: conversion_7_file_path,
                        conversion_8_Key: conversion_8_file_path,
                        conversion_9_Key: conversion_9_file_path,
                        conversion_10_Key: conversion_10_file_path,
                    }
                },
                "clickProps": {
                    "clickBoundsHeightFactor": click_bounds_height_factor_value,
                    "clickBoundsWidthFactor": click_bounds_width_factor_value,
                    "mapping": {
                        "mapTop": top,
                        "mapRight": right,
                        "mapBottom": bottom,
                        "mapLeft": left,
                        "mapPressPull1": press_pull1,
                        "mapPressPull2": press_pull2,
                    }
                },
                "knobProps": {
                    "rotation": {
                        rotation_1_Key: rotation_1_angle,
                        rotation_2_Key: rotation_2_angle,
                        rotation_3_Key: rotation_3_angle,
                        rotation_4_Key: rotation_4_angle,
                        rotation_5_Key: rotation_5_angle,
                        rotation_6_Key: rotation_6_angle,
                        rotation_7_Key: rotation_7_angle,
                        rotation_8_Key: rotation_8_angle,
                        rotation_9_Key: rotation_9_angle,
                        rotation_10_Key: rotation_10_angle,
                    }
                },
                "analogProps": {
                    "conversion": {
                        Value_conversion_1_Key: Value_conversion_1_angle,
                        Value_conversion_2_Key: Value_conversion_2_angle,
                        Value_conversion_3_Key: Value_conversion_3_angle,
                        Value_conversion_4_Key: Value_conversion_4_angle,
                        Value_conversion_5_Key: Value_conversion_5_angle,
                    }
                },
                "stringProps": {
                    "maxStringLength": String_Length
                },
                "blinking": {
                    "color": color_value
                },
                "logger": {
                    "display": Loggerstate,
                }
            }
        }
        if add_Switch == True:
            # Read existing data from the JSON file
            try:
                with open("alpha_data.json", "r") as file:
                    existing_data = json.load(file)
            except FileNotFoundError:
                existing_data = []

            # Append the new data
            existing_data.append(data)

            # Write the updated data back to the JSON file
            with open("alpha_data.json", "w") as file:
                json.dump(existing_data, file, indent=4)

        elif add_Switch == False:
            # Read existing data from the JSON file
            with open(picture.json_file_path, 'r', encoding='utf-8') as file:
                olddata = json.load(file)

            try:
                with open("alpha_data.json", "w") as file:
                    json.dump([], file)
                with open("alpha_data.json", "r") as file:
                    existing_data = json.load(file)
            except FileNotFoundError:
                existing_data = []    
            
             # update  the selected item from the existing JSON data
            olddata = [item for item in olddata if item['backendName'] != picture.imageName]
            if len(olddata) != 0:
                existing_data.extend(olddata)
                existing_data.append(data) # insert the new data 
            else:
                existing_data.append(data) #olddata = data # prevert duplication of data in case no aditional (other switches) data in the json file


            #existing_data.extend(olddata)

             # Write the updated data back to the temp JSON file
            with open("alpha_data.json", "w") as file:
                json.dump(existing_data, file, indent=4)
            
            # Write the updated data back to the JSON file
            with open(picture.json_file_path, "w") as file:
                json.dump(existing_data, file, indent=4)
        
        # Reset the rotation angle to 0
        rotation_angle = 0

        Switch_name_listbox(root)
        alpha_form.destroy()

    alpha_form = Toplevel(root)
    alpha_form.title("Alpha Data Form")


    # Get the position and size of the Image Browser window
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()

    # Set the position of the alpha_form window to the right of the Image Browser window
    alpha_width = 700
    alpha_height = 900
    alpha_form.geometry(f"+{width}+10")
    alpha_form.geometry(f"{alpha_width}x{alpha_height}")
    rNum = 0 #relative row number
    cNum = 0 #relative column number
    # Create a label to display the selected panel name
    Label(alpha_form, text="switch name :").grid(row=rNum, column=0)
    switch_name_entry = Entry(alpha_form)
    switch_name_entry.grid(row=rNum, column=1)
    switch_name_entry.insert(0, picture.imageName)
    switch_name_entry.config(background='grey')

    rNum += 1
    Label(alpha_form, text="Image Size:").grid(row=rNum, column=0)
    image_size_entry = Entry(alpha_form, width=10)
    image_size_entry.grid(row=rNum, column=1)
    image_size_entry.insert(0, str(picture.width)+" X "+str(picture.height))  # Assuming the resized image size
    image_size_entry.config(background='grey')
  
    Label(alpha_form, text="Image scale:").grid(row=rNum, column=2)
    image_scale_entry = Entry(alpha_form, width=10)
    image_scale_entry.grid(row=rNum, column=3)
    image_scale_entry.insert(0, picture.scale)  # Assuming the resized image size
    #image_scale_entry.insert(0, str(picture.scale))  # Assuming the resized image size
    image_scale_entry.config(background='grey')
    rNum += 1
    Label(alpha_form, text="Image Position:").grid(row=rNum, column=0)
    image_position_entry = Entry(alpha_form, width=10)
    image_position_entry.grid(row=rNum, column=1)
    image_position_entry.insert(0, str(picture.x)+","+str(picture.y))  # Initial position
    image_position_entry.config(background='grey')

    Label(alpha_form, text="Rotation:").grid(row=rNum, column=2)
    rotation_entry = Entry(alpha_form, width=10)
    rotation_entry.grid(row=rNum, column=3)
    rotation_entry.insert(0, str(tempData.disp_rotation_angle))  # Initial rotation 
    rotation_entry.config(background='grey')
    rNum += 1   

    Label(alpha_form, text="Type:").grid(row=rNum, column=0)
    type_var = StringVar(alpha_form)
    type_var.set(picture.type_value)  # Default type value
    type_options = load_parameters_from_Jason("Switch_type")
    type_menu = OptionMenu(alpha_form, type_var, *type_options)
    type_menu.grid(row=3, column=1)
    rNum += 1
    offset_on_var = create_label_entry_pair(alpha_form, "offset on:", rNum, 0, picture.offset_on_value)
    rNum += 1
    offset_off_var = create_label_entry_pair(alpha_form, "offset off:", rNum, 0, picture.offset_off_value)
    rNum += 1

    Label(alpha_form, text="debug Mode:").grid(row=rNum, column=0)
    debugMode_var = StringVar(alpha_form)
    debugMode_var.set("False")  # Default type value
    debugMode_var_options = ("False", "True")
    debugMode_var_menu = OptionMenu(alpha_form, debugMode_var, *debugMode_var_options)
    debugMode_var_menu.grid(row=rNum, column=1)

    #debugMode_var = create_label_entry_pair(alpha_form, "debug Mode:", rNum, 0, picture.debugMode_value)
    rNum += 1

    Label(alpha_form, text="is clickable:").grid(row=rNum, column=0)
    is_clickable_var = StringVar(alpha_form)
    is_clickable_var.set("True")  # Default type value
    is_clickable_var_options = ("False", "True")
    is_clickable_var_menu = OptionMenu(alpha_form, is_clickable_var, *is_clickable_var_options)
    is_clickable_var_menu.grid(row=rNum, column=1)

    #is_clickable_var = create_label_entry_pair(alpha_form, "is clickable:", rNum, 0, picture.is_clickable_value)
    rNum += 1
    click_bounds_height_factor_var = create_label_entry_pair(alpha_form, "bounds height factor:", rNum, 0, picture.click_bounds_height_factor_value)
    rNum += 1
    click_bounds_width_factor_var = create_label_entry_pair(alpha_form, "bounds width factor:", rNum, 0, picture.click_bounds_width_factor_value)
    rNum += 3
    
    Label(alpha_form, text="for Toggle behave define \n ""INCREASE\DECREASE"" :").grid(row=rNum, column=0)
    rNum += 1
    top_var = create_label_entry_pair(alpha_form, "top:", rNum, 0, picture.top)
    rNum += 1
    right_var = create_label_entry_pair(alpha_form, "right:", rNum, 0, picture.right)
    rNum += 1
    bottom_var = create_label_entry_pair(alpha_form, "bottom:", rNum, 0, picture.bottom)
    rNum += 1
    left_var = create_label_entry_pair(alpha_form, "left:", rNum, 0, picture.left)
    rNum += 1
    press_pull1_var = create_label_entry_pair(alpha_form, "press_pull1:", rNum, 0, picture.press_pull1)
    rNum += 1
    press_pull2_var = create_label_entry_pair(alpha_form, "press_pull2:", rNum, 0, picture.press_pull2)
    rNum += 3
    
    global DBSimElementValues_Display_update_var
    
    Update_DBSim_Button = Button(alpha_form, text="Update Data from DBSim ", command=lambda: Update_Data_FromDBSIM(picture, root,tempData,DBSIM_Mapping_entry,DBSIM_Element_entry,DBSIM_Element_Type_entry))
    Update_DBSim_Button.grid(row=rNum, column=0)
    rNum += 1
    Label(alpha_form, text="DBSIM Element:").grid(row=rNum, column=0)
    DBSIM_Element_entry = Entry(alpha_form)
    DBSIM_Element_entry.grid(row=rNum, column=1)
    DBSIM_Element_entry.insert(0, str(picture.DBSIM_Element))  
    DBSIM_Element_entry.config(background='grey')
    

    Label(alpha_form, text="DBSIM Mapping:").grid(row=rNum-1, column=2)
    #DBSIM_Mapping_entry = Entry(alpha_form)
    DBSIM_Mapping_entry = tk.Text(alpha_form, wrap=tk.WORD, width=20)
    stringDBSimElementValues = "".join(picture.DBSimElementValues_Display)
    DBSIM_Mapping_entry.insert(tk.END, stringDBSimElementValues)  
    num_lines = stringDBSimElementValues.count('\n') + 1
    DBSIM_Mapping_entry.config(height=num_lines)
    DBSIM_Mapping_entry.grid(row=rNum, column=2)
    DBSIM_Mapping_entry.config(background='grey')
    rNum += 1
    Label(alpha_form, text="DBSIM Element type:").grid(row=rNum, column=0)
    DBSIM_Element_Type_entry = Entry(alpha_form)
    DBSIM_Element_Type_entry.grid(row=rNum, column=1)
    DBSIM_Element_Type_entry.insert(0, str(picture.DBSimelementType))  
    DBSIM_Element_Type_entry.config(background='grey')
    rNum += 3
    Label(alpha_form, text="Blinking color:").grid(row=rNum, column=0)
    color_var= StringVar(alpha_form)
    color_var.set(picture.color)  # Default type value
    color_options = load_parameters_from_Jason("color")
    color_menu = OptionMenu(alpha_form, color_var, *color_options)
    color_menu.grid(row=rNum, column=1)
    rNum += 1
    String_Length_Var = create_label_entry_pair(alpha_form, "String Length:", rNum, 0, picture.String_Length)
    rNum += 1
    Label(alpha_form, text="Logger caption:").grid(row=rNum, column=0)
    Logger_var = StringVar(alpha_form)
    Logger_var.set(picture.Logger)  # Default type value
    Logger_options = load_parameters_from_Jason("logger")
    Logger_menu = OptionMenu(alpha_form, Logger_var, *Logger_options)
    Logger_menu.grid(row=rNum, column=1)
    rNum += 1
    Z_index_var = create_label_entry_pair(alpha_form, "Z_index:", rNum, 0, picture.Z_index)
    rNum += 1
    # Create a frame for rotation commands
    knob_props_frame = ttk.Frame(alpha_form, padding="10")
    knob_props_frame.grid(row=4, column=2, columnspan=3, sticky="nsew")

    # Initially hide the frame
    knob_props_frame.grid_remove()

    # Create a toggle button to show/hide the additional frame
    toggle_additional_button = ttk.Button(alpha_form, text="Knob rotate", command=lambda: toggle_frame(knob_props_frame, toggle_additional_button))
    toggle_additional_button.grid(row=3, column=2, columnspan=3, padx=5, pady=5)


    # Use the function to create label and entry pairs
    rotation_1_Key_Var = create_label_entry_pair(knob_props_frame, " 1 command: ", 4, 2, picture.rotation[0][0])
    rotation_1_angle_Var = create_label_entry_pair(knob_props_frame, " 1 angle: ", 4, 4, picture.rotation[0][1])
    rotation_2_Key_Var = create_label_entry_pair(knob_props_frame, " 2 command: ", 5, 2, picture.rotation[1][0])
    rotation_2_angle_Var = create_label_entry_pair(knob_props_frame, " 2 angle: ", 5, 4, picture.rotation[1][1])
    rotation_3_Key_Var = create_label_entry_pair(knob_props_frame, " 3 command: ", 6, 2, picture.rotation[2][0])
    rotation_3_angle_Var = create_label_entry_pair(knob_props_frame, " 3 angle: ", 6, 4, picture.rotation[2][1])
    rotation_4_Key_Var = create_label_entry_pair(knob_props_frame, " 4 command: ", 7, 2, picture.rotation[3][0])
    rotation_4_angle_Var = create_label_entry_pair(knob_props_frame, " 4 angle: ", 7, 4,   picture.rotation[3][1])
    rotation_5_Key_Var = create_label_entry_pair(knob_props_frame, " 5 command: ", 8, 2, picture.rotation[4][0])
    rotation_5_angle_Var = create_label_entry_pair(knob_props_frame, " 5 angle: ", 8, 4,    picture.rotation[4][1])
    rotation_6_Key_Var = create_label_entry_pair(knob_props_frame, " 6 command: ", 9, 2, picture.rotation[5][0])
    rotation_6_angle_Var = create_label_entry_pair(knob_props_frame, " 6 angle: ", 9, 4,    picture.rotation[5][1])
    rotation_7_Key_Var = create_label_entry_pair(knob_props_frame, " 7 command: ", 10, 2, picture.rotation[6][0])
    rotation_7_angle_Var = create_label_entry_pair(knob_props_frame, " 7 angle: ", 10, 4,  picture.rotation[6][1])
    rotation_8_Key_Var = create_label_entry_pair(knob_props_frame, " 8 command: ", 11, 2, picture.rotation[7][0])
    rotation_8_angle_Var = create_label_entry_pair(knob_props_frame, " 8 angle: ", 11, 4, picture.rotation[7][1])
    rotation_9_Key_Var = create_label_entry_pair(knob_props_frame, " 9 command: ", 12, 2, picture.rotation[8][0])
    rotation_9_angle_Var = create_label_entry_pair(knob_props_frame, " 9 angle: ", 12, 4, picture.rotation[8][1])
    rotation_10_Key_Var = create_label_entry_pair(knob_props_frame, " 10 command: ", 13, 2, picture.rotation[9][0])
    rotation_10_angle_Var = create_label_entry_pair(knob_props_frame, " 10 angle: ", 13, 4, picture.rotation[9][1])


        # Create a frame for rotation commands
    imageProps_frame = ttk.Frame(alpha_form, padding="10")
    imageProps_frame.grid(row=6, column=2, columnspan=3, sticky="nsew")

    # Initially hide the frame
    imageProps_frame.grid_remove()

    # Create a toggle button to show/hide the additional frame
    toggle_additional_button = ttk.Button(alpha_form, text="Knob Image", command=lambda: toggle_frame(imageProps_frame, toggle_additional_button))
    toggle_additional_button.grid(row=5, column=2, columnspan=3, padx=5, pady=5)

    conversion_1_Key_Var = create_label_entry_pair(imageProps_frame, " 1 command: ", 14, 2, picture.conversion[0][0])
    conversion_1_file_path_Var = create_file_path_entry(imageProps_frame, 14, 4, picture.conversion[0][1])
    conversion_2_Key_Var = create_label_entry_pair(imageProps_frame, " 2 command: ", 15, 2, picture.conversion[1][0])
    conversion_2_file_path_Var = create_file_path_entry(imageProps_frame, 15, 4, picture.conversion[1][1])
    conversion_3_Key_Var = create_label_entry_pair(imageProps_frame, " 3 command: ", 16, 2, picture.conversion[2][0])
    conversion_3_file_path_Var = create_file_path_entry(imageProps_frame, 16, 4, picture.conversion[2][1])
    conversion_4_Key_Var = create_label_entry_pair(imageProps_frame, " 4 command: ", 17, 2, picture.conversion[3][0])
    conversion_4_file_path_Var = create_file_path_entry(imageProps_frame, 17, 4, picture.conversion[3][1])
    conversion_5_Key_Var = create_label_entry_pair(imageProps_frame, " 5 command: ", 18, 2, picture.conversion[4][0])
    conversion_5_file_path_Var = create_file_path_entry(imageProps_frame, 18, 4, picture.conversion[4][1])
    conversion_6_Key_Var = create_label_entry_pair(imageProps_frame, " 6 command: ", 19, 2, picture.conversion[5][0])
    conversion_6_file_path_Var = create_file_path_entry(imageProps_frame, 19, 4, picture.conversion[5][1])
    conversion_7_Key_Var = create_label_entry_pair(imageProps_frame, " 7 command: ", 20, 2, picture.conversion[6][0])
    conversion_7_file_path_Var = create_file_path_entry(imageProps_frame, 20, 4, picture.conversion[6][1])
    conversion_8_Key_Var = create_label_entry_pair(imageProps_frame, " 8 command: ", 21, 2, picture.conversion[7][0])
    conversion_8_file_path_Var = create_file_path_entry(imageProps_frame, 21, 4, picture.conversion[7][1])
    conversion_9_Key_Var = create_label_entry_pair(imageProps_frame, " 9 command: ", 22, 2, picture.conversion[8][0])
    conversion_9_file_path_Var = create_file_path_entry(imageProps_frame, 22, 4, picture.conversion[8][1])
    conversion_10_Key_Var = create_label_entry_pair(imageProps_frame, " 10 command: ", 23, 2, picture.conversion[9][0])
    conversion_10_file_path_Var = create_file_path_entry(imageProps_frame, 23, 4, picture.conversion[9][1])

    # Create a frame for rotation commands
    Conversion_frame = ttk.Frame(alpha_form, padding="10")
    Conversion_frame.grid(row=8, column=2, columnspan=3, sticky="nsew")

    # Initially hide the frame
    Conversion_frame.grid_remove()

    # Create a toggle button to show/hide the additional frame
    toggle_additional_button = ttk.Button(alpha_form, text="value Conversion", command=lambda: toggle_frame(Conversion_frame, toggle_additional_button))
    toggle_additional_button.grid(row=7, column=2, columnspan=3, padx=5, pady=5)

    Value_conversion_1_Key_Var = create_label_entry_pair(Conversion_frame, " 1 Value: ", 24, 2, picture.value_conversion[0][0])
    Value_conversion_1_angle_Var = create_label_entry_pair(Conversion_frame, " 1 angle: ", 24, 4, picture.value_conversion[0][1])
    Value_conversion_2_Key_Var = create_label_entry_pair(Conversion_frame, " 2 Value: ", 25, 2, picture.value_conversion[1][0])
    Value_conversion_2_angle_Var = create_label_entry_pair(Conversion_frame, " 2 angle: ", 25, 4, picture.value_conversion[1][1])
    Value_conversion_3_Key_Var = create_label_entry_pair(Conversion_frame, " 3 Value: ", 26, 2, picture.value_conversion[2][0])
    Value_conversion_3_angle_Var = create_label_entry_pair(Conversion_frame, " 3 angle: ", 26, 4, picture.value_conversion[2][1])
    Value_conversion_4_Key_Var = create_label_entry_pair(Conversion_frame, " 4 Value: ", 27, 2, picture.value_conversion[3][0])
    Value_conversion_4_angle_Var = create_label_entry_pair(Conversion_frame, " 4 angle: ", 27, 4, picture.value_conversion[3][1])
    Value_conversion_5_Key_Var = create_label_entry_pair(Conversion_frame, " 5 Value: ", 28, 2, picture.value_conversion[4][0])
    Value_conversion_5_angle_Var = create_label_entry_pair(Conversion_frame, " 5 angle: ", 28, 4, picture.value_conversion[4][1])



    imageDefault_var = create_label_entry_pair(alpha_form, " Switch IMG Path Var: ", rNum, 0, picture.file_path)
    rNum += 3
    save_button = Button(alpha_form, text="Save", command=lambda: save_alpha_data(add_Switch,picture, root,tempData))
    save_button.grid(row=rNum, columnspan=1)

