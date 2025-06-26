import os
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, Radiobutton, StringVar

from fastapi import BackgroundTasks

from app.environments.env import DEFAULT_TEMP_DIR
from app.hwp import make_sps_hwp
from app.parser import parser
from app.schema.enums import CHECKSUM
from app.schema.web_api import SpsRequest
from app.util.util import create_random_named_folder, extract_zip

def select_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        file_label.config(text=file_path)

def calculate_checksum(file_path, algorithm):
    import hashlib
    try:
        hasher = hashlib.new(algorithm)
        with open(file_path, 'rb') as f:
            buf = f.read()
            hasher.update(buf)
        return hasher.hexdigest()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to calculate checksum: {e}")
        return None

def process_upload():
    # Collect form data
    selected_file = file_label.cget("text")
    device = device_entry.get()
    csu = csu_entry.get()
    version = version_entry.get()
    partnumber = partnumber_entry.get()
    checksum_type = checksum_var.get()

    if not selected_file:
        messagebox.showerror("Error", "Please select a file to upload.")
        return

    try:
        os.makedirs(DEFAULT_TEMP_DIR, exist_ok=True)
        os.makedirs("uploads", exist_ok=True)

        try:
            target = create_random_named_folder(DEFAULT_TEMP_DIR)
        except OSError as e:
            return

        file_path = Path(selected_file)
        
        file_location = f"{target}/{file_path.name}"
        directory_path = f"{target}/{file_path.stem}"
        save_as_location = f"{directory_path}.hwp"

        if file_path.name.endswith(".zip"):
            extract_zip(file_location, directory_path)

        # Create SpsRequest from form data
        device_request = SpsRequest(
            device=device,
            csu=csu,
            version=version,
            partnumber=partnumber,
            checksum_type=CHECKSUM(checksum_type)
        )

        retval = parser.get_sps_data(device_request, directory_path)

        make_sps_hwp.make(retval, save_as_location)

        messagebox.showinfo("Success", f"File processed: {processed_data}")

    except Exception as e:
        messagebox.showerror("Error", f"Failed to process file: {e}")

# Create main window
root = tk.Tk()
root.title("Upload File")

# Create and place widgets in the window
tk.Label(root, text="Select file:").grid(row=0, column=0)
file_label = tk.Label(root, text="No file selected", anchor="w")
file_label.grid(row=0, column=1)
tk.Button(root, text="Browse...", command=select_file).grid(row=0, column=2)

# Metadata fields
tk.Label(root, text="Device:").grid(row=1, column=0)
device_entry = tk.Entry(root)
device_entry.grid(row=1, column=1)

tk.Label(root, text="CSU:").grid(row=2, column=0)
csu_entry = tk.Entry(root)
csu_entry.grid(row=2, column=1)

tk.Label(root, text="Version:").grid(row=3, column=0)
version_entry = tk.Entry(root)
version_entry.grid(row=3, column=1)

tk.Label(root, text="Drawing No.:").grid(row=4, column=0)
partnumber_entry = tk.Entry(root)
partnumber_entry.grid(row=4, column=1)

# Checksum type
checksum_var = StringVar(value="MD5")
tk.Label(root, text="Checksum Type:").grid(row=5, column=0)
Radiobutton(root, text="MD5", variable=checksum_var, value="MD5").grid(row=5, column=1, sticky="w")
Radiobutton(root, text="SHA256", variable=checksum_var, value="SHA256").grid(row=5, column=2)

# Submit button
tk.Button(root, text="Upload", command=process_upload).grid(row=6, columnspan=3)

# Run the application
root.mainloop()
