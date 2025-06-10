import tkinter as tk
from tkinter import ttk, messagebox
from filesystem import FileSystem

class FileManagerGUI:
    def __init__(self):
        self.fs = FileSystem()
        self.window = tk.Tk()
        self.window.title("Simulasi Manajemen File")
        self.window.geometry("600x400")

        # Menambahkan label untuk menampilkan current directory
        self.pwd_label = tk.Label(self.window, text="/root")
        self.pwd_label.pack(fill=tk.X)

        self.command_entry = tk.Entry(self.window)
        self.command_entry.pack(fill=tk.X)

        self.output = tk.Text(self.window, height=20)
        self.output.pack(fill=tk.BOTH, expand=True)

        # Menambahkan help text
        help_text = """Perintah yang tersedia:
- mkdir <nama_folder> : membuat folder baru
- touch <nama_file> : membuat file baru
- ls : melihat isi direktori
- cd <nama_folder> : pindah ke direktori (cd .. untuk kembali)
- rm <nama> : hapus file atau folder
- cat <nama_file> : lihat isi file
- write <nama_file> <isi> : tulis ke file
- pwd : lihat direktori saat ini
- clear : bersihkan layar output
- help : tampilkan bantuan"""
        
        self.output.insert(tk.END, help_text + "\n\n")
        self.command_entry.bind("<Return>", self.execute_command)

    def execute_command(self, event):
        cmd = self.command_entry.get().strip()
        if not cmd:
            return

        # Parse command dengan mempertimbangkan tanda kutip
        parts = []
        current_part = []
        in_quotes = False
        
        for char in cmd:
            if char == '"':
                in_quotes = not in_quotes
            elif char == ' ' and not in_quotes:
                if current_part:
                    parts.append(''.join(current_part))
                    current_part = []
            else:
                current_part.append(char)
        
        if current_part:
            parts.append(''.join(current_part))

        if not parts:
            return

        command = parts[0].lower()
        
        result = "Perintah tidak dikenal. Ketik 'help' untuk bantuan."
        
        if command == "mkdir" and len(parts) > 1:
            result = self.fs.mkdir(parts[1])
        elif command == "touch" and len(parts) > 1:
            result = self.fs.touch(parts[1])
        elif command == "ls":
            recursive = False
            target_folder = None
            
            # Parse opsi ls
            for i in range(1, len(parts)):
                if parts[i] in ['-r', '-R', '--recursive']:
                    recursive = True
                elif not parts[i].startswith('-'):
                    target_folder = parts[i]
            
            if target_folder:
                # Jika ada argument untuk ls, cek folder tersebut
                node = self.fs.current_node
                if target_folder in node.children and node.children[target_folder].is_folder:
                    temp_node = self.fs.current_node
                    self.fs.current_node = node.children[target_folder]
                    result = self.fs.ls(recursive)
                    self.fs.current_node = temp_node
                else:
                    result = f"Folder '{target_folder}' tidak ditemukan"
            else:
                result = self.fs.ls(recursive)
        elif command == "cd" and len(parts) > 1:
            result = self.fs.cd(parts[1])
            self.pwd_label.config(text="/" + self.fs.pwd())
        elif command == "rm" and len(parts) > 1:
            result = self.fs.rm(parts[1])
        elif command == "cat" and len(parts) > 1:
            result = self.fs.cat(parts[1])
        elif command == "write" and len(parts) > 2:
            content = " ".join(parts[2:])
            result = self.fs.write(parts[1], content)
        elif command == "pwd":
            result = "/" + self.fs.pwd()
        elif command == "clear":
            self.output.delete(1.0, tk.END)
            return
        elif command == "help":
            help_text = """Perintah yang tersedia:
- mkdir "<nama_folder>" : membuat folder baru
- touch "<nama_file>" : membuat file baru
- ls [-r|-R] [nama_folder] : melihat isi direktori
  Opsi:
  -r atau -R : tampilkan isi subfolder secara rekursif
- cd "<nama_folder>" : pindah ke direktori (cd .. untuk kembali)
- rm "<nama>" : hapus file atau folder
- cat "<nama_file>" : lihat isi file
- write "<nama_file>" <isi> : tulis ke file
- pwd : lihat direktori saat ini
- clear : bersihkan layar output
- help : tampilkan bantuan

Catatan: Gunakan tanda kutip (") untuk nama file/folder yang mengandung spasi"""
            self.output.insert(tk.END, help_text + "\n\n")
            return

        self.output.insert(tk.END, f"> {cmd}\n{result}\n\n")
        self.output.see(tk.END)
        self.command_entry.delete(0, tk.END)

    def run(self):
        self.window.mainloop()
