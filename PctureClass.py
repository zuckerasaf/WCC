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

       


        