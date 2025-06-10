"""
Implementasi File System untuk Simulator
Berisi logika untuk manajemen file dan direktori
"""

import os
import time
from datetime import datetime
from typing import Dict, List, Optional, Union
import random

class FileSystemNode:
    """Representasi node dalam file system (file atau direktori)"""
    
    def __init__(self, name: str, node_type: str, parent: Optional['FileSystemNode'] = None):
        self.name = name
        self.type = node_type  # 'file' atau 'directory'
        self.parent = parent
        self.children: Dict[str, 'FileSystemNode'] = {}
        self.size = random.randint(1, 100) if node_type == 'file' else 0  # MB
        self.created = datetime.now()
        self.modified = datetime.now()
        self.permissions = "rwxr-xr--" if node_type == 'directory' else "rw-r--r--"
    
    def add_child(self, child: 'FileSystemNode') -> None:
        """Menambahkan child node"""
        self.children[child.name] = child
        child.parent = self
        self.modified = datetime.now()
    
    def remove_child(self, name: str) -> Optional['FileSystemNode']:
        """Menghapus child node"""
        if name in self.children:
            child = self.children[name]
            del self.children[name]
            child.parent = None
            self.modified = datetime.now()
            return child
        return None
    
    def get_child(self, name: str) -> Optional['FileSystemNode']:
        """Mendapatkan child node berdasarkan nama"""
        return self.children.get(name)
    
    def get_path(self) -> str:
        """Mendapatkan path lengkap dari node"""
        if not self.parent:
            return '/'
        parent_path = self.parent.get_path()
        return os.path.join(parent_path, self.name) if parent_path != '/' else f'/{self.name}'
    
    def get_total_size(self) -> int:
        """Mendapatkan total ukuran (termasuk semua children)"""
        if self.type == 'file':
            return self.size
        
        total = 0
        for child in self.children.values():
            total += child.get_total_size()
        return total
    
    def is_empty(self) -> bool:
        """Mengecek apakah direktori kosong"""
        return len(self.children) == 0
    
    def list_children(self) -> List['FileSystemNode']:
        """Mendapatkan daftar children yang sudah diurutkan"""
        children = list(self.children.values())
        # Urutkan: direktori dulu, kemudian file, keduanya alfabetis
        children.sort(key=lambda x: (x.type == 'file', x.name.lower()))
        return children

class FileSystem:
    """Implementasi file system simulator"""
    
    def __init__(self, total_storage: int = 1024):
        self.root = FileSystemNode('', 'directory')
        self.current_directory = self.root
        self.total_storage = total_storage  # MB
        self.command_history = []
        # Hapus inisialisasi default structure agar dimulai dengan sistem kosong
        # self._initialize_default_structure()
    
    def _initialize_default_structure(self):
        """Inisialisasi struktur direktori default (TIDAK DIGUNAKAN LAGI)"""
        # Method ini dibiarkan untuk referensi tapi tidak dipanggil
        # Buat beberapa direktori dan file default
        self.mkdir('home')
        self.mkdir('var')
        self.mkdir('tmp')
        
        # Pindah ke home dan buat beberapa file
        self.cd('home')
        self.touch('document.txt')
        self.touch('readme.md')
        self.mkdir('downloads')
        
        # Kembali ke root
        self.cd('/')
    
    def get_used_storage(self) -> int:
        """Mendapatkan storage yang sudah digunakan"""
        return self.root.get_total_size()
    
    def get_free_storage(self) -> int:
        """Mendapatkan storage yang masih tersedia"""
        return max(0, self.total_storage - self.get_used_storage())
    
    def get_current_path(self) -> str:
        """Mendapatkan path direktori saat ini"""
        return self.current_directory.get_path()
    
    def resolve_path(self, path: str) -> Optional[FileSystemNode]:
        """Resolve path ke node yang sesuai"""
        if not path or path == '.':
            return self.current_directory
        
        if path == '/':
            return self.root
        
        if path == '..':
            return self.current_directory.parent or self.root
        
        # Tentukan starting point
        if path.startswith('/'):
            current = self.root
            path = path[1:]  # Remove leading slash
        else:
            current = self.current_directory
        
        if not path:  # Path was just '/'
            return current
        
        # Split path dan traverse
        parts = [p for p in path.split('/') if p]
        
        for part in parts:
            if part == '.':
                continue
            elif part == '..':
                current = current.parent or self.root
            else:
                child = current.get_child(part)
                if not child:
                    return None
                current = child
        
        return current
    
    def pwd(self) -> str:
        """Print working directory"""
        return self.get_current_path()
    
    def ls(self, path: str = '') -> List[Dict]:
        """List directory contents"""
        if path:
            target = self.resolve_path(path)
            if not target:
                raise FileNotFoundError(f"Path '{path}' tidak ditemukan")
        else:
            target = self.current_directory
        
        if target.type != 'directory':
            raise NotADirectoryError(f"'{path}' bukan direktori")
        
        result = []
        for child in target.list_children():
            result.append({
                'name': child.name,
                'type': child.type,
                'size': child.size if child.type == 'file' else child.get_total_size(),
                'modified': child.modified.strftime('%Y-%m-%d %H:%M'),
                'permissions': child.permissions
            })
        
        return result
    
    def mkdir(self, name: str) -> bool:
        """Membuat direktori baru"""
        if not name or '/' in name:
            raise ValueError("Nama direktori tidak valid")
        
        if self.current_directory.get_child(name):
            raise FileExistsError(f"'{name}' sudah ada")
        
        new_dir = FileSystemNode(name, 'directory')
        self.current_directory.add_child(new_dir)
        self.command_history.append(f"mkdir {name}")
        return True
    
    def rmdir(self, name: str) -> bool:
        """Menghapus direktori kosong"""
        if not name:
            raise ValueError("Nama direktori diperlukan")
        
        target = self.current_directory.get_child(name)
        if not target:
            raise FileNotFoundError(f"Direktori '{name}' tidak ditemukan")
        
        if target.type != 'directory':
            raise NotADirectoryError(f"'{name}' bukan direktori")
        
        if not target.is_empty():
            raise OSError(f"Direktori '{name}' tidak kosong")
        
        self.current_directory.remove_child(name)
        self.command_history.append(f"rmdir {name}")
        return True
    
    def touch(self, name: str) -> bool:
        """Membuat file baru"""
        if not name or '/' in name:
            raise ValueError("Nama file tidak valid")
        
        if self.current_directory.get_child(name):
            # Update modified time jika file sudah ada
            existing_file = self.current_directory.get_child(name)
            existing_file.modified = datetime.now()
            return True
        
        new_file = FileSystemNode(name, 'file')
        self.current_directory.add_child(new_file)
        self.command_history.append(f"touch {name}")
        return True
    
    def rm(self, name: str) -> bool:
        """Menghapus file"""
        if not name:
            raise ValueError("Nama file diperlukan")
        
        target = self.current_directory.get_child(name)
        if not target:
            raise FileNotFoundError(f"File '{name}' tidak ditemukan")
        
        if target.type != 'file':
            raise IsADirectoryError(f"'{name}' adalah direktori. Gunakan rmdir")
        
        self.current_directory.remove_child(name)
        self.command_history.append(f"rm {name}")
        return True
    
    def cd(self, path: str = '/') -> bool:
        """Change directory"""
        target = self.resolve_path(path)
        if not target:
            raise FileNotFoundError(f"Direktori '{path}' tidak ditemukan")
        
        if target.type != 'directory':
            raise NotADirectoryError(f"'{path}' bukan direktori")
        
        self.current_directory = target
        self.command_history.append(f"cd {path}")
        return True
    
    def cp(self, source: str, destination: str) -> bool:
        """Copy file atau direktori"""
        src_node = self.current_directory.get_child(source)
        if not src_node:
            raise FileNotFoundError(f"'{source}' tidak ditemukan")
        
        if self.current_directory.get_child(destination):
            raise FileExistsError(f"'{destination}' sudah ada")
        
        # Buat copy
        new_node = FileSystemNode(destination, src_node.type)
        new_node.size = src_node.size
        new_node.permissions = src_node.permissions
        
        # Jika direktori, copy semua isi (recursive)
        if src_node.type == 'directory':
            self._copy_directory_contents(src_node, new_node)
        
        self.current_directory.add_child(new_node)
        self.command_history.append(f"cp {source} {destination}")
        return True
    
    def _copy_directory_contents(self, source: FileSystemNode, destination: FileSystemNode):
        """Helper untuk copy isi direktori secara recursive"""
        for child in source.children.values():
            new_child = FileSystemNode(child.name, child.type)
            new_child.size = child.size
            new_child.permissions = child.permissions
            
            if child.type == 'directory':
                self._copy_directory_contents(child, new_child)
            
            destination.add_child(new_child)
    
    def mv(self, source: str, destination: str) -> bool:
        """Move/rename file atau direktori"""
        src_node = self.current_directory.get_child(source)
        if not src_node:
            raise FileNotFoundError(f"'{source}' tidak ditemukan")
        
        if self.current_directory.get_child(destination):
            raise FileExistsError(f"'{destination}' sudah ada")
        
        # Remove dari parent dan ubah nama
        self.current_directory.remove_child(source)
        src_node.name = destination
        self.current_directory.add_child(src_node)
        
        self.command_history.append(f"mv {source} {destination}")
        return True
    
    def get_disk_usage(self) -> Dict:
        """Mendapatkan informasi penggunaan disk"""
        used = self.get_used_storage()
        free = self.get_free_storage()
        total = self.total_storage
        
        return {
            'total': total,
            'used': used,
            'free': free,
            'usage_percent': (used / total * 100) if total > 0 else 0
        }
    
    def get_directory_size(self, path: str = '') -> int:
        """Mendapatkan ukuran direktori"""
        if path:
            target = self.resolve_path(path)
            if not target:
                raise FileNotFoundError(f"Path '{path}' tidak ditemukan")
        else:
            target = self.current_directory
        
        return target.get_total_size()
    
    def get_tree_structure(self) -> List[Dict]:
        """Mendapatkan struktur tree dari root"""
        def build_tree(node: FileSystemNode, prefix: str = '', is_last: bool = True) -> List[Dict]:
            result = []
            
            connector = '└── ' if is_last else '├── '
            icon = '📁' if node.type == 'directory' else '📄'
            
            result.append({
                'name': node.name or '/',
                'type': node.type,
                'size': node.size if node.type == 'file' else None,
                'display': f"{prefix}{connector}{icon} {node.name or '/'}",
                'level': len(prefix) // 4
            })
            
            if node.type == 'directory':
                children = node.list_children()
                for i, child in enumerate(children):
                    is_child_last = i == len(children) - 1
                    new_prefix = prefix + ('    ' if is_last else '│   ')
                    result.extend(build_tree(child, new_prefix, is_child_last))
            
            return result
        
        return build_tree(self.root)
    
    def count_files(self) -> int:
        """Menghitung jumlah file"""
        def count_recursive(node: FileSystemNode) -> int:
            count = 1 if node.type == 'file' else 0
            for child in node.children.values():
                count += count_recursive(child)
            return count
        
        return count_recursive(self.root)
    
    def count_directories(self) -> int:
        """Menghitung jumlah direktori"""
        def count_recursive(node: FileSystemNode) -> int:
            count = 1 if node.type == 'directory' else 0
            for child in node.children.values():
                count += count_recursive(child)
            return count
        
        return count_recursive(self.root)
    
    def get_command_history(self) -> List[str]:
        """Mendapatkan history perintah"""
        return self.command_history.copy()
    
    def clear_history(self) -> None:
        """Menghapus history perintah"""
        self.command_history.clear()
    
    def reset(self) -> None:
        """Reset file system ke kondisi awal"""
        self.__init__(self.total_storage)