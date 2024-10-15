import json


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
        print(f"rotation : {self.rotation}")

    def update_parameters_from_json(self, json_file_path, item_name):
        """
        Update the parameters of the item from the JSON file.
        :param json_file_path: Path to the JSON file.
        :param item_name: Name of the item to update.
        """
        try:
            with open(json_file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                item = next((item for item in data if item['name'] == item_name), None)
                if item:
                    self.imageName = item.get('backend_name', self.imageName)  
                    self.image_id = item.get('imageDefault', self.image_id) 
                    self.file_path = item.get('imageDefault', self.file_path) 
                    self.width = item.get('width', self.width) 
                    self.height = item.get('height', self.height) 
                    self.x = item.get('left', self.x) 
                    self.y = item.get('top', self.y) 
                    self.rotation = "0" 
                    self.type_value = item.get('type', self.type_value) 
                    self.offset_on_value = item.get('offset_on', self.offset_on_value) 
                    self.offset_off_value = item.get('offset_off', self.offset_off_value) 
                    self.debugMode_value = item.get('debugMode', self.debugMode_value) 
                    self.is_clickable_value = item.get('is_clickable', self.is_clickable_value)
                    # Read the "click_props" dictionary
                    click_props = item.get('click_props', {})
                    self.click_bounds_height_factor_value = click_props.get('click_bounds_height_factor', self.click_bounds_height_factor_value) 
                    self.click_bounds_width_factor_value = click_props.get('click_bounds_width_factor', self.click_bounds_width_factor_value) 
                    mapping = click_props.get('mapping', {})
                    self.top = mapping.get('top', self.top)
                    self.right = mapping.get('right', self.right)
                    self.bottom = mapping.get('bottom',self.bottom)
                    self.left = mapping.get('left', self.left)
                    self.press_pull1 = mapping.get('press_pull1', self.press_pull1)
                    self.press_pull2 = mapping.get('press_pull2', self.press_pull2)
                    blinking = item.get('string_props', {})
                    self.color = blinking.get('color', self.color) 
                    self.grid_direction = "ud"
                    string_props = item.get('string_props', {})
                    self.String_Length = string_props.get('maxStringLength', self.String_Length) 
                    self.Z_index = item.get('Z_index', self.Z_index) 
                    self.rotation =[["none","0"],["none","0"],["none","0"],["none","0"],["none","0"],["none","0"],["none","0"],["none","0"],["none","0"],["none","0"]]
                    self.conversion =[["none","none"],["none","none"],["none","none"],["none","none"],["none","none"],["none","none"],["none","none"],["none","none"],["none","none"],["none","none"]]
                    self.value_conversion =[["0","0"],["0","0"],["0","0"],["0","0"],["0","0"]]   

                    print(f"Updated parameters for {item_name} from {json_file_path}")
                else:
                    print(f"Item with name {item_name} not found in {json_file_path}")
        except FileNotFoundError:
            print(f"File {json_file_path} not found")
        except json.JSONDecodeError:
            print(f"Error decoding JSON from {json_file_path}")   

class Panel:
    def __init__(self, name):
        self.Name = name
        
        

    # Method to display picture information
    def display_info(self):
        print(f"Panel Name: {self.Name}")

       


        