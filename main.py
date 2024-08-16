import tkinter as tk
from tkinter import messagebox, Label, Button, Frame
from tkinterdnd2 import TkinterDnD, DND_FILES
from PIL import Image
import os
from tkinter import ttk

class ConvJFIFApp(TkinterDnD.Tk):
    def __init__(self):
        super().__init__()

        self.title("ConvJFIF - JFIF to PNG Converter")
        self.geometry("600x400")

        frame = Frame(self)
        frame.pack(pady=10, fill=tk.BOTH, expand=True)

        self.label = Label(frame, text="Drag and drop JFIF files here or click 'Select Files'")
        self.label.pack(pady=10)

        self.convert_button = Button(frame, text="Convert to PNG", command=self.convert_jfif_to_png, state=tk.DISABLED)
        self.convert_button.pack(pady=10)

        self.drop_target = Label(self, text="\n\n\nDrop JFIF files here", relief="solid", width=60, height=10)
        self.drop_target.pack(pady=10)
        self.drop_target.drop_target_register(DND_FILES)
        self.drop_target.dnd_bind('<<Drop>>', self.on_drop)

        self.file_tree = ttk.Treeview(frame, columns=("filename", "convert"), show="headings", selectmode="none")
        self.file_tree.heading("filename", text="Filename")
        self.file_tree.heading("convert", text="Convert")
        self.file_tree.column("filename", width=400)
        self.file_tree.column("convert", width=100, anchor=tk.CENTER)
        self.file_tree.pack(fill=tk.BOTH, expand=True)

        self.files = []

    def on_drop(self, event):
        files = self.split_files(event.data)
        valid_files = [f for f in files if f.lower().endswith('.jfif')]
        for file in valid_files:
            if file not in self.files:
                self.files.append(file)
                self.file_tree.insert("", "end", values=(os.path.basename(file), "Yes"), tags=("selected",))

        if self.files:
            self.label.config(text=f"{len(self.files)} file(s) ready for conversion")
            self.convert_button.config(state=tk.NORMAL)

    def split_files(self, file_paths):
        return self.tk.splitlist(file_paths)

    def convert_jfif_to_png(self):
        for item in self.file_tree.get_children():
            filename = self.file_tree.item(item, "values")[0]
            convert = self.file_tree.item(item, "values")[1] == "Yes"
            if convert:
                file_path = next((f for f in self.files if os.path.basename(f) == filename), None)
                if file_path:
                    try:
                        img = Image.open(file_path)
                        output_file = os.path.splitext(file_path)[0] + '.png'
                        img.save(output_file, 'PNG')
                    except Exception as e:
                        messagebox.showerror("Error", f"Failed to convert {filename}: {e}")
                        continue

        messagebox.showinfo("Complete", "All selected images have been successfully converted to PNG.")
        self.label.config(text="Drag and drop JFIF files here or click 'Select Files'")
        self.convert_button.config(state=tk.DISABLED)
        self.files.clear()
        self.file_tree.delete(*self.file_tree.get_children())

if __name__ == "__main__":
    app = ConvJFIFApp()
    app.mainloop()
