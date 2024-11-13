import json


class Switch:
    def __init__(self, image_id, file_path, width, height):
        emptyList = [["none","none"],["none","none"],["none","none"],["none","none"],["none","none"],["none","none"],["none","none"],["none","none"],["none","none"],["none","none"]]
        self.imageName = "switch"
        self.image_id = image_id
        self.file_path = file_path
        self.scale = 1.0
        self.width = width
        self.height = height
        self.x = 0
        self.y = 0
        self.rotation = 0
        self.type_value = "stateN"
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
        self.rotation =emptyList #[["none","none"],["none","none"],["none","none"],["none","none"],["none","none"],["none","none"],["none","none"],["none","none"],["none","none"],["none","none"]]
        self.conversion =emptyList #[["none","none"],["none","none"],["none","none"],["none","none"],["none","none"],["none","none"],["none","none"],["none","none"],["none","none"],["none","none"]]
        self.value_conversion =emptyList #[["none","none"],["none","none"],["none","none"],["none","none"],["none","none"]]  
        self.scale = 1 
        self.IMG_rotation = "100"   
        self.json_file_path = "none"  
        self.InPanelName = "In_panel_name"
        self.DBSIM_Element = "none"
        self.DBSimElementValues = emptyList
        self.DBSimElementValues_Display = []
        
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
                    self.type_value = item.get('type', self.type_value)
                    self.imageName = item.get('backend_name', self.imageName)  
                    
                    backend = item.get('backend', {})
                    dbsimProps = backend.get('dbsimProps', {})
                    self.DBSimElementValues = dbsimProps.get('enumMapping', {})
                    for i in range(len(self.DBSimElementValues)):
                        self.DBSimElementValues_Display.append(self.DBSimElementValues[i] + "\n") 
                    self.DBSIM_Element =  self.imageName
                    
                    component = item.get('component', {})
                    self.debugMode_value = component.get('debugMode', self.debugMode_value) 
                    self.is_clickable_value = component.get('is_clickable', self.is_clickable_value)
                    
                    position = component.get('position', {})
                    self.width = position.get('img_width', self.width) 
                    self.height = position.get('img_height', self.height) 
                    self.x = position.get('pos_left', self.x) 
                    self.y = position.get('pos_top', self.y) 
                    self.scale = position.get('scale', self.scale)  
                    self.Z_index = position.get('Z_index', self.Z_index) 
                    
                    imageProps = component.get('imageProps', {})
                    self.image_id = imageProps.get('imageDefault', self.image_id) 
                    self.file_path = imageProps.get('imageDefault', self.file_path)
                                   # Read and update the "additionalImageData" dictionary
                    self.conversion =[["none","none"],["none","none"],["none","none"],["none","none"],["none","none"],["none","none"],["none","none"],["none","none"],["none","none"],["none","none"]]
                    additionalImageData = imageProps.get('additionalImageData')
                    updated_additionalImageData = [[Pic, Path] for Pic, Path in additionalImageData.items()]
                    for j in range(len(updated_additionalImageData)):
                        self.conversion[j] = updated_additionalImageData[j]


                    click_props = component.get('click_props', {})
                    self.click_bounds_height_factor_value = click_props.get('click_bounds_height_factor', self.click_bounds_height_factor_value) 
                    self.click_bounds_width_factor_value = click_props.get('click_bounds_width_factor', self.click_bounds_width_factor_value) 
                    mapping = click_props.get('mapping', {})
                    self.top = mapping.get('map_top', self.top)
                    self.right = mapping.get('map_right', self.right)
                    self.bottom = mapping.get('map_bottom',self.bottom)
                    self.left = mapping.get('map_left', self.left)
                    self.press_pull1 = mapping.get('map_press_pull1', self.press_pull1)
                    self.press_pull2 = mapping.get('map_press_pull2', self.press_pull2)

                                        # Read and update the "knob_props" dictionary
                    self.rotation =[["none","none"],["none","none"],["none","none"],["none","none"],["none","none"],["none","none"],["none","none"],["none","none"],["none","none"],["none","none"]]
                    knob_props = component.get('knob_props')
                    rotation_conversion = knob_props.get('rotation')
                    updated_rotation = [[angle, value] for angle, value in rotation_conversion.items()]
                    for i in range(len(updated_rotation)):
                        self.rotation[i] = updated_rotation[i]

                    self.value_conversion =[["none","none"],["none","none"],["none","none"],["none","none"],["none","none"]]   
                    analog_props = component.get('analog_props')
                    Value_conversion = analog_props.get('conversion')
                    updated_value_conversion = [[ang1, ang2] for ang1, ang2 in Value_conversion.items()]
                    for k in range(len(updated_value_conversion)):
                        self.value_conversion[k] = updated_value_conversion[k]

                    string_props = component.get('string_props', {})
                    self.String_Length = string_props.get('maxStringLength', self.String_Length) 
                    
                    blinking = component.get('blinking', {})
                    self.color = blinking.get('color', self.color) 
                    
                    logger = component.get('logger', {})
                    self.Logger = logger.get('display', self.Logger)

                    # self.type_value = item.get('type', self.type_value) 
                    # self.offset_on_value = item.get('offset_on', self.offset_on_value) 
                    # self.offset_off_value = item.get('offset_off', self.offset_off_value) 
                    # self.grid_direction = "ud"
                    # self.value_conversion =[["none","none"],["none","none"],["none","none"],["none","none"],["none","none"]]   
                    # analog_props = item.get('analog_props')
                    # Value_conversion = analog_props.get('Value_conversion')
                    # updated_value_conversion = [[ang1, ang2] for ang1, ang2 in Value_conversion.items()]
                    # for k in range(len(updated_value_conversion)):
                    #     self.value_conversion[k] = updated_value_conversion[k]
                    self.grid_direction = "ud"
                    self.IMG_rotation = "0" 
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
        self.DBSIM_Default_file = None
        self.DB_Default_File_Path = None
        self.DBSIM_panel = None
        self.panelName = None

