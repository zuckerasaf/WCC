import tkinter as tk
from tkinter import filedialog, simpledialog, Toplevel, Label, Entry, Button, StringVar, OptionMenu
from PIL import Image, ImageTk
import os
import json

# Global variables
current_image_path = None
new_image_path = None
new_image_position = (0, 0)
combined_image_path = None
base_img = None  # Add a global variable to store the base image
move_pixels = 10  # Default number of pixels to move
image_position_entry = None  # Reference to the image position entry field in the alpha form


class Picture:
    def __init__(self, image_id, file_path, width, height):
        self.image_id = image_id
        self.file_path = file_path
        self.width = width
        self.height = height

def hello_world():
    print("Hello, World!")

def browse_image():

    # Create a new, empty alpha_data.json file
    with open("alpha_data.json", "w") as file:
        json.dump([], file)

    global current_image_path, image_id, new_image_path, new_image_position, combined_image_path
    # Open file dialog to select an image file
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.gif")])
    if file_path:
        current_image_path = os.path.normpath(file_path)
        new_image_path = None  # Reset the new image path
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
    global current_image_path, new_image_path, new_image_position, base_img
    if current_image_path:
        # Open file dialog to select another image file
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.gif")])
        if file_path:
            new_image_path = file_path
            new_image_position = (0, 0)  # Start at the top-left corner
            base_img = Image.open(current_image_path)  # Open and store the base image
            image_id = os.path.basename(file_path)
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


def move_image(event):
    global new_image_position, move_pixels
    if new_image_path:
        if event.keysym == 'Right':
            new_image_position = (new_image_position[0] + move_pixels, new_image_position[1])
        elif event.keysym == 'Left':
            new_image_position = (new_image_position[0] - move_pixels, new_image_position[1])
        elif event.keysym == 'Up':
            new_image_position = (new_image_position[0], new_image_position[1] - move_pixels)
        elif event.keysym == 'Down':
            new_image_position = (new_image_position[0], new_image_position[1] + move_pixels)
        combine_images()
        update_info_label()
        if image_position_entry:
            image_position_entry.delete(0, tk.END)
            image_position_entry.insert(0, str(new_image_position))

def combine_images():
    global current_image_path, new_image_path, new_image_position, combined_image_path, base_img
    if base_img and new_image_path:
        # Open the new image
        new_img = Image.open(new_image_path)

        # Create a copy of the base image to avoid modifying the original
        combined_img = base_img.copy()

        # Paste the new image on top of the base image at the current position
        combined_img.paste(new_img, new_image_position, new_img if new_img.mode == 'RGBA' else None)

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
    global image_position_entry

    def save_alpha_data():
        image_name = image_name_entry.get()
        image_size = image_size_entry.get()
        image_position = image_position_entry.get()
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

        try:
            width, height = image_size.split('x')
        except ValueError:
            width, height = "0", "0"  # Default values in case of error

        data = {
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

    Label(alpha_form, text="Image Name:").grid(row=0, column=0)
    image_name_entry = Entry(alpha_form)
    image_name_entry.grid(row=0, column=1)
    image_name_entry.insert(0, picture.image_id)

    Label(alpha_form, text="Image Size:").grid(row=1, column=0)
    image_size_entry = Entry(alpha_form)
    image_size_entry.grid(row=1, column=1)
    image_size_entry.insert(0, str(picture.width)+" X "+str(picture.height))  # Assuming the resized image size

    Label(alpha_form, text="Image Position:").grid(row=2, column=0)
    image_position_entry = Entry(alpha_form)
    image_position_entry.grid(row=2, column=1)
    image_position_entry.insert(0, str(new_image_position))

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

    Label(alpha_form, text="offset_on:").grid(row=5, column=0)
    offset_on_var = Entry(alpha_form)
    offset_on_var.grid(row=5, column=1)
    offset_on_var.insert(0, "0")  # Assuming the offset_on_var = 0

    Label(alpha_form, text="offset_off:").grid(row=6, column=0)
    offset_off_var = Entry(alpha_form)
    offset_off_var.grid(row=6, column=1)
    offset_off_var.insert(0, "0")  # Assuming the offset_off_var = 0 

    Label(alpha_form, text="debug Mode:").grid(row=7, column=0)
    debugMode_var = Entry(alpha_form)
    debugMode_var.grid(row=7, column=1)
    debugMode_var.insert(0, "false")  

    Label(alpha_form, text="is clickable:").grid(row=8, column=0)
    is_clickable_var= Entry(alpha_form)
    is_clickable_var.grid(row=8, column=1)
    is_clickable_var.insert(0, "true")   

    Label(alpha_form, text="click bounds height factor:").grid(row=9, column=0)
    click_bounds_height_factor_var= Entry(alpha_form)
    click_bounds_height_factor_var.grid(row=9, column=1)
    click_bounds_height_factor_var.insert(0, "2")   

    Label(alpha_form, text="click bounds width factor:").grid(row=10, column=0)
    click_bounds_width_factor_var = Entry(alpha_form)
    click_bounds_width_factor_var.grid(row=10, column=1)
    click_bounds_width_factor_var.insert(0, "1.5")

    Label(alpha_form, text="grid size:").grid(row=11, column=0)
    grid_size_var = Entry(alpha_form)
    grid_size_var.grid(row=11, column=1)
    grid_size_var.insert(0, "2")

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

    save_button = Button(alpha_form, text="Save", command=save_alpha_data)
    save_button.grid(row=14, columnspan=2)

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
root.bind('<Right>', move_image)
root.bind('<Left>', move_image)
root.bind('<Up>', move_image)
root.bind('<Down>', move_image)

# Create a button to save the combined image
save_button = tk.Button(root, text="Save Image", command=save_image)
save_button.pack()

# Create a button to close the form
close_button = tk.Button(root, text="Close", command=root.destroy)
close_button.pack()

# Start the Tkinter event loop
root.mainloop()