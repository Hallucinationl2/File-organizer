import os
import shutil
import customtkinter as ctk
from tkinter import messagebox

# Initialize customtkinter with dark theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

# Global variables to track moved files and user-selected files
moved_files = {}
selected_files = {}


def load_files():
    global selected_files
    selected_files.clear()

    try:
        # Get the desktop path
        desktop_path = os.path.expanduser("~/Desktop")

        # Clear the scrollable frame
        for widget in file_frame.winfo_children():
            widget.destroy()

        # Loop through all files on the desktop
        for filename in os.listdir(desktop_path):
            file_path = os.path.join(desktop_path, filename)

            # Check if it's a file
            if os.path.isfile(file_path):
                # Add a checkbox for each file
                var = ctk.StringVar(value="unchecked")
                checkbox = ctk.CTkCheckBox(file_frame, text=filename, variable=var, onvalue="checked",
                                           offvalue="unchecked")
                checkbox.pack(anchor="w", padx=10, pady=2)
                selected_files[file_path] = var

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while loading files: {e}")


def organize_selected_files():
    global moved_files
    moved_files = {}  # Reset moved files tracking

    try:
        # Get the desktop path
        desktop_path = os.path.expanduser("~/Desktop")

        # Dictionary to store file paths by file extension
        files_by_extension = {}
        total_files = 0

        # Collect only user-selected files
        for file_path, var in selected_files.items():
            if var.get() == "checked":
                total_files += 1
                file_extension = os.path.splitext(file_path)[1]

                # Add file path and file extension to the dictionary
                if file_extension not in files_by_extension:
                    files_by_extension[file_extension] = []

                files_by_extension[file_extension].append(file_path)

        # Create a folder for each file type and move files into their folders
        for file_extension, file_paths in files_by_extension.items():
            folder_name = f"{file_extension[1:].upper()} Files"
            folder_path = os.path.join(desktop_path, folder_name)

            # Create folder if it does not exist
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)

            # Move files to their folders
            for file_path in file_paths:
                new_path = os.path.join(folder_path, os.path.basename(file_path))
                shutil.move(file_path, new_path)
                moved_files[new_path] = file_path  # Track the moved file

        # Display summary of the operation
        summary_message = f"Files organized successfully!\n\nTotal files: {total_files}\nFile types: {', '.join(files_by_extension.keys()) or 'None'}"
        messagebox.showinfo("Success", summary_message)

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")


def undo_organize():
    global moved_files

    try:
        if not moved_files:
            messagebox.showinfo("Undo", "No changes to undo!")
            return

        # Move files back to their original locations
        for new_path, original_path in moved_files.items():
            shutil.move(new_path, original_path)

        moved_files = {}  # Clear the moved files tracking after undo
        messagebox.showinfo("Undo", "Files have been restored to their original locations!")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while undoing: {e}")


def select_all_files():
    for var in selected_files.values():
        var.set("checked")  # Set all checkboxes to selected state


def deselect_all_files():
    for var in selected_files.values():
        var.set("unchecked")  # Set all checkboxes to deselected state


# Main block to start the application
if __name__ == "__main__":
    # Create the main application window
    app = ctk.CTk()
    app.geometry("500x500")
    app.title("Desktop File Organizer")

    # Add a title label
    title_label = ctk.CTkLabel(app, text="Desktop File Organizer", font=("Arial", 18))
    title_label.pack(pady=10)

    # Add a scrollable frame to display files
    file_frame = ctk.CTkScrollableFrame(app, width=400, height=200)
    file_frame.pack(pady=10, padx=10, fill="both", expand=True)

    # Load files initially
    load_files()

    # Add a button to trigger the organization process
    organize_button = ctk.CTkButton(app, text="Organize Selected Files", command=organize_selected_files)
    organize_button.pack(pady=10)

    # Add a button to undo the organization process
    undo_button = ctk.CTkButton(app, text="Undo", command=undo_organize)
    undo_button.pack(pady=10)

    # Add buttons for select all and deselect all
    select_all_button = ctk.CTkButton(app, text="Select All", command=select_all_files)
    select_all_button.pack(pady=5)

    deselect_all_button = ctk.CTkButton(app, text="Deselect All", command=deselect_all_files)
    deselect_all_button.pack(pady=5)

    # Add a button to reload files
    reload_button = ctk.CTkButton(app, text="Reload Files", command=load_files)
    reload_button.pack(pady=10)

    # Start the application
    app.mainloop()
