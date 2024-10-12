import tkinter as tk
from  PctureClass import Switch, Panel
from tkinter import filedialog, simpledialog, ttk
from tkinter.filedialog import asksaveasfilename
from PIL import Image, ImageTk , ImageFont, ImageDraw
import os
import json
from Util import move_image, rotate_image, load_panel_names, open_alpha_form, load_switch_names  # Import the move_image function
#from shared import selected_panel_name  # Import from shared.py


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
panel_name_label_String = None  # Add a global variable to store the panel name label


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

        select_panel_name()

        # Create a switch instance with the image name as the ID
        image_id = os.path.basename(file_path)
        switch = Switch(image_id=image_id, file_path=file_path, width=width, height=height)
        
        # Update the text label with image_id and file_path
        info_label.config(text=f"Image ID: {switch.image_id}\nFile Path: {switch.file_path}")
        print(f"Created switch instance: ID={switch.image_id}, Path={switch.file_path}")
       
        # Save the image details to a text file
        with open("image_details.txt", "a") as file:
            file.write(f"Image ID: {switch.image_id}, File Path: {switch.file_path}\n")

def select_switch_name(panel_name, switch):
    print("panel_name",panel_name)
   
    if panel_name is None:
        print("No panel selected")
        return
    switch_names = load_switch_names(panel_name)

    
    # Sort the switch names alphabetically
    switch_names_sorted = sorted(switch_names)

    # Create a new window for switch name selection
    switch_window = tk.Toplevel(root)
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
            switch.imageName = selected_switch_name.get()
            print(switch.imageName)
            switch_window.destroy()
            
    

    # Create a button to proceed
    proceed_button = ttk.Button(switch_window, text="Proceed", command=proceed)
    proceed_button.pack(padx=10, pady=10)

    switch_window.wait_window()

# Function to select a panel name
def select_panel_name():
    global panel
    panel_names = load_panel_names()
        
    # Sort the switch names alphabetically
    panel_names_sorted = sorted(panel_names)

    # Create a new window for panel name selection
    panel_window = tk.Toplevel(root)
    panel_window.title("Select Panel Name")

    # Set the width of the panel_window to twice its default width
    default_width = 200  # Example default width, adjust as needed
    panel_window.geometry(f"{default_width * 2}x120")  # Adjust height as needed

    # Create a StringVar to track the selected panel name
    selected_panel_name = tk.StringVar()

    # Create a label and combobox for panel name selection
    panel_label = ttk.Label(panel_window, text="Select Panel Name:")
    panel_label.pack(padx=10, pady=5)

    panel_combobox = ttk.Combobox(panel_window, textvariable=selected_panel_name, values=panel_names_sorted, width=40)
    panel_combobox.pack(padx=10, pady=5)

    # Function to proceed after panel name is selected
    def proceed():
        if selected_panel_name.get():
            panel_window.destroy()
            panel_name_label.config(text=selected_panel_name.get())
            add_button.config(state=tk.NORMAL)
    # Create a button to proceed
    proceed_button = ttk.Button(panel_window, text="Proceed", command=proceed)
    proceed_button.pack(padx=10, pady=10)

    panel_window.wait_window()


def combine_switch_name_with_image(file_path, switch_name, position):
    # Open the image
    img = Image.open(file_path)

    # Initialize ImageDraw
    draw = ImageDraw.Draw(img)

    # Define the font and size
    font = ImageFont.load_default()

    # Add switch name to the image at the specified position
    draw.text(position, switch_name, font=font, fill="white")

    # Save the modified image
    modified_file_path = file_path[:-4] + "_withcaption.png"
    img.save(modified_file_path)

    print(f"Saved modified image with switch name '{switch_name}' at position {position}")
    return modified_file_path

def add_Switch(panel):
    global current_image_path, new_image_path, rotated_new_img, new_image_position, base_img, img, img_tk, image_id, rotation_angle,switch
    rotation_angle = 0
    if current_image_path:
        # Open file dialog to select another image file
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.gif")])
        if file_path:
            new_image_path = file_path
            new_image_position = (0, 0)  # Start at the top-left corner
            base_img = Image.open(current_image_path)  # Open and store the base image
            image_id = os.path.basename(file_path)
            img = Image.open(file_path)
            width, height = img.width, img.height

            switch = Switch(image_id=image_id, file_path=file_path, width=width, height=height)
            select_switch_name(panel, switch)                      
            switch_name = switch.imageName
            print("here "  + switch_name)

            new_image_path = combine_switch_name_with_image(file_path, switch_name, [0,0])

            # Combine images and update info label
            combine_images(rotation_angle)
            update_info_label()

            # Open the alpha form
            open_alpha_form(root,new_image_position, disp_rotation_angle, switch, f"{width}x{height}",panel)

def combine_images(rotation_angle):
    global current_image_path,  rotated_new_img, new_image_path, new_image_path, new_image_position, combined_image_path, base_img, disp_rotation_angle
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
        # Assuming switch is an object with image_id and file_path attributes
        switch = type('switch', (object,), {'image_id': 1, 'file_path': current_image_path})()
        info_label.config(text=f"Image ID: {switch.image_id}\nFile Path: {switch.file_path}\nNew Image Position: {new_image_position}")

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

def handle_move_image(event):
    global new_image_position
    small_step = 1
    if event.state & 0x0001:  # Check if Shift key is pressed
        small_step = 10
    new_image_position = move_image(event, new_image_position, move_pixels, new_image_path, small_step, combine_images, update_info_label,rotation_angle,switch)

def handle_rotate_image(event, direction):
    global rotation_angle
    small_rotate = 1
    if event.state & 0x0004:  # Check if Ctrl key is pressed
        small_rotate = 10
    if direction == "left":
        rotation_angle = rotate_image(event, img, rotation_angle, -rotate_degree // small_rotate, image_label, combine_images)# , update_info_label)
    elif direction == "right":
        rotation_angle = rotate_image(event, img, rotation_angle, rotate_degree // small_rotate, image_label, combine_images)#, update_info_label)

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
browse_button = tk.Button(root, text="Create panel ", command=browse_image)
browse_button.grid(row=0, column=0)

# Create a label to display the image
image_label = tk.Label(root)
image_label.grid(row=1, column=0, columnspan=4, sticky="nsew")

# Create a label to display the image_id and file_path
info_label = tk.Label(root, text="")
info_label = tk.Label(root, text="Image ID: \nFile Path: \nNew Image Position: (0, 0)")
info_label.grid(row=2, column=1, padx=5, pady=5)

# # Create a button to select panel name
# panel_name_button = ttk.Button(root, text="Panel Name", command=select_panel_name)
# panel_name_button.grid(row=3, column=0, padx=5, pady=5)

# Create a label to display the selected panel name
panel_name_label = ttk.Label(root, text="No panel selected")
panel_name_label.grid(row=0, column=1, padx=5, pady=5)

# Create a button to add another image on top
add_button = tk.Button(root, text="Add Switch", command=lambda: add_Switch(panel_name_label.cget("text")), state=tk.DISABLED)
add_button.grid(row=3, column=1, padx=5, pady=5)

# Create a frame to hold the widgets
frame = ttk.Frame(root)
frame.grid(row=4, column=0, padx=10, pady=10)

# Create and place the set pixels button
set_pixels_button = tk.Button(frame, text="Set Move Pixels", command=set_move_pixels)
set_pixels_button.grid(row=0, column=0, padx=0, pady=5)

# Create and place the step size label next to the set pixels button
step_size_label = tk.Label(frame, text=f" Step : {move_pixels} pixels")
step_size_label.grid(row=0, column=1, padx=0, pady=5)

# Create and place the set pixels button
set_angle_button = tk.Button(frame, text="Set angle rotation", command=set_rotate_degree)
set_angle_button.grid(row=1, column=0, padx=1, pady=5)

# Create and place the step size label next to the set pixels button
step_angle_label = tk.Label(frame, text=f" Angle : {rotate_degree} degree")
step_angle_label.grid(row=1, column=1, padx=1, pady=5)

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