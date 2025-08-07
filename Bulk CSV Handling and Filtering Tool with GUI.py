import os
import pandas as pd
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from datetime import datetime

class CSVSearcherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CSV Searcher with UI")
        self.root.geometry("900x600")
        self.root.minsize(700, 500)

        # Configure grid
        for i in range(3):
            self.root.grid_columnconfigure(i, weight=1)
        for i in range(10):
            self.root.grid_rowconfigure(i, weight=1)

        # Create UI components
        self.filters = []
        self.search_results = []
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="Source Folder:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.source_entry = tk.Entry(self.root, width=50)
        self.source_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
        ttk.Button(self.root, text="Browse", command=self.browse_source).grid(row=0, column=2, padx=5, pady=5)

        tk.Label(self.root, text="Destination Folder:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.dest_entry = tk.Entry(self.root, width=50)
        self.dest_entry.grid(row=1, column=1, sticky="ew", padx=5, pady=5)
        ttk.Button(self.root, text="Browse", command=self.browse_destination).grid(row=1, column=2, padx=5, pady=5)

        # **Apply Filter Title Row**
        filter_title_row = tk.Frame(self.root)
        filter_title_row.grid(row=2, column=0, columnspan=3, sticky="ew", pady=5)

        tk.Label(filter_title_row, text="Apply Filter", font=("Arial", 12, "bold")).grid(row=0, column=0, sticky="w", padx=5)
        ttk.Button(filter_title_row, text="+", command=self.add_filter, width=5).grid(row=0, column=1, padx=5, pady=2)
        ttk.Button(filter_title_row, text="🗑 Clear Filters", command=self.clear_filters).grid(row=0, column=2, padx=5, pady=2)

        # **Scrollable Filter Section**
        self.filter_frame_container = tk.Frame(self.root)
        self.filter_frame_container.grid(row=3, column=0, columnspan=3, padx=5, pady=5, sticky="ew")

        self.canvas = tk.Canvas(self.filter_frame_container, height=150)  # **Fixed height**
        scrollbar = ttk.Scrollbar(self.filter_frame_container, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Start with one filter row
        self.add_filter()

        # Buttons
        self.search_btn = ttk.Button(self.root, text="Search", command=self.search_csv_files)
        self.search_btn.grid(row=4, column=1, pady=10, padx=5)

        self.export_btn = ttk.Button(self.root, text="Export", command=self.export_results)  # ✅ FIXED!
        self.export_btn.grid(row=4, column=2, pady=10, padx=5)

        # Results Table with Scrollbar
        frame = ttk.Frame(self.root)
        frame.grid(row=5, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

        self.tree = ttk.Treeview(frame, show="headings")
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def add_filter(self):
        """Dynamically adds a new filter row."""
        row_index = len(self.filters) * 2  # Each filter takes two rows

        tk.Label(self.scrollable_frame, text=f"Filter {len(self.filters) + 1}", font=("Arial", 10, "bold")).grid(row=row_index, column=0, padx=5, pady=2)

        tk.Label(self.scrollable_frame, text="Column Name", font=("Arial", 10, "bold")).grid(row=row_index, column=1, sticky="w", padx=5, pady=2)
        column_entry = tk.Entry(self.scrollable_frame, width=30)
        column_entry.grid(row=row_index, column=2, padx=5, pady=2)

        tk.Label(self.scrollable_frame, text="Search String", font=("Arial", 10, "bold")).grid(row=row_index + 1, column=1, sticky="w", padx=5, pady=2)
        search_entry = tk.Entry(self.scrollable_frame, width=30)
        search_entry.grid(row=row_index + 1, column=2, padx=5, pady=2)

        # Store references for filtering
        self.filters.append((column_entry, search_entry))

    def clear_filters(self):
        """Clears all filters except the first one."""
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        # Keep only the first filter
        self.filters = []
        self.add_filter()  

    def export_results(self):
        """Exports the search results to a CSV file."""
        if not self.search_results:
            messagebox.showwarning("Warning", "No search results to export!")
            return

        result_directory = self.dest_entry.get()
        if not os.path.exists(result_directory):
            messagebox.showerror("Error", "Invalid destination directory")
            return

        combined_results = pd.concat(self.search_results, ignore_index=True)
        if not combined_results.empty:
            current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            result_file_name = f"search_results_{current_time}.csv"
            result_file_path = os.path.join(result_directory, result_file_name)
            combined_results.to_csv(result_file_path, index=False, encoding='utf-8')
            messagebox.showinfo("Success", f"Results exported to {result_file_path}")

    def browse_source(self):
        folder = filedialog.askdirectory()
        self.source_entry.delete(0, tk.END)
        self.source_entry.insert(0, folder)

    def browse_destination(self):
        folder = filedialog.askdirectory()
        self.dest_entry.delete(0, tk.END)
        self.dest_entry.insert(0, folder)

    def search_csv_files(self):
        """Performs the search operation."""
        directory = self.source_entry.get()
        if not os.path.exists(directory):
            messagebox.showerror("Error", "Invalid source directory")
            return

        self.tree.delete(*self.tree.get_children())
        self.search_results = []

        filters = [(col.get().strip(), val.get().strip()) for col, val in self.filters if col.get().strip() and val.get().strip()]
        if not filters:
            messagebox.showwarning("Warning", "Please enter at least one filter.")
            return

        for file in os.listdir(directory):
            if file.endswith(".csv"):
                file_path = os.path.join(directory, file)
                try:
                    df = pd.read_csv(file_path, encoding="utf-8", on_bad_lines="skip")
                    for col, val in filters:
                        if col in df.columns:
                            df = df[df[col].astype(str).str.contains(val, case=False, na=False)]
                    if not df.empty:
                        self.search_results.append(df)
                        for _, row in df.iterrows():
                            self.tree.insert("", "end", values=[file] + row.astype(str).tolist())
                except Exception as e:
                    print(f"Error processing {file}: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = CSVSearcherApp(root)
    root.mainloop()
