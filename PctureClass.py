class Switch:
    def __init__(self, image_id, file_path, width, height):
        self.imageName = "switch"
        self.image_id = image_id
        self.file_path = file_path
        self.width = width
        self.height = height
        self.x = 0
        self.y = 0
        self.rotation = 0
        self.type_value = "state2"
        self.offset_on_value = "0"
        self.offset_off_value = "0"
        self.debugMode_value = "false"
        self.is_clickable_value = "true"
        self.click_bounds_height_factor_value = "2"
        self.click_bounds_width_factor_value = "1.5"
        self.top = "none"
        self.right = "none"
        self.bottom = "none"
        self.left = "none"
        self.press_pull1 = "none"
        self.press_pull2 ="none"
        self.color = "yellow"
        self.Logger = "true"
        self.grid_direction = "ud"
        self.String_Length = "0"
        self.Z_index = "0"
        self.rotation =[["none","0"],["none","0"],["none","0"],["none","0"],["none","0"],["none","0"],["none","0"],["none","0"],["none","0"],["none","0"]]
        self.conversion =[["none","none"],["none","none"],["none","none"],["none","none"],["none","none"],["none","none"],["none","none"],["none","none"],["none","none"],["none","none"]]
        self.value_conversion =[["0","0"],["0","0"],["0","0"],["0","0"],["0","0"]]        

# Method to resize the picture
    def resize(self, new_width, new_height):
        self.width = new_width
        self.height = new_height
        print(f"Picture resized to {self.width}x{self.height}")


    # Method to display picture information
    def display_info(self):
        print(f"Image ID: {self.image_id}")
        print(f"File Path: {self.file_path}")
        print(f"Width: {self.width}")
        print(f"Height: {self.height}")
        print(f"rotation: {self.rotation}")

class Panel:
    def __init__(self, name):
        self.Name = name
        
        

    # Method to display picture information
    def display_info(self):
        print(f"Panel Name: {self.Name}")

       


        