"""
GUI Interface untuk File System Simulator
Menggunakan Tkinter untuk antarmuka grafis
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from tkinter import font as tkFont
import threading
from typing import List, Dict, Optional
from filesystem import FileSystem

class FileManagerGUI:
    """Main GUI class untuk File Manager"""
    
    def __init__(self, file_system: FileSystem):
        self.fs = file_system
        self.root = tk.Tk()
        self.setup_window()
        self.create_widgets()
        self.update_display()
        
    def setup_window(self):
        """Setup main window properties"""
        self.root.title("🖥️ Simulator Sistem Manajemen File")
        self.root.geometry("1400x900")
        self.root.minsize(1200, 700)
        
        # Set colors and theme
        self.colors = {
            'bg_primary': '#2c3e50',
            'bg_secondary': '#34495e',
            'accent': '#3498db',
            'success': '#27ae60',
            'warning': '#f39c12',
            'danger': '#e74c3c',
            'text': '#ecf0f1',
            'text_secondary': '#bdc3c7'
        }
        
        self.root.configure(bg=self.colors['bg_primary'])
        
        # Configure styles
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.configure_styles()
    
    def configure_styles(self):
        """Configure custom styles"""
        # Frame styles
        self.style.configure('Primary.TFrame', background=self.colors['bg_primary'])
        self.style.configure('Secondary.TFrame', background=self.colors['bg_secondary'])
        
        # Label styles
        self.style.configure('Title.TLabel', 
                           background=self.colors['bg_primary'],
                           foreground=self.colors['text'],
                           font=('Arial', 16, 'bold'))
        
        self.style.configure('Info.TLabel',
                           background=self.colors['bg_secondary'],
                           foreground=self.colors['text'],
                           font=('Arial', 10))
        
        # Button styles
        self.style.configure('Action.TButton',
                           font=('Arial', 10, 'bold'))
        
        # Treeview styles
        self.style.configure('Custom.Treeview',
                           background='#34495e',
                           foreground='#ecf0f1',
                           fieldbackground='#34495e',
                           font=('Courier New', 10))
        
        self.style.configure('Custom.Treeview.Heading',
                           background='#2c3e50',
                           foreground='#ecf0f1',
                           font=('Arial', 10, 'bold'))
    
    def create_widgets(self):
        """Create all GUI widgets"""
        # Main container
        main_frame = ttk.Frame(self.root, style='Primary.TFrame')
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Header
        self.create_header(main_frame)
        
        # Content area
        content_frame = ttk.Frame(main_frame, style='Primary.TFrame')
        content_frame.pack(fill='both', expand=True, pady=10)
        
        # Left panel (Terminal)
        left_frame = ttk.Frame(content_frame, style='Secondary.TFrame')
        left_frame.pack(side='left', fill='both', expand=True, padx=(0, 5))
        self.create_terminal_section(left_frame)
        
        # Right panel (Info & Tree)
        right_frame = ttk.Frame(content_frame, style='Secondary.TFrame')
        right_frame.pack(side='right', fill='both', padx=(5, 0))
        self.create_info_section(right_frame)
    
    def create_header(self, parent):
        """Create header section"""
        header_frame = ttk.Frame(parent, style='Primary.TFrame')
        header_frame.pack(fill='x', pady=(0, 10))
        
        # Title
        title_label = ttk.Label(header_frame, 
                               text="Simulator Sistem Manajemen File",
                               style='Title.TLabel')
        title_label.pack()
    
    def create_terminal_section(self, parent):
        """Create terminal section"""
        # Terminal header
        terminal_header = ttk.Frame(parent, style='Secondary.TFrame')
        terminal_header.pack(fill='x', padx=10, pady=10)
        
        terminal_title = ttk.Label(terminal_header,
                                 text="Terminal",
                                 style='Info.TLabel',
                                 font=('Arial', 12, 'bold'))
        terminal_title.pack(anchor='w')
        
        # Terminal output
        terminal_frame = ttk.Frame(parent, style='Secondary.TFrame')
        terminal_frame.pack(fill='both', expand=True, padx=10, pady=(0, 10))
        
        self.terminal_output = scrolledtext.ScrolledText(
            terminal_frame,
            wrap=tk.WORD,
            width=80,
            height=25,
            bg='#000000',
            fg='#00ff00',
            font=('Courier New', 10),
            insertbackground='#00ff00'
        )
        self.terminal_output.pack(fill='both', expand=True)
        
        # Command input
        cmd_frame = ttk.Frame(parent, style='Secondary.TFrame')
        cmd_frame.pack(fill='x', padx=10, pady=(0, 10))
        
        self.prompt_label = ttk.Label(cmd_frame,
                                    text="root@simulator:/$ ",
                                    foreground='#00ff00',
                                    background='#000000',
                                    font=('Courier New', 10, 'bold'))
        self.prompt_label.pack(side='left')
        
        self.command_entry = tk.Entry(
            cmd_frame,
            bg='#000000',
            fg='#00ff00',
            font=('Courier New', 10),
            insertbackground='#00ff00',
            relief='flat'
        )
        self.command_entry.pack(side='left', fill='x', expand=True, padx=(5, 10))
        self.command_entry.bind('<Return>', self.execute_command)
        self.command_entry.focus()
        
        # Control buttons
        btn_frame = ttk.Frame(parent, style='Secondary.TFrame')
        btn_frame.pack(fill='x', padx=10, pady=(0, 10))
        
        ttk.Button(btn_frame, text="Execute", 
                  command=self.execute_command, 
                  style='Action.TButton').pack(side='left', padx=(0, 5))
        
        ttk.Button(btn_frame, text="Clear", 
                  command=self.clear_terminal,
                  style='Action.TButton').pack(side='left', padx=5)
        
        ttk.Button(btn_frame, text="Reset System", 
                  command=self.reset_system,
                  style='Action.TButton').pack(side='left', padx=5)
        
        # Initialize terminal
        self.write_terminal("Sistem File Simulator v1.0", "success")
        self.write_terminal("Selamat datang! Sistem dimulai dengan direktori kosong.", "success")
        self.write_terminal("Ketik 'help' untuk melihat daftar perintah.", "success")
        self.write_terminal(f"Direktori saat ini: {self.fs.get_current_path()}")
        self.write_terminal("Memori yang digunakan: 0 MB", "info")
        self.write_terminal("=" * 60)
    
    def create_info_section(self, parent):
        """Create information section"""
        parent.configure(style='Secondary.TFrame')
        
        # System info
        sys_frame = ttk.LabelFrame(parent, text="📊 Informasi Sistem", 
                                  style='Secondary.TFrame')
        sys_frame.pack(fill='x', padx=10, pady=10)
        
        self.sys_info_frame = ttk.Frame(sys_frame, style='Secondary.TFrame')
        self.sys_info_frame.pack(fill='x', padx=10, pady=10)
        
        # File list
        files_frame = ttk.LabelFrame(parent, text="📁 Isi Direktori Saat Ini",
                                   style='Secondary.TFrame')
        files_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Treeview for files
        columns = ('Name', 'Type', 'Size', 'Modified')
        self.file_tree = ttk.Treeview(files_frame, columns=columns, 
                                     show='tree headings', style='Custom.Treeview')
        
        # Configure columns
        self.file_tree.heading('#0', text='', anchor='w')
        self.file_tree.column('#0', width=30, minwidth=30)
        
        for col in columns:
            self.file_tree.heading(col, text=col, anchor='w')
            if col == 'Name':
                self.file_tree.column(col, width=150, minwidth=100)
            elif col == 'Type':
                self.file_tree.column(col, width=80, minwidth=60)
            elif col == 'Size':
                self.file_tree.column(col, width=80, minwidth=60)
            else:  # Modified
                self.file_tree.column(col, width=120, minwidth=100)
        
        # Scrollbar for treeview
        tree_scroll = ttk.Scrollbar(files_frame, orient='vertical', 
                                   command=self.file_tree.yview)
        self.file_tree.configure(yscrollcommand=tree_scroll.set)
        
        self.file_tree.pack(side='left', fill='both', expand=True)
        tree_scroll.pack(side='right', fill='y')
        
        # Directory tree
        tree_frame = ttk.LabelFrame(parent, text="🌳 Struktur Direktori",
                                  style='Secondary.TFrame')
        tree_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.dir_tree_text = scrolledtext.ScrolledText(
            tree_frame,
            wrap=tk.NONE,
            width=40,
            height=15,
            bg='#34495e',
            fg='#ecf0f1',
            font=('Courier New', 9)
        )
        self.dir_tree_text.pack(fill='both', expand=True, padx=5, pady=5)
    
    def write_terminal(self, text: str, msg_type: str = "normal"):
        """Write text to terminal with color coding"""
        colors = {
            'normal': '#ecf0f1',
            'success': '#27ae60',
            'error': '#e74c3c',
            'warning': '#f39c12',
            'info': '#3498db'
        }
        
        self.terminal_output.configure(state='normal')
        
        # Add timestamp for commands
        if msg_type == 'command':
            self.terminal_output.insert(tk.END, f"{self.prompt_label.cget('text')}{text}\n", 'command')
        else:
            self.terminal_output.insert(tk.END, f"{text}\n")
        
        # Configure tags for colors
        for tag, color in colors.items():
            self.terminal_output.tag_configure(tag, foreground=color)
        
        if msg_type in colors:
            # Get the last line and apply color
            lines = self.terminal_output.get('1.0', tk.END).strip().split('\n')
            if lines:
                last_line_start = f"{len(lines)}.0"
                last_line_end = f"{len(lines)}.end"
                self.terminal_output.tag_add(msg_type, last_line_start, last_line_end)
        
        self.terminal_output.configure(state='disabled')
        self.terminal_output.see(tk.END)
    
    def execute_command(self, event=None):
        """Execute command from entry"""
        command = self.command_entry.get().strip()
        if not command:
            return
        
        # Clear entry
        self.command_entry.delete(0, tk.END)
        
        # Show command in terminal
        self.write_terminal(f"{self.prompt_label.cget('text')}{command}", 'command')
        
        # Parse and execute command
        try:
            self.process_command(command)
        except Exception as e:
            self.write_terminal(f"Error: {str(e)}", 'error')
        
        # Update display
        self.update_display()
    
    def process_command(self, command: str):
        """Process and execute file system commands"""
        parts = command.split()
        if not parts:
            return
        
        cmd = parts[0].lower()
        args = parts[1:]
        
        if cmd == 'help':
            self.show_help()
        elif cmd == 'pwd':
            self.write_terminal(self.fs.pwd())
        elif cmd == 'ls':
            path = args[0] if args else ''
            self.show_ls_output(path)
        elif cmd == 'mkdir':
            if not args:
                self.write_terminal("mkdir: missing operand", 'error')
            else:
                self.fs.mkdir(args[0])
                self.write_terminal(f"Directory '{args[0]}' created", 'success')
        elif cmd == 'rmdir':
            if not args:
                self.write_terminal("rmdir: missing operand", 'error')
            else:
                self.fs.rmdir(args[0])
                self.write_terminal(f"Directory '{args[0]}' removed", 'success')
        elif cmd == 'touch':
            if not args:
                self.write_terminal("touch: missing operand", 'error')
            else:
                self.fs.touch(args[0])
                self.write_terminal(f"File '{args[0]}' created/updated", 'success')
        elif cmd == 'rm':
            if not args:
                self.write_terminal("rm: missing operand", 'error')
            else:
                self.handle_rm_command(args)
        elif cmd == 'cd':
            path = args[0] if args else '/'
            self.fs.cd(path)
            self.write_terminal(f"Changed to directory: {self.fs.get_current_path()}", 'success')
            self.update_prompt()
        elif cmd == 'cp':
            if len(args) < 2:
                self.write_terminal("cp: missing destination operand", 'error')
            else:
                self.fs.cp(args[0], args[1])
                self.write_terminal(f"'{args[0]}' copied to '{args[1]}'", 'success')
        elif cmd == 'mv':
            if len(args) < 2:
                self.write_terminal("mv: missing destination operand", 'error')
            else:
                self.fs.mv(args[0], args[1])
                self.write_terminal(f"'{args[0]}' moved to '{args[1]}'", 'success')
        elif cmd == 'tree':
            self.show_tree()
        elif cmd == 'df':
            self.show_disk_usage()
        elif cmd == 'du':
            path = args[0] if args else ''
            self.show_directory_usage(path)
        elif cmd == 'history':
            self.show_command_history()
        elif cmd == 'clear':
            self.clear_terminal()
        elif cmd == 'reset':
            self.reset_system()
        elif cmd == 'exit' or cmd == 'quit':
            self.root.quit()
        else:
            self.write_terminal(f"Command '{cmd}' not found. Type 'help' for available commands.", 'error')
    
    def handle_rm_command(self, args: List[str]):
        """Handle rm command with different options"""
        if not args:
            self.write_terminal("rm: missing operand", 'error')
            return
        
        # Check for options
        recursive = False
        force = False
        files_to_remove = []
        
        for arg in args:
            if arg.startswith('-'):
                if 'r' in arg or 'R' in arg:
                    recursive = True
                if 'f' in arg:
                    force = True
            else:
                files_to_remove.append(arg)
        
        if not files_to_remove:
            self.write_terminal("rm: missing file operand", 'error')
            return
        
        # Process each file/directory
        for filename in files_to_remove:
            try:
                if recursive:
                    # Use rm_recursive for directories
                    success = self.fs.rm_recursive(filename, force)
                    if success:
                        self.write_terminal(f"'{filename}' removed recursively", 'success')
                else:
                    # Use regular rm for files only
                    self.fs.rm(filename)
                    self.write_terminal(f"File '{filename}' removed", 'success')
                    
            except FileNotFoundError as e:
                if not force:
                    self.write_terminal(f"rm: {str(e)}", 'error')
            except IsADirectoryError as e:
                self.write_terminal(f"rm: {str(e)}", 'error')
                self.write_terminal("Hint: Use 'rm -r' to remove directories", 'warning')
            except OSError as e:
                self.write_terminal(f"rm: {str(e)}", 'error')
            except Exception as e:
                self.write_terminal(f"rm: {str(e)}", 'error')
    
    def show_help(self):
        """Show help information"""
        help_text = """
Available Commands:
==================
File Operations:
  touch <filename>     - Create a new file or update timestamp
  rm <filename>        - Remove a file
  rm -r <name>         - Remove file or directory recursively
  rm -rf <name>        - Remove file or directory recursively (force)
  rm -f <filename>     - Remove file forcefully (no error if not exists)
  cp <source> <dest>   - Copy file or directory
  mv <source> <dest>   - Move/rename file or directory

Directory Operations:
  mkdir <dirname>      - Create a new directory
  rmdir <dirname>      - Remove empty directory
  cd <path>           - Change directory (cd .. for parent, cd / for root)
  pwd                 - Show current directory path
  ls [path]           - List directory contents

System Information:
  tree                - Show directory tree structure
  df                  - Show disk usage information
  du [path]           - Show directory size
  history             - Show command history

Utility Commands:
  help                - Show this help message
  clear               - Clear terminal screen
  reset               - Reset file system to initial state
  exit/quit           - Exit the application

Examples:
  mkdir documents
  cd documents
  touch readme.txt
  mkdir subfolder
  touch subfolder/file.txt
  ls
  rm -r subfolder
  cd ..
  tree
        """
        self.write_terminal(help_text.strip(), 'info')
    
    def show_ls_output(self, path: str = ''):
        """Show ls command output"""
        try:
            files = self.fs.ls(path)
            if not files:
                self.write_terminal("Directory is empty")
                return
            
            # Format output like Unix ls -l
            self.write_terminal("total " + str(len(files)))
            for file_info in files:
                permissions = file_info['permissions']
                size = str(file_info['size']) + " MB" if file_info['type'] == 'file' else str(file_info['size']) + " MB"
                modified = file_info['modified']
                name = file_info['name']
                
                # Add icon based on type
                icon = "📁" if file_info['type'] == 'directory' else "📄"
                
                line = f"{permissions} {size:>8} {modified} {icon} {name}"
                self.write_terminal(line)
                
        except Exception as e:
            self.write_terminal(f"ls: {str(e)}", 'error')
    
    def show_tree(self):
        """Show tree structure"""
        tree_data = self.fs.get_tree_structure()
        for item in tree_data:
            self.write_terminal(item['display'])
    
    def show_disk_usage(self):
        """Show disk usage information"""
        usage = self.fs.get_disk_usage()
        self.write_terminal("Disk Usage Information:", 'info')
        self.write_terminal(f"Total Storage: {usage['total']} MB")
        self.write_terminal(f"Used Storage:  {usage['used']} MB")
        self.write_terminal(f"Free Storage:  {usage['free']} MB")
        self.write_terminal(f"Usage:         {usage['usage_percent']:.1f}%")
        
        # Visual bar
        bar_length = 50
        used_bars = int((usage['usage_percent'] / 100) * bar_length)
        free_bars = bar_length - used_bars
        bar = "█" * used_bars + "░" * free_bars
        self.write_terminal(f"[{bar}] {usage['usage_percent']:.1f}%")
    
    def show_directory_usage(self, path: str = ''):
        """Show directory usage"""
        try:
            size = self.fs.get_directory_size(path)
            dir_path = path or self.fs.get_current_path()
            self.write_terminal(f"Directory '{dir_path}' size: {size} MB")
        except Exception as e:
            self.write_terminal(f"du: {str(e)}", 'error')
    
    def show_command_history(self):
        """Show command history"""
        history = self.fs.get_command_history()
        if not history:
            self.write_terminal("No commands in history")
            return
        
        self.write_terminal("Command History:", 'info')
        for i, cmd in enumerate(history, 1):
            self.write_terminal(f"{i:3d}  {cmd}")
    
    def clear_terminal(self):
        """Clear terminal output"""
        self.terminal_output.configure(state='normal')
        self.terminal_output.delete('1.0', tk.END)
        self.terminal_output.configure(state='disabled')
    
    def reset_system(self):
        """Reset file system"""
        if messagebox.askyesno("Reset System", "Are you sure you want to reset the file system? All data will be lost."):
            self.fs.reset()
            self.clear_terminal()
            self.write_terminal("System reset successfully", 'success')
            self.write_terminal(f"Current directory: {self.fs.get_current_path()}")
            self.update_prompt()
            self.update_display()
    
    def update_prompt(self):
        """Update command prompt with current directory"""
        current_path = self.fs.get_current_path()
        if current_path == '/':
            prompt = "root@simulator:/$ "
        else:
            # Show only the last directory name if path is long
            parts = current_path.strip('/').split('/')
            if len(parts) > 2:
                display_path = f".../{'/'.join(parts[-2:])}"
            else:
                display_path = current_path
            prompt = f"root@simulator:{display_path}$ "
        
        self.prompt_label.configure(text=prompt)
    
    def update_display(self):
        """Update all display elements"""
        self.update_system_info()
        self.update_file_list()
        self.update_directory_tree()
    
    def update_system_info(self):
        """Update system information display"""
        # Clear existing info
        for widget in self.sys_info_frame.winfo_children():
            widget.destroy()
        
        # Get system stats
        usage = self.fs.get_disk_usage()
        file_count = self.fs.count_files()
        dir_count = self.fs.count_directories()
        current_path = self.fs.get_current_path()
        
        # Create info labels
        info_data = [
            ("Current Directory:", current_path),
            ("Total Files:", str(file_count)),
            ("Total Directories:", str(dir_count)),
            ("Used Storage:", f"{usage['used']} MB"),
            ("Free Storage:", f"{usage['free']} MB"),
            ("Storage Usage:", f"{usage['usage_percent']:.1f}%")
        ]
        
        for i, (label, value) in enumerate(info_data):
            row = i // 2
            col = i % 2
            
            frame = ttk.Frame(self.sys_info_frame, style='Secondary.TFrame')
            frame.grid(row=row, column=col, sticky='w', padx=10, pady=2)
            
            ttk.Label(frame, text=label, style='Info.TLabel', 
                     font=('Arial', 9, 'bold')).pack(side='left')
            ttk.Label(frame, text=value, style='Info.TLabel',
                     font=('Arial', 9)).pack(side='left', padx=(5, 0))
    
    def update_file_list(self):
        """Update file list treeview"""
        # Clear existing items
        for item in self.file_tree.get_children():
            self.file_tree.delete(item)
        
        # Get current directory contents
        try:
            files = self.fs.ls()
            for file_info in files:
                icon = "📁" if file_info['type'] == 'directory' else "📄"
                size_str = f"{file_info['size']} MB" if file_info['type'] == 'file' else f"({file_info['size']} MB)"
                
                self.file_tree.insert('', 'end', text=icon, values=(
                    file_info['name'],
                    file_info['type'].capitalize(),
                    size_str,
                    file_info['modified']
                ))
        except Exception as e:
            pass  # Directory might be empty or inaccessible
    
    def update_directory_tree(self):
        """Update directory tree display"""
        self.dir_tree_text.configure(state='normal')
        self.dir_tree_text.delete('1.0', tk.END)
        
        try:
            tree_data = self.fs.get_tree_structure()
            for item in tree_data:
                self.dir_tree_text.insert(tk.END, item['display'] + '\n')
        except Exception as e:
            self.dir_tree_text.insert(tk.END, f"Error: {str(e)}\n")
        
        self.dir_tree_text.configure(state='disabled')
    
    def run(self):
        """Run the GUI application"""
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            print("\nApplication terminated by user")
        except Exception as e:
            print(f"Application error: {str(e)}")
        finally:
            try:
                self.root.destroy()
            except:
                pass