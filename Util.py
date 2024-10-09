import tkinter as tk
from tkinter import filedialog, simpledialog, Toplevel, Label, Entry, Button, StringVar, OptionMenu, ttk
from PIL import ImageTk
import json


def move_image(event, new_image_position, move_pixels, new_image_path, small_Step, combine_images, update_info_label,rotation_angle,Picture):
    
    if new_image_path:
        if event.keysym == 'Right':
            new_image_position = (new_image_position[0] + move_pixels // small_Step, new_image_position[1])
        elif event.keysym == 'Left':
            new_image_position = (new_image_position[0] - move_pixels // small_Step, new_image_position[1])
        elif event.keysym == 'Up':
            new_image_position = (new_image_position[0], new_image_position[1] - move_pixels // small_Step)
        elif event.keysym == 'Down':
            new_image_position = (new_image_position[0], new_image_position[1] + move_pixels // small_Step)
        combine_images(rotation_angle)
        update_info_label()
        Picture.x = new_image_position[0]
        Picture.y = new_image_position[1]


        if image_position_entry:
            image_position_entry.delete(0, tk.END)
            image_position_entry.insert(0, str(new_image_position))
    return new_image_position


def rotate_image(event, img, rotation_angle, rotate_degree, image_label,combine_images):#, update_info_label):
    disp_rotation_angle = 0
    # Check if img is not None
    if img is None:
        print("No image loaded to rotate.")
        return rotation_angle

    # rotation_angle = (rotation_angle + rotate_degree // small_Step) % 360
    # Increment the rotation angle by 30 degrees  
    rotation_angle = (rotation_angle + rotate_degree) % 360


    # Rotate the image
    rotated_img = img.rotate(rotation_angle, expand=True)
    img_tk = ImageTk.PhotoImage(rotated_img)
    image_label.config(image=img_tk)
    image_label.image = img_tk  # Keep a reference to avoid garbage collection

    # Update the rotation value in the alpha form
    if rotation_entry:
        rotation_entry.delete(0, tk.END)
        if rotation_angle < 180:
            disp_rotation_angle = 0 - rotation_angle
        else:
            disp_rotation_angle = 360- rotation_angle
        rotation_entry.insert(0, str(disp_rotation_angle))

    combine_images(rotation_angle)

    return rotation_angle 


def Bring_File_path ():
    global file_path
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.gif")])
    return file_path

def load_panel_names():
    with open('Panel_Switch_DB.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
        return data["panel_names"]
    
def load_switch_names(panel_name):
    print("panel_name", panel_name)
    with open('Panel_Switch_DB.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
        panels = data.get("panels", [])
        for panel in panels:
            if panel.get("panel_name") == panel_name:
                return list(panel.get("Items", {}).values())
        return []
# Function to select a switch name

def select_switch_name(panel_name , switch_name_entry):
    print("panel_name",panel_name)
   
    if panel_name is None:
        print("No panel selected")
        return
    switch_names = load_switch_names(panel_name)

    
    # Sort the switch names alphabetically
    switch_names_sorted = sorted(switch_names)

    # Create a new window for switch name selection
    switch_window = Toplevel()
    switch_window.title("Select Switch Name")

    # Set the width of the switch_window to twice its default width
    default_width = 200  # Example default width, adjust as needed
    switch_window.geometry(f"{default_width * 2}x150")  # Adjust height as needed

    # Create a StringVar to track the selected switch name
    selected_switch_name = tk.StringVar()

        # Create a label and combobox for panel name selection
    Switch_label = ttk.Label(switch_window, text="Select switch Name:")
    Switch_label.pack(padx=10, pady=5)

    Switch_combobox = ttk.Combobox(switch_window, textvariable=selected_switch_name, values=switch_names_sorted, width=40)
    Switch_combobox.pack(padx=10, pady=5)

    # Function to proceed after switch name is selected
    def proceed():
        if selected_switch_name.get():
            switch_name_entry.delete(0, tk.END)
            switch_name_entry.insert(0, selected_switch_name.get())
            switch_window.destroy()
    

    # Create a button to proceed
    proceed_button = ttk.Button(switch_window, text="Proceed", command=proceed)
    proceed_button.pack(padx=10, pady=10)

def open_alpha_form(root,new_image_position, disp_rotation_angle, picture,image_size,panel_name):
    global rotation_entry,image_position_entry,file_path
    # print("panel_name",panel_name)
    

    def on_bring_file_path(var):
        file_path = Bring_File_path()
        if file_path:
            var.set(file_path)

    # Function to create label and entry pair
    def create_label_entry_pair(parent, label_text, row, column, default_value=""):
        label = Label(parent, text=label_text)
        label.grid(row=row, column=column)
        
        entry_var = StringVar()
        entry = Entry(parent, textvariable=entry_var)
        entry.grid(row=row, column=column + 1)
        entry_var.set(default_value)
    
        return entry_var
    
    def create_file_path_entry(frame, row, var_name):
        # Create the label
        Label(frame, text="File Path:").grid(row=row, column=4)
        
        # Create the StringVar
        file_path_var = StringVar(name=var_name)
        
        # Create the entry widget with right-aligned text
        file_path_entry = Entry(frame, textvariable=file_path_var, justify="right")
        file_path_entry.grid(row=row, column=5)
        
        # Set the cursor to the end of the text and scroll to the end
        file_path_entry.icursor(tk.END)
        file_path_entry.xview_moveto(1)
        
        # Create the button
        file_path_button = Button(frame, text="file", command=lambda: on_bring_file_path(file_path_var))
        file_path_button.grid(row=row, column=6)
        
        return file_path_var
    
    def toggle_frame(frame, button):
        if frame.winfo_viewable():
            frame.grid_remove()
            button.config(text=f" {button.cget('text').split(' ')[1]} Commands")
        else:
            frame.grid()
            button.config(text=f" {button.cget('text').split(' ')[1]} Commands")


    def save_alpha_data():
        
        global rotation_angle

        backend_name = switch_name_entry.get()
        image_size = image_size_entry.get()
        image_position = image_position_entry.get()
        type_value = type_var.get()
        offset_on_value = offset_on_var.get()
        offset_off_value = offset_off_var.get()
        debugMode_value = debugMode_var.get()
        is_clickable_value = is_clickable_var.get()
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

        # try:
        #     width, height = image_size.split('x')
        # except ValueError:
        #     width, height = "0", "0"  # Default values in case of error

        data = {
            "type": type_value,
            "backend_name": backend_name,
            # "group": group_value,
            "width": picture.width,
            "height": picture.height,
            "left": picture.x,#image_position[0],
            "top": picture.y,#image_position[1],
            "offset_on": offset_on_value,
            "offset_off": offset_off_value,
            "imageProps": {
                "imageDefault": picture.file_path,
                "additionalImageData": {
                    conversion_1_Key : conversion_1_file_path,
                    conversion_2_Key : conversion_2_file_path,
                    conversion_3_Key : conversion_3_file_path,
                    conversion_4_Key : conversion_4_file_path,
                    conversion_5_Key : conversion_5_file_path,
                    conversion_6_Key : conversion_6_file_path,
                    conversion_7_Key : conversion_7_file_path,
                    conversion_8_Key : conversion_8_file_path,
                    conversion_9_Key : conversion_9_file_path,
                    conversion_10_Key : conversion_10_file_path,
                 }
            },
            
            # "image_off": "/CMDSPanel/SWITCH_10_DOWN_1.png",
            "debugMode": debugMode_value,
            "is_clickable": is_clickable_value,
            "click_props": {
                "click_bounds_height_factor": click_bounds_height_factor_value,
                "click_bounds_width_factor": click_bounds_width_factor_value,
                "mapping": {
                    "top": top,
                    "right": right,
                    "bottom": bottom,
                    "left ": left,
                    "press_pull1 ": press_pull1,
                    "press_pull2 ": press_pull2,
                }
            },
            "knob_props": {
                    "conversion": {
                    rotation_1_Key :  rotation_1_angle, 
                    rotation_2_Key :  rotation_2_angle,
                    rotation_3_Key :  rotation_3_angle, 
                    rotation_4_Key :  rotation_4_angle,
                    rotation_5_Key :  rotation_5_angle, 
                    rotation_6_Key :  rotation_6_angle,
                    rotation_7_Key :  rotation_7_angle, 
                    rotation_8_Key :  rotation_8_angle,
                    rotation_9_Key :  rotation_9_angle, 
                    rotation_10_Key :  rotation_10_angle,
                    }
            },
            "analog_props": {
                    "conversion": {
                    Value_conversion_1_Key :  Value_conversion_1_angle, 
                    Value_conversion_2_Key :  Value_conversion_2_angle,
                    Value_conversion_3_Key :  Value_conversion_3_angle, 
                    Value_conversion_4_Key :  Value_conversion_4_angle,
                    Value_conversion_5_Key :  Value_conversion_5_angle, 
                }
            },
            "string_props": {
                "maxStringLength": String_Length
            },

            "blinking": {
                "color": color_value
            },
        }

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
        
        # Reset the rotation angle to 0
        rotation_angle = 0

        alpha_form.destroy()

    alpha_form = Toplevel(root)
    alpha_form.title("Alpha Data Form")


    # Get the position and size of the Image Browser window
    root.update_idletasks()
    x = root.winfo_x()
    y = root.winfo_y()
    width = root.winfo_width()
    height = root.winfo_height()

    # Set the position of the alpha_form window to the right of the Image Browser window
    alpha_form.geometry(f"+{x + width + 10}+{y}")

    # Create a label to display the selected panel name
    Label(alpha_form, text="switch name :").grid(row=0, column=0)
    switch_name_entry = Entry(alpha_form)
    switch_name_entry.grid(row=0, column=1)
    switch_name_entry.insert(0, "no switch selected")


    # image_key_entry = create_label_entry_pair(alpha_form, "Image key:", 0, 2, "0")
    #image_name_entry = create_label_entry_pair(alpha_form, "switch name:", 0, 0, picture.image_id)

    switch_name_button = Button(alpha_form, text="Switch Name", command=lambda: select_switch_name(panel_name, switch_name_entry))#command=select_switch_name)
    switch_name_button.grid(row=0, column=2, columnspan=2)

    
    Label(alpha_form, text="Image Size:").grid(row=1, column=0)
    image_size_entry = Entry(alpha_form)
    image_size_entry.grid(row=1, column=1)
    image_size_entry.insert(0, str(picture.width)+" X "+str(picture.height))  # Assuming the resized image size

    Label(alpha_form, text="Image Position:").grid(row=2, column=0)
    image_position_entry = Entry(alpha_form)
    image_position_entry.grid(row=2, column=1)
    image_position_entry.insert(0, str(new_image_position))


    Label(alpha_form, text="Rotation:").grid(row=2, column=2)
    rotation_entry = Entry(alpha_form)
    rotation_entry.grid(row=2, column=3)
    rotation_entry.insert(0, str(disp_rotation_angle))  # Initial rotation 

    Label(alpha_form, text="Type:").grid(row=3, column=0)
    type_var = StringVar(alpha_form)
    type_var.set("state2")  # Default type value
    type_options = ["state2" , "stateN" , "knobInteger" , "analog" , "string" , "number"]
    type_menu = OptionMenu(alpha_form, type_var, *type_options)
    type_menu.grid(row=3, column=1)

    offset_on_var = create_label_entry_pair(alpha_form, "offset on:", 5, 0, "0")
    offset_off_var = create_label_entry_pair(alpha_form, "offset on:", 6, 0, "0")
    debugMode_var = create_label_entry_pair(alpha_form, "debug Mode:", 7, 0, "false")
    is_clickable_var = create_label_entry_pair(alpha_form, "is clickable:", 8, 0, "true")
    click_bounds_height_factor_var = create_label_entry_pair(alpha_form, "click bounds height factor:", 9, 0, "2")
    click_bounds_width_factor_var = create_label_entry_pair(alpha_form, "click bounds width factor:", 10, 0, "1.5")
    top_var = create_label_entry_pair(alpha_form, "top:", 12, 0, "none")
    right_var = create_label_entry_pair(alpha_form, "right:", 13, 0, "none")
    bottom_var = create_label_entry_pair(alpha_form, "bottom:", 14, 0, "none")
    left_var = create_label_entry_pair(alpha_form, "left:", 15, 0, "none")
    press_pull1_var = create_label_entry_pair(alpha_form, "press_pull1:", 16, 0, "none")
    press_pull2_var = create_label_entry_pair(alpha_form, "press_pull2:", 17, 0, "none")
    
    Label(alpha_form, text="grid direction:").grid(row=19, column=0)
    grid_direction_var = StringVar(alpha_form)
    grid_direction_var.set("ud")  # Default type value
    grid_direction_options = ["ud", "lr", "none"]
    grid_direction_menu = OptionMenu(alpha_form, grid_direction_var, *grid_direction_options)
    grid_direction_menu.grid(row=19, column=1)

    Label(alpha_form, text="Blinking color:").grid(row=20, column=0)
    color_var= StringVar(alpha_form)
    color_var.set("yellow")  # Default type value
    color_options = ["yellow", "red", "blue"]
    color_menu = OptionMenu(alpha_form, color_var, *color_options)
    color_menu.grid(row=20, column=1)

    String_Length_Var = create_label_entry_pair(alpha_form, "String Length:", 22, 0, "0")

    Label(alpha_form, text="Logger caption:").grid(row=23, column=0)
    Logger_var = StringVar(alpha_form)
    Logger_var.set("true")  # Default type value
    Logger_options = ["true" , "stateN" , "knobInteger" , "false"]
    Logger_menu = OptionMenu(alpha_form, Logger_var, *Logger_options)
    Logger_menu.grid(row=23, column=1)

    # Create a frame for rotation commands
    knob_props_frame = ttk.Frame(alpha_form, padding="10")
    knob_props_frame.grid(row=4, column=2, columnspan=3, sticky="nsew")

    # Initially hide the frame
    knob_props_frame.grid_remove()

    # Create a toggle button to show/hide the additional frame
    toggle_additional_button = ttk.Button(alpha_form, text="Knob rotate", command=lambda: toggle_frame(knob_props_frame, toggle_additional_button))
    toggle_additional_button.grid(row=3, column=2, columnspan=3, padx=5, pady=5)


    # Use the function to create label and entry pairs
    rotation_1_Key_Var = create_label_entry_pair(knob_props_frame, " 1 rotation command: ", 4, 2, "none")
    rotation_1_angle_Var = create_label_entry_pair(knob_props_frame, " 1 angle: ", 4, 4, "0")
    rotation_2_Key_Var = create_label_entry_pair(knob_props_frame, " 2 rotation command: ", 5, 2, "none")
    rotation_2_angle_Var = create_label_entry_pair(knob_props_frame, " 2 angle: ", 5, 4, "0")
    rotation_3_Key_Var = create_label_entry_pair(knob_props_frame, " 3 rotation command: ", 6, 2, "none")
    rotation_3_angle_Var = create_label_entry_pair(knob_props_frame, " 3 angle: ", 6, 4, "0")
    rotation_4_Key_Var = create_label_entry_pair(knob_props_frame, " 4 rotation command: ", 7, 2, "none")
    rotation_4_angle_Var = create_label_entry_pair(knob_props_frame, " 4 angle: ", 7, 4, "0")
    rotation_5_Key_Var = create_label_entry_pair(knob_props_frame, " 5 rotation command: ", 8, 2, "none")
    rotation_5_angle_Var = create_label_entry_pair(knob_props_frame, " 5 angle: ", 8, 4, "0")
    rotation_6_Key_Var = create_label_entry_pair(knob_props_frame, " 6 rotation command: ", 9, 2, "none")
    rotation_6_angle_Var = create_label_entry_pair(knob_props_frame, " 6 angle: ", 9, 4, "0")
    rotation_7_Key_Var = create_label_entry_pair(knob_props_frame, " 7 rotation command: ", 10, 2, "none")
    rotation_7_angle_Var = create_label_entry_pair(knob_props_frame, " 7 angle: ", 10, 4, "0")
    rotation_8_Key_Var = create_label_entry_pair(knob_props_frame, " 8 rotation command: ", 11, 2, "none")
    rotation_8_angle_Var = create_label_entry_pair(knob_props_frame, " 8 angle: ", 11, 4, "0")
    rotation_9_Key_Var = create_label_entry_pair(knob_props_frame, " 9 rotation command: ", 12, 2, "none")
    rotation_9_angle_Var = create_label_entry_pair(knob_props_frame, " 9 angle: ", 12, 4, "0")
    rotation_10_Key_Var = create_label_entry_pair(knob_props_frame, " 10 rotation command: ", 13, 2, "none")
    rotation_10_angle_Var = create_label_entry_pair(knob_props_frame, " 10 angle: ", 13, 4, "0")


        # Create a frame for rotation commands
    imageProps_frame = ttk.Frame(alpha_form, padding="10")
    imageProps_frame.grid(row=6, column=2, columnspan=3, sticky="nsew")

    # Initially hide the frame
    imageProps_frame.grid_remove()

    # Create a toggle button to show/hide the additional frame
    toggle_additional_button = ttk.Button(alpha_form, text="Knob Image", command=lambda: toggle_frame(imageProps_frame, toggle_additional_button))
    toggle_additional_button.grid(row=5, column=2, columnspan=3, padx=5, pady=5)

    conversion_1_Key_Var = create_label_entry_pair(imageProps_frame, " 1 pos command: ", 14, 2, "none")
    conversion_1_file_path_Var = create_file_path_entry(imageProps_frame, 14, "conversion_1_file_path_Var")
    conversion_2_Key_Var = create_label_entry_pair(imageProps_frame, " 2 pos command: ", 15, 2, "none")
    conversion_2_file_path_Var = create_file_path_entry(imageProps_frame, 15, "conversion_2_file_path_Var")
    conversion_3_Key_Var = create_label_entry_pair(imageProps_frame, " 3 pos command: ", 16, 2, "none")
    conversion_3_file_path_Var = create_file_path_entry(imageProps_frame, 16, "conversion_3_file_path_Var")
    conversion_4_Key_Var = create_label_entry_pair(imageProps_frame, " 4 pos command: ", 17, 2, "none")
    conversion_4_file_path_Var = create_file_path_entry(imageProps_frame, 17, "conversion_4_file_path_Var")
    conversion_5_Key_Var = create_label_entry_pair(imageProps_frame, " 5 pos command: ", 18, 2, "none")
    conversion_5_file_path_Var = create_file_path_entry(imageProps_frame, 18, "conversion_5_file_path_Var")
    conversion_6_Key_Var = create_label_entry_pair(imageProps_frame, " 6 pos command: ", 19, 2, "none")
    conversion_6_file_path_Var = create_file_path_entry(imageProps_frame, 19, "conversion_6_file_path_Var")
    conversion_7_Key_Var = create_label_entry_pair(imageProps_frame, " 7 pos command: ", 20, 2, "none")
    conversion_7_file_path_Var = create_file_path_entry(imageProps_frame, 20, "conversion_7_file_path_Var")
    conversion_8_Key_Var = create_label_entry_pair(imageProps_frame, " 8 pos command: ", 21, 2, "none")
    conversion_8_file_path_Var = create_file_path_entry(imageProps_frame, 21, "conversion_8_file_path_Var")
    conversion_9_Key_Var = create_label_entry_pair(imageProps_frame, " 9 pos command: ", 22, 2, "none")
    conversion_9_file_path_Var = create_file_path_entry(imageProps_frame, 22, "conversion_9_file_path_Var")
    conversion_10_Key_Var = create_label_entry_pair(imageProps_frame, " 10 pos command: ", 23, 2, "none")
    conversion_10_file_path_Var = create_file_path_entry(imageProps_frame, 23, "conversion_10_file_path_Var")

    # Create a frame for rotation commands
    Conversion_frame = ttk.Frame(alpha_form, padding="10")
    Conversion_frame.grid(row=8, column=2, columnspan=3, sticky="nsew")

    # Initially hide the frame
    Conversion_frame.grid_remove()

    # Create a toggle button to show/hide the additional frame
    toggle_additional_button = ttk.Button(alpha_form, text="value Conversion", command=lambda: toggle_frame(Conversion_frame, toggle_additional_button))
    toggle_additional_button.grid(row=7, column=2, columnspan=3, padx=5, pady=5)

    Value_conversion_1_Key_Var = create_label_entry_pair(Conversion_frame, " 1  Value command: ", 24, 2, "none")
    Value_conversion_1_angle_Var = create_label_entry_pair(Conversion_frame, " 1 Conversion angle: ", 24, 4, "0")
    Value_conversion_2_Key_Var = create_label_entry_pair(Conversion_frame, " 2 Value command: ", 25, 2, "none")
    Value_conversion_2_angle_Var = create_label_entry_pair(Conversion_frame, " 2 Conversion angle: ", 25, 4, "0")
    Value_conversion_3_Key_Var = create_label_entry_pair(Conversion_frame, " 3 Value command: ", 26, 2, "none")
    Value_conversion_3_angle_Var = create_label_entry_pair(Conversion_frame, " 3 Conversion angle: ", 26, 4, "0")
    Value_conversion_4_Key_Var = create_label_entry_pair(Conversion_frame, " 4 Value command: ", 27, 2, "none")
    Value_conversion_4_angle_Var = create_label_entry_pair(Conversion_frame, " 4 Conversion angle: ", 27, 4, "0")
    Value_conversion_5_Key_Var = create_label_entry_pair(Conversion_frame, " 5 Value command: ", 28, 2, "none")
    Value_conversion_5_angle_Var = create_label_entry_pair(Conversion_frame, " 5 Conversion angle: ", 28, 4, "0")

    save_button = Button(alpha_form, text="Save", command=save_alpha_data)
    save_button.grid(row=25, columnspan=2)


