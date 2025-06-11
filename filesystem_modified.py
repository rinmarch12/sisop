"""
Implementasi File System dengan Algoritma First Fit Memory Allocation
Berisi logika untuk manajemen file dan direktori dengan simulasi blok memori
"""

import os
import time
from datetime import datetime
from typing import Dict, List, Optional, Union, Tuple
import random

class MemoryBlock:
    """Representasi blok memori"""
    
    def __init__(self, start_address: int, size: int, is_free: bool = True):
        self.start_address = start_address
        self.size = size
        self.is_free = is_free
        self.file_name = None
        self.allocated_time = None
    
    def allocate(self, file_name: str) -> None:
        """Alokasi blok untuk file"""
        self.is_free = False
        self.file_name = file_name
        self.allocated_time = datetime.now()
    
    def deallocate(self) -> None:
        """Dealokasi blok"""
        self.is_free = True
        self.file_name = None
        self.allocated_time = None
    
    def get_end_address(self) -> int:
        """Mendapatkan alamat akhir blok"""
        return self.start_address + self.size - 1

class MemoryManager:
    """Manager untuk alokasi memori dengan algoritma First Fit"""
    
    def __init__(self, total_size: int = 1024, block_size: int = 4):
        self.total_size = total_size  # Total ukuran dalam MB
        self.block_size = block_size  # Ukuran minimum blok dalam MB
        self.total_blocks = total_size // block_size
        
        # Inisialisasi dengan satu blok besar yang kosong
        self.memory_blocks: List[MemoryBlock] = [
            MemoryBlock(0, self.total_blocks, True)
        ]
        
        # Tracking untuk statistik
        self.allocation_history = []
        self.fragmentation_events = 0
    
    def first_fit_allocate(self, size_needed: int, file_name: str) -> Optional[int]:
        """
        Algoritma First Fit untuk alokasi memori
        Returns: start_address jika berhasil, None jika gagal
        """
        blocks_needed = (size_needed + self.block_size - 1) // self.block_size  # Ceiling division
        
        # Cari blok kosong pertama yang cukup besar
        for i, block in enumerate(self.memory_blocks):
            if block.is_free and block.size >= blocks_needed:
                # Alokasikan blok
                allocated_block = MemoryBlock(block.start_address, blocks_needed, False)
                allocated_block.allocate(file_name)
                
                # Update blok yang ada
                if block.size == blocks_needed:
                    # Blok pas, ganti dengan blok yang dialokasikan
                    self.memory_blocks[i] = allocated_block
                else:
                    # Blok lebih besar, split menjadi dua
                    remaining_block = MemoryBlock(
                        block.start_address + blocks_needed,
                        block.size - blocks_needed,
                        True
                    )
                    
                    # Ganti blok lama dengan blok yang dialokasikan dan sisa
                    self.memory_blocks[i] = allocated_block
                    self.memory_blocks.insert(i + 1, remaining_block)
                
                # Catat history
                self.allocation_history.append({
                    'action': 'allocate',
                    'file_name': file_name,
                    'size': size_needed,
                    'blocks_used': blocks_needed,
                    'start_address': allocated_block.start_address,
                    'timestamp': datetime.now()
                })
                
                return allocated_block.start_address
        
        return None  # Tidak ada ruang yang cukup
    
    def deallocate(self, file_name: str) -> bool:
        """Dealokasi memori untuk file"""
        # Cari blok yang dialokasikan untuk file ini
        for i, block in enumerate(self.memory_blocks):
            if not block.is_free and block.file_name == file_name:
                # Dealokasi blok
                block.deallocate()
                
                # Gabungkan dengan blok kosong yang berdekatan
                self._merge_free_blocks()
                
                # Catat history
                self.allocation_history.append({
                    'action': 'deallocate',
                    'file_name': file_name,
                    'start_address': block.start_address,
                    'timestamp': datetime.now()
                })
                
                return True
        
        return False
    
    def _merge_free_blocks(self) -> None:
        """Gabungkan blok-blok kosong yang berdekatan untuk mengurangi fragmentasi"""
        if len(self.memory_blocks) <= 1:
            return
        
        merged = True
        while merged:
            merged = False
            new_blocks = []
            i = 0
            
            while i < len(self.memory_blocks):
                current_block = self.memory_blocks[i]
                
                if current_block.is_free and i + 1 < len(self.memory_blocks):
                    next_block = self.memory_blocks[i + 1]
                    
                    # Cek apakah blok bersebelahan dan keduanya kosong
                    if (next_block.is_free and 
                        current_block.get_end_address() + 1 == next_block.start_address):
                        
                        # Gabungkan blok
                        merged_block = MemoryBlock(
                            current_block.start_address,
                            current_block.size + next_block.size,
                            True
                        )
                        new_blocks.append(merged_block)
                        i += 2  # Skip next block karena sudah digabung
                        merged = True
                        self.fragmentation_events += 1
                    else:
                        new_blocks.append(current_block)
                        i += 1
                else:
                    new_blocks.append(current_block)
                    i += 1
            
            self.memory_blocks = new_blocks
    
    def get_memory_status(self) -> Dict:
        """Mendapatkan status memori"""
        total_free = sum(block.size for block in self.memory_blocks if block.is_free)
        total_used = sum(block.size for block in self.memory_blocks if not block.is_free)
        
        # Hitung fragmentasi
        free_blocks = [block for block in self.memory_blocks if block.is_free]
        largest_free_block = max([block.size for block in free_blocks], default=0)
        
        # Fragmentasi eksternal = total free - largest free block
        external_fragmentation = (total_free - largest_free_block) * self.block_size
        
        return {
            'total_blocks': self.total_blocks,
            'used_blocks': total_used,
            'free_blocks': total_free,
            'total_size_mb': self.total_size,
            'used_size_mb': total_used * self.block_size,
            'free_size_mb': total_free * self.block_size,
            'external_fragmentation_mb': external_fragmentation,
            'fragmentation_percentage': (external_fragmentation / self.total_size * 100) if self.total_size > 0 else 0,
            'number_of_free_segments': len(free_blocks),
            'largest_free_block_mb': largest_free_block * self.block_size
        }
    
    def get_memory_map(self) -> List[Dict]:
        """Mendapatkan peta memori untuk visualisasi"""
        memory_map = []
        
        for block in self.memory_blocks:
            memory_map.append({
                'start_address': block.start_address,
                'end_address': block.get_end_address(),
                'size': block.size,
                'size_mb': block.size * self.block_size,
                'is_free': block.is_free,
                'file_name': block.file_name,
                'allocated_time': block.allocated_time
            })
        
        return memory_map
    
    def get_allocation_history(self) -> List[Dict]:
        """Mendapatkan history alokasi"""
        return self.allocation_history.copy()

class FileSystemNode:
    """Representasi node dalam file system (file atau direktori)"""
    
    def __init__(self, name: str, node_type: str, parent: Optional['FileSystemNode'] = None):
        self.name = name
        self.type = node_type  # 'file' atau 'directory'
        self.parent = parent
        self.children: Dict[str, 'FileSystemNode'] = {}
        self.size = random.randint(4, 32) if node_type == 'file' else 0  # File: 4-32 MB (kelipatan 4)
        self.created = datetime.now()
        self.modified = datetime.now()
        self.permissions = "rwxr-xr--" if node_type == 'directory' else "rw-r--r--"
        self.memory_address = None  # Alamat memori jika file
    
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
    """Implementasi file system simulator dengan First Fit Memory Allocation"""
    
    def __init__(self, total_storage: int = 1024, block_size: int = 4):
        self.root = FileSystemNode('', 'directory')
        self.current_directory = self.root
        self.memory_manager = MemoryManager(total_storage, block_size)
        self.command_history = []
    
    def get_used_storage(self) -> int:
        """Mendapatkan storage yang sudah digunakan"""
        status = self.memory_manager.get_memory_status()
        return status['used_size_mb']
    
    def get_free_storage(self) -> int:
        """Mendapatkan storage yang masih tersedia"""
        status = self.memory_manager.get_memory_status()
        return status['free_size_mb']
    
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
                'permissions': child.permissions,
                'memory_address': child.memory_address
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
    
    def rm_recursive(self, name: str, force: bool = False) -> bool:
        """Menghapus file atau direktori secara recursive"""
        if not name:
            raise ValueError("Nama file/direktori diperlukan")
        
        target = self.current_directory.get_child(name)
        if not target:
            if force:
                return True  # Dengan -f, tidak error jika file tidak ada
            raise FileNotFoundError(f"'{name}' tidak ditemukan")
        
        # Jika ini adalah file, dealokasi memori dan hapus
        if target.type == 'file':
            if target.memory_address is not None:
                self.memory_manager.deallocate(target.name)
            self.current_directory.remove_child(name)
            self.command_history.append(f"rm {'-rf' if force else '-r'} {name}")
            return True
        
        # Jika ini adalah direktori, hapus secara recursive
        if target.type == 'directory':
            # Hapus semua children secara recursive
            children_names = list(target.children.keys())
            for child_name in children_names:
                child = target.get_child(child_name)
                if child.type == 'directory':
                    # Recursive call untuk subdirektori
                    self._remove_directory_recursive(child)
                else:
                    # Dealokasi memori dan hapus file
                    if child.memory_address is not None:
                        self.memory_manager.deallocate(child.name)
                    target.remove_child(child_name)
            
            # Setelah semua children dihapus, hapus direktori itu sendiri
            self.current_directory.remove_child(name)
            self.command_history.append(f"rm {'-rf' if force else '-r'} {name}")
            return True
        
        return False
    
    def _remove_directory_recursive(self, directory: FileSystemNode) -> None:
        """Helper function untuk menghapus direktori secara recursive"""
        # Hapus semua children terlebih dahulu
        children_names = list(directory.children.keys())
        for child_name in children_names:
            child = directory.get_child(child_name)
            if child.type == 'directory':
                # Recursive call untuk subdirektori
                self._remove_directory_recursive(child)
            else:
                # Dealokasi memori dan hapus file
                if child.memory_address is not None:
                    self.memory_manager.deallocate(child.name)
                directory.remove_child(child_name)
    
    def touch(self, name: str) -> bool:
        """Membuat file baru dengan alokasi memori First Fit"""
        if not name or '/' in name:
            raise ValueError("Nama file tidak valid")
        
        if self.current_directory.get_child(name):
            # Update modified time jika file sudah ada
            existing_file = self.current_directory.get_child(name)
            existing_file.modified = datetime.now()
            return True
        
        new_file = FileSystemNode(name, 'file')
        
        # Alokasi memori menggunakan First Fit
        memory_address = self.memory_manager.first_fit_allocate(new_file.size, name)
        
        if memory_address is None:
            raise OSError(f"Tidak dapat mengalokasikan memori untuk file '{name}'. Ruang tidak cukup atau terfragmentasi.")
        
        new_file.memory_address = memory_address
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
            raise IsADirectoryError(f"'{name}' adalah direktori. Gunakan rmdir atau rm -r")
        
        # Dealokasi memori
        if target.memory_address is not None:
            self.memory_manager.deallocate(name)
        
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
        """Copy file atau direktori dengan alokasi memori"""
        src_node = self.current_directory.get_child(source)
        if not src_node:
            raise FileNotFoundError(f"'{source}' tidak ditemukan")
        
        if self.current_directory.get_child(destination):
            raise FileExistsError(f"'{destination}' sudah ada")
        
        # Buat copy
        new_node = FileSystemNode(destination, src_node.type)
        new_node.size = src_node.size
        new_node.permissions = src_node.permissions
        
        # Jika file, alokasi memori
        if src_node.type == 'file':
            memory_address = self.memory_manager.first_fit_allocate(new_node.size, destination)
            if memory_address is None:
                raise OSError(f"Tidak dapat mengalokasikan memori untuk file '{destination}'. Ruang tidak cukup atau terfragmentasi.")
            new_node.memory_address = memory_address
        
        # Jika direktori, copy semua isi (recursive)
        if src_node.type == 'directory':
            self._copy_directory_contents(src_node, new_node)
        
        self.current_directory.add_child(new_node)
        self.command_history.append(f"cp {source} {destination}")
        return True
    
    def _copy_directory_contents(self, source: FileSystemNode, destination: FileSystemNode):
        """Helper untuk copy isi direktori secara recursive dengan alokasi memori"""
        for child in source.children.values():
            new_child = FileSystemNode(child.name, child.type)
            new_child.size = child.size
            new_child.permissions = child.permissions
            
            # Jika file, alokasi memori
            if child.type == 'file':
                memory_address = self.memory_manager.first_fit_allocate(new_child.size, new_child.name)
                if memory_address is not None:
                    new_child.memory_address = memory_address
                else:
                    continue  # Skip file jika tidak bisa dialokasikan
            
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
        
        # Update nama di memory manager jika file
        if src_node.type == 'file' and src_node.memory_address is not None:
            # Cari blok dan update nama file
            for block in self.memory_manager.memory_blocks:
                if not block.is_free and block.file_name == source:
                    block.file_name = destination
                    break
        
        # Remove dari parent dan ubah nama
        self.current_directory.remove_child(source)
        src_node.name = destination
        self.current_directory.add_child(src_node)
        
        self.command_history.append(f"mv {source} {destination}")
        return True
    
    def get_disk_usage(self) -> Dict:
        """Mendapatkan informasi penggunaan disk dengan info fragmentasi"""
        status = self.memory_manager.get_memory_status()
        
        return {
            'total': status['total_size_mb'],
            'used': status['used_size_mb'],
            'free': status['free_size_mb'],
            'usage_percent': (status['used_size_mb'] / status['total_size_mb'] * 100) if status['total_size_mb'] > 0 else 0,
            'external_fragmentation': status['external_fragmentation_mb'],
            'fragmentation_percent': status['fragmentation_percentage'],
            'free_segments': status['number_of_free_segments'],
            'largest_free_block': status['largest_free_block_mb']
        }
    
    def get_memory_status(self) -> Dict:
        """Mendapatkan status memori lengkap"""
        return self.memory_manager.get_memory_status()
    
    def get_memory_map(self) -> List[Dict]:
        """Mendapatkan peta memori untuk visualisasi"""
        return self.memory_manager.get_memory_map()
    
    def get_allocation_history(self) -> List[Dict]:
        """Mendapatkan history alokasi memori"""
        return self.memory_manager.get_allocation_history()
    
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
            
            # Tambahkan info alamat memori untuk file
            memory_info = f" [@{node.memory_address}]" if node.memory_address is not None else ""
            
            result.append({
                'name': node.name or '/',
                'type': node.type,
                'size': node.size if node.type == 'file' else None,
                'display': f"{prefix}{connector}{icon} {node.name or '/'}{memory_info}",
                'level': len(prefix) // 4,
                'memory_address': node.memory_address
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
        self.memory_manager.allocation_history.clear()
    
    def reset(self) -> None:
        """Reset file system ke kondisi awal"""
        self.__init__(self.memory_manager.total_size, self.memory_manager.block_size)
