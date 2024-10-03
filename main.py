import tkinter as tk
from tkinter import filedialog, simpledialog, Toplevel, Label, Entry, Button, StringVar, OptionMenu, ttk
from tkinter.filedialog import asksaveasfilename
from PIL import Image, ImageTk
import os
import json
from Util import move_image, rotate_image, Bring_File_path  # Import the move_image function

# Global variables
rotation_angle = 0
disp_rotation_angle = 0
current_image_path = None
new_image_path = None
new_image_position = (0, 0)
combined_image_path = None
base_img = None  # Add a global variable to store the base image
move_pixels = 10  # Default number of pixels to move
rotate_degree = 10
image_position_entry = None  # Reference to the image position entry field in the alpha form
img = None  # Add a global variable to store the image
image_label = None  # Add a global variable to store the image label

class Picture:
    def __init__(self, image_id, file_path, width, height):
        self.image_id = image_id
        self.file_path = file_path
        self.width = width
        self.height = height

def hello_world():
    print("Hello, World!")

def browse_image():
    global img, img_tk, image_label, new_image_path, current_image_path, image_id,rotated_new_img,  new_image_path, new_image_position, combined_image_path

    # Create a new, empty alpha_data.json file
    with open("alpha_data.json", "w") as file:
        json.dump([], file)

    # Open file dialog to select an image file
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.gif")])
    if file_path:
        current_image_path = os.path.normpath(file_path)
        new_image_path = None  # Reset the new image path
        rotated_new_img = 0
        new_image_position = (0, 0)  # Reset the new image position
        combined_image_path = None  # Reset the combined image path
        # Open and display the image
        img = Image.open(file_path)
        img_tk = ImageTk.PhotoImage(img)
        image_label.config(image=img_tk)
        image_label.image = img_tk  # Keep a reference to avoid garbage collection

        # Get the image size
        width, height = img.width, img.height

        # Create a Picture instance with the image name as the ID
        image_id = os.path.basename(file_path)
        picture = Picture(image_id=image_id, file_path=file_path, width=width, height=height)
        
        # Update the text label with image_id and file_path
        info_label.config(text=f"Image ID: {picture.image_id}\nFile Path: {picture.file_path}")
        print(f"Created Picture instance: ID={picture.image_id}, Path={picture.file_path}")
       
        # Save the image details to a text file
        with open("image_details.txt", "a") as file:
            file.write(f"Image ID: {picture.image_id}, File Path: {picture.file_path}\n")

        # Open the alpha form
        #open_alpha_form(picture)

    
def add_image():
    global current_image_path, new_image_path, rotated_new_img, new_image_position, base_img, img, img_tk, image_id

    if current_image_path:
        # Open file dialog to select another image file
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.gif")])
        if file_path:

            new_image_path = file_path
            new_image_position = (0, 0)  # Start at the top-left corner
            base_img = Image.open(current_image_path)  # Open and store the base image
            image_id = os.path.basename(file_path)

            # Combine images and update info label
            combine_images()
            update_info_label()

            # Create a Picture instance with the image name as the ID
            image_id = os.path.basename(file_path)
             # Get the image size
            img = Image.open(file_path)
            width, height = img.width, img.height
            picture = Picture(image_id=image_id, file_path=file_path, width=width, height=height)

            # Open the alpha form
            open_alpha_form(picture, f"{width}x{height}")

def combine_images():
    global current_image_path,  rotated_new_img, new_image_path, new_image_path, new_image_position, combined_image_path, base_img, rotation_angle, disp_rotation_angle
    if base_img and new_image_path:
        # Open the new image
        new_img = Image.open(new_image_path)

        # Calculate the center of the original image
        original_center_x = new_image_position[0] + new_img.width // 2
        original_center_y = new_image_position[1] + new_img.height // 2

        # Rotate the image
        rotated_new_img = new_img.rotate(rotation_angle, expand=True)

        # Calculate the new position to keep the rotated image centered
        new_x = original_center_x - rotated_new_img.width // 2
        new_y = original_center_y - rotated_new_img.height // 2
        new_position = (new_x, new_y)

        # Create a copy of the base image to avoid modifying the original
        combined_img = base_img.copy()

        # Paste the rotated new image on top of the base image at the current position
        combined_img.paste(rotated_new_img, new_position, rotated_new_img if rotated_new_img.mode == 'RGBA' else None)


        # Save the combined image to a temporary file
        combined_image_path = os.path.join(os.path.dirname(current_image_path), "combined_image.png")
        combined_img.save(combined_image_path)

        # Update the current image path to the combined image
        current_image_path = combined_image_path

        # Update the image label with the combined image
        img_tk = ImageTk.PhotoImage(combined_img)
        image_label.config(image=img_tk)
        image_label.image = img_tk  # Keep a reference to avoid garbage collection

# Function to update the info label
def update_info_label():
    global current_image_path, new_image_position
    if current_image_path:
        # Assuming picture is an object with image_id and file_path attributes
        picture = type('Picture', (object,), {'image_id': 1, 'file_path': current_image_path})()
        info_label.config(text=f"Image ID: {picture.image_id}\nFile Path: {picture.file_path}\nNew Image Position: {new_image_position}")

def set_move_pixels():
    global move_pixels
    pixels = simpledialog.askinteger("Input", "Enter the number of pixels to move:", minvalue=1)
    if pixels:
        move_pixels = pixels
        step_size_label.config(text=f"Step : {move_pixels} pixels")

def set_rotate_degree():
    global rotate_degree, disp_rotation_angle
    degree = simpledialog.askinteger("Input", "Enter the roattion degree step:", minvalue=1)
    if degree:
        rotate_degree = degree
        step_angle_label.config(text=f"step: {rotate_degree} degree")

def save_image():
    global combined_image_path
    if combined_image_path:
        # Open file dialog to select save location
        save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
        if save_path:
            # Save the combined image to the specified location
            img = Image.open(combined_image_path)
            img.save(save_path)
            print(f"Image saved to {save_path}")

def open_alpha_form(picture,image_size):
    global image_position_entry, rotation_entry,file_path
    

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

        image_name = image_name_entry.get()
        image_size = image_size_entry.get()
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
            "backend_name": image_name,
            "type": type_value,
            # "group": group_value,
            "width": picture.width,
            "height": picture.height,
            "left": new_image_position[0],
            "top": new_image_position[1],
            "offset_on": offset_on_value,
            "offset_off": offset_off_value,
            "imageProps": {
                "imageDefault": image_name,
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

    # image_key_entry = create_label_entry_pair(alpha_form, "Image key:", 0, 2, "0")
    image_name_entry = create_label_entry_pair(alpha_form, "Image Name:", 0, 0, picture.image_id)
    
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
    save_button.grid(row=24, columnspan=2)

def handle_move_image(event):
    global new_image_position
    small_step = 1
    if event.state & 0x0001:  # Check if Shift key is pressed
        small_step = 10
    new_image_position = move_image(event, new_image_position, move_pixels, new_image_path, image_position_entry, small_step, combine_images, update_info_label)

def handle_rotate_image(event, direction):
    global rotation_angle
    small_rotate = 1
    if event.state & 0x0004:  # Check if Ctrl key is pressed
        small_rotate = 10
    if direction == "left":
        rotation_angle = rotate_image(event, img, rotation_angle, -rotate_degree // small_rotate, rotation_entry, image_label, combine_images)# , update_info_label)
    elif direction == "right":
        rotation_angle = rotate_image(event, img, rotation_angle, rotate_degree // small_rotate, rotation_entry, image_label, combine_images)#, update_info_label)

def handle_rotate_left(event):
    handle_rotate_image(event, "left")

def handle_rotate_right(event):
    handle_rotate_image(event, "right")

def save_and_close():
    # Read data from alpha_data.json
    try:
        with open("alpha_data.json", 'r') as json_file:
            data = json.load(json_file)
    except FileNotFoundError:
        print("alpha_data.json not found.")
        return

    # Prompt the user for a new filename
    file_path = asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json"), ("All files", "*.*")])
    if file_path:
        # Save the data to the new JSON file
        with open(file_path, 'w') as new_json_file:
            json.dump(data, new_json_file, indent=4)
    
    # Close the form
    root.destroy()
# Create the main window
root = tk.Tk()
root.title("Image Browser")

current_image_path = None
new_image_path = None
new_image_position = (0, 0)
combined_image_path = None

# Create a button to browse files
browse_button = tk.Button(root, text="Browse Image", command=browse_image)
browse_button.grid(row=0, column=1)

# Create a label to display the image
image_label = tk.Label(root)
image_label.grid(row=1, column=0, columnspan=4, sticky="nsew")

# Create a label to display the image_id and file_path
info_label = tk.Label(root, text="")
info_label = tk.Label(root, text="Image ID: \nFile Path: \nNew Image Position: (0, 0)")
info_label.grid(row=2, column=1, padx=5, pady=5)

# Create a button to add another image on top
add_button = tk.Button(root, text="Add Image", command=add_image)
add_button.grid(row=3, column=1, padx=5, pady=5)

# Create and place the set pixels button
set_pixels_button = tk.Button(root, text="Set Move Pixels", command=set_move_pixels)
set_pixels_button.grid(row=4, column=0, padx=5, pady=5)

# Create and place the step size label next to the set pixels button
step_size_label = tk.Label(root, text=f" Step : {move_pixels} pixels")
step_size_label.grid(row=4, column=1, padx=5, pady=5)

# Create and place the set pixels button
set_angle_button = tk.Button(root, text="Set angle rotation", command=set_rotate_degree)
set_angle_button.grid(row=4, column=2, padx=5, pady=5)

# Create and place the step size label next to the set pixels button
step_angle_label = tk.Label(root, text=f" Angle : {rotate_degree} degree")
step_angle_label.grid(row=4, column=3, padx=5, pady=5)

# Bind arrow keys to the move_image function
root.bind('<Right>', handle_move_image)
root.bind('<Left>', handle_move_image)
root.bind('<Up>', handle_move_image)
root.bind('<Down>', handle_move_image)

# Bind the "R" key to rotate the image to the left
root.bind("<r>", handle_rotate_left)

# Bind the "T" key to rotate the image to the right
root.bind("<t>", handle_rotate_right)

# Create a button to close the form
close_button = tk.Button(root, text="Save and Close", command=save_and_close)
close_button.grid(row=7, column=1, padx=5, pady=5)

# Configure grid rows and columns
for i in range(8):
    root.grid_rowconfigure(i, weight=1)

for i in range(3):
    root.grid_columnconfigure(i, weight=1)

# Start the Tkinter event loop
root.mainloop()