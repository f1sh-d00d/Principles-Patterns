class FileSystemComponent:
    """Generic class for components in the file system."""
    def __init__(self, name):
        self.name = name
        self.parent = None

    def accept(self, visitor):
        pass


class File(FileSystemComponent):
    """Concrete implementation for files."""
    def accept(self, visitor):
        visitor.visit_file(self)


class Directory(FileSystemComponent):
    """Concrete implementation for directories."""
    def __init__(self, name):
        super().__init__(name)
        self.children = {}                                      #init directory to keep track of children

    def add(self, component):
        self.children[component.name] = component
        component.parent = self

    def get_child(self, name):
        return self.children.get(name)

    def accept(self, visitor):
        visitor.visit_directory(self)


class Visitor:
    """Base Visitor class."""
    def visit_file(self, file):
        pass

    def visit_directory(self, directory):
        pass


class ListVisitor(Visitor):
    """Visitor for listing items in a directory."""
    def __init__(self):
        self.result = []

    def visit_file(self, file):
        self.result.append(file.name)

    def visit_directory(self, directory):
        self.result.extend(directory.children.keys())           #collect names of all children

    def get_result(self):
        return " ".join(self.result)


class ListAllVisitor(Visitor):
    """Visitor for listing all items recursively."""
    def __init__(self):
        self.result = []
        self.level = 0                                          #track depth for indentation

    def visit_file(self, file):
        self.result.append(" " * (self.level * 3) + file.name)

    def visit_directory(self, directory):
        self.result.append(" " * (self.level * 3) + directory.name + ":")
        self.level += 1
        for child in directory.children.values():
            child.accept(self)                                  #visit each child
        self.level -= 1                                         #reduce depth after visiting children

    def get_result(self):
        return "\n".join(self.result)


class CountVisitor(Visitor):                        
    """Visitor for counting files in a directory."""
    def __init__(self):
        self.count = 0

    def visit_file(self, file):
        self.count += 1

    def get_count(self):
        return self.count


class CountAllVisitor(Visitor):
    """Visitor for counting all items recursively."""
    def __init__(self):
        self.count = 0

    def visit_file(self, file):
        self.count += 1

    def visit_directory(self, directory):
        self.count += 1                                     #count the directory itself
        for child in directory.children.values():
            child.accept(self)                              #count files and subdirectories

    def get_count(self):
        return self.count


class DirectoryFactory:
    """Class to generate file hierarchy from input file."""
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


class FindVisitor(Visitor):
    """Visitor for finding entries with a specific name."""
    def __init__(self, target_name):
        self.target_name = target_name
        self.matches = []
        self.level = 0

    def visit_file(self, file):
        if file.name == self.target_name:
            self.matches.append(("file", " " * (self.level * 3) + file.name))

    def visit_directory(self, directory):
        if directory.name == self.target_name:
            self.matches.append(("directory", " " * (self.level * 3) + directory.name + ":"))
        self.level += 1
        for child in directory.children.values():
            child.accept(self)
        self.level -= 1

    def get_result(self):
        return self.matches


class CountDirsVisitor(Visitor):
    """Visitor for counting directories."""
    def __init__(self):
        self.count = 0

    def visit_file(self, file):
        pass                                                #ignore files

    def visit_directory(self, directory):
        self.count += 1                                     #count the directory itself
        for child in directory.children.values():
            child.accept(self)

    def get_count(self):
        return self.count


class Explorer:
    """Class to provide a user interface for directory traversal."""
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
                visitor = ListVisitor()
                self.current_directory.accept(visitor)
                print(visitor.get_result())
            elif action == "listall":
                visitor = ListAllVisitor()
                self.current_directory.accept(visitor)
                print(visitor.get_result())
            elif action == "count":
                visitor = CountVisitor()
                self.current_directory.accept(visitor)
                print(visitor.get_count())
            elif action == "countall":
                visitor = CountAllVisitor()
                self.current_directory.accept(visitor)
                print(visitor.get_count())
            elif action == "find":
                if len(command) < 2:
                    print("invalid command")
                else:
                    self.find_entry(command[1])
            elif action == "countdirs":
                visitor = CountDirsVisitor()
                self.current_directory.accept(visitor)
                print(visitor.get_count())
            elif action == "chdir":
                if len(command) < 2:
                    print("invalid command")
                else:
                    self.change_directory(command[1])
            elif action == "up":
                self.go_up()
            elif action == "q":
                break
            else:
                print("invalid command")

    def find_entry(self, name):
        """Find entries with the specified name."""
        visitor = FindVisitor(name)
        self.current_directory.accept(visitor)
        results = visitor.get_result()
        if not results:
            print(f"No entry found with name '{name}'")
        else:
            for entry_type, entry in results:
                if entry_type == "file":
                    print(f"Found file: {entry.strip()}")
                elif entry_type == "directory":
                    print(f"Found directory: {entry.strip()}")
                    #traverse the directory tree to find the actual Directory object
                    listall_visitor = ListAllVisitor()
                    for child in self.current_directory.children.values():
                        if isinstance(child, Directory) and child.name == name:
                            child.accept(listall_visitor)
                            print(listall_visitor.get_result())
                            break   

    def change_directory(self, name):
        target = self.current_directory.get_child(name)
        if isinstance(target, Directory):
            self.current_directory = target
        else:
            print("no such directory")

    def go_up(self):
        """Move up to the parent directory."""
        if self.current_directory.parent is not None:
            self.current_directory = self.current_directory.parent
        else:
            print("no parent directory")


def main():
    """Main function to start the Explorer."""
    #set up the directory
    with open("directory.dat") as f:
        directory_tree = DirectoryFactory.create_dir_tree(f.readlines())

    #start the Explorer
    explorer = Explorer(directory_tree)
    explorer.process()


if __name__ == "__main__":
    main()
