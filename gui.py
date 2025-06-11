"""
GUI Interface untuk File System Simulator dengan Visualisasi Memory Allocation
Menggunakan Tkinter untuk antarmuka grafis dengan tampilan blok memori
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from tkinter import font as tkFont
import threading
from typing import List, Dict, Optional
from filesystem_modified import FileSystem
import math

class MemoryVisualization:
    """Widget untuk visualisasi memori"""
    
    def __init__(self, parent, memory_manager):
        self.parent = parent
        self.memory_manager = memory_manager
        self.canvas_width = 800
        self.canvas_height = 400
        self.block_width = 8
        self.block_height = 20
        self.blocks_per_row = self.canvas_width // (self.block_width + 1)
        
        self.create_widgets()
    
    def create_widgets(self):
        """Buat widget visualisasi"""
        # Frame untuk visualisasi
        viz_frame = ttk.LabelFrame(self.parent, text="🧠 Visualisasi Memori (First Fit Algorithm)")
        viz_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Canvas untuk gambar memori
        self.canvas = tk.Canvas(
            viz_frame,
            width=self.canvas_width,
            height=self.canvas_height,
            bg='#2c3e50',
            highlightthickness=0
        )
        self.canvas.pack(side='top', padx=10, pady=10)
        
        # Legend frame
        legend_frame = ttk.Frame(viz_frame)
        legend_frame.pack(fill='x', padx=10, pady=5)
        
        # Legend items
        legend_items = [
            ("🟩", "#27ae60", "Blok Kosong"),
            ("🟥", "#e74c3c", "Blok Terisi"),
            ("⬜", "#bdc3c7", "Fragmentasi"),
        ]
        
        for i, (emoji, color, label) in enumerate(legend_items):
            ttk.Label(legend_frame, text=emoji, font=("Arial", 12)).grid(row=0, column=i*3, padx=5)
            color_box = tk.Canvas(legend_frame, width=15, height=15, bg=color, highlightthickness=0)
            color_box.grid(row=0, column=i*3+1, padx=2)
            ttk.Label(legend_frame, text=label).grid(row=0, column=i*3+2, padx=5)
        
        # Statistik memori
        stats_frame = ttk.LabelFrame(viz_frame, text="📊 Statistik Memori")
        stats_frame.pack(fill='x', padx=10, pady=5)
        
        # Status memori: Total, used, free, fragmentation
        self.memory_status = {
            'total': tk.StringVar(value="Total: 0 MB"),
            'used': tk.StringVar(value="Terpakai: 0 MB"),
            'free': tk.StringVar(value="Kosong: 0 MB"),
            'fragmentation': tk.StringVar(value="Fragmentasi: 0%"),
            'segments': tk.StringVar(value="Segmen Kosong: 0"),
        }
        
        status_frame = ttk.Frame(stats_frame)
        status_frame.pack(fill='x', padx=5, pady=5)
        
        # First column
        ttk.Label(status_frame, textvariable=self.memory_status['total']).grid(row=0, column=0, padx=5, sticky='w')
        ttk.Label(status_frame, textvariable=self.memory_status['used']).grid(row=1, column=0, padx=5, sticky='w')
        
        # Second column
        ttk.Label(status_frame, textvariable=self.memory_status['free']).grid(row=0, column=1, padx=5, sticky='w')
        ttk.Label(status_frame, textvariable=self.memory_status['fragmentation']).grid(row=1, column=1, padx=5, sticky='w')
        
        # Third column
        ttk.Label(status_frame, textvariable=self.memory_status['segments']).grid(row=0, column=2, padx=5, sticky='w')
        
    def update_visualization(self):
        """Update visualisasi blok memori"""
        self.canvas.delete('all')
        
        # Dapatkan peta memori
        memory_map = self.memory_manager.get_memory_map()
        memory_status = self.memory_manager.get_memory_status()
        
        # Update statistik
        self.memory_status['total'].set(f"Total: {memory_status['total_size_mb']} MB")
        self.memory_status['used'].set(f"Terpakai: {memory_status['used_size_mb']} MB")
        self.memory_status['free'].set(f"Kosong: {memory_status['free_size_mb']} MB")
        self.memory_status['fragmentation'].set(f"Fragmentasi: {memory_status['fragmentation_percentage']:.1f}%")
        self.memory_status['segments'].set(f"Segmen Kosong: {memory_status['number_of_free_segments']}")
        
        # Hitung total blocks untuk visualisasi
        total_blocks = self.memory_manager.total_blocks
        
        # Hitung baris dan kolom
        cols = self.blocks_per_row
        rows = math.ceil(total_blocks / cols)
        
        # Gambar setiap blok
        for block in memory_map:
            start_block = block['start_address']
            end_block = start_block + block['size'] - 1
            
            for b in range(start_block, end_block + 1):
                row = b // cols
                col = b % cols
                
                x1 = col * (self.block_width + 1)
                y1 = row * (self.block_height + 1)
                x2 = x1 + self.block_width
                y2 = y1 + self.block_height
                
                # Warna berdasarkan status blok
                if block['is_free']:
                    color = "#27ae60"  # Hijau untuk blok kosong
                else:
                    color = "#e74c3c"  # Merah untuk blok terisi
                    
                    # Jika ini adalah blok pertama, tambahkan label
                    if b == start_block:
                        # Potong nama file jika terlalu panjang
                        short_name = block['file_name']
                        if len(short_name) > 8:
                            short_name = short_name[:7] + "…"
                            
                        # Label untuk nama file
                        self.canvas.create_text(
                            x1 + self.block_width/2,
                            y1 + self.block_height/2,
                            text=short_name,
                            fill="#ffffff",
                            font=("Arial", 7),
                            anchor="center"
                        )
                
                # Gambar blok
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="")
                
                # Tambahkan detail tooltip
                self.canvas.tag_bind(
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline=""),
                    '<Enter>',
                    lambda e, b=block: self._show_block_tooltip(e, b)
                )
                self.canvas.tag_bind(
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline=""),
                    '<Leave>',
                    self._hide_tooltip
                )
        
        # Tambahkan visualisasi fragmentasi eksternal
        if memory_status['external_fragmentation_mb'] > 0:
            # Gambar indikator fragmentasi di bawah blok memori
            frag_height = 10
            frag_width = self.canvas_width * (memory_status['external_fragmentation_mb'] / memory_status['total_size_mb'])
            
            # Posisi di bawah visualisasi blok
            frag_y = (rows + 1) * (self.block_height + 1)
            
            # Gambar bar fragmentasi
            self.canvas.create_rectangle(
                0, frag_y, 
                frag_width, frag_y + frag_height,
                fill="#bdc3c7",
                outline=""
            )
            
            # Label fragmentasi
            self.canvas.create_text(
                frag_width / 2,
                frag_y + frag_height / 2,
                text=f"Fragmentasi: {memory_status['external_fragmentation_mb']} MB",
                fill="#2c3e50",
                font=("Arial", 8)
            )
    
    def _show_block_tooltip(self, event, block):
        """Menampilkan tooltip saat mouse hover di blok"""
        x, y = event.x, event.y
        
        # Buat tooltip frame
        self.tooltip = tk.Toplevel(self.canvas)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.geometry(f"+{x + 10}+{y + 10}")
        
        # Isi tooltip
        tooltip_frame = ttk.Frame(self.tooltip, relief="solid", borderwidth=1)
        tooltip_frame.pack(fill="both", expand=True)
        
        if block['is_free']:
            ttk.Label(tooltip_frame, text=f"Blok Kosong").pack(padx=5, pady=2)
            ttk.Label(tooltip_frame, text=f"Alamat: {block['start_address']}").pack(padx=5, pady=2)
            ttk.Label(tooltip_frame, text=f"Ukuran: {block['size'] * self.memory_manager.block_size} MB").pack(padx=5, pady=2)
        else:
            ttk.Label(tooltip_frame, text=f"File: {block['file_name']}").pack(padx=5, pady=2)
            ttk.Label(tooltip_frame, text=f"Alamat: {block['start_address']}").pack(padx=5, pady=2)
            ttk.Label(tooltip_frame, text=f"Ukuran: {block['size'] * self.memory_manager.block_size} MB").pack(padx=5, pady=2)
            if 'allocation_time' in block and block['allocation_time']:
                ttk.Label(tooltip_frame, text=f"Dialokasikan: {block['allocation_time'].strftime('%H:%M:%S')}").pack(padx=5, pady=2)
    
    def _hide_tooltip(self, event):
        """Sembunyikan tooltip"""
        if hasattr(self, 'tooltip'):
            self.tooltip.destroy()

class FileSystemGUI:
    """GUI untuk File System Simulator"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("File System Simulator - First Fit Memory Allocation")
        self.root.geometry("1200x800")
        self.root.configure(bg="#ecf0f1")
        
        # Set font
        self.default_font = tkFont.Font(family="Arial", size=10)
        self.mono_font = tkFont.Font(family="Courier", size=10)
        
        # Create file system instance
        self.fs = FileSystem(total_storage=1024, block_size=4)
        
        # Create UI
        self.create_menu()
        self.create_widgets()
        
        # Initial refresh
        self.refresh_ui()
    
    def create_menu(self):
        """Create menu bar"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Reset File System", command=self.reset_file_system)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # View menu
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="View", menu=view_menu)
        view_menu.add_command(label="Refresh", command=self.refresh_ui)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
    
    def create_widgets(self):
        """Create main UI widgets"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding=(10, 5))
        main_frame.pack(fill='both', expand=True)
        
        # Create paned window
        main_paned = ttk.PanedWindow(main_frame, orient='horizontal')
        main_paned.pack(fill='both', expand=True)
        
        # Left frame - File Explorer & Commands
        left_frame = ttk.Frame(main_paned, width=400)
        main_paned.add(left_frame, weight=1)
        
        # Right frame - Memory Visualization
        right_frame = ttk.Frame(main_paned, width=800)
        main_paned.add(right_frame, weight=2)
        
        # Setup left frame
        self.setup_left_frame(left_frame)
        
        # Setup memory visualization
        self.memory_viz = MemoryVisualization(right_frame, self.fs.memory_manager)
    
    def setup_left_frame(self, parent):
        """Setup file explorer and command section"""
        # File system info
        info_frame = ttk.LabelFrame(parent, text="💽 Informasi File System")
        info_frame.pack(fill='x', padx=10, pady=5)
        
        self.fs_info = {
            'path': tk.StringVar(value="/"),
            'free': tk.StringVar(value="Kosong: 0 MB"),
            'used': tk.StringVar(value="Terpakai: 0 MB"),
            'total': tk.StringVar(value="Total: 0 MB"),
            'files': tk.StringVar(value="File: 0"),
            'dirs': tk.StringVar(value="Direktori: 0")
        }
        
        # Current path
        path_frame = ttk.Frame(info_frame)
        path_frame.pack(fill='x', padx=5, pady=2)
        ttk.Label(path_frame, text="Path:").grid(row=0, column=0, sticky='w', padx=2)
        ttk.Entry(path_frame, textvariable=self.fs_info['path'], state="readonly").grid(row=0, column=1, sticky='ew', padx=2)
        path_frame.columnconfigure(1, weight=1)
        
        # Storage info
        storage_frame = ttk.Frame(info_frame)
        storage_frame.pack(fill='x', padx=5, pady=2)
        ttk.Label(storage_frame, textvariable=self.fs_info['free']).grid(row=0, column=0, sticky='w', padx=5)
        ttk.Label(storage_frame, textvariable=self.fs_info['used']).grid(row=0, column=1, sticky='w', padx=5)
        ttk.Label(storage_frame, textvariable=self.fs_info['total']).grid(row=0, column=2, sticky='w', padx=5)
        
        # Count info
        count_frame = ttk.Frame(info_frame)
        count_frame.pack(fill='x', padx=5, pady=2)
        ttk.Label(count_frame, textvariable=self.fs_info['files']).grid(row=0, column=0, sticky='w', padx=5)
        ttk.Label(count_frame, textvariable=self.fs_info['dirs']).grid(row=0, column=1, sticky='w', padx=5)
        
        # File explorer
        explorer_frame = ttk.LabelFrame(parent, text="📂 File Explorer")
        explorer_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Treeview
        self.tree = ttk.Treeview(explorer_frame, columns=("type", "size", "address"))
        self.tree.heading("#0", text="Name")
        self.tree.heading("type", text="Type")
        self.tree.heading("size", text="Size")
        self.tree.heading("address", text="Address")
        self.tree.column("#0", width=150)
        self.tree.column("type", width=70)
        self.tree.column("size", width=70)
        self.tree.column("address", width=70)
        self.tree.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Command frame
        cmd_frame = ttk.LabelFrame(parent, text="💻 Command")
        cmd_frame.pack(fill='x', padx=10, pady=5)
        
        # Command entry
        cmd_entry_frame = ttk.Frame(cmd_frame)
        cmd_entry_frame.pack(fill='x', padx=5, pady=5)
        ttk.Label(cmd_entry_frame, text="$").grid(row=0, column=0, sticky='w', padx=2)
        self.cmd_entry = ttk.Entry(cmd_entry_frame)
        self.cmd_entry.grid(row=0, column=1, sticky='ew', padx=2)
        self.cmd_entry.bind("<Return>", self.execute_command)
        cmd_entry_frame.columnconfigure(1, weight=1)
        
        # Command buttons
        btn_frame = ttk.Frame(cmd_frame)
        btn_frame.pack(fill='x', padx=5, pady=5)
        
        common_cmds = [
            ("ls", self.cmd_ls),
            ("pwd", self.cmd_pwd),
            ("cd", self.cmd_cd),
            ("mkdir", self.cmd_mkdir),
            ("touch", self.cmd_touch),
            ("rm", self.cmd_rm)
        ]
        
        for i, (cmd, callback) in enumerate(common_cmds):
            ttk.Button(btn_frame, text=cmd, command=callback).grid(row=0, column=i, padx=2)
        
        # Output/history
        history_frame = ttk.LabelFrame(parent, text="📜 Output")
        history_frame.pack(fill='x', padx=10, pady=5)
        
        self.output_text = scrolledtext.ScrolledText(history_frame, wrap=tk.WORD, height=6, font=self.mono_font)
        self.output_text.pack(fill='x', padx=5, pady=5)
    
    def execute_command(self, event=None):
        """Execute user command"""
        command = self.cmd_entry.get().strip()
        if not command:
            return
        
        self.output_text.insert(tk.END, f"$ {command}\n")
        
        # Parse command
        parts = command.split()
        cmd = parts[0]
        args = parts[1:]
        
        try:
            if cmd == "ls":
                self.exec_ls(" ".join(args) if args else "")
            elif cmd == "cd":
                self.fs.cd(" ".join(args) if args else "/")
            elif cmd == "pwd":
                self.output_text.insert(tk.END, f"{self.fs.pwd()}\n")
            elif cmd == "mkdir":
                if not args:
                    self.output_text.insert(tk.END, "Error: Missing directory name\n")
                else:
                    self.fs.mkdir(args[0])
            elif cmd == "touch":
                if not args:
                    self.output_text.insert(tk.END, "Error: Missing file name\n")
                else:
                    self.fs.touch(args[0])
            elif cmd == "rm":
                if not args:
                    self.output_text.insert(tk.END, "Error: Missing file name\n")
                    return
                
                force = "-f" in args
                recursive = "-r" in args or "-rf" in args or "-fr" in args
                
                # Filter out flags
                file_args = [arg for arg in args if not arg.startswith("-")]
                
                if not file_args:
                    self.output_text.insert(tk.END, "Error: Missing file name\n")
                    return
                
                if recursive:
                    self.fs.rm_recursive(file_args[0], force)
                else:
                    self.fs.rm(file_args[0])
            elif cmd == "rmdir":
                if not args:
                    self.output_text.insert(tk.END, "Error: Missing directory name\n")
                else:
                    self.fs.rmdir(args[0])
            elif cmd == "cp":
                if len(args) < 2:
                    self.output_text.insert(tk.END, "Error: cp requires source and destination\n")
                else:
                    self.fs.cp(args[0], args[1])
            elif cmd == "mv":
                if len(args) < 2:
                    self.output_text.insert(tk.END, "Error: mv requires source and destination\n")
                else:
                    self.fs.mv(args[0], args[1])
            elif cmd == "clear":
                self.output_text.delete(1.0, tk.END)
                return
            else:
                self.output_text.insert(tk.END, f"Error: Unknown command '{cmd}'\n")
                return
        except Exception as e:
            self.output_text.insert(tk.END, f"Error: {str(e)}\n")
        
        # Refresh UI
        self.refresh_ui()
        
        # Clear command entry
        self.cmd_entry.delete(0, tk.END)
        
        # Auto-scroll to bottom
        self.output_text.see(tk.END)
    
    def refresh_ui(self):
        """Refresh the entire UI"""
        # Update file system info
        self.fs_info['path'].set(self.fs.get_current_path())
        self.fs_info['free'].set(f"Kosong: {self.fs.get_free_storage()} MB")
        self.fs_info['used'].set(f"Terpakai: {self.fs.get_used_storage()} MB")
        self.fs_info['total'].set(f"Total: {self.fs.memory_manager.total_size} MB")
        self.fs_info['files'].set(f"File: {self.fs.count_files()}")
        self.fs_info['dirs'].set(f"Direktori: {self.fs.count_directories()}")
        
        # Update file explorer
        self.update_file_explorer()
        
        # Update memory visualization
        self.memory_viz.update_visualization()
    
    def update_file_explorer(self):
        """Update file explorer tree"""
        self.tree.delete(*self.tree.get_children())
        
        try:
            items = self.fs.ls()
            for item in items:
                icon = "🗂️ " if item['type'] == 'directory' else "📄 "
                size_str = f"{item['size']} MB" if item['type'] == 'file' else ""
                address_str = f"@{item['memory_address']}" if item['memory_address'] is not None else ""
                
                self.tree.insert(
                    "", tk.END, text=icon + item['name'],
                    values=(item['type'], size_str, address_str)
                )
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def exec_ls(self, path):
        """Execute ls command and show output"""
        try:
            items = self.fs.ls(path)
            for item in items:
                icon = "📁" if item['type'] == 'directory' else "📄"
                size_str = f"{item['size']} MB" if item['type'] == 'file' else "DIR"
                address_str = f"@{item['memory_address']}" if item['memory_address'] is not None else ""
                
                self.output_text.insert(tk.END, f"{icon} {item['name']:<20} {size_str:<10} {address_str}\n")
        except Exception as e:
            self.output_text.insert(tk.END, f"Error: {str(e)}\n")
    
    def cmd_ls(self):
        """Command button for ls"""
        self.cmd_entry.delete(0, tk.END)
        self.cmd_entry.insert(0, "ls")
        self.execute_command()
    
    def cmd_pwd(self):
        """Command button for pwd"""
        self.cmd_entry.delete(0, tk.END)
        self.cmd_entry.insert(0, "pwd")
        self.execute_command()
    
    def cmd_cd(self):
        """Command button for cd"""
        self.cmd_entry.delete(0, tk.END)
        self.cmd_entry.insert(0, "cd ")
        self.cmd_entry.focus()
        self.cmd_entry.icursor(tk.END)
    
    def cmd_mkdir(self):
        """Command button for mkdir"""
        self.cmd_entry.delete(0, tk.END)
        self.cmd_entry.insert(0, "mkdir ")
        self.cmd_entry.focus()
        self.cmd_entry.icursor(tk.END)
    
    def cmd_touch(self):
        """Command button for touch"""
        self.cmd_entry.delete(0, tk.END)
        self.cmd_entry.insert(0, "touch ")
        self.cmd_entry.focus()
        self.cmd_entry.icursor(tk.END)
    
    def cmd_rm(self):
        """Command button for rm"""
        self.cmd_entry.delete(0, tk.END)
        self.cmd_entry.insert(0, "rm ")
        self.cmd_entry.focus()
        self.cmd_entry.icursor(tk.END)
    
    def reset_file_system(self):
        """Reset file system"""
        if messagebox.askokcancel("Reset File System", "Are you sure you want to reset the file system? All data will be lost."):
            self.fs.reset()
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, "File system reset.\n")
            self.refresh_ui()
    
    def show_about(self):
        """Show about dialog"""
        messagebox.showinfo(
            "About File System Simulator",
            "File System Simulator with First Fit Memory Allocation\n\n"
            "Visualisasi algoritma alokasi memori First Fit untuk simulasi file system.\n\n"
            "© 2025"
        )

# Fungsi main untuk menjalankan aplikasi
def main():
    root = tk.Tk()
    app = FileSystemGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()