import tkinter as tk
from tkinter import filedialog, simpledialog
from PIL import Image, ImageTk

def move_image(event, new_image_position, move_pixels, new_image_path, image_position_entry, small_Step, combine_images, update_info_label):
    if new_image_path:
        if event.keysym == 'Right':
            new_image_position = (new_image_position[0] + move_pixels // small_Step, new_image_position[1])
        elif event.keysym == 'Left':
            new_image_position = (new_image_position[0] - move_pixels // small_Step, new_image_position[1])
        elif event.keysym == 'Up':
            new_image_position = (new_image_position[0], new_image_position[1] - move_pixels // small_Step)
        elif event.keysym == 'Down':
            new_image_position = (new_image_position[0], new_image_position[1] + move_pixels // small_Step)
        combine_images()
        update_info_label()
        if image_position_entry:
            image_position_entry.delete(0, tk.END)
            image_position_entry.insert(0, str(new_image_position))
    return new_image_position


def rotate_image(event, img, rotation_angle, rotate_degree, rotation_entry, image_label,combine_images):#, update_info_label):
    disp_rotation_angle = 0
    # Check if img is not None
    if img is None:
        print("No image loaded to rotate.")
        return rotation_angle

    # # Increment the rotation angle by 30 degrees
    # rotation_angle = (rotation_angle + rotate_degree // small_Step) % 360
    # Increment the rotation angle by 30 degrees  
    rotation_angle = (rotation_angle + rotate_degree) % 360


    # Rotate the image
    rotated_img = img.rotate(rotation_angle, expand=True)
    img_tk = ImageTk.PhotoImage(rotated_img)
    image_label.config(image=img_tk)
    image_label.image = img_tk  # Keep a reference to avoid garbage collection

    # Update the rotation value in the alpha form
    if rotation_entry:
        rotation_entry.delete(0, tk.END)
        if rotation_angle < 180:
            disp_rotation_angle = 0 - rotation_angle
        else:
            disp_rotation_angle = 360- rotation_angle
        rotation_entry.insert(0, str(disp_rotation_angle))

    # Combine images and update info label
    combine_images()
    #update_info_label()
    #print (rotation_angle)


    return rotation_angle 


def Bring_File_path ():
    global file_path
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.gif")])
    return file_path

