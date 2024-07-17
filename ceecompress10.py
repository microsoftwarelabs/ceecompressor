import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pyzipper
import os
import shutil

class CEEFileManager:

    def __init__(self, root):
        self.root = root
        self.root.title("CEE File Manager")
        self.file_path = ""
        self.zip_file = None  # Variável para armazenar o objeto zip aberto

        # Create menu
        self.menu = tk.Menu(self.root)
        self.root.config(menu=self.menu)

        self.file_menu = tk.Menu(self.menu)
        self.menu.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="New", command=self.new_file)
        self.file_menu.add_command(label="Open", command=self.open_file)
        self.file_menu.add_command(label="Save", command=self.save_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.root.quit)

        self.edit_menu = tk.Menu(self.menu)
        self.menu.add_cascade(label="Edit", menu=self.edit_menu)
        self.edit_menu.add_command(label="Add Content", command=self.add_content)
        self.edit_menu.add_command(label="Edit Content", command=self.edit_content)

        self.view_menu = tk.Menu(self.menu)
        self.menu.add_cascade(label="View", menu=self.view_menu)
        self.view_menu.add_command(label="View Files and Folders", command=self.view_files_and_folders)
        self.view_menu.add_command(label="View Text Content", command=self.view_text_content)

        # Create buttons
        self.compress_button = tk.Button(self.root, text="Compress", command=self.compress_file)
        self.compress_button.pack()

        self.extract_button = tk.Button(self.root, text="Extract", command=self.extract_file)
        self.extract_button.pack()

        # Create treeview for file and folder view
        self.tree = ttk.Treeview(self.root, columns=("size"))
        self.tree.heading("#0", text="Files and Folders")
        self.tree.heading("size", text="Size (bytes)")
        self.tree.pack()

        # Create text area
        self.text_area = tk.Text(self.root)
        self.text_area.pack()

    def new_file(self):
        self.file_path = filedialog.asksaveasfilename(filetypes=[("CEE files", "*.cee")], defaultextension=".cee")
        if self.file_path:
            # Criar um novo arquivo zip com AESZipFile
            self.zip_file = pyzipper.AESZipFile(self.file_path, 'w', compression=pyzipper.ZIP_LZMA)
            self.update_treeview()
            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(tk.END, "New file created: " + self.file_path)

    def open_file(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("CEE files", "*.cee")])
        if self.file_path:
            try:
                self.zip_file = pyzipper.AESZipFile(self.file_path, 'r')
                self.update_treeview()
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(tk.END, "File opened: " + self.file_path)
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def save_file(self):
        if self.zip_file:
            try:
                # Atualiza o conteúdo no arquivo zip antes de salvar
                with self.zip_file.open(os.path.basename(self.file_path)[:-4], 'w') as f:
                    f.write(self.text_area.get(1.0, tk.END).encode())
                self.zip_file.close()
                self.zip_file = None
                messagebox.showinfo("Success", "File saved and compressed successfully")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def compress_files(directory, output_file):
    output_file = output_file + '.cee'  # Add.cee extension to output file
    temp_file = tempfile.NamedTemporaryFile(suffix='.zip', delete=False)
    with zipfile.ZipFile(temp_file.name, mode="w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for root, dirs, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, directory)
                archive.write(file_path, arcname)

    for _ in range(56):  # Loop compression 56 more times
        with zipfile.ZipFile(temp_file.name, mode="r") as input_archive:
            temp_file_tmp = tempfile.NamedTemporaryFile(suffix='.zip', delete=False)
            with zipfile.ZipFile(temp_file_tmp.name, mode="w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as output_archive:
                for item in input_archive.infolist():
                    output_archive.writestr(item, input_archive.read(item.filename))
        os.replace(temp_file_tmp.name, temp_file.name)
                messagebox.showinfo("Success", "File compressed successfully")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def add_content(self):
        files = filedialog.askopenfilenames(filetypes=[("All files", "*.*")])
        if files:
            for file in files:
                try:
                    with open(file, 'r', encoding='latin-1') as f:
                        content = f.read()
                        self.text_area.insert(tk.END, content)
                except Exception as e:
                    messagebox.showerror("Error", str(e))



    def edit_content(self):
        if self.file_path:
            edit_window = tk.Toplevel(self.root)
            edit_window.title("Edit Content")

            copy_button = tk.Button(edit_window, text="Copy", command=lambda: self.copy_file_to_directory(self.file_path))
            copy_button.pack()

            extract_button = tk.Button(edit_window, text="Extract", command=lambda: self.extract_file_to_directory(self.file_path))
            extract_button.pack()

            delete_button = tk.Button(edit_window, text="Delete", command=lambda: self.delete_file_from_archive(self.file_path))
            delete_button.pack()

    def copy_file_to_directory(self, file_path):
        destination = filedialog.askdirectory()
        if destination:
            try:
                with pyzipper.AESZipFile(self.file_path, 'r') as zip_file:
                    zip_file.extract(file_path, destination)
                messagebox.showinfo("Success", "File copied successfully")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def extract_file_to_directory(self, file_path):
        destination = filedialog.askdirectory()
        if destination:
            try:
                with pyzipper.AESZipFile(file_path, 'r') as zip_file:
                    zip_file.extractall(destination)
                messagebox.showinfo("Success", "File extracted successfully")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def delete_file_from_archive(self, file_path):
        if messagebox.askyesno("Confirm", "Are you sure you want to delete the file?"):
            try:
                with pyzipper.AESZipFile(self.file_path, 'w') as zip_file:
                    zip_file.remove(file_path)
                messagebox.showinfo("Success", "File deleted successfully")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def view_files_and_folders(self):
        if self.zip_file:
            try:
                self.tree.delete(*self.tree.get_children())
                for file in self.zip_file.filelist:
                    size_bytes = file.file_size
                    self.tree.insert('', 'end', text=file.filename, values=(size_bytes,))
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def view_text_content(self):
        if self.zip_file:
            try:
                self.text_area.delete(1.0, tk.END)
                for file in self.zip_file.filelist:
                    if self.is_text_file(file):
                        with self.zip_file.open(file.filename, 'r') as f:
                            content = f.read().decode()
                            self.text_area.insert(tk.END, content)
                            self.text_area.insert(tk.END, "\n---\n")  # Separador entre arquivos
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def is_text_file(self, file):
        # Verifica se o tipo de arquivo é compatível com texto (pode ser ajustado conforme necessário)
        text_extensions = ['.txt', '.py', '.c', '.cpp', '.java', '.html', '.css', '.js']
        file_ext = os.path.splitext(file.filename)[1].lower()
        return file_ext in text_extensions

    def update_treeview(self):
        if self.zip_file:  
            try:
                self.tree.delete(*self.tree.get_children())
                for file in self.zip_file.filelist:
                    size_bytes = file.file_size
                    self.tree.insert('', 'end', text=file.filename, values=(size_bytes,))
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def extract_file(self):
        if self.file_path:
            try:
                self.zip_file = pyzipper.AESZipFile(self.file_path, 'r')
                self.update_treeview()
                messagebox.showinfo("Success", "File extracted successfully")
            except Exception as e:
                messagebox.showerror("Error", str(e))


root = tk.Tk()
app = CEEFileManager(root)
root.mainloop()
