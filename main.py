#!/usr/bin/env python3
"""
Simulator Sistem Manajemen File dengan First Fit Memory Allocation
Tugas Sistem Operasi - Implementasi File System Management dan Visualisasi Memori
Main Application Entry Point
"""

import sys
import os
from pathlib import Path

# Tambahkan direktori root ke Python path
root_dir = Path(__file__).parent
sys.path.insert(0, str(root_dir))

# Import modules
from filesystem_modified import FileSystem
from gui import FileSystemGUI

def main():
    """Main application entry point"""
    try:
        print("🖥️  Memulai Simulator Sistem Manajemen File dengan First Fit Memory Allocation...")
        print("=" * 60)
        
        # Inisialisasi GUI dengan Tkinter
        import tkinter as tk
        root = tk.Tk()
        app = FileSystemGUI(root)
        print("✅ GUI berhasil diinisialisasi")
        
        print("🚀 Aplikasi siap digunakan!")
        print("=" * 60)
        
        # Jalankan aplikasi
        root.mainloop()
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        print("🔧 Pastikan semua dependencies telah terinstall")
        sys.exit(1)

if __name__ == "__main__":
    main()