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
    def __init__(self, image_id, file_path):
        self.image_id = image_id
        self.file_path = file_path

def hello_world():
    print("Hello, World!")

def browse_image():
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
        #img = img.resize((250, 250), Image.LANCZOS)  # Resize image to fit the label
        img_tk = ImageTk.PhotoImage(img)
        image_label.config(image=img_tk)
        image_label.image = img_tk  # Keep a reference to avoid garbage collection

        # Create a Picture instance with the image name as the ID
        image_id = os.path.basename(file_path)
        picture = Picture(image_id=image_id, file_path=file_path)
        
        # Update the text label with image_id and file_path
        info_label.config(text=f"Image ID: {picture.image_id}\nFile Path: {picture.file_path}")
        print(f"Created Picture instance: ID={picture.image_id}, Path={picture.file_path}")
       
        # Save the image details to a text file
        with open("image_details.txt", "a") as file:
            file.write(f"Image ID: {picture.image_id}, File Path: {picture.file_path}\n")

        # Open the alpha form
        open_alpha_form(picture)

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
            picture = Picture(image_id=image_id, file_path=file_path)

            # Open the alpha form
            open_alpha_form(picture)


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

def open_alpha_form(picture):
    global image_position_entry

    #def save_alpha_data():
    #    image_name = image_name_entry.get()
    #    image_size = image_size_entry.get()
    #    image_position = image_position_entry.get()
    #    level = level_entry.get()
    #    trigger = trigger_entry.get()
    #    with open("alpha_data.txt", "a") as file:
    #        file.write(f"Image Name: {image_name}, Image Size: {image_size}, Image Position: {image_position}, Level: {level}, Trigger: {trigger}\n")
    #    alpha_form.destroy()

    def save_alpha_data():
        image_name = image_name_entry.get()
        image_size = image_size_entry.get()
        image_position = image_position_entry.get()
        type_value = type_entry.get()
        group_value = group_entry.get()
        data = {
            "type": type_value,
            "group": group_value,
            "backend_name": image_name,
            "width": image_size.split('x')[0],
            "height": image_size.split('x')[1],
            "left": new_image_position[0],
            "top": new_image_position[1],
            "offset_on": "0",
            "offset_off": "0",
            "image_on": "/CMDSPanel/SWITCH_10_UP1.png",
            "image_off": "/CMDSPanel/SWITCH_10_DOWN_1.png",
            "debugMode": False,
            "is_clickable": True,
            "click_props": {
                "click_bounds_height_factor": 2,
                "click_bounds_width_factor": 1.5,
                "grid_size": 2,
                "grid_direction": "ud,lr,none"
            },
            "blinking": {
                "color": "yellow"
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
    image_size_entry.insert(0, "250x250")  # Assuming the resized image size

    Label(alpha_form, text="Image Position:").grid(row=2, column=0)
    image_position_entry = Entry(alpha_form)
    image_position_entry.grid(row=2, column=1)
    image_position_entry.insert(0, str(new_image_position))

    Label(alpha_form, text="Type:").grid(row=5, column=0)
    type_var = StringVar(alpha_form)
    type_var.set("boolean")  # Default type value
    type_options = ["a", "b", "boolean"]
    type_menu = OptionMenu(alpha_form, type_var, *type_options)
    type_menu.grid(row=3, column=1)

    Label(alpha_form, text="Group:").grid(row=6, column=0)
    group_var = StringVar(alpha_form)
    group_var.set("state2")  # Default group value
    group_options = ["a", "b", "state2"]
    group_menu = OptionMenu(alpha_form, group_var, *group_options)
    group_menu.grid(row=4, column=1)


    save_button = Button(alpha_form, text="Save", command=save_alpha_data)
    save_button.grid(row=5, columnspan=2)

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