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
        self.rotation =[["none","none"],["none","none"],["none","none"],["none","none"],["none","none"],["none","none"],["none","none"],["none","none"],["none","none"],["none","none"]]
        self.conversion =[["none","none"],["none","none"],["none","none"],["none","none"],["none","none"],["none","none"],["none","none"],["none","none"],["none","none"],["none","none"]]
        self.value_conversion =[["none","none"],["none","none"],["none","none"],["none","none"],["none","none"]]  
        self.scale = 1 
        self.IMG_rotation = "100"   
        self.json_file_path = "none"  
        self.InPanelName = "In_panel_name"

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
                item = next((item for item in data if item['backend_name'] == item_name), None)
                if item:
                    self.imageName = item.get('backend_name', self.imageName)  
                    self.image_id = item.get('imageDefault', self.image_id) 
                    imageProps = item.get('imageProps', {})
                    self.file_path = imageProps.get('imageDefault', self.file_path) 
                    self.width = item.get('img_width', self.width) 
                    self.height = item.get('img_height', self.height) 
                    self.x = item.get('pos_left', self.x) 
                    self.y = item.get('pos_top', self.y) 
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
                    self.top = mapping.get('map_top', self.top)
                    self.right = mapping.get('map_right', self.right)
                    self.bottom = mapping.get('map_bottom',self.bottom)
                    self.left = mapping.get('map_left', self.left)
                    self.press_pull1 = mapping.get('map_press_pull1', self.press_pull1)
                    self.press_pull2 = mapping.get('map_press_pull2', self.press_pull2)
                    blinking = item.get('string_props', {})
                    self.color = blinking.get('color', self.color) 
                    self.grid_direction = "ud"
                    string_props = item.get('string_props', {})
                    self.String_Length = string_props.get('maxStringLength', self.String_Length) 
                    self.Z_index = item.get('Z_index', self.Z_index) 
                    # Read and update the "knob_props" dictionary
                    self.rotation =[["none","none"],["none","none"],["none","none"],["none","none"],["none","none"],["none","none"],["none","none"],["none","none"],["none","none"],["none","none"]]
                    knob_props = item.get('knob_props')
                    conversion = knob_props.get('conversion')
                    updated_rotation = [[angle, value] for angle, value in conversion.items()]
                    for i in range(len(updated_rotation)):
                        self.rotation[i] = updated_rotation[i]

                    # Read and update the "additionalImageData" dictionary
                    self.conversion =[["none","none"],["none","none"],["none","none"],["none","none"],["none","none"],["none","none"],["none","none"],["none","none"],["none","none"],["none","none"]]
                    imageProps = item.get('imageProps')
                    additionalImageData = imageProps.get('additionalImageData')
                    updated_additionalImageData = [[Pic, Path] for Pic, Path in additionalImageData.items()]
                    for j in range(len(updated_additionalImageData)):
                        self.conversion[j] = updated_additionalImageData[j]

                    self.value_conversion =[["none","none"],["none","none"],["none","none"],["none","none"],["none","none"]]   
                    analog_props = item.get('analog_props')
                    Value_conversion = analog_props.get('Value_conversion')
                    updated_value_conversion = [[ang1, ang2] for ang1, ang2 in Value_conversion.items()]
                    for k in range(len(updated_value_conversion)):
                        self.value_conversion[k] = updated_value_conversion[k]

                    self.json_file_path = json_file_path

                    print(f"Updated parameters for {item_name} from {json_file_path}")
                else:
                    print(f"Item with name {item_name} not found in {json_file_path}")
        except FileNotFoundError:
            print(f"File {json_file_path} not found")
        except json.JSONDecodeError:
            print(f"Error decoding JSON from {json_file_path}")   

class TempData:
    def __init__(self):
        self.new_scale = 1.0
        self.new_position= (0, 0)
        self.rotation_angle = 0
        self.disp_rotation_angle = 0
        self.current_image_path = None
        self.new_image_path = None
        self.rotated_new_img = None
        self.new_image_position = (0, 0)
        self.combined_image_path = None
        self.base_img = None  # Add a global variable to store the base image
        self.move_pixels = 10  # Default number of pixels to move
        self.rotate_degree = 10
        self.image_position_entry = None  # Reference to the image position entry field in the alpha form
        self.img = None  # Add a global variable to store the image
        self.image_label = None  # Add a global variable to store the image label
        self.panel_name_label_String = None  # Add a global variable to store the panel name label
