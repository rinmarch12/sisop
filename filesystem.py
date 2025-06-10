class Node:
    def __init__(self, name, is_folder):
        self.name = name
        self.is_folder = is_folder
        self.children = {} if is_folder else None
        self.content = "" if not is_folder else None


class FileSystem:
    def __init__(self):
        self.root = Node("root", True)
        self.current_node = self.root
        self.path = ["root"]

    def mkdir(self, name):
        if name in self.current_node.children:
            return f"Folder '{name}' sudah ada."
        self.current_node.children[name] = Node(name, True)
        return f"Folder '{name}' berhasil dibuat."

    def touch(self, name):
        if name in self.current_node.children:
            return f"File '{name}' sudah ada."
        self.current_node.children[name] = Node(name, False)
        return f"File '{name}' berhasil dibuat."

    def ls_recursive(self, node=None, prefix=""):
        if node is None:
            node = self.current_node
        
        result = []
        for name, child in sorted(node.children.items()):
            if child.is_folder:
                result.append(f"{prefix}📁 {name}/")
                # Rekursif untuk folder
                child_content = self.ls_recursive(child, prefix + "  ")
                if child_content:
                    result.extend(child_content)
            else:
                result.append(f"{prefix}📄 {name}")
        
        return result

    def ls(self, recursive=False):
        if not self.current_node.children:
            return "Direktori kosong"
        
        if recursive:
            result = self.ls_recursive()
        else:
            result = []
            for name, node in sorted(self.current_node.children.items()):
                if node.is_folder:
                    result.append(f"📁 {name}/")
                else:
                    result.append(f"📄 {name}")
        
        return "\n".join(result)

    def cd(self, path):
        if path == "..":
            if len(self.path) > 1:
                self.path.pop()
                current = self.root
                for dir_name in self.path[1:]:
                    current = current.children[dir_name]
                self.current_node = current
                return f"Pindah ke direktori '{'/'.join(self.path)}'"
            return "Sudah berada di root"
        
        if path not in self.current_node.children:
            return f"Direktori '{path}' tidak ditemukan"
        
        node = self.current_node.children[path]
        if not node.is_folder:
            return f"'{path}' bukan direktori"
        
        self.current_node = node
        self.path.append(path)
        return f"Pindah ke direktori '{'/'.join(self.path)}'"

    def rm(self, name):
        if name not in self.current_node.children:
            return f"'{name}' tidak ditemukan"
        del self.current_node.children[name]
        return f"'{name}' berhasil dihapus"

    def cat(self, name):
        if name not in self.current_node.children:
            return f"File '{name}' tidak ditemukan"
        node = self.current_node.children[name]
        if node.is_folder:
            return f"'{name}' adalah folder, bukan file"
        return node.content if node.content else f"(File '{name}' kosong)"

    def write(self, name, content):
        if name not in self.current_node.children:
            return f"File '{name}' tidak ditemukan"
        node = self.current_node.children[name]
        if node.is_folder:
            return f"'{name}' adalah folder, bukan file"
        node.content = content
        return f"Berhasil menulis ke file '{name}'"

    def pwd(self):
        return '/'.join(self.path)
