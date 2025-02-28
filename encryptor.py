import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox, ttk, Toplevel
import pyzipper
import os
import shutil
import logging

# Set up logging
logging.basicConfig(filename='encryptor.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

class EncryptorApp(tk.Tk):
    """Main application class for the file/folder encryptor GUI."""
    def __init__(self):
        super().__init__()
        self.title("Advanced File/Folder Encryptor")
        self.geometry("400x250")
        self.status_var = tk.StringVar(value="Ready")
        self._setup_ui()
        self._setup_menu()

    def _setup_ui(self):
        """Initialize the GUI components."""
        title_label = tk.Label(self, text="Advanced File/Folder Encryptor", font=("Helvetica", 16, "bold"))
        title_label.pack(pady=10)

        button_frame = ttk.Frame(self)
        button_frame.pack(pady=10)
        style = ttk.Style()
        style.configure("TButton", font=("Helvetica", 12))

        self.encrypt_file_btn = ttk.Button(button_frame, text="Encrypt File", command=self.encrypt_file, width=20)
        self.encrypt_file_btn.pack(pady=5)
        self.create_tooltip(self.encrypt_file_btn, "Encrypt a single file with password protection")

        self.encrypt_folder_btn = ttk.Button(button_frame, text="Encrypt Folder", command=self.encrypt_folder, width=20)
        self.encrypt_folder_btn.pack(pady=5)
        self.create_tooltip(self.encrypt_folder_btn, "Encrypt an entire folder with password protection")

        self.decrypt_btn = ttk.Button(button_frame, text="Decrypt", command=self.decrypt, width=20)
        self.decrypt_btn.pack(pady=5)
        self.create_tooltip(self.decrypt_btn, "Decrypt an encrypted file or folder")

        status_label = ttk.Label(self, textvariable=self.status_var, relief="sunken", anchor="w")
        status_label.pack(side="bottom", fill="x")

    def _setup_menu(self):
        """Set up the help menu."""
        menubar = tk.Menu(self)
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="Help", command=self.show_help)
        menubar.add_cascade(label="Help", menu=help_menu)
        self.config(menu=menubar)

    def encrypt_file(self):
        """Encrypt a single file."""
        self.status_var.set("Encrypting file...")
        self.update()
        file_path = filedialog.askopenfilename()
        if not file_path:
            self.status_var.set("Ready")
            return
        output_dir = filedialog.askdirectory(title="Select Output Directory")
        if not output_dir:
            self.status_var.set("Ready")
            return
        password = simpledialog.askstring("Password", "Enter password for encryption:", show="*")
        if not password:
            messagebox.showerror("Error", "Password cannot be empty")
            self.status_var.set("Ready")
            return

        progress_win, progress_bar = self.show_progress_window("Encrypting")
        try:
            zip_name = os.path.basename(file_path) + ".enc.zip"
            zip_path = os.path.join(output_dir, zip_name)

            with pyzipper.AESZipFile(zip_path, 'w', compression=pyzipper.ZIP_LZMA, encryption=pyzipper.WZ_AES) as zf:
                zf.setpassword(password.encode())
                zf.write(file_path, arcname=os.path.basename(file_path))

            with pyzipper.AESZipFile(zip_path) as zf:
                zf.setpassword(password.encode())
                zf.testzip()

            os.remove(file_path)
            logging.info(f"Deleted original file: {file_path}")

            encrypted_size = os.path.getsize(zip_path) / 1024  # Size in KB
            progress_bar.stop()
            progress_win.destroy()
            messagebox.showinfo("Success", 
                                f"File encrypted successfully!\n"
                                f"Encrypted size: {self.format_size(encrypted_size)}\n"
                                f"Saved to: {zip_path}")
            logging.info(f"Encrypted file: {file_path} to {zip_path}")
            self.status_var.set("Encryption complete")
        except Exception as e:
            progress_bar.stop()
            progress_win.destroy()
            messagebox.showerror("Error", f"Encryption failed: {str(e)}")
            logging.error(f"Encryption failed for {file_path}: {str(e)}")
            self.status_var.set("Encryption failed")

    def encrypt_folder(self):
        """Encrypt a folder, preserving structure including empty directories."""
        self.status_var.set("Encrypting folder...")
        self.update()
        folder_path = filedialog.askdirectory()
        if not folder_path:
            self.status_var.set("Ready")
            return
        output_dir = filedialog.askdirectory(title="Select Output Directory")
        if not output_dir:
            self.status_var.set("Ready")
            return
        password = simpledialog.askstring("Password", "Enter password for encryption:", show="*")
        if not password:
            messagebox.showerror("Error", "Password cannot be empty")
            self.status_var.set("Ready")
            return

        progress_win, progress_bar = self.show_progress_window("Encrypting")
        try:
            zip_name = os.path.basename(folder_path) + ".enc.zip"
            zip_path = os.path.join(output_dir, zip_name)

            with pyzipper.AESZipFile(zip_path, 'w', compression=pyzipper.ZIP_LZMA, encryption=pyzipper.WZ_AES) as zf:
                zf.setpassword(password.encode())
                for root, dirs, files in os.walk(folder_path):
                    # Add directory entries
                    for dir in dirs:
                        dir_path = os.path.join(root, dir)
                        arcname = os.path.join(os.path.basename(folder_path), os.path.relpath(dir_path, folder_path)) + '/'
                        zf.writestr(arcname, '')
                    # Add files
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.join(os.path.basename(folder_path), os.path.relpath(file_path, folder_path))
                        zf.write(file_path, arcname=arcname)

            with pyzipper.AESZipFile(zip_path) as zf:
                zf.setpassword(password.encode())
                zf.testzip()

            shutil.rmtree(folder_path)
            logging.info(f"Deleted original folder: {folder_path}")

            encrypted_size = os.path.getsize(zip_path) / 1024  # Size in KB
            progress_bar.stop()
            progress_win.destroy()
            messagebox.showinfo("Success", 
                                f"Folder encrypted successfully!\n"
                                f"Encrypted size: {self.format_size(encrypted_size)}\n"
                                f"Saved to: {zip_path}")
            logging.info(f"Encrypted folder: {folder_path} to {zip_path}")
            self.status_var.set("Encryption complete")
        except Exception as e:
            progress_bar.stop()
            progress_win.destroy()
            messagebox.showerror("Error", f"Encryption failed: {str(e)}")
            logging.error(f"Encryption failed for {folder_path}: {str(e)}")
            self.status_var.set("Encryption failed")

    def decrypt(self):
        """Decrypt an encrypted ZIP file with attempt tracking."""
        self.status_var.set("Decrypting...")
        self.update()
        zip_path = filedialog.askopenfilename(filetypes=[("Encrypted ZIP", "*.enc.zip")])
        if not zip_path:
            self.status_var.set("Ready")
            return
        output_dir = filedialog.askdirectory(title="Select Output Directory")
        if not output_dir:
            self.status_var.set("Ready")
            return

        attempts = 0
        max_attempts = 5
        while attempts < max_attempts:
            password = simpledialog.askstring("Password", "Enter password for decryption:", show="*")
            if password is None:
                self.status_var.set("Ready")
                break
            progress_win, progress_bar = self.show_progress_window("Decrypting")
            try:
                with pyzipper.AESZipFile(zip_path) as zf:
                    zf.setpassword(password.encode())
                    zf.extractall(path=output_dir)
                progress_bar.stop()
                progress_win.destroy()
                messagebox.showinfo("Success", f"Decryption successful! Extracted to: {output_dir}")
                logging.info(f"Decrypted {zip_path}")
                self.status_var.set("Decryption successful")
                return
            except RuntimeError:
                attempts += 1
                progress_bar.stop()
                progress_win.destroy()
                messagebox.showerror("Error", f"Incorrect password. Attempts left: {max_attempts - attempts}")
        if attempts == max_attempts:
            downloads_dir = os.path.join(os.path.expanduser("~"), "Downloads")
            new_folder = os.path.join(downloads_dir, "new_folder")
            if not os.path.exists(new_folder):
                os.makedirs(new_folder)
            shutil.move(zip_path, new_folder)
            messagebox.showinfo("Warning", "You entered password wrong too many times, file moved and hidden.")
            logging.info(f"Moved {zip_path} to {new_folder} after {max_attempts} failed attempts")
            self.status_var.set("File moved after failed attempts")

    @staticmethod
    def format_size(size_kb):
        """Format size in KB to a human-readable string."""
        if size_kb < 1024:
            return f"{size_kb:.2f} KB"
        size_mb = size_kb / 1024
        return f"{size_mb:.2f} MB"

    def show_progress_window(self, operation):
        """Create and return a progress window with a bar."""
        progress_win = Toplevel(self)
        progress_win.title(f"{operation} in Progress")
        progress_win.geometry("300x100")
        progress_win.transient(self)
        progress_win.grab_set()
        tk.Label(progress_win, text=f"{operation}...").pack(pady=10)
        progress_bar = ttk.Progressbar(progress_win, mode='indeterminate')
        progress_bar.pack(pady=10)
        progress_bar.start()
        return progress_win, progress_bar

    def create_tooltip(self, widget, text):
        """Create a tooltip for a widget."""
        tooltip = None
        def enter(event):
            nonlocal tooltip
            x, y, _, _ = widget.bbox("insert")
            x += widget.winfo_rootx() + 25
            y += widget.winfo_rooty() + 25
            tooltip = Toplevel(widget)
            tooltip.wm_overrideredirect(True)
            tooltip.wm_geometry(f"+{x}+{y}")
            label = tk.Label(tooltip, text=text, background="yellow", relief="solid", borderwidth=1)
            label.pack()
        def leave(event):
            nonlocal tooltip
            if tooltip:
                tooltip.destroy()
                tooltip = None
        widget.bind("<Enter>", enter)
        widget.bind("<Leave>", leave)

    def show_help(self):
        """Show help instructions."""
        messagebox.showinfo("Help", "This tool allows you to encrypt and decrypt files and folders with password protection.\n\n"
                                    "Instructions:\n"
                                    "- To encrypt a file or folder, select the corresponding button and follow the prompts.\n"
                                    "- To decrypt, select the encrypted ZIP file and enter the correct password.\n"
                                    "- After 5 failed decryption attempts, the file will be moved to a 'new_folder' in your Downloads directory.")

if __name__ == "__main__":
    app = EncryptorApp()
    app.mainloop()