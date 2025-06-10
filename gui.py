import tkinter as tk
from tkinter import ttk, messagebox
from filesystem import FileSystem
import tkinter.font as tkFont

class FileManagerGUI:
    def __init__(self):
        self.fs = FileSystem()
        self.window = tk.Tk()
        self.window.title("File System Manager")
        self.window.geometry("900x700")
        self.window.configure(bg='#0f1419')
        
        # Tema warna biru
        self.colors = {
            'bg_primary': '#0f1419',      # Dark blue background
            'bg_secondary': '#1e2837',    # Lighter blue
            'bg_tertiary': '#2a3441',     # Card background
            'accent': '#3b82f6',          # Bright blue
            'accent_light': '#60a5fa',    # Light blue
            'text_primary': '#f8fafc',    # White text
            'text_secondary': '#cbd5e1',  # Gray text
            'success': '#10b981',         # Green
            'error': '#ef4444',           # Red
            'warning': '#f59e0b',         # Orange
            'folder': '#3b82f6',          # Blue for folders
            'file': '#94a3b8',            # Gray for files
        }
        
        # Konfigurasi style dengan tema biru
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure ttk styles
        style.configure('Title.TLabel', 
                       font=('Segoe UI', 18, 'bold'),
                       foreground=self.colors['text_primary'],
                       background=self.colors['bg_primary'])
        
        style.configure('Subtitle.TLabel',
                       font=('Segoe UI', 11),
                       foreground=self.colors['text_secondary'],
                       background=self.colors['bg_primary'])
        
        style.configure('Path.TLabel',
                       font=('Segoe UI', 10, 'bold'),
                       foreground=self.colors['accent_light'],
                       background=self.colors['bg_secondary'])
        
        style.configure('Card.TFrame',
                       background=self.colors['bg_tertiary'],
                       relief='flat',
                       borderwidth=1)
        
        style.configure('Main.TFrame',
                       background=self.colors['bg_primary'])
        
        style.configure('Secondary.TFrame',
                       background=self.colors['bg_secondary'])
        
        # Entry style
        style.configure('Modern.TEntry',
                       font=('Consolas', 11),
                       foreground=self.colors['text_primary'],
                       fieldbackground=self.colors['bg_tertiary'],
                       borderwidth=2,
                       relief='flat',
                       insertcolor=self.colors['accent'])
        
        # Main container
        main_container = ttk.Frame(self.window, style='Main.TFrame')
        main_container.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)
        
        # Header section dengan gradient effect
        header_frame = tk.Frame(main_container, 
                               bg=self.colors['bg_secondary'],
                               height=80)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        header_frame.pack_propagate(False)
        
        # Header content
        header_content = tk.Frame(header_frame, bg=self.colors['bg_secondary'])
        header_content.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)
        
        # Title dengan icon
        title_frame = tk.Frame(header_content, bg=self.colors['bg_secondary'])
        title_frame.pack(fill=tk.X)
        
        # Icon (menggunakan Unicode)
        icon_label = tk.Label(title_frame,
                             text="📁",
                             font=('Segoe UI', 24),
                             bg=self.colors['bg_secondary'],
                             fg=self.colors['accent'])
        icon_label.pack(side=tk.LEFT, padx=(0, 15))
        
        # Title text
        title_label = tk.Label(title_frame,
                              text="File System Manager",
                              font=('Segoe UI', 20, 'bold'),
                              bg=self.colors['bg_secondary'],
                              fg=self.colors['text_primary'])
        title_label.pack(side=tk.LEFT, anchor='w')
        
        # Subtitle
        subtitle_label = tk.Label(header_content,
                                 text="Modern file system interface with advanced features",
                                 font=('Segoe UI', 10),
                                 bg=self.colors['bg_secondary'],
                                 fg=self.colors['text_secondary'])
        subtitle_label.pack(anchor='w', pady=(5, 0))
        
        # Content area
        content_frame = ttk.Frame(main_container, style='Main.TFrame')
        content_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=(0, 20))
        
        # Current path card
        path_card = tk.Frame(content_frame,
                            bg=self.colors['bg_tertiary'],
                            relief='flat',
                            bd=1)
        path_card.pack(fill=tk.X, pady=(0, 20))
        
        path_content = tk.Frame(path_card, bg=self.colors['bg_tertiary'])
        path_content.pack(fill=tk.X, padx=20, pady=15)
        
        path_icon = tk.Label(path_content,
                            text="📍",
                            font=('Segoe UI', 14),
                            bg=self.colors['bg_tertiary'],
                            fg=self.colors['accent'])
        path_icon.pack(side=tk.LEFT, padx=(0, 10))
        
        path_label = tk.Label(path_content,
                             text="Current Path:",
                             font=('Segoe UI', 11),
                             bg=self.colors['bg_tertiary'],
                             fg=self.colors['text_secondary'])
        path_label.pack(side=tk.LEFT, padx=(0, 10))
        
        self.pwd_label = tk.Label(path_content,
                                 text="/root",
                                 font=('Consolas', 11, 'bold'),
                                 bg=self.colors['bg_tertiary'],
                                 fg=self.colors['accent_light'])
        self.pwd_label.pack(side=tk.LEFT)
        
        # Command input card
        cmd_card = tk.Frame(content_frame,
                           bg=self.colors['bg_tertiary'],
                           relief='flat',
                           bd=1)
        cmd_card.pack(fill=tk.X, pady=(0, 20))
        
        cmd_content = tk.Frame(cmd_card, bg=self.colors['bg_tertiary'])
        cmd_content.pack(fill=tk.X, padx=20, pady=15)
        
        cmd_icon = tk.Label(cmd_content,
                           text="⚡",
                           font=('Segoe UI', 14),
                           bg=self.colors['bg_tertiary'],
                           fg=self.colors['accent'])
        cmd_icon.pack(side=tk.LEFT, padx=(0, 10))
        
        cmd_label = tk.Label(cmd_content,
                            text="Enter command:",
                            font=('Segoe UI', 11),
                            bg=self.colors['bg_tertiary'],
                            fg=self.colors['text_secondary'])
        cmd_label.pack(side=tk.LEFT, padx=(0, 15))
        
        # Custom entry with border effect
        entry_frame = tk.Frame(cmd_content, bg=self.colors['bg_tertiary'])
        entry_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        self.command_entry = tk.Entry(entry_frame,
                                     font=('Consolas', 11),
                                     bg=self.colors['bg_primary'],
                                     fg=self.colors['text_primary'],
                                     insertbackground=self.colors['accent'],
                                     relief='flat',
                                     bd=2,
                                     highlightthickness=2,
                                     highlightcolor=self.colors['accent'],
                                     highlightbackground=self.colors['bg_secondary'])
        self.command_entry.pack(fill=tk.X, ipady=8, ipadx=10)
        
        # Output area
        output_card = tk.Frame(content_frame,
                              bg=self.colors['bg_tertiary'],
                              relief='flat',
                              bd=1)
        output_card.pack(fill=tk.BOTH, expand=True)
        
        # Output header
        output_header = tk.Frame(output_card, bg=self.colors['bg_tertiary'])
        output_header.pack(fill=tk.X, padx=20, pady=(15, 0))
        
        output_icon = tk.Label(output_header,
                              text="💻",
                              font=('Segoe UI', 14),
                              bg=self.colors['bg_tertiary'],
                              fg=self.colors['accent'])
        output_icon.pack(side=tk.LEFT, padx=(0, 10))
        
        output_title = tk.Label(output_header,
                               text="Terminal Output",
                               font=('Segoe UI', 11, 'bold'),
                               bg=self.colors['bg_tertiary'],
                               fg=self.colors['text_primary'])
        output_title.pack(side=tk.LEFT)
        
        # Output text area
        output_frame = tk.Frame(output_card, bg=self.colors['bg_tertiary'])
        output_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(10, 20))
        
        self.output = tk.Text(output_frame,
                            font=('Consolas', 10),
                            wrap=tk.WORD,
                            bg=self.colors['bg_primary'],
                            fg=self.colors['text_primary'],
                            insertbackground=self.colors['accent'],
                            selectbackground=self.colors['accent'],
                            selectforeground=self.colors['text_primary'],
                            relief='flat',
                            padx=15,
                            pady=15,
                            spacing1=2,
                            spacing2=2,
                            spacing3=2)
        self.output.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Scrollbar dengan style kustom
        scrollbar = tk.Scrollbar(output_frame,
                               orient=tk.VERTICAL,
                               command=self.output.yview,
                               bg=self.colors['bg_secondary'],
                               troughcolor=self.colors['bg_primary'],
                               activebackground=self.colors['accent'],
                               width=12)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.output.configure(yscrollcommand=scrollbar.set)
        
        # Configure text tags dengan warna tema biru
        self.output.tag_configure('command', 
                                 foreground=self.colors['accent_light'], 
                                 font=('Consolas', 10, 'bold'))
        self.output.tag_configure('success', 
                                 foreground=self.colors['success'],
                                 font=('Consolas', 10, 'bold'))
        self.output.tag_configure('error', 
                                 foreground=self.colors['error'],
                                 font=('Consolas', 10, 'bold'))
        self.output.tag_configure('warning',
                                 foreground=self.colors['warning'])
        self.output.tag_configure('folder', 
                                 foreground=self.colors['folder'],
                                 font=('Consolas', 10, 'bold'))
        self.output.tag_configure('file', 
                                 foreground=self.colors['file'])
        self.output.tag_configure('prompt',
                                 foreground=self.colors['accent'],
                                 font=('Consolas', 10, 'bold'))
        self.output.tag_configure('info',
                                 foreground=self.colors['text_secondary'])
        
        # Welcome message
        self.show_welcome_message()
        
        # Bind events
        self.command_entry.bind("<Return>", self.execute_command)
        self.command_entry.bind("<Up>", self.show_previous_command)
        self.command_entry.bind("<Down>", self.show_next_command)
        self.command_entry.focus_set()
        
        # Command history
        self.command_history = []
        self.current_history_index = -1
        
        # Hover effects
        self.setup_hover_effects()

    def setup_hover_effects(self):
        """Setup hover effects untuk elemen interaktif"""
        def on_enter(event):
            event.widget.configure(highlightcolor=self.colors['accent_light'])
        
        def on_leave(event):
            event.widget.configure(highlightcolor=self.colors['accent'])
        
        self.command_entry.bind("<Enter>", on_enter)
        self.command_entry.bind("<Leave>", on_leave)

    def show_welcome_message(self):
        """Tampilkan pesan selamat datang dengan styling yang menarik"""
        welcome_text = f"""╭─────────────────────────────────────────────────────────────────────╮
│                    🎉 Welcome to File System Manager! 🎉                │
╰─────────────────────────────────────────────────────────────────────╯

"""
        
        help_text = """💡 AVAILABLE COMMANDS:

📁 mkdir "<folder_name>"      → Create a new folder
📄 touch "<file_name>"        → Create a new file  
📋 ls [-r|-R] [folder_name]   → List directory contents
   Options: -r or -R for recursive listing
🚶 cd "<folder_name>"         → Change directory (use .. to go back)
❌ rm "<name>"                → Remove file or folder
👀 cat "<file_name>"          → View file contents
✏️  write "<file_name>" <content> → Write content to file
📍 pwd                        → Show current directory path
🧹 clear                      → Clear terminal screen
❓ help                       → Show this help message

💡 TIP: Use quotes (") for names containing spaces
🎯 Use ↑/↓ arrow keys to navigate command history

"""
        
        # Insert welcome message
        self.output.insert(tk.END, welcome_text, 'success')
        self.output.insert(tk.END, help_text, 'info')
        self.output.insert(tk.END, "Ready to use! Type a command below:\n\n", 'command')

    def show_previous_command(self, event):
        if self.command_history:
            if self.current_history_index < len(self.command_history) - 1:
                self.current_history_index += 1
                self.command_entry.delete(0, tk.END)
                self.command_entry.insert(0, self.command_history[-(self.current_history_index + 1)])
        return "break"
    
    def show_next_command(self, event):
        if self.command_history:
            if self.current_history_index > 0:
                self.current_history_index -= 1
                self.command_entry.delete(0, tk.END)
                self.command_entry.insert(0, self.command_history[-(self.current_history_index + 1)])
            elif self.current_history_index == 0:
                self.current_history_index = -1
                self.command_entry.delete(0, tk.END)
        return "break"

    def execute_command(self, event):
        cmd = self.command_entry.get().strip()
        if not cmd:
            return

        # Simpan command ke history
        self.command_history.append(cmd)
        self.current_history_index = -1

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
        
        # Tampilkan command dengan style yang menarik
        self.output.insert(tk.END, f"┌─ ", 'prompt')
        self.output.insert(tk.END, f"/{self.fs.pwd()}", 'info')
        self.output.insert(tk.END, f"\n└─❯ ", 'prompt')
        self.output.insert(tk.END, f"{cmd}\n", 'command')
        
        result = "❌ Command not recognized. Type 'help' for available commands."
        tag = 'error'
        
        if command == "mkdir" and len(parts) > 1:
            result = self.fs.mkdir(parts[1])
            tag = 'success' if "berhasil" in result else 'error'
            if "berhasil" in result:
                result = f"✅ {result}"
            else:
                result = f"❌ {result}"
                
        elif command == "touch" and len(parts) > 1:
            result = self.fs.touch(parts[1])
            tag = 'success' if "berhasil" in result else 'error'
            if "berhasil" in result:
                result = f"✅ {result}"
            else:
                result = f"❌ {result}"
                
        elif command == "ls":
            recursive = False
            target_folder = None
            
            for i in range(1, len(parts)):
                if parts[i] in ['-r', '-R', '--recursive']:
                    recursive = True
                elif not parts[i].startswith('-'):
                    target_folder = parts[i]
            
            if target_folder:
                node = self.fs.current_node
                if target_folder in node.children and node.children[target_folder].is_folder:
                    temp_node = self.fs.current_node
                    self.fs.current_node = node.children[target_folder]
                    result = self.fs.ls(recursive)
                    self.fs.current_node = temp_node
                    tag = 'info'
                else:
                    result = f"❌ Folder '{target_folder}' tidak ditemukan"
                    tag = 'error'
            else:
                result = self.fs.ls(recursive)
                tag = 'info'
                
        elif command == "cd" and len(parts) > 1:
            result = self.fs.cd(parts[1])
            tag = 'success' if "Pindah" in result else 'error'
            if "Pindah" in result:
                result = f"✅ {result}"
                self.pwd_label.config(text="/" + self.fs.pwd())
            else:
                result = f"❌ {result}"
                
        elif command == "rm" and len(parts) > 1:
            result = self.fs.rm(parts[1])
            tag = 'success' if "berhasil" in result else 'error'
            if "berhasil" in result:
                result = f"✅ {result}"
            else:
                result = f"❌ {result}"
                
        elif command == "cat" and len(parts) > 1:
            result = self.fs.cat(parts[1])
            tag = 'file' if not "tidak ditemukan" in result else 'error'
            if "tidak ditemukan" in result:
                result = f"❌ {result}"
            else:
                result = f"📄 File contents:\n{result}"
                
        elif command == "write" and len(parts) > 2:
            content = " ".join(parts[2:])
            result = self.fs.write(parts[1], content)
            tag = 'success' if "Berhasil" in result else 'error'
            if "Berhasil" in result:
                result = f"✅ {result}"
            else:
                result = f"❌ {result}"
                
        elif command == "pwd":
            result = f"📍 Current path: /{self.fs.pwd()}"
            tag = 'info'
            
        elif command == "clear":
            self.output.delete(1.0, tk.END)
            self.show_welcome_message()
            self.command_entry.delete(0, tk.END)
            return
            
        elif command == "help":
            self.output.delete(1.0, tk.END)
            self.show_welcome_message()
            self.command_entry.delete(0, tk.END)
            return

        # Tampilkan hasil dengan formatting yang lebih baik
        if command == "ls" and tag == 'info':
            # Special handling untuk ls output
            lines = result.split('\n')
            for line in lines:
                if line.strip():
                    if line.startswith('📁'):
                        self.output.insert(tk.END, f"{line}\n", 'folder')
                    elif line.startswith('📄'):
                        self.output.insert(tk.END, f"{line}\n", 'file')
                    else:
                        self.output.insert(tk.END, f"{line}\n", 'info')
        else:
            self.output.insert(tk.END, f"{result}\n", tag)
        
        self.output.insert(tk.END, "\n")
        self.output.see(tk.END)
        self.command_entry.delete(0, tk.END)

    def run(self):
        self.window.mainloop()