import tkinter as tk
from tkinter import filedialog, messagebox
import os, shutil

class MP3Organizer:
    def __init__(self, root):
        self.root = root
        self.root.title("MP3 Organizer")
        self.root.geometry("450x350")

        self.listbox = tk.Listbox(root, selectmode=tk.SINGLE, font=("Arial", 12))
        self.listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        btn_frame = tk.Frame(root)
        btn_frame.pack(fill=tk.X, pady=5)

        tk.Button(btn_frame, text="Load Source", command=self.load_source).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Select SD", command=self.select_destination).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="↑ Up", command=self.move_up).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="↓ Down", command=self.move_down).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Save to SD", command=self.save_order).pack(side=tk.RIGHT, padx=5)

        self.source_folder = None
        self.dest_folder = None
        self.files = []

    def load_source(self):
        self.source_folder = filedialog.askdirectory(title="Select Source Folder")
        if not self.source_folder:
            return
        self.files = [f for f in os.listdir(self.source_folder) if f.lower().endswith(".mp3")]
        self.files.sort()
        self.refresh_list()

    def select_destination(self):
        self.dest_folder = filedialog.askdirectory(title="Select Destination (SD Card)")
        if self.dest_folder:
            messagebox.showinfo("Destination Selected", f"SD card folder:\n{self.dest_folder}")

    def refresh_list(self):
        self.listbox.delete(0, tk.END)
        for f in self.files:
            self.listbox.insert(tk.END, f)

    def move_up(self):
        idx = self.listbox.curselection()
        if not idx: return
        i = idx[0]
        if i > 0:
            self.files[i], self.files[i-1] = self.files[i-1], self.files[i]
            self.refresh_list()
            self.listbox.select_set(i-1)

    def move_down(self):
        idx = self.listbox.curselection()
        if not idx: return
        i = idx[0]
        if i < len(self.files)-1:
            self.files[i], self.files[i+1] = self.files[i+1], self.files[i]
            self.refresh_list()
            self.listbox.select_set(i+1)

    def save_order(self):
        if not self.source_folder or not self.files:
            messagebox.showerror("Error", "No source files loaded!")
            return
        if not self.dest_folder:
            messagebox.showerror("Error", "No destination (SD card) selected!")
            return

        for f in os.listdir(self.dest_folder):
            if f.lower().endswith(".mp3"):
                os.remove(os.path.join(self.dest_folder, f))

        for i, f in enumerate(self.files, start=1):
            newname = f"{i:04}.mp3"  
            src = os.path.join(self.source_folder, f)
            dst = os.path.join(self.dest_folder, newname)
            shutil.copy2(src, dst)

        messagebox.showinfo("Done", "Songs copied and renamed on SD card!")

if __name__ == "__main__":
    root = tk.Tk()
    app = MP3Organizer(root)
    root.mainloop()
