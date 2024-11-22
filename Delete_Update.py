   
import json
import tkinter as tk
from tkinter import Entry, StringVar, filedialog, messagebox
from tkinter import ttk
from Util import Bring_File_path


def delete_item():
    # Browse for the JSON file
    json_file_path = filedialog.askopenfilename(
    title="Select JSON File to delete from",
    filetypes=(("JSON Files", "*.json"), ("All Files", "*.*"))
    )
    if not json_file_path:
        return
        
    # Read the JSON file
    with open(json_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        
    # Get the list of backend_name items
    backend_names = [item['backend_name'] for item in data]
        
    # Create a new window to display the list of backend_name items
    list_window = tk.Toplevel()
    list_window.title("Select Item to Delete")
        
        # Create a listbox to display the backend_name items
    listbox = tk.Listbox(list_window)
    listbox.pack(pady=10, padx=10)
        
    for name in backend_names:
        listbox.insert(tk.END, name)
        
        # Add a delete button to the list window
    def confirm_delete(data):
        selected_index = listbox.curselection()
        if not selected_index:
            messagebox.showwarning("Warning", "No item selected")
            return
            
        selected_name = listbox.get(selected_index)
            
        # Delete the selected item from the JSON data
        data = [item for item in data if item['backend_name'] != selected_name]
            
        # Write the updated data back to the JSON file
        with open(json_file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4)
            
        messagebox.showinfo("Info", f"Item '{selected_name}' deleted successfully")

        with open("alpha_data.json", "w") as file:
                json.dump(data, file, indent=4)
        list_window.destroy()
        
    delete_button = ttk.Button(list_window, text="Delete", command=lambda: confirm_delete(data))
    delete_button.pack(pady=10)


def update_item() :
    # Browse for the JSON file
    json_file_path = filedialog.askopenfilename(
        title="Select JSON File",
        filetypes=(("JSON Files", "*.json"), ("All Files", "*.*"))
        )
    if not json_file_path:
        return
        
        # Read the JSON file
    with open(json_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        
        # Get the list of backend_name items
    backend_names = [item['backend_name'] for item in data]
        
        # Create a new window to display the list of backend_name items
    list_window = tk.Toplevel()
    list_window.title("Select Item to Update")
        
        # Create a listbox to display the backend_name items
    listbox = tk.Listbox(list_window)
    listbox.pack(pady=10, padx=10)
        
    for name in backend_names:
        listbox.insert(tk.END, name)
        
        # Add an update button to the list window
    def confirm_update():
        global selected_name
        selected_index = listbox.curselection()
        if not selected_index:
            messagebox.showwarning("Warning", "No item selected")
            return
            
        selected_name = listbox.get(selected_index)
            
        # # Create an instance of PctureClass and update parameters from JSON
        # switch = Switch(image_id="image_id", file_path="file_path", width="width", height="height") 
        # switch.update_parameters_from_json(json_file_path, selected_name)

        list_window.destroy()
        print(json_file_path, selected_name)
        #return json_file_path, selected_name
       
    update_button = ttk.Button(list_window, text="Update", command=confirm_update)
    update_button.pack(pady=10)

    list_window.wait_window()
    return json_file_path, selected_name




    
