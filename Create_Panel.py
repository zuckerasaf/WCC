from lxml import etree
import tkinter as tk
from tkinter import messagebox
from  PctureClass import Switch, TempData
from tkinter import filedialog, simpledialog, ttk
from tkinter.filedialog import asksaveasfilename
from PIL import Image, ImageTk , ImageFont, ImageDraw
import os
import json
from Util import update_scale_image, update_image_position_entry, update_rotation_entry, load_panel_names, open_alpha_form, load_switch_names,str2DBSIMelement  # Import the move_image function
from Delete_Update import delete_item, update_item


def hello_world():
    print("Hello, World!")

# Function to read the JSON file and extract the default DB path
def get_default_db_path(json_file,type):
    try:
        with open(json_file, 'r') as file:
            data = json.load(file)
            db_default_folder = data[0]["DB_Default_Folder"]
            db_default_file = data[0]["DB_Default_file"]
            dbsim_default_file = data[0]["DBSIM_Default_file"]
            if type == "ORS":
                full_path = os.path.join(db_default_folder, db_default_file)
                if os.path.exists(full_path):
                    browse_button.config(state=tk.NORMAL)
                    return full_path
                else: return "No DB selected yet"
            elif type == "DBSIM":
                full_path = os.path.join(db_default_folder, dbsim_default_file)
                if os.path.exists(full_path):
                    browse_button.config(state=tk.NORMAL)
                    return full_path

    except FileNotFoundError:
        return "No DB selected yet"

def browse_DB(db_name_var):
    # Open a file dialog to select a new database file
    file_path = filedialog.askopenfilename(
        title="Select Database File",
        initialdir=r'C:\projectPython\WCC\DB',  # Set the initial directory
        filetypes=(("JSON Files", "*.json"), ("All Files", "*.*"))
    )
    if file_path:
        browse_button.config(state=tk.NORMAL)
        db_name_var.set(file_path)

def browse_image(DB_file_path,DBSIM_file_Path,image_label):
    global tempData, switch
    tempData.DB_Default_File_Path = DB_file_path
    tempData.DBSIM_Default_file = DBSIM_file_Path
    # global img, img_tk, new_image_path, current_image_path, image_id,rotated_new_img,  new_image_path, new_image_position, combined_image_path

    # Create a new, empty alpha_data.json file
    with open("alpha_data.json", "w") as file:
        json.dump([], file)
    
    # Open file dialog to select an image file
    file_path = filedialog.askopenfilename(title="Select panel image",filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.gif")])
    if file_path:
        tempData.current_image_path = os.path.normpath(file_path)
        tempData.panel_Image_Path = os.path.normpath(file_path)
        img = Image.open(file_path)
        img_tk = ImageTk.PhotoImage(img)
        image_label.config(image=img_tk)
        image_label.image = img_tk  # Keep a reference to avoid garbage collection

        # Get the image size
        width, height = img.width, img.height

        select_panel_name(DB_file_path,DBSIM_file_Path)

        # Create a switch instance with the image name as the ID
        image_id = os.path.basename(file_path)
        switch = Switch(image_id=image_id, file_path=file_path, width=width, height=height)

       
        # Update the text label with image_id and file_path
        info_label.config(text=f"Image ID: {switch.image_id}\nFile Path: {switch.file_path}")
        print(f"Created switch instance: ID={switch.image_id}, Path={switch.file_path}")
       

def select_switch_name(DB_file_path,panel_name, switch,elements,DBSIM_file_Path):
    print("panel_name",panel_name)
    tree = etree.parse(DBSIM_file_Path)
    if panel_name is None:
        print("No panel selected")
        return
    switch_names = load_switch_names(DB_file_path,panel_name)

    
    # Sort the switch names alphabetically
    switch_names_sorted = sorted(switch_names)
    elements_sorted = (elements)

    # Create a new window for switch name selection
    switch_window = tk.Toplevel(root)
    switch_window.title("Select Switch Name")

    # Set the width of the switch_window to twice its default width
    default_width = 200  # Example default width, adjust as needed
    switch_window.geometry(f"{default_width * 2}x180")  # Adjust height as needed

    # Create a StringVar to track the selected switch name
    selected_switch_name = tk.StringVar()
    selected_switch_name_DBSIM = tk.StringVar()

        # Create a label and combobox for panel name selection
    Switch_label = ttk.Label(switch_window, text="Select switch Name ORS:")
    Switch_label.pack(padx=10, pady=5)

    Switch_combobox = ttk.Combobox(switch_window, textvariable=selected_switch_name, values=switch_names_sorted, width=40)
    Switch_combobox.pack(padx=10, pady=5)

            # Create a label and combobox for panel name selection
    Switch_label_DBSIM = ttk.Label(switch_window, text="Select switch Name DBSIM:")
    Switch_label_DBSIM.pack(padx=10, pady=5)

    Switch_combobox_DBSIM = ttk.Combobox(switch_window, textvariable=selected_switch_name_DBSIM, values=elements_sorted, width=40)
    Switch_combobox_DBSIM.pack(padx=10, pady=5)


    # Function to proceed after switch name is selected
    def proceed():
        DBSimElementValues = []
        DBSimElementValues_Display = []
        i = 0
        if selected_switch_name.get():
            switch.imageName = selected_switch_name.get()
            switch.DBSIM_Element = selected_switch_name_DBSIM.get()
            if switch.DBSIM_Element != "" or switch.DBSIM_Element == "none":
                elemtypDef  = tree.xpath(f'//Types/TypeDefinition/Elements/Element[@Name="{switch.DBSIM_Element}"]/TypeDefinition')
                listnameelme = tree.xpath(f'//Types/TypeDefinition[@Name="{elemtypDef[0].text}"]/Enumerators/Enumerator/@Name')
                listEngValueelme = tree.xpath(f'//Types/TypeDefinition[@Name="{elemtypDef[0].text}"]/Enumerators/Enumerator/EngValue')
                for i in range(len(listEngValueelme)):
                    DBSimElementValues_Display.append(listnameelme[i] + " = " + listEngValueelme[i].text + "\n") 
                    DBSimElementValues.append(listnameelme[i] + " = " + listEngValueelme[i].text) 
                switch.DBSimElementValues = DBSimElementValues
                switch.DBSimElementValues_Display = DBSimElementValues_Display
                
            else:
                switch.DBSIM_Element = "none"
            print(switch.imageName)
            if switch.DBSIM_Element != "none":
                switch.DBSimelementType = tree.xpath(f'//Types/TypeDefinition[@Name="{elemtypDef[0].text}"]/EngType')[0].text
            else:
                switch.DBSimelementType = "none"

            switch_window.destroy()
            
    

    # Create a button to proceed
    proceed_button = ttk.Button(switch_window, text="Proceed", command=proceed)
    proceed_button.pack(padx=10, pady=10)

    switch_window.wait_window()

# Function to select a panel name

def select_panel_name(DB_file_path,DBSIM_file_Path):
    tree = etree.parse(DBSIM_file_Path)
    #root = tree.getroot()
 
    panel_names = load_panel_names(DB_file_path)

    panel_name_DBISM = tree.xpath('//MessageDefinitions/MessageDefinition/@Name')
        
    # Sort the switch names alphabetically
    panel_names_sorted = sorted(panel_names)

    panel_name_DBISM_sortes = sorted(panel_name_DBISM) 

    # Create a new window for panel name selection
    panel_window = tk.Toplevel(root)
    panel_window.title("Select Panel Name")

    # Set the width of the panel_window to twice its default width
    default_width = 200  # Example default width, adjust as needed
    panel_window.geometry(f"{default_width * 2}x180")  # Adjust height as needed

    # Create a StringVar to track the selected panel name
    selected_panel_name = tk.StringVar()
    selected_panel_name_DBsim = tk.StringVar()

    # Create a label and combobox for panel name selection
    panel_label = ttk.Label(panel_window, text="Select Panel Name from ORS :")
    panel_label.pack(padx=10, pady=5)

    panel_combobox = ttk.Combobox(panel_window, textvariable=selected_panel_name, values=panel_names_sorted, width=40)
    panel_combobox.pack(padx=10, pady=5)

        # Create a label and combobox for panel name selection
    panel_label_DBsim = ttk.Label(panel_window, text="Select Panel Name from DBSIM :")
    panel_label_DBsim.pack(padx=10, pady=5)

    panel_DBsim_combobox = ttk.Combobox(panel_window, textvariable=selected_panel_name_DBsim, values=panel_name_DBISM_sortes, width=40)
    panel_DBsim_combobox.pack(padx=10, pady=5)

    # Function to proceed after panel name is selected
    def proceed():
        if selected_panel_name.get():
            panel_window.destroy()
            panel_name_label.config(text=selected_panel_name.get())
            panel_name_label_DBSim.config(text=selected_panel_name_DBsim.get())
            add_button.config(state=tk.NORMAL)
            # update_button.config(state=tk.NORMAL)
            # delete_button.config(state=tk.NORMAL)
            # update_button_IMG.config(state=tk.NORMAL)
            # update_button_add_switch.config(state=tk.NORMAL)

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
    #modified_file_path = file_path[:-4] + "_withcaption.png"
    modified_file_path =  transform_file_path(file_path,"withcaption")

    img.save(modified_file_path)

    print(f"Saved modified image with switch name '{switch_name}' at position {position}")
    return modified_file_path

def transform_file_path(file_path, text ):
    # Extract the directory and filename
    directory = os.path.dirname(file_path)
    filename = os.path.basename(file_path)
    
       # Modify the directory and filename
    new_directory = os.path.join(directory, "Working")

        # Ensure the directory exists
    os.makedirs(new_directory, exist_ok=True)

    name, ext = os.path.splitext(filename)
    new_filename = f"{name}_{text}{ext}"
    
    # Reconstruct the new file path
    new_file_path = os.path.join(new_directory, new_filename)
    return new_file_path

def add_Switch(DB_file_path,panel,update,panelName,DBSIM_file_Path, DBSIM_panel,image_label,panel_name_label,panel_name_label_DBSim):
    global tempData, switch
    if DBSIM_panel !="" and update==1:
        tree = etree.parse(DBSIM_file_Path)
        switch_type = tree.xpath(f'//MessageDefinitions/MessageDefinition [@Name="{DBSIM_panel}"]/Elements/Element/TypeDefinition')[0].text
        elements = tree.xpath(f'//Types/TypeDefinition[@Name="{switch_type}"]/Elements/Element/@Name')
    else:
       elements = ["none"] 


        

    
    tempData.DBSIM_panel = DBSIM_panel
    tempData.panelName = DBSIM_panel

    #global new_scale, current_image_path, new_image_path, rotated_new_img, new_image_position, base_img, img, img_tk, image_id, rotation_angle,switch
    rotation_angle = 0
    if tempData.current_image_path and update==1:
        # Update the switch data to contain the panel name and the panel image path image_id and file_path
        if panel_name_label_DBSim.cget("text") != "No DBSIM panel selected":
            switch.panelName = panel_name_label_DBSim.cget("text")
            switch.panel_Image_Path = tempData.panel_Image_Path 
        elif panel_name_label.cget("text") != "No ORS panel selected":
            switch.panelName = panel_name_label.cget("text")
            switch.panel_Image_Path = tempData.panel_Image_Path 
        else:
            pass
        # add new image to new panel 
        file_path = filedialog.askopenfilename(title="Select switch image",filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.gif")])
        if file_path:
            tempData.new_image_path = file_path
            tempData.base_img = Image.open(tempData.current_image_path)  # Open and store the base image 
            image_id = os.path.basename(file_path)
            img = Image.open(file_path)
            width, height = img.width, img.height

            switch = Switch(image_id=image_id, file_path=file_path, width=width, height=height)
            switch.InPanelName = panelName
            switch.scale = tempData.new_scale
            print("scale",switch.scale)
            select_switch_name(DB_file_path,panel, switch,elements,DBSIM_file_Path)                      
            switch_name = switch.imageName
            print("here "  + switch_name)

            tempData.new_image_path = combine_switch_name_with_image(file_path, switch_name, [0,0])
            combine_images()
            update_info_label()
            
            open_alpha_form(root,True,tempData,switch)
#    elif tempData.current_image_path and update==2:
    elif update==2:
        # up date switch data  in  exsit  panel in json_file_path
        selected_name = ""
        json_file_path = ""
        
        # Create an instance of PctureClass and update parameters from JSON
        switch = Switch(image_id="image_id", file_path="file_path", width="width", height="height") 
        json_file_path, selected_name = update_item()
        switch.update_parameters_from_json(json_file_path, selected_name)
        tempData.current_image_path = switch.panel_Image_Path
        tempData.panel_Image_Path = switch.panel_Image_Path
        tempData.DB_Default_File_Path = DB_file_path
        tempData.DBSIM_Default_file = DBSIM_file_Path
        tempData.DBSIM_panel = switch.panelName
        #img = Image.open(switch.panel_Image_Path)
        #image_path = 'C:\\projectPython\\WCC\\Cockpit-Control\\frontend\\public\\CMDSPanel\\CMDS.png'
        image_path = switch.panel_Image_Path #'C:\\projectPython\\WCC\\Cockpit-Control\\frontend\\public\\CMDSPanel\\CMDS.png'
        img = Image.open(image_path)
        img_tk = ImageTk.PhotoImage(img)
        image_label.config(image=img_tk)
        image_label.image = img_tk  # Keep a reference to avoid garbage collection

        tempData.new_scale=switch.scale

        tempData.new_image_path = combine_switch_name_with_image(switch.file_path, switch.imageName, [0,0])
        tempData.new_image_position = (switch.x, switch.y)
        tempData.base_img = Image.open(tempData.current_image_path)

            # Combine images and update info label
        combine_images()
        update_info_label()

        open_alpha_form(root,False,tempData,switch)
        #open_alpha_form(root,(switch.x,switch.y), disp_rotation_angle, switch,False,new_scale)#, f"{width}x{height}",panel)
    elif tempData.current_image_path and update==3:
        # up date switch image in  exsit  panel in json_file_path
        selected_name = ""
        json_file_path = ""
        
        file_path = filedialog.askopenfilename(title="Select switch image",filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.gif")])
        tempData.new_image_path = file_path

        # Create an instance of PctureClass and update parameters from JSON
        switch = Switch(image_id="image_id", file_path="file_path", width="width", height="height") 
        json_file_path, selected_name = update_item()
        switch.update_parameters_from_json(json_file_path, selected_name)
        switch.file_path = tempData.new_image_path
        switch.image_id = tempData.new_image_path
        tempData.new_scale=switch.scale
        #switch.scale = new_scale

        tempData.new_image_path = combine_switch_name_with_image(switch.file_path, switch.imageName, [0,0])
        tempData.new_image_position = (switch.x, switch.y)
        tempData.base_img = Image.open(tempData.current_image_path)

            # Combine images and update info label
        combine_images()
        update_info_label()

            # Open the alpha form
        #open_alpha_form(root,(switch.x,switch.y), disp_rotation_angle, switch,False,new_scale)#, f"{width}x{height}",panel)
        open_alpha_form(root,False,tempData,switch)
    elif tempData.current_image_path and update==4:
        selected_name = ""
        json_file_path = ""
        # add new image to exsit  panel in json_file_path
        json_file_path = filedialog.askopenfilename(
        title="Select JSON File for adding the switch",
        filetypes=(("JSON Files", "*.json"), ("All Files", "*.*"))
        )
        file_path = filedialog.askopenfilename(title="Select switch image to add",filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.gif")])
        if file_path:
            tempData.new_image_path = file_path
            tempData.base_img = Image.open(tempData.current_image_path)  # Open and store the base image 
            image_id = os.path.basename(file_path)
            img = Image.open(file_path)
            width, height = img.width, img.height
            # new_image_path = file_path
            # new_image_position = (0, 0)  # Start at the top-left corner
            # base_img = Image.open(current_image_path)  # Open and store the base image
            # image_id = os.path.basename(file_path)
            # img = Image.open(file_path)
            # width, height = img.width, img.height

            switch = Switch(image_id=image_id, file_path=file_path, width=width, height=height)
            switch.json_file_path= json_file_path
            switch.scale = tempData.new_scale
            print("scale",switch.scale)
            select_switch_name(DB_file_path,panel, switch,elements)                      
            switch_name = switch.imageName
            print("here "  + switch_name)

            new_image_path = combine_switch_name_with_image(file_path, switch_name, [0,0])

            # Combine images and update info label
            combine_images()
            update_info_label()

            # Open the alpha form
            open_alpha_form(root,False,tempData,switch)
            #open_alpha_form(root,new_image_position, disp_rotation_angle, switch, False,new_scale)#, f"{width}x{height}",panel)

def combine_images():

    #global new_scale, current_image_path,  rotated_new_img, new_image_path, new_image_path, new_image_position, combined_image_path, base_img, disp_rotation_angle
    global tempData, switch
    if tempData.base_img and tempData.new_image_path:
        # Open the new image
        new_img = Image.open(tempData.new_image_path)
       # Resize the new image according to the scale factor
        new_width = int(new_img.width * float(tempData.new_scale))
        new_height = int(new_img.height * float(tempData.new_scale))
        new_img = new_img.resize((new_width, new_height), Image.LANCZOS)

        # Calculate the center of the original image
        original_center_x = tempData.new_image_position[0] + new_img.width // 2
        original_center_y = tempData.new_image_position[1] + new_img.height // 2

        # Rotate the image
        tempData.rotated_new_img = new_img.rotate(tempData.rotation_angle, expand=True)

        # Calculate the new position to keep the rotated image centered
        new_x = original_center_x - tempData.rotated_new_img.width // 2
        new_y = original_center_y - tempData.rotated_new_img.height // 2
        tempData.new_position = (new_x, new_y)

        # Create a copy of the base image to avoid modifying the original
        combined_img = tempData.base_img.copy()

        # Paste the rotated new image on top of the base image at the current position
        combined_img.paste(tempData.rotated_new_img, tempData.new_position, tempData.rotated_new_img if tempData.rotated_new_img.mode == 'RGBA' else None)

        # Save the combined image to a temporary file
        combined_image_path = os.path.join(os.path.dirname(tempData.current_image_path), "combined_image.png")
        combined_img.save(combined_image_path)

        # Update the current image path to the combined image
        tempData.current_image_path = combined_image_path

        # Update the image label with the combined image
        img_tk = ImageTk.PhotoImage(combined_img)
        image_label.config(image=img_tk)
        image_label.image = img_tk  # Keep a reference to avoid garbage collection

# Function to update the info label
def update_info_label():
    #global current_image_path, new_image_position
    if current_image_path:
        # Assuming switch is an object with image_id and file_path attributes
        switch = type('switch', (object,), {'image_id': 1, 'file_path': current_image_path})()
        info_label.config(text=f"Image ID: {switch.image_id}\nFile Path: {switch.file_path}\nNew Image Position: {new_image_position}")

def set_move_pixels():
    global tempData
    pixels = simpledialog.askinteger("Input", "Enter the number of pixels to move:", minvalue=1)
    if pixels:
        tempData.move_pixels = pixels
        step_size_label.config(text=f"Step : {tempData.move_pixels} pixels")

def set_rotate_degree():
    global tempData
    degree = simpledialog.askinteger("Input", "Enter the roattion degree step:", minvalue=1)
    if degree:
        tempData.rotate_degree = degree
        step_angle_label.config(text=f"step: {tempData.rotate_degree} degree")

def save_image():
    global tempData
    if tempData.combined_image_path:
        # Open file dialog to select save location
        save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
        if save_path:
            # Save the combined image to the specified location
            img = Image.open(tempData.combined_image_path)
            img.save(save_path)
            print(f"Image saved to {save_path}")

def smallstep_handle(event):
    small_step = 1
    print(f"event.state: {event.state}")
    if event.state & 0x20000:  # Check if Shift key is pressed
        small_step = 10
    elif event.state & 0x0004:  # Check if Ctrl key is pressed
        small_step = 0.1
    return small_step


def handle_move_image(event):
    global tempData,switch
    # small_step = 1
    # print(f"event.state: {event.state}")
    # if event.state & 0x0001:  # Check if Shift key is pressed
    #     small_step = 10
    # elif event.state & 0x0004:  # Check if Ctrl key is pressed
    #     small_step = 0.1
    small_step=smallstep_handle(event)

    if tempData.new_image_path:
        if event.keysym == 'Right':
            tempData.new_image_position = (int(tempData.new_image_position[0] + tempData.move_pixels // small_step), tempData.new_image_position[1])
        elif event.keysym == 'Left':
            tempData.new_image_position = (int(tempData.new_image_position[0] - tempData.move_pixels // small_step), tempData.new_image_position[1])
        elif event.keysym == 'Up':
            tempData.new_image_position = (tempData.new_image_position[0], int(tempData.new_image_position[1] - tempData.move_pixels // small_step))
        elif event.keysym == 'Down':
            tempData.new_image_position = (tempData.new_image_position[0], int(tempData.new_image_position[1] + tempData.move_pixels // small_step))
        elif event.keysym == 'd':
            tempData.new_image_position = (-100, -100)
        combine_images()
        update_info_label()
        switch.x = tempData.new_image_position[0]
        switch.y = tempData.new_image_position[1]

        update_image_position_entry(tempData)

 
def handle_rotate_image(event):
    global tempData,switch
    # print(f"event.state: {event.state}")
    # small_rotate = 1
    # if event.state & 0x0001:  # Check if Shift key is pressed
    #     small_rotate = 10
    # elif event.state & 0x0004:  # Check if Ctrl key is pressed
    #     small_rotate = 0.1
    small_rotate = smallstep_handle(event)

    if event.keysym == 'r':
        tempData.rotation_angle = int((tempData.rotation_angle - tempData.rotate_degree// small_rotate)) % 360
    elif event.keysym == 't':
        tempData.rotation_angle = int((tempData.rotation_angle + tempData.rotate_degree// small_rotate)) % 360

    combine_images()

    if tempData.rotation_angle < 180:
        tempData.disp_rotation_angle = 0 - tempData.rotation_angle
    else:
        tempData.disp_rotation_angle = 360- tempData.rotation_angle

    update_rotation_entry(tempData)


def handle_scale_image(event):
    global tempData,switch

    if event.keysym == 'plus':
        switch.scale = float(switch.scale) + 0.05
        switch.width = int(switch.width  + switch.width *0.05)
        switch.height = int(switch.height + switch.height *0.05)
    elif event.keysym == 'minus':
        switch.scale = float(switch.scale) - 0.05
        switch.width = int(switch.width  - switch.width *0.05)
        switch.height = int(switch.height - switch.height *0.05)

    combine_images()
    tempData.new_scale = switch.scale
    update_scale_image(switch)


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
        # Delete the alpha_data.json file
        with open("alpha_data.json", "w") as file:
            json.dump([], file)
    # Close the form
    root.destroy()


######################################## Start ####################################################
# Create the main window

tempData = None
switch = None

root = tk.Tk()
root.title("configure Json for panel")
# Set the position of the root window to the top-left corner of the screen
root.geometry("+10+10")

current_image_path = None

# Create a frame to hold the widgets
name_frame = ttk.Frame(root)
name_frame.grid(row=0, column=0, padx=10, pady=10)

# Create a label to display the image
image_label = tk.Label(root)
image_label.grid(row=1, column=0, columnspan=4, sticky="nsew")

tempData = TempData()

# Create a label to display the selected panel name
ORS_label = tk.Label(name_frame, text=f" name from ORS -> ")
ORS_label.grid(row=1, column=0, padx=0, pady=0)
panel_name_label = ttk.Label(name_frame, text="No ORS panel selected", anchor='w')
panel_name_label.grid(row=1, column=1, padx=0, pady=0, sticky='w')

DBSIM_label = tk.Label(name_frame, text=f" name from DBSIM -> ")
DBSIM_label.grid(row=1, column=4, padx=0, pady=0)
panel_name_label_DBSim = ttk.Label(name_frame, text="No DBSIM panel selected", anchor='w')
panel_name_label_DBSim.grid(row=1, column=5, padx=0, pady=0, sticky='w')

# Create a button to browse files
browse_button = tk.Button(name_frame, text="Create panel ", command=lambda:browse_image(db_name_label.cget("text"),dbsim_name_label.cget("text"),image_label), state=tk.DISABLED)
browse_button.grid(row=0, column=0)

json_file_path = 'InitValues.json'

# Create the "browse_DB" button
browse_db_button = ttk.Button(name_frame, text="Browse ORS DB", command=lambda: browse_DB(db_name_var), state=tk.NORMAL)
browse_db_button.grid(row=0, column=3, padx=10, pady=10)

# Create the DB_name label with a default value
defualt_db_name_var = get_default_db_path(json_file_path, "ORS")
db_name_var = tk.StringVar(value=defualt_db_name_var)
db_name_label = ttk.Label(name_frame, textvariable=db_name_var)
db_name_label.grid(row=0, column=4, padx=10, pady=10)

# Create the "browse_DBSIM" button
browse_dbSIM_button = ttk.Button(name_frame, text="Browse DBSIM", command=lambda: browse_DB(db_name_var), state=tk.NORMAL)
browse_dbSIM_button.grid(row=0, column=5, padx=10, pady=10)

# Create the DB_name label with a default value
defualt_dbsim_name_var = get_default_db_path(json_file_path, "DBSIM")
dbsim_name_var = tk.StringVar(value=defualt_dbsim_name_var)
dbsim_name_label = ttk.Label(name_frame, textvariable=dbsim_name_var)
dbsim_name_label.grid(row=0, column=6, padx=10, pady=10)

# Create a label to display the image_id and file_path
info_label = tk.Label(root, text="Image ID: \nFile Path: \nNew Image Position: (0, 0)")
info_label.grid(row=2, column=0, padx=5, pady=5)


# Create a frame to hold the widgets
switchbuttonframe = ttk.Frame(root)
switchbuttonframe.grid(row=3, column=0, padx=10, pady=10)

# Create a button to add another image on top
add_button = tk.Button(switchbuttonframe, text="Add Switch", command=lambda: add_Switch(db_name_label.cget("text"),panel_name_label.cget("text"), 1,panel_name_label.cget("text"),dbsim_name_label.cget("text"),panel_name_label_DBSim.cget("text"),image_label,panel_name_label,panel_name_label_DBSim), state=tk.DISABLED, bg="lightgreen")
add_button.grid(row=3, column=0, padx=5, pady=5)

# Create a button to add update switch from the Jason file
update_button = tk.Button(switchbuttonframe, text="update switch data", command=lambda: add_Switch(db_name_label.cget("text"),panel_name_label.cget("text"), 2,panel_name_label.cget("text"),dbsim_name_label.cget("text"),panel_name_label_DBSim.cget("text"),image_label,panel_name_label,panel_name_label_DBSim), state=tk.NORMAL , bg="lightyellow")
update_button.grid(row=3, column=1, padx=5, pady=5)

# Create a button to add update switch from the Jason file
update_button_IMG = tk.Button(switchbuttonframe, text="update switch img", command=lambda: add_Switch( db_name_label.cget("text"),panel_name_label.cget("text"), 3,panel_name_label.cget("text"),dbsim_name_label.cget("text"),panel_name_label_DBSim.cget("text"),image_label,panel_name_label,panel_name_label_DBSim), state=tk.NORMAL , bg="lightyellow")
update_button_IMG.grid(row=3, column=2, padx=5, pady=5)

# Create a button to add update switch from the Jason file
update_button_add_switch = tk.Button(switchbuttonframe, text="add switch to exsit panel", command=lambda: add_Switch( db_name_label.cget("text"),panel_name_label.cget("text"), 4,panel_name_label.cget("text"),dbsim_name_label.cget("text"),panel_name_label_DBSim.cget("text"),image_label,panel_name_label,panel_name_label_DBSim), state=tk.NORMAL , bg="lightyellow")
update_button_add_switch.grid(row=3, column=3, padx=5, pady=5)

# Create a button to add delete switch from the Jason file 
delete_button = tk.Button(switchbuttonframe, text="delete switch", command=delete_item, state=tk.DISABLED,bg="lightcoral")
delete_button.grid(row=3, column=4, padx=5, pady=5)


# Create a frame to hold the widgets
frame = ttk.Frame(root)
frame.grid(row=4, column=0, padx=10, pady=10)

# Move the image by the specified number of pixels in the specified direction
set_pixels_button = tk.Button(frame, text="Set Move Pixels", command=set_move_pixels)
set_pixels_button.grid(row=0, column=0, padx=0, pady=5)

step_size_label = tk.Label(frame, text=f" Step : {tempData.move_pixels} pixels")
step_size_label.grid(row=0, column=1, padx=0, pady=5)

step_info_label = tk.Label(frame, text=f"arrows for move, \n with ""ALT"" * 0.1, with  ""CTRL"" * 10 step")
step_info_label.grid(row=1, column=0, padx=0, pady=5)


# Rotate the image by the specified number of degrees in the specified direction
set_angle_button = tk.Button(frame, text="Set angle rotation", command=set_rotate_degree)
set_angle_button.grid(row=0, column=2, padx=1, pady=5)

step_angle_label = tk.Label(frame, text=f" Angle : {tempData.rotate_degree} degree")
step_angle_label.grid(row=0, column=3, padx=1, pady=5)

step_angle_info_label = tk.Label(frame, text=f" ""R"" rotate  right ""T"" rotate left \n with ""ALT"" * 0.1, with  ""CTRL"" * 0.1 step")
step_angle_info_label.grid(row=1, column=2, padx=0, pady=5)


step_angle_info_label = tk.Label(frame, text=f" ""D"" to move image to -100/-100")
step_angle_info_label.grid(row=2, column=0, padx=0, pady=5)

step_angle_info_label = tk.Label(frame, text=f" ""+"" or ""-"" foor scale up and down the image in 5%")
step_angle_info_label.grid(row=2, column=2, padx=0, pady=5)


# Bind arrow keys to the move_image function
root.bind('<Right>', handle_move_image)
root.bind('<Left>', handle_move_image)
root.bind('<Up>', handle_move_image)
root.bind('<Down>', handle_move_image)
root.bind('<KeyPress-d>', handle_move_image) # move the image out of the screen 
root.bind('<KeyPress-r>', handle_rotate_image) # rotate the image to the right 
root.bind('<KeyPress-t>', handle_rotate_image) # rotate the image to the left 
root.bind("<plus>", handle_scale_image) # scale up the image symetric way  
root.bind("<minus>", handle_scale_image) # scale down the image symetric way

# Create a button to close the form
close_button = tk.Button(root, text="Save and Close", command=save_and_close)
close_button.grid(row=8, column=1, padx=5, pady=5)

# Configure grid rows and columns
for i in range(8):
    root.grid_rowconfigure(i, weight=1)

for i in range(3):
    root.grid_columnconfigure(i, weight=1)

# Start the Tkinter event loop
root.mainloop()