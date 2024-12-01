class FileSystemComponent:
    '''Generic class for componenets in the file system'''
    def __init__(self, name):
        self.name = name

    def list(self):
        pass

    def list_all(self, level):
        pass

    def count_files(self):
        pass

    def count_files_all(self):
        pass


class File(FileSystemComponent):
    '''Concrete implementation for files'''
    def list(self):
        return self.name

    def list_all(self, level=0):
        print(" " * (level * 3) + self.name)

    def count_files(self):
        return 1

    def count_files_all(self):
        return 1


class Directory(FileSystemComponent):
    '''Concrete implementation for directories'''
    def __init__(self, name):
        super().__init__(name)
        self.children = {}                              #init dir to keep track of children

    def add(self, component):
        self.children[component.name] = component

    def get_child(self, name):
        return self.children.get(name)

    def list(self):
        return " ".join(self.children.keys())           #list children horizontally

    def list_all(self, level=0):
        '''List children and their contentents recursively, and vertically'''
        print(" " * (level * 3) + self.name + ":")
        for child in self.children.values():
            child.list_all(level + 1)                   #print contents of children, increasing level with each call

    def count_files(self):
        return sum(1 for child in self.children.values() if isinstance(child, File))

    def count_files_all(self):
        return sum(child.count_files_all() for child in self.children.values())


class DirectoryFactory:
    '''Class with a class method to generate file heirarchy from input file'''
    @staticmethod
    def create_dir_tree(input_lines):
        root = None
        stack = []
        for line in input_lines:
            depth = line.count("   ")
            name = line.strip()
            if name.endswith(":"):
                directory = Directory(name[:-1])
                if depth == 0:
                    root = directory
                else:
                    stack[depth - 1].add(directory)
                if depth < len(stack):
                    stack[depth] = directory
                else:
                    stack.append(directory)
            else:
                file = File(name)
                stack[depth - 1].add(file)
        return root


class Explorer:
    '''Class to provide user interface'''
    def __init__(self, root):
        self.current_directory = root
        self.root = root

    def process(self):
        while True:
            command = input(f"{self.current_directory.name}> ").strip().split()
            if not command:
                print("invalid command")
                continue
            action = command[0]
            if action == "list":
                print(self.current_directory.list())
            elif action == "listall":
                self.current_directory.list_all()
            elif action == "chdir":
                if len(command) < 2:
                    print("invalid command")
                else:
                    self.change_directory(command[1])
            elif action == "up":
                self.go_up()
            elif action == "count":
                print(self.current_directory.count_files())
            elif action == "countall":
                print(self.current_directory.count_files_all())
            elif action == "q":
                break
            else:
                print("invalid command")

    def change_directory(self, name):
        target = self.current_directory.get_child(name)
        if isinstance(target, Directory):
            self.current_directory = target
        else:
            print("no such directory")

    def go_up(self):
        if self.current_directory != self.root:
            for directory in self.root.children.values():
                if directory == self.current_directory:
                    self.current_directory = self.root
                    return
                elif isinstance(directory, Directory):
                    parent = self.find_parent(directory, self.current_directory)
                    if parent:
                        self.current_directory = parent
                        return
        print("no parent directory")

    def find_parent(self, parent, target):
        if target in parent.children.values():
            return parent
        for child in parent.children.values():
            if isinstance(child, Directory):
                found_parent = self.find_parent(child, target)
                if found_parent:
                    return found_parent
        return None


def main():
    #set up the directory
    with open("directory.dat") as f:
        directory_tree = DirectoryFactory.create_dir_tree(f.readlines())

    #tart the Explorer
    explorer = Explorer(directory_tree)
    explorer.process()


main()
