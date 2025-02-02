import os
import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox

def get_new_filename(directory):
    """Generate a new result filename if one already exists."""
    base_name = "result"
    ext = ".csv"
    counter = 1
    new_file = os.path.join(directory, f"{base_name}{ext}")

    while os.path.exists(new_file):
        new_file = os.path.join(directory, f"{base_name}_{counter}{ext}")
        counter += 1

    return new_file

def search_csv_files(directory, column_name, search_string, result_directory, result_columns):
    results = []
    all_matches = []

    if not os.path.exists(directory) or not os.path.exists(result_directory):
        messagebox.showerror("Error", "Invalid directories selected.")
        return

    for file in os.listdir(directory):
        if file.endswith(".csv"):
            file_path = os.path.join(directory, file)
            try:
                df = pd.read_csv(file_path, encoding='utf-8')

                if column_name not in df.columns:
                    continue

                matching_rows = df[df[column_name].astype(str).str.contains(search_string, case=False, na=False)]

                if not matching_rows.empty:
                    results.append((file, matching_rows))

                    if all(col in df.columns for col in result_columns):
                        all_matches.append(matching_rows[result_columns])

            except:
                continue

    if all_matches:
        combined_results = pd.concat(all_matches, ignore_index=True)
        if not combined_results.empty:
            result_file_path = get_new_filename(result_directory)
            combined_results.to_csv(result_file_path, index=False, encoding='utf-8')
            messagebox.showinfo("Success", f"File written to CSV\nSaved as: {os.path.basename(result_file_path)}")

def browse_directory(entry_widget):
    """Open directory selection dialog and update entry field."""
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        entry_widget.delete(0, tk.END)
        entry_widget.insert(0, folder_selected)

def start_search():
    directory = dir_entry.get().strip()
    column_name = column_entry.get().strip()
    search_string = search_entry.get().strip()
    result_columns = result_entry.get().strip().split(",")
    result_directory = result_dir_entry.get().strip()

    if not all([directory, column_name, search_string, result_columns, result_directory]):
        messagebox.showerror("Error", "All fields are required.")
        return

    result_columns = [col.strip() for col in result_columns]
    search_csv_files(directory, column_name, search_string, result_directory, result_columns)

# Create GUI window
root = tk.Tk()
root.title("CSV Search Tool")
root.geometry("500x350")

# Directory Selection
tk.Label(root, text="CSV Folder:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
dir_entry = tk.Entry(root, width=40)
dir_entry.grid(row=0, column=1, padx=10, pady=5)
tk.Button(root, text="Browse", command=lambda: browse_directory(dir_entry)).grid(row=0, column=2)

# Column Name
tk.Label(root, text="Column Name:").grid(row=1, column=0, sticky="w", padx=10, pady=5)
column_entry = tk.Entry(root, width=40)
column_entry.grid(row=1, column=1, padx=10, pady=5)

# Search String
tk.Label(root, text="Search String:").grid(row=2, column=0, sticky="w", padx=10, pady=5)
search_entry = tk.Entry(root, width=40)
search_entry.grid(row=2, column=1, padx=10, pady=5)

# Columns for Result
tk.Label(root, text="Columns for Result (comma-separated):").grid(row=3, column=0, sticky="w", padx=10, pady=5)
result_entry = tk.Entry(root, width=40)
result_entry.grid(row=3, column=1, padx=10, pady=5)

# Result Directory Selection
tk.Label(root, text="Save CSV To:").grid(row=4, column=0, sticky="w", padx=10, pady=5)
result_dir_entry = tk.Entry(root, width=40)
result_dir_entry.grid(row=4, column=1, padx=10, pady=5)
tk.Button(root, text="Browse", command=lambda: browse_directory(result_dir_entry)).grid(row=4, column=2)

# Search Button
tk.Button(root, text="Search", command=start_search, bg="green", fg="white").grid(row=5, column=1, pady=20)

# Run the GUI
root.mainloop()
