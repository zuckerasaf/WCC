import tkinter as tk
from tkinter import filedialog, simpledialog, Toplevel, Label, Entry, Button, StringVar, OptionMenu
from PIL import Image, ImageTk
import os
import json
from Util import move_image, rotate_image, Bring_File_path  # Import the move_image function

# Define rotation_angle and rotation_entry as global variables at the top of the script
rotation_angle = 0
#rotation_entry = None

# Global variables
current_image_path = None
new_image_path = None
new_image_position = (0, 0)
combined_image_path = None
base_img = None  # Add a global variable to store the base image
move_pixels = 10  # Default number of pixels to move
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
    global current_image_path,  rotated_new_img, new_image_path, new_image_path, new_image_position, combined_image_path, base_img, rotation_angle
    if base_img and new_image_path:
        # Open the new image
        new_img = Image.open(new_image_path)

        # Rotate the new image
        rotated_new_img = new_img.rotate(rotation_angle, expand=True)

        # Calculate the new position to keep the rotated image centered
        new_x = new_image_position[0] - (rotated_new_img.width - new_img.width) // 2
        new_y = new_image_position[1] - (rotated_new_img.height - new_img.height) // 2
        new_position = (new_x, new_y)

        # Create a copy of the base image to avoid modifying the original
        combined_img = base_img.copy()

       # # Paste the new image on top of the base image at the current position
       #combined_img.paste(new_img, new_image_position, new_img if new_img.mode == 'RGBA' else None)

        # Paste the rotated new image on top of the base image at the current position
        combined_img.paste(rotated_new_img, new_image_position, rotated_new_img if rotated_new_img.mode == 'RGBA' else None)


        # Save the combined image to a temporary file
        combined_image_path = os.path.join(os.path.dirname(current_image_path), "combined_image.png")
        combined_img.save(combined_image_path)

        # Update the current image path to the combined image
        current_image_path = combined_image_path

        # Update the image label with the combined image
        img_tk = ImageTk.PhotoImage(combined_img)
        image_label.config(image=img_tk)
        image_label.image = img_tk  # Keep a reference to avoid garbage collection

#def update_info_label():
#   global new_image_position
#    info_label.config(text=f"New Image Position: {new_image_position}")

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
        step_size_label.config(text=f"Current Step Size: {move_pixels} pixels")

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

    def save_alpha_data():
        image_key = image_key_entry.get()
        image_name = image_name_entry.get()
        image_size = image_size_entry.get()
        image_position = image_position_entry.get()
        rotation = rotation_entry.get()
        type_value = type_var.get()
        group_value = group_var.get()
        offset_on_value = offset_on_var.get()
        offset_off_value = offset_off_var.get()
        debugMode_value = debugMode_var.get()
        is_clickable_value = is_clickable_var.get()
        click_bounds_height_factor_value = click_bounds_height_factor_var.get()
        click_bounds_width_factor_value = click_bounds_width_factor_var.get()
        grid_size_value = grid_size_var.get()
        grid_direction_value = grid_direction_var.get()
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


        try:
            width, height = image_size.split('x')
        except ValueError:
            width, height = "0", "0"  # Default values in case of error

        data = {
            "key": image_key,
            "type": type_value,
            "group": group_value,
            "backend_name": image_name,
            "width": width,
            "height": height,
            "left": new_image_position[0],
            "top": new_image_position[1],
            "offset_on": offset_on_value,
            "offset_off": offset_off_value,
            "image_on": "/CMDSPanel/SWITCH_10_UP1.png",
            "image_off": "/CMDSPanel/SWITCH_10_DOWN_1.png",
            "debugMode": debugMode_value,
            "is_clickable": is_clickable_value,
            "click_props": {
                "click_bounds_height_factor": click_bounds_height_factor_value,
                "click_bounds_width_factor": click_bounds_width_factor_value,
                "grid_size": grid_size_value,
                "grid_direction": grid_direction_value,
            },
            "analog_props": {
                    "rotation": {
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
            "knob_props": {
                "conversion": {
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

    image_key_entry = create_label_entry_pair(alpha_form, "Image key:", 0, 2, "0")
    image_name_entry = create_label_entry_pair(alpha_form, "Image Name:", 0, 0, picture.image_id)
    
    Label(alpha_form, text="Image Size:").grid(row=1, column=0)
    image_size_entry = Entry(alpha_form)
    image_size_entry.grid(row=1, column=1)
    image_size_entry.insert(0, str(picture.width)+" X "+str(picture.height))  # Assuming the resized image size

    Label(alpha_form, text="Image Position:").grid(row=2, column=0)
    image_position_entry = Entry(alpha_form)
    image_position_entry.grid(row=2, column=1)
    image_position_entry.insert(0, str(new_image_position))

    Label(alpha_form, text="Rotation:").grid(row=3, column=2)
    rotation_entry = Entry(alpha_form)
    rotation_entry.grid(row=3, column=3)
    rotation_entry.insert(0, str(rotation_angle))  # Initial rotation 

    Label(alpha_form, text="Type:").grid(row=3, column=0)
    type_var = StringVar(alpha_form)
    type_var.set("boolean")  # Default type value
    type_options = ["a", "b", "boolean"]
    type_menu = OptionMenu(alpha_form, type_var, *type_options)
    type_menu.grid(row=3, column=1)

    Label(alpha_form, text="Group:").grid(row=4, column=0)
    group_var = StringVar(alpha_form)
    group_var.set("state2")  # Default group value
    group_options = ["a", "b", "state2"]
    group_menu = OptionMenu(alpha_form, group_var, *group_options)
    group_menu.grid(row=4, column=1)


    offset_on_var = create_label_entry_pair(alpha_form, "offset_on:", 5, 0, "0")
    offset_off_var = create_label_entry_pair(alpha_form, "offset_on:", 6, 0, "0")
    debugMode_var = create_label_entry_pair(alpha_form, "debug Mode:", 7, 0, "false")
    is_clickable_var = create_label_entry_pair(alpha_form, "is clickable:", 8, 0, "true")
    click_bounds_height_factor_var = create_label_entry_pair(alpha_form, "click bounds height factor:", 9, 0, "2")
    click_bounds_width_factor_var = create_label_entry_pair(alpha_form, "click bounds width factor:", 10, 0, "1.5")
    grid_size_var = create_label_entry_pair(alpha_form, "grid size:", 11, 0, "2")



    Label(alpha_form, text="grid direction:").grid(row=12, column=0)
    grid_direction_var = StringVar(alpha_form)
    grid_direction_var.set("UD")  # Default type value
    grid_direction_options = ["UD", "LR", "Other"]
    grid_direction_menu = OptionMenu(alpha_form, grid_direction_var, *grid_direction_options)
    grid_direction_menu.grid(row=12, column=1)

    Label(alpha_form, text="Blinking color:").grid(row=13, column=0)
    color_var= StringVar(alpha_form)
    color_var.set("yellow")  # Default type value
    color_options = ["yellow", "red", "blue"]
    color_menu = OptionMenu(alpha_form, color_var, *color_options)
    color_menu.grid(row=13, column=1)

    # Use the function to create label and entry pairs
    rotation_1_Key_Var = create_label_entry_pair(alpha_form, " 1 rotation command: ", 4, 2, "none")
    rotation_1_angle_Var = create_label_entry_pair(alpha_form, " 1 angle: ", 4, 4, "0")
    rotation_2_Key_Var = create_label_entry_pair(alpha_form, " 2 rotation command: ", 5, 2, "none")
    rotation_2_angle_Var = create_label_entry_pair(alpha_form, " 2 angle: ", 5, 4, "0")
    rotation_3_Key_Var = create_label_entry_pair(alpha_form, " 3 rotation command: ", 6, 2, "none")
    rotation_3_angle_Var = create_label_entry_pair(alpha_form, " 3 angle: ", 6, 4, "0")
    rotation_4_Key_Var = create_label_entry_pair(alpha_form, " 4 rotation command: ", 7, 2, "none")
    rotation_4_angle_Var = create_label_entry_pair(alpha_form, " 4 angle: ", 7, 4, "0")
    rotation_5_Key_Var = create_label_entry_pair(alpha_form, " 5 rotation command: ", 8, 2, "none")
    rotation_5_angle_Var = create_label_entry_pair(alpha_form, " 5 angle: ", 8, 4, "0")
    rotation_6_Key_Var = create_label_entry_pair(alpha_form, " 6 rotation command: ", 9, 2, "none")
    rotation_6_angle_Var = create_label_entry_pair(alpha_form, " 6 angle: ", 9, 4, "0")
    rotation_7_Key_Var = create_label_entry_pair(alpha_form, " 7 rotation command: ", 10, 2, "none")
    rotation_7_angle_Var = create_label_entry_pair(alpha_form, " 7 angle: ", 10, 4, "0")
    rotation_8_Key_Var = create_label_entry_pair(alpha_form, " 8 rotation command: ", 11, 2, "none")
    rotation_8_angle_Var = create_label_entry_pair(alpha_form, " 8 angle: ", 11, 4, "0")
    rotation_9_Key_Var = create_label_entry_pair(alpha_form, " 9 rotation command: ", 12, 2, "none")
    rotation_9_angle_Var = create_label_entry_pair(alpha_form, " 9 angle: ", 12, 4, "0")
    rotation_10_Key_Var = create_label_entry_pair(alpha_form, " 10 rotation command: ", 13, 2, "none")
    rotation_10_angle_Var = create_label_entry_pair(alpha_form, " 10 angle: ", 13, 4, "0")


    conversion_1_Key_Var = create_label_entry_pair(alpha_form, " 1 pos command: ", 14, 2, "none")

    Label(alpha_form, text="File Path:").grid(row=14, column=4)
    conversion_1_file_path_Var = StringVar()
    file_path_entry = Entry(alpha_form, textvariable=conversion_1_file_path_Var)
    file_path_entry.grid(row=14, column=5)
    
    file_path_button = Button(alpha_form, text="file", command=lambda: on_bring_file_path(conversion_1_file_path_Var))
    file_path_button.grid(row=14, column=6)

    conversion_2_Key_Var = create_label_entry_pair(alpha_form, " 2 pos command: ", 15, 2, "none")

    Label(alpha_form, text="File Path:").grid(row=15, column=4)
    conversion_2_file_path_Var = StringVar()
    file_path_entry = Entry(alpha_form, textvariable=conversion_2_file_path_Var)
    file_path_entry.grid(row=15, column=5)
    
    file_path_button = Button(alpha_form, text="file", command=lambda: on_bring_file_path(conversion_2_file_path_Var))
    file_path_button.grid(row=15, column=6)

    conversion_3_Key_Var = create_label_entry_pair(alpha_form, " 3 pos command: ", 16, 2, "none")

    Label(alpha_form, text="File Path:").grid(row=16, column=4)
    conversion_3_file_path_Var = StringVar()
    file_path_entry = Entry(alpha_form, textvariable=conversion_3_file_path_Var)
    file_path_entry.grid(row=16, column=5)
    
    file_path_button = Button(alpha_form, text="file", command=lambda: on_bring_file_path(conversion_3_file_path_Var))
    file_path_button.grid(row=16, column=6)

    conversion_4_Key_Var = create_label_entry_pair(alpha_form, " 4 pos command: ", 17, 2, "none")

    Label(alpha_form, text="File Path:").grid(row=17, column=4)
    conversion_4_file_path_Var = StringVar()
    file_path_entry = Entry(alpha_form, textvariable=conversion_4_file_path_Var)
    file_path_entry.grid(row=17, column=5)
    
    file_path_button = Button(alpha_form, text="file", command=lambda: on_bring_file_path(conversion_4_file_path_Var))
    file_path_button.grid(row=17, column=6)

    conversion_5_Key_Var = create_label_entry_pair(alpha_form, " 5 pos command: ", 18, 2, "none")

    Label(alpha_form, text="File Path:").grid(row=18, column=4)
    conversion_5_file_path_Var = StringVar()
    file_path_entry = Entry(alpha_form, textvariable=conversion_5_file_path_Var)
    file_path_entry.grid(row=18, column=5)
    
    file_path_button = Button(alpha_form, text="file", command=lambda: on_bring_file_path(conversion_5_file_path_Var))
    file_path_button.grid(row=18, column=6)

    conversion_6_Key_Var = create_label_entry_pair(alpha_form, " 6 pos command: ", 19, 2, "none")

    Label(alpha_form, text="File Path:").grid(row=19, column=4)
    conversion_6_file_path_Var = StringVar()
    file_path_entry = Entry(alpha_form, textvariable=conversion_6_file_path_Var)
    file_path_entry.grid(row=19, column=5)
    
    file_path_button = Button(alpha_form, text="file", command=lambda: on_bring_file_path(conversion_6_file_path_Var))
    file_path_button.grid(row=19, column=6)

    conversion_7_Key_Var = create_label_entry_pair(alpha_form, " 7 pos command: ", 20, 2, "none")

    Label(alpha_form, text="File Path:").grid(row=20, column=4)
    conversion_7_file_path_Var = StringVar()
    file_path_entry = Entry(alpha_form, textvariable=conversion_7_file_path_Var)
    file_path_entry.grid(row=20, column=5)
    
    file_path_button = Button(alpha_form, text="file", command=lambda: on_bring_file_path(conversion_7_file_path_Var))
    file_path_button.grid(row=20, column=6)

    conversion_8_Key_Var = create_label_entry_pair(alpha_form, " 8 pos command: ", 21, 2, "none")

    Label(alpha_form, text="File Path:").grid(row=21, column=4)
    conversion_8_file_path_Var = StringVar()
    file_path_entry = Entry(alpha_form, textvariable=conversion_8_file_path_Var)
    file_path_entry.grid(row=21, column=5)
    
    file_path_button = Button(alpha_form, text="file", command=lambda: on_bring_file_path(conversion_8_file_path_Var))
    file_path_button.grid(row=21, column=6)

    conversion_9_Key_Var = create_label_entry_pair(alpha_form, " 9 pos command: ", 22, 2, "none")

    Label(alpha_form, text="File Path:").grid(row=22, column=4)
    conversion_9_file_path_Var = StringVar()
    file_path_entry = Entry(alpha_form, textvariable=conversion_9_file_path_Var)
    file_path_entry.grid(row=22, column=5)
    
    file_path_button = Button(alpha_form, text="file", command=lambda: on_bring_file_path(conversion_9_file_path_Var))
    file_path_button.grid(row=22, column=6)

    conversion_10_Key_Var = create_label_entry_pair(alpha_form, " 10 pos command: ", 23, 2, "none")

    Label(alpha_form, text="File Path:").grid(row=23, column=4)
    conversion_10_file_path_Var = StringVar()
    file_path_entry = Entry(alpha_form, textvariable=conversion_10_file_path_Var)
    file_path_entry.grid(row=23, column=5)
    
    file_path_button = Button(alpha_form, text="file", command=lambda: on_bring_file_path(conversion_10_file_path_Var))
    file_path_button.grid(row=23, column=6)

    save_button = Button(alpha_form, text="Save", command=save_alpha_data)
    save_button.grid(row=15, columnspan=2)

def handle_move_image(event):
    global new_image_position
    new_image_position = move_image(event, new_image_position, move_pixels, new_image_path, image_position_entry, combine_images, update_info_label)

def handle_rotate_image(event):
    global rotation_angle
    rotation_angle = rotate_image(event, img, rotation_angle, rotation_entry, image_label, combine_images, update_info_label)

# Create the main window
root = tk.Tk()
root.title("Image Browser")

current_image_path = None
new_image_path = None
new_image_position = (0, 0)
combined_image_path = None

# Create a button to browse files
browse_button = tk.Button(root, text="Browse Image", command=browse_image)
browse_button.pack()

# Create a label to display the image
image_label = tk.Label(root)
image_label.pack()

# Create a label to display the image_id and file_path
info_label = tk.Label(root, text="")
info_label = tk.Label(root, text="Image ID: \nFile Path: \nNew Image Position: (0, 0)")
info_label.pack()

# Create a button to add another image on top
add_button = tk.Button(root, text="Add Image", command=add_image)
add_button.pack()


# Create and place the set pixels button
set_pixels_button = tk.Button(root, text="Set Move Pixels", command=set_move_pixels)
set_pixels_button.pack()

# Create and place the step size label next to the set pixels button
step_size_label = tk.Label(root, text=f"Current Step Size: {move_pixels} pixels")
step_size_label.pack()

# Bind arrow keys to the move_image function
root.bind('<Right>', handle_move_image)
root.bind('<Left>', handle_move_image)
root.bind('<Up>', handle_move_image)
root.bind('<Down>', handle_move_image)

 # Bind the "R" key to rotate the image
root.bind("<r>", handle_rotate_image)


# Create a button to save the combined image
save_button = tk.Button(root, text="Save Image", command=save_image)
save_button.pack()

# Create a button to close the form
close_button = tk.Button(root, text="Close", command=root.destroy)
close_button.pack()

# Start the Tkinter event loop
root.mainloop()