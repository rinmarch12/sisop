#!/usr/bin/env python3
"""
Simulator Sistem Manajemen File
Tugas Sistem Operasi - Implementasi File System Management
Main Application Entry Point
"""

import sys
import os
from pathlib import Path

# Tambahkan direktori root ke Python path
root_dir = Path(__file__).parent
sys.path.insert(0, str(root_dir))

# Import modules
from filesystem import FileSystem
from gui import FileManagerGUI

def main():
    """Main application entry point"""
    try:
        print("🖥️  Memulai Simulator Sistem Manajemen File...")
        print("=" * 50)
        
        # Inisialisasi file system
        file_system = FileSystem()
        print("✅ File system berhasil diinisialisasi")
        
        # Inisialisasi GUI
        app = FileManagerGUI(file_system)
        print("✅ GUI berhasil diinisialisasi")
        
        print("🚀 Aplikasi siap digunakan!")
        print("=" * 50)
        
        # Jalankan aplikasi
        app.run()
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        print("🔧 Pastikan semua dependencies telah terinstall")
        sys.exit(1)

if __name__ == "__main__":
    main()