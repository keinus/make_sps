import tkinter as tk
from tkinter import filedialog, messagebox
import requests


def browse_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        file_entry.delete(0, tk.END)
        file_entry.insert(0, file_path)


def upload_file():
    # Get all the form data
    device = device_entry.get()
    csu = csu_entry.get()
    version = version_entry.get()
    partnumber = partnumber_entry.get()
    checksum_type = checksum_var.get()

    if not file_entry.get():
        messagebox.showerror("Error", "Please select a file to upload.")
        return

    # Prepare the form data
    with open(file_entry.get(), 'rb') as f:
        files = {'file': f}
        data = {
            'device': device,
            'csu': csu,
            'version': version,
            'partnumber': partnumber,
            'checksum_type': checksum_type
        }

        try:
            response = requests.post(
                "http://localhost:8000/uploadfile/", files=files, data=data)
            if response.ok:
                messagebox.showinfo("Success", "File uploaded successfully!")
            else:
                messagebox.showerror(
                    "Error", f"Failed to upload file. Error: {response.text}")
        except Exception as e:
            messagebox.showerror("Error", f"Error: {str(e)}")


# Create the main window
root = tk.Tk()
root.title("File Upload Form")
root.geometry("600x750")
root.configure(bg="#f0f0f0")

# Custom font for all widgets
default_font = ("Helvetica", 12)

# File selection section
file_frame = tk.Frame(root, bg="#f0f0f0")
tk.Label(file_frame, text="Select file:", font=("Helvetica", 14, "bold"),
         bg="#f0f0f0").pack(pady=(20, 5))
file_entry = tk.Entry(file_frame, width=40, font=default_font)
browse_button = tk.Button(
    file_frame,
    text="Browse...",
    command=browse_file,
    font=default_font,
    bg="#dcdcdc"
)
file_entry.pack(side=tk.LEFT, padx=(0, 10))
browse_button.pack(side=tk.RIGHT)
file_frame.pack(pady=(20, 30))

# Create input fields with better organization
input_fields = [
    ("장비식별자:", "device"),
    ("CSU:", "csu"),
    ("Version:", "version"),
    ("도면번호(SW부품번호):", "partnumber")
]

# Initialize entry variables
device_entry = None
csu_entry = None
version_entry = None
partnumber_entry = None

for label_text, var_name in input_fields:
    field_frame = tk.Frame(root, bg="#f0f0f0")
    tk.Label(field_frame, text=label_text, font=("Helvetica", 12),
             bg="#f0f0f0").pack(side=tk.LEFT)
    globals()[f"{var_name}_entry"] = tk.Entry(
        field_frame, width=40, font=default_font)
    # Assign to variables for use in upload_file
    if var_name == "device":
        device_entry = globals()[f"{var_name}_entry"]
    elif var_name == "csu":
        csu_entry = globals()[f"{var_name}_entry"]
    elif var_name == "version":
        version_entry = globals()[f"{var_name}_entry"]
    elif var_name == "partnumber":
        partnumber_entry = globals()[f"{var_name}_entry"]
    globals()[f"{var_name}_entry"].pack(side=tk.RIGHT)
    field_frame.pack(pady=(10, 20), fill=tk.X, padx=30)

# Create radio buttons for checksum type with better layout
checksum_frame = tk.Frame(root, bg="#f0f0f0")
tk.Label(checksum_frame, text="Checksum Type:", font=("Helvetica", 12),
         bg="#f0f0f0").pack(side=tk.LEFT)
checksum_var = tk.StringVar(value="MD5")
tk.Radiobutton(
    checksum_frame,
    text="MD5",
    variable=checksum_var,
    value="MD5",
    font=default_font,
    bg="#f0f0f0"
).pack(side=tk.LEFT, padx=(20, 10))
tk.Radiobutton(
    checksum_frame,
    text="SHA256",
    variable=checksum_var,
    value="SHA256",
    font=default_font,
    bg="#f0f0f0"
).pack(side=tk.LEFT)
checksum_frame.pack(pady=(10, 30), fill=tk.X, padx=30)

# Create upload button with improved styling
upload_button = tk.Button(
    root,
    text="Upload",
    command=upload_file,
    font=("Helvetica", 14),
    bg="#007bff",
    fg="white"
)
upload_button.pack(pady=(20, 30))

# Start the main event loop
root.mainloop()
