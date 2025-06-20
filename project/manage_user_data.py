import tkinter as tk
from tkinter import messagebox, ttk
import os
import re

# File path for user_data.txt
DATA_FILE = 'D:/Btech/Coding/python-Project/project/user_data.txt'

class UserDataManager:
    def __init__(self, root):
        self.root = root
        self.root.title("User Data Manager")
        # Maximize window (resizable with window controls)
        self.root.state('zoomed')
        # Allow exit with Escape key
        self.root.bind('<Escape>', lambda e: self.root.quit())
        
        # Outer frame to center content
        self.outer_frame = ttk.Frame(self.root)
        self.outer_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        # Main frame for content
        self.main_frame = ttk.Frame(self.outer_frame, padding="10")
        self.main_frame.grid(row=0, column=0, pady=20, padx=20)
        self.outer_frame.columnconfigure(0, weight=1)
        self.outer_frame.rowconfigure(0, weight=1)
        
        # Button frame
        self.button_frame = ttk.Frame(self.main_frame)
        self.button_frame.grid(row=0, column=0, pady=10, sticky=tk.EW)
        self.main_frame.columnconfigure(0, weight=1)
        
        # Buttons
        ttk.Button(self.button_frame, text="View Data", command=self.view_data).grid(row=0, column=0, padx=5)
        ttk.Button(self.button_frame, text="Delete Selected", command=self.delete_data).grid(row=0, column=1, padx=5)
        ttk.Button(self.button_frame, text="Exit", command=self.root.quit).grid(row=0, column=2, padx=5)
        
        # Data display
        self.data_tree = ttk.Treeview(self.main_frame, columns=("Index", "Name", "Age"), show="headings")
        self.data_tree.heading("Index", text="#")
        self.data_tree.heading("Name", text="Name")
        self.data_tree.heading("Age", text="Age")
        self.data_tree.column("Index", width=50)
        self.data_tree.column("Name", width=300)
        self.data_tree.column("Age", width=100)
        self.data_tree.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(self.main_frame, orient=tk.VERTICAL, command=self.data_tree.yview)
        scrollbar.grid(row=1, column=1, sticky=(tk.N, tk.S))
        self.data_tree.configure(yscrollcommand=scrollbar.set)
        
        # Initial data load
        self.view_data()
    
    def read_data(self):
        """Read data from user_data.txt."""
        try:
            if os.path.exists(DATA_FILE):
                with open(DATA_FILE, 'r') as file:
                    lines = file.readlines()
                return [line.strip() for line in lines if line.strip()]
            return []
        except (IOError, PermissionError) as e:
            messagebox.showerror("Error", f"Error reading file: {e}")
            return []
    
    def save_data(self, lines):
        """Save data to user_data.txt."""
        try:
            os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
            with open(DATA_FILE, 'w') as file:
                file.writelines(line + '\n' for line in lines)
        except (IOError, PermissionError) as e:
            messagebox.showerror("Error", f"Error writing to file: {e}")
    
    def view_data(self):
        """Display all data in the Treeview."""
        # Clear current display
        for item in self.data_tree.get_children():
            self.data_tree.delete(item)
        
        lines = self.read_data()
        if not lines:
            messagebox.showinfo("Info", "No data found in the file.")
        
        for index, line in enumerate(lines, 1):
            match = re.match(r"Name: (.*), Age: (\d+)", line)
            if match:
                name, age = match.groups()
                self.data_tree.insert("", tk.END, values=(index, name, age))
    
    def delete_data(self):
        """Delete the selected entry."""
        selected = self.data_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select an entry to delete.")
            return
        
        index = int(self.data_tree.item(selected, "values")[0]) - 1
        lines = self.read_data()
        if index < 0 or index >= len(lines):
            messagebox.showerror("Error", "Invalid selection.")
            return
        
        if messagebox.askyesno("Confirm", f"Delete: {lines[index]}?"):
            deleted_line = lines.pop(index)
            self.save_data(lines)
            messagebox.showinfo("Success", f"Deleted: {deleted_line}")
            self.view_data()

if __name__ == '__main__':
    root = tk.Tk()
    app = UserDataManager(root)
    root.mainloop()