from lxml import etree
import tkinter as tk
from tkinter import messagebox
from  PctureClass import Switch, TempData
from tkinter import filedialog, simpledialog, ttk
from tkinter.filedialog import asksaveasfilename
from PIL import Image, ImageTk , ImageFont, ImageDraw
import os
import json
from Util import update_scale_image, update_image_position_entry, update_rotation_entry, load_panel_names, open_alpha_form, load_switch_names,Switch_name_listbox  # Import the move_image function
from Delete_Update import delete_item, update_item
from Create_Jason_File import transfer_to_json


def hello_world():
    print("Hello, World!")

def show_panel(image_label):
    json_file_path = filedialog.askopenfilename(title="Select JSON File present the panel from", filetypes=(("JSON Files", "*.json"), ("All Files", "*.*")))
    base_combine_panel_Img = Draw_panel_from_Jason(json_file_path)
    image_path = base_combine_panel_Img #'C:\\projectPython\\WCC\\Cockpit-Control\\frontend\\public\\CMDSPanel\\CMDS.png'
    img = Image.open(image_path)
    img_tk = ImageTk.PhotoImage(img)
    image_label.config(image=img_tk)
    image_label.image = img_tk  # Keep a reference to avoid garbage collection
    
    file_name = os.path.basename(json_file_path)
    info_label.config(text=f"Image ID: {file_name}\nFile Path: {json_file_path}")


def Pixsel_Step_Define(json_file):
    try:
        with open(json_file, 'r') as file:
            data = json.load(file)
            Move_Pixel_Step = data[0]["Move_Pixel_Step"]
            Rotate_Pixel_Step = data[0]["Rotate_Degree_Step"]
            return Move_Pixel_Step, Rotate_Pixel_Step
    except FileNotFoundError:
        return "No DB selected yet"



def Draw_panel_from_Jason(file):
    with open(file, 'r', encoding='utf-8') as file_Json:
        data = json.load(file_Json)
        first = True
        #item = next((item for item in data if item['backend_name'] != item_name), None)
        for item in data:
            #if item['backend_name'] != item_name:
            if first == True:
                tempData.base_img = item.get('panelNamePath', {}) 
                tempData.current_image_path = tempData.base_img
                first = False

            component = item.get('component', {})
            position = component.get('position', {})
            new_width = int(position.get('imgWidth',{}))
            new_height = int(position.get('imgHeight', {}))
            #new_img = new_img.resize((new_width, new_height), Image.LANCZOS)
            tempData.new_scale = float(position.get('imgScale', {}))
            imageProps = component.get('imageProps', {})
            new_img = Image.open(imageProps.get('imageDefault', {}))
            new_img = new_img.resize((int(new_width*tempData.new_scale), int(new_height*tempData.new_scale)), Image.LANCZOS)
            tempData.new_position = (position.get('posLeft', {}) , position.get('posTop',{}))

            tempData.base_img = Image.open(tempData.base_img)
            combined_img = tempData.base_img.copy()

            tempData.rotated_new_img = new_img.rotate(0, expand=True)

            # Paste the rotated new image on top of the base image at the current position
            combined_img.paste(tempData.rotated_new_img, tempData.new_position, tempData.rotated_new_img if tempData.rotated_new_img.mode == 'RGBA' else None)

            # Save the combined image to a temporary file
            combined_image_path = os.path.join(os.path.dirname(tempData.current_image_path), "combined_image.png")
            combined_img.save(combined_image_path)

            # Update the current image path to the combined image
            tempData.current_image_path = combined_image_path
            tempData.base_img = combined_image_path 

            # # Update the image label with the combined image
            # img_tk = ImageTk.PhotoImage(combined_img)
            # image_label.config(image=img_tk)
            # image_label.image = img_tk  # Keep a reference to avoid garbage collection
    #print("Done")
    return combined_image_path
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
                else: 
                    return "No DB selected yet"
            elif type == "DBSIM":
                full_path = os.path.join(db_default_folder, dbsim_default_file)
                if os.path.exists(full_path):
                    browse_button.config(state=tk.NORMAL)
                    return full_path
                else: 
                    return "No DBSIM selected yet"

    except FileNotFoundError:
        return "No DB selected yet"

def browse_DB(db_name_var, Type):
    # Open a file dialog to select a new database file
    file_path = filedialog.askopenfilename(
        title="Select Database File",
        initialdir=r'C:\projectPython\WCC\DB',  # Set the initial directory
        filetypes=(("DB Files", Type), ("All Files", "*.*"))
    )
    if file_path:
        browse_button.config(state=tk.NORMAL)
        db_name_var.set(file_path)

def browse_image(DB_file_path,DBSIM_file_Path,image_label,Imagecanvas):
    global tempData, switch
    panel_name_label.config(text="No ORS panel selected")
    panel_name_label_DBSim.config(text="No DBSIM panel selected")
    image_label.config(image='')

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
        # Update the scroll region of the canvas when the image is loaded
        def update_scroll_region(event=None):
            Imagecanvas.configure(scrollregion=Imagecanvas.bbox("all"))

        image_label.bind("<Configure>", update_scroll_region)
        # Get the image size
        width, height = img.width, img.height

        select_panel_name(DB_file_path,DBSIM_file_Path)

        # Create a switch instance with the image name as the ID
        image_id = os.path.basename(file_path)
        switch = Switch(image_id=image_id, file_path=file_path, width=width, height=height)

       
        # Update the text label with image_id and file_path
        info_label.config(text=f"Image ID: {switch.image_id}\nFile Path: {switch.file_path}")
        #print(f"Created switch instance: ID={switch.image_id}, Path={switch.file_path}")

def list_of_DBSIM_elemnt (DBSIM_panel,DBSIM_file_Path):
    if DBSIM_panel !="" and DBSIM_panel != "No DBSIM panel selected" and DBSIM_panel != "none":
        tree = etree.parse(DBSIM_file_Path)
        switch_type = tree.xpath(f'//MessageDefinitions/MessageDefinition [@Name="{DBSIM_panel}"]/Elements/Element/TypeDefinition')[0].text
        elements = tree.xpath(f'//Types/TypeDefinition[@Name="{switch_type}"]/Elements/Element/@Name')
    else:
       elements = ["none"] 
    return elements
           

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
            if switch.DBSIM_Element != "" and switch.DBSIM_Element != "none":
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


def Update_Panel_DBSIM_Name():
    global tempData, switch
    if tempData.DBSIM_Default_file == "No DBSIM selected yet" or tempData.DBSIM_Default_file == "" or tempData.DBSIM_Default_file == "none":
        messagebox.showwarning("Warning", "No Panel selected yet")
        return
    tree = etree.parse(tempData.DBSIM_Default_file)
    #root = tree.getroot()

    panel_name_DBISM = tree.xpath('//MessageDefinitions/MessageDefinition/@Name')
        

    panel_name_DBISM_sortes = sorted(panel_name_DBISM) 

    # Create a new window for panel name selection
    panel_window = tk.Toplevel(root)
    panel_window.title("Update panel DBSIM name ")

    # Set the width of the panel_window to twice its default width
    default_width = 200  # Example default width, adjust as needed
    panel_window.geometry(f"{default_width * 2}x100")  # Adjust height as needed

    # Create a StringVar to track the selected panel name
    selected_panel_name_DBsim = tk.StringVar()

    # Create a label and combobox for panel name selection
    panel_label_DBsim = ttk.Label(panel_window, text="Select Panel Name from DBSIM :")
    panel_label_DBsim.pack(padx=10, pady=5)

    panel_DBsim_combobox = ttk.Combobox(panel_window, textvariable=selected_panel_name_DBsim, values=panel_name_DBISM_sortes, width=40)
    panel_DBsim_combobox.pack(padx=10, pady=5)

    # Function to proceed after panel name is selected
    def proceed():
        if selected_panel_name_DBsim.get():
            panel_window.destroy()
            panel_name_label_DBSim.config(text=selected_panel_name_DBsim.get())
            tempData.DBSIM_panel = selected_panel_name_DBsim.get()
            panel_name_label_DBSim.config(text=tempData.DBSIM_panel)

    # Create a button to proceed
    proceed_button = ttk.Button(panel_window, text="Proceed", command=proceed)
    proceed_button.pack(padx=10, pady=10)

    panel_window.wait_window()


# Function to select a panel name

def select_panel_name(DB_file_path,DBSIM_file_Path):
    global tempData, switch
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


            tempData.panelName = selected_panel_name.get()
            tempData.DBSIM_panel = selected_panel_name_DBsim.get()


            add_button.config(state=tk.NORMAL)
            Switch_name_listbox(root)
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

    #print(f"Saved modified image with switch name '{switch_name}' at position {position}")
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
    
    Switch_name_listbox(root)
    
    tempData.DBSIM_panel = DBSIM_panel
    tempData.panelName = panelName

    # add new image to new panel 
    if update==1 or update == 4:
        if update ==1 :
            if DBSIM_panel == 'No DBSIM panel selected' and panelName == 'No ORS panel selected':
                messagebox.showwarning("Warning", "No panel selected yet")
                return
                
            elements = list_of_DBSIM_elemnt(DBSIM_panel,DBSIM_file_Path)
        
        if update == 4 :
            selected_name = ""
            json_file_path = ""
            
            #pick the json to work with 
            json_file_path = filedialog.askopenfilename(
            title="Select JSON File for adding the switch",
            filetypes=(("JSON Files", "*.json"), ("All Files", "*.*")))

            base_combine_panel_Img = Draw_panel_from_Jason(json_file_path)

            #get the panel name from the json file
            with open(json_file_path, "r") as file:
                existing_data = json.load(file)
            try:
                tempData.current_image_path = existing_data[0]['panelNamePath']
                tempData.DBSIM_panel = existing_data[0]['panelName']
                tempData.panelName = existing_data[0]['panelNameORS']
                tempData.panel_Image_Path = existing_data[0]['panelNamePath']

                panel = tempData.panelName
            except:
                messagebox.showwarning("Warning", "no panel name in the selected Jason file ")
                return
            elements = list_of_DBSIM_elemnt(tempData.DBSIM_panel,DBSIM_file_Path)
        file_path = filedialog.askopenfilename(title="Select new switch image",filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.gif")])

        # init the temp data for the new switch 
        tempData.new_scale = 1.0
        tempData.new_image_position = (0, 0)
        tempData.rotation_angle = 0

        if file_path:
            tempData.new_image_path = file_path
            if update == 1:
                tempData.base_img = Image.open(tempData.current_image_path)  # Open and store the base image 
            if update == 4:
                tempData.base_img = Image.open(base_combine_panel_Img)  # Open and store the base image 
            image_id = os.path.basename(file_path)
            img = Image.open(file_path)
            width, height = img.width, img.height

            switch = Switch(image_id=image_id, file_path=file_path, width=width, height=height)

            # Update the switch data to contain the panel name and the panel image path image_id and file_path
            if tempData.DBSIM_panel != "" :
                switch.panelName = tempData.DBSIM_panel
                switch.panel_Image_Path = tempData.panel_Image_Path 
            if tempData.panelName != "" :
                switch.panelNameORS = tempData.panelName
                switch.panel_Image_Path = tempData.panel_Image_Path 
            # else:
            #     pass

            switch.InPanelName = panelName
            switch.scale = tempData.new_scale
            #print("scale",switch.scale)
            select_switch_name(DB_file_path,panel, switch,elements,DBSIM_file_Path)                      
            switch_name = switch.imageName
            #print("here "  + switch_name)

            tempData.new_image_path = combine_switch_name_with_image(file_path, switch_name, [0,0])
            combine_images()
            update_info_label()
            if update == 1 :
                open_alpha_form(root,True,tempData,switch)
            if update == 4 :
                switch.json_file_path= json_file_path
                open_alpha_form(root,False,tempData,switch)    
#    
     # up date switch data  in  exsit  panel in json_file_path
    elif update==2 or update==3:
       
        selected_name = ""
        json_file_path = ""
        image_label.config(image='')
        
        # Create an instance of PctureClass and update parameters from JSON
        switch = Switch(image_id="image_id", file_path="file_path", width="width", height="height") 
        json_file_path = filedialog.askopenfilename(title="Select JSON File for update ", filetypes=(("JSON Files", "*.json"), ("All Files", "*.*")))
        base_combine_panel_Img = Draw_panel_from_Jason(json_file_path)
        json_file_path, selected_name = update_item(json_file_path)
        switch.update_parameters_from_json(json_file_path, selected_name)
        tempData.current_image_path = switch.panel_Image_Path
        tempData.panel_Image_Path = switch.panel_Image_Path
        tempData.DB_Default_File_Path = DB_file_path
        tempData.DBSIM_Default_file = DBSIM_file_Path
        if (switch.panelName == "" or switch.panelName == "none" or switch.panelName == "No DBSIM panel selected") and tempData.DBSIM_panel!= "No DBSIM panel selected":
            tempData.DBSIM_panel = DBSIM_panel
        else:
            tempData.DBSIM_panel = switch.panelName
        tempData.panelName = switch.panelNameORS

        panel_name_label.config(text=tempData.panelName)
        panel_name_label_DBSim.config(text=tempData.DBSIM_panel)
  
        # Update the switch data to contain the panel name and the panel image path image_id and file_path

        if update==3:
            file_path = filedialog.askopenfilename(title="Select image for up date  ",filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.gif")])
            tempData.new_image_path = file_path
            switch.file_path = tempData.new_image_path
            switch.image_id = tempData.new_image_path

        image_path = base_combine_panel_Img #'C:\\projectPython\\WCC\\Cockpit-Control\\frontend\\public\\CMDSPanel\\CMDS.png'
        img = Image.open(image_path)
        img_tk = ImageTk.PhotoImage(img)
        image_label.config(image=img_tk)
        image_label.image = img_tk  # Keep a reference to avoid garbage collection

        tempData.new_scale=switch.scale

        tempData.new_image_path = combine_switch_name_with_image(switch.file_path, switch.imageName, [0,0])
        tempData.new_image_position = (switch.x, switch.y)
        tempData.base_img = Image.open(base_combine_panel_Img)

            # Combine images and update info label
        combine_images()
        update_info_label()

        open_alpha_form(root,False,tempData,switch)
        Switch_name_listbox(root)

   
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

        def update_scroll_region(event=None):
            Imagecanvas.configure(scrollregion=Imagecanvas.bbox("all"))

        image_label.bind("<Configure>", update_scroll_region)

# Function to update the info label
def update_info_label():
    #global current_image_path, new_image_position
    if current_image_path:
        # Assuming switch is an object with image_id and file_path attributes
        switch = type('switch', (object,), {'image_id': 1, 'file_path': current_image_path})()
        info_label.config(text=f"Image ID: {switch.image_id}\nFile Path: {switch.file_path}\nNew Image Position: {new_image_position}")

# def set_move_pixels():
#     global tempData
#     pixels = simpledialog.askinteger("Input", "Enter the number of pixels to move:", minvalue=1)
#     if pixels:
#         tempData.move_pixels = pixels
#         step_size_label.config(text=f"Step : {tempData.move_pixels} pixels")

# def set_rotate_degree():
#     global tempData
#     degree = simpledialog.askinteger("Input", "Enter the roattion degree step:", minvalue=1)
#     if degree:
#         tempData.rotate_degree = degree
#         step_angle_label.config(text=f"step: {tempData.rotate_degree} degree")

def save_image():
    global tempData
    if tempData.combined_image_path:
        # Open file dialog to select save location
        save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
        if save_path:
            # Save the combined image to the specified location
            img = Image.open(tempData.combined_image_path)
            img.save(save_path)
            #print(f"Image saved to {save_path}")

def smallstep_handle(event):
    small_step = 1
    #print(f"event.state: {event.state}")
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
        # switch.width = int(switch.width  + switch.width *0.05)
        # switch.height = int(switch.height + switch.height *0.05)
    elif event.keysym == 'minus':
        switch.scale = float(switch.scale) - 0.05
        # switch.width = int(switch.width  - switch.width *0.05)
        # switch.height = int(switch.height - switch.height *0.05)

    combine_images()
    tempData.new_scale = switch.scale
    update_scale_image(switch)


def save(image_label,panel_name_label,panel_name_label_DBSim):
    global tempData,switch
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

        # Read the current contents of "Panel list.txt"
        file_name = os.path.basename(file_path)
        panel_list = []
        if os.path.exists("Panel list.txt"):
            with open("Panel list.txt", 'r') as panel_list_file:
                panel_list = panel_list_file.readlines()

            # Check if the file_name already exists in the list
            updated = False
            for i in range(len(panel_list)):
                if panel_list[i].startswith(file_name + "\t"):
                    panel_list[i] = f"{file_name}\t{file_path}\n"
                    updated = True
                    break

            # If the file_name does not exist, append the new entry
            if not updated:
                panel_list.append(f"{file_name}\t{file_path}\n")

            # Write the updated list back to "Panel list.txt"
            with open("Panel list.txt", 'w') as panel_list_file:
                panel_list_file.writelines(panel_list)
        else:
            messagebox.showwarning("Warning", "Panel list file not found")

    # Close the form
    panel_name_label.config(text="No ORS panel selected")
    panel_name_label_DBSim.config(text="No DBSIM panel selected")
    image_label.config(image='')
    #tempData = None
    #switch = None


def close():
    root.destroy()


######################################## Start ####################################################
# Create the main window

tempData = None
switch = None

# Create a new, empty alpha_data.json file
with open("alpha_data.json", "w") as file:
    json.dump([], file)


root = tk.Tk()
root.title("configure Json for panel")
# Set the position of the root window to the top-left corner of the screen
root.geometry("+0+0")

current_image_path = None

# Create a frame to hold the widgets
name_frame = ttk.Frame(root)
name_frame.grid(row=0, column=0, padx=10, pady=10)

# Create a label to display the image
# image_label = tk.Label(root)
# image_label.grid(row=1, column=0, columnspan=4, sticky="nsew")
# Define the maximum size for the image label
# Define the maximum size for the image label
max_width = 1000
max_height = 600

# Create a canvas widget
Imagecanvas = tk.Canvas(root, width=max_width, height=max_height)
Imagecanvas.grid(row=1, column=0, columnspan=4, sticky="nsew")

# Add horizontal and vertical scrollbars
h_scrollbar = ttk.Scrollbar(root, orient="horizontal", command=Imagecanvas.xview)
h_scrollbar.grid(row=2, column=0, columnspan=4, sticky="ew")

v_scrollbar = ttk.Scrollbar(root, orient="vertical", command=Imagecanvas.yview)
v_scrollbar.grid(row=1, column=4, sticky="ns")

# Configure the canvas to use the scrollbars
Imagecanvas.configure(xscrollcommand=h_scrollbar.set, yscrollcommand=v_scrollbar.set)

# Create a frame inside the canvas to hold the image label
image_frame = tk.Frame(Imagecanvas)
Imagecanvas.create_window((0, 0), window=image_frame, anchor="nw")

# Create a label to display the image inside the frame
image_label = tk.Label(image_frame)
image_label.pack()

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
browse_button = tk.Button(name_frame, text="Create panel ", command=lambda:browse_image(db_name_label.cget("text"),dbsim_name_label.cget("text"),image_label,Imagecanvas), state=tk.DISABLED)
browse_button.grid(row=0, column=0)

# Create a button to browse files
Show_panel = tk.Button(name_frame, text="present exsit panel", command=lambda:show_panel(image_label))
Show_panel.grid(row=0, column=1)

# Create a Panel DBSIM Update button 
Panel_DBSIM_Update = tk.Button(name_frame, text="Panel DBSIM Update ", command=Update_Panel_DBSIM_Name)
Panel_DBSIM_Update.grid(row=1, column=6)


json_file_path = 'InitValues.json'

# Create the "browse_DB" button
browse_db_button = ttk.Button(name_frame, text="Browse ORS DB", command=lambda: browse_DB(db_name_var, "*.json"), state=tk.NORMAL)
browse_db_button.grid(row=0, column=3, padx=10, pady=10)

# Create the DB_name label with a default value
defualt_db_name_var = get_default_db_path(json_file_path, "ORS")
db_name_var = tk.StringVar(value=defualt_db_name_var)
db_name_label = ttk.Label(name_frame, textvariable=db_name_var)
db_name_label.grid(row=0, column=4, padx=10, pady=10)

# Create the "browse_DBSIM" button
browse_dbSIM_button = ttk.Button(name_frame, text="Browse DBSIM", command=lambda: browse_DB(dbsim_name_var, "*.lrux"), state=tk.NORMAL)
browse_dbSIM_button.grid(row=0, column=5, padx=10, pady=10)

# Create the DB_name label with a default value
defualt_dbsim_name_var = get_default_db_path(json_file_path, "DBSIM")
dbsim_name_var = tk.StringVar(value=defualt_dbsim_name_var)
dbsim_name_label = ttk.Label(name_frame, textvariable=dbsim_name_var)
dbsim_name_label.grid(row=0, column=6, padx=10, pady=10)

# Create a button to updadte the JSON ORS DB file
Create_JSON_ORS_DB_button = tk.Button(name_frame, text="Create ORS JSON", command=transfer_to_json)
Create_JSON_ORS_DB_button.grid(row=0, column=7, padx=10, pady=10)

# Create a label to display the image_id and file_path
info_label = tk.Label(root, text="Image ID: File Path: New Image Position: (0, 0)")
info_label.grid(row=3, column=0, padx=5, pady=5)


# Create a frame to hold the widgets
switchbuttonframe = ttk.Frame(root)
switchbuttonframe.grid(row=4, column=0, padx=10, pady=5)

# panel_name_label = ttk.Label(switchbuttonframe, text="No panel selected", anchor='w')

# Create a button to add another image on top
add_button = tk.Button(switchbuttonframe, text="Add Switch", command=lambda: add_Switch(db_name_label.cget("text"),panel_name_label.cget("text"), 1,panel_name_label.cget("text"),dbsim_name_label.cget("text"),panel_name_label_DBSim.cget("text"),image_label,panel_name_label,panel_name_label_DBSim), state=tk.DISABLED, bg="lightgreen")
add_button.grid(row=3, column=0, padx=100, pady=0)

# Create a button to add update switch from the Jason file
update_button = tk.Button(switchbuttonframe, text="update switch data", command=lambda: add_Switch(db_name_label.cget("text"),panel_name_label.cget("text"), 2,panel_name_label.cget("text"),dbsim_name_label.cget("text"),panel_name_label_DBSim.cget("text"),image_label,panel_name_label,panel_name_label_DBSim), state=tk.NORMAL , bg="lightyellow")
update_button.grid(row=3, column=1, padx=5, pady=0)

# Create a button to add update switch from the Jason file
update_button_IMG = tk.Button(switchbuttonframe, text="update switch img", command=lambda: add_Switch( db_name_label.cget("text"),panel_name_label.cget("text"), 3,panel_name_label.cget("text"),dbsim_name_label.cget("text"),panel_name_label_DBSim.cget("text"),image_label,panel_name_label,panel_name_label_DBSim), state=tk.NORMAL , bg="lightyellow")
update_button_IMG.grid(row=3, column=2, padx=5, pady=0)

# Create a button to add update switch from the Jason file
update_button_add_switch = tk.Button(switchbuttonframe, text="add switch to exsit panel", command=lambda: add_Switch( db_name_label.cget("text"),panel_name_label.cget("text"), 4,panel_name_label.cget("text"),dbsim_name_label.cget("text"),panel_name_label_DBSim.cget("text"),image_label,panel_name_label,panel_name_label_DBSim), state=tk.NORMAL , bg="lightyellow")
update_button_add_switch.grid(row=3, column=4, padx=5, pady=0)

# Create a button to add delete switch from the Jason file 
delete_button = tk.Button(switchbuttonframe, text="delete switch", command=delete_item, state=tk.NORMAL,bg="lightcoral")
delete_button.grid(row=3, column=5, padx=100, pady=0)


# Create a frame to hold the widgets
frame = ttk.Frame(root)
frame.grid(row=5, column=0, padx=10, pady=5)


tempData.move_pixels, tempData.rotate_degree = Pixsel_Step_Define(json_file_path)

step_info_label = tk.Label(frame, text="""arrows for move image,"R" rotate right, "T" rotate left -> with "ALT" * 0.1, with "CTRL" * 10. "D" to move image to -100/-100""")
step_info_label.grid(row=0, column=0, padx=0, pady=0)


step_angle_info_label = tk.Label(frame, text=f" ""+"" or ""-"" foor scale up and down the image in 5%")
step_angle_info_label.grid(row=1, column=0, padx=0, pady=0)


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


save_button = tk.Button(root, text="Save", command=lambda: save(image_label,panel_name_label,panel_name_label_DBSim))
save_button.grid(row=8, column=1, padx=5, pady=5, sticky='e')


close_button = tk.Button(root, text="Close", command=close)
close_button.grid(row=8, column=0, padx=5, pady=5, sticky='w')

# Configure grid rows and columns
for i in range(8):
    root.grid_rowconfigure(i, weight=1)

for i in range(3):
    root.grid_columnconfigure(i, weight=1)

# Start the Tkinter event loop
root.mainloop()