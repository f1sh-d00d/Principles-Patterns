import sys


class Database:
    def __init__(self, db_id):
        self.db_id = db_id
        self.data = {}
        self.file_name = "Output.txt"

    def getId(self):
        return self.db_id

    def add(self, key, value):
       self.data[key] = value

    def get(self, key):
        return self.data[key]

    def update(self, key, value):
        self.data[key] = value

    def remove(self, key):
        if key not in self.data:
            with open (self.file_name, "a") as fout:
                fout.write(f"Error: Key '{key}' not found in database '{self.db_id}'.\n")
            return False
        del self.data[key]

    def display(self, fout):
        fout.write(f"Database {self.db_id}:\n")
        for key, value in self.data.items():
            fout.write(f"{key}| {value}\n")
        fout.write("\n")


class Command:
    def __init__(self):
        self.file_name = "Output.txt"
        self.failed = False

    def execute(self):
        pass

    def undo(self):
        pass


class AddCommand(Command):
    def __init__(self, database, key, value):
        super().__init__()
        self.database = database
        self.key = key
        self.value = value

    def execute(self):
        if self.key in self.database.data:
            with open(self.file_name, "a") as fout:
                fout.write(f"Key '{self.key}' already exists in database '{self.database.getId()}'\n")
                self.failed = True
        else:
            self.database.add(self.key, self.value)
        
    def undo(self):
        if self.failed:
            with open(self.file_name, "a") as fout:
                fout.write(f"Cannot undo Add Command because Add Command did not execute\n")
        else:
            with open(self.file_name, 'a') as fout:
                fout.write(f"Undoing Add Command\n")
                self.database.display(fout)
            self.database.remove(self.key)


class UpdateCommand(Command):
    def __init__(self, database, key, value):
        super().__init__()
        self.database = database
        self.key = key
        self.new_value = value
        self.old_value = None

    def execute(self):
        if self.key not in self.database.data:
            with open(self.file_name, "a") as fout:
                fout.write(f"Key '{self.key}' not in database '{self.database.getId()}'\n")
            self.failed = True
        else:
            self.old_value = self.database.data[self.key]
            self.database.update(self.key, self.new_value)
    
    def undo(self):
        if self.failed:
            with open(self.file_name, 'a') as fout:
                fout.write(f"Cannot undo Update Command because Update Command did not execute\n")
        else:
            with open(self.file_name, "a") as fout:
                fout.write(f"Undoing Update Command\n")
                self.database.display(fout)
                self.database.update(self.key, self.old_value)


class RemoveCommand(Command):
    def __init__(self, database, key):
        super().__init__()
        self.database = database
        self.key = key
        self.old_value = None

    def execute(self):
        if self.key not in self.database.data:
            with open(self.file_name, "a") as fout:
                fout.write(f"Key '{self.key}' not in database '{self.database.getId()}'\n")
            self.failed = True
        else:
            self.old_value = self.database.data[self.key]
            self.database.remove(self.key)

    def undo(self):
        if self.failed:
            with open(self.file_name, 'a') as fout:
                fout.write(f"Cannot undo Remove Command because Remove Command did not execute\n")
        else:
            with open(self.file_name, 'a') as fout:
                fout.write(f"Undoing Remove Command\n")
                self.database.display(fout)
            self.database.add(self.key, self.old_value)


class MacroCommand(Command):
    def __init__(self):
        super().__init__()
        self.commands = []

    def add_command(self, command):
        self.commands.append(command)

    def execute(self):
        with open(self.file_name, "a") as fout:
            fout.write("\nBeginning a Macro\n")
            for command in self.commands:
                command.execute()
            fout.write("Ending a Macro\n\n")

    def undo(self):
        with open(self.file_name, "a") as fout:
            fout.write("\nBegin Undoing Macro\n")
        
        for command in reversed(self.commands):
            command.undo()

        with open(self.file_name, "a") as fout:    
            fout.write("End Undoing Macro\n\n")


class Invoker:
    def __init__(self):
        self.databases = []
        self.commands = []
        self.macro_stack = []  # Stack to support nested macros
        self.file_name = "Output.txt"

    def printDatabases(self):
        with open(self.file_name, "a") as fout:
            fout.write("Contents of databases:\n")
            for db in self.databases:   
                db.display(fout)

    def getDb(self, db_id):
        for db in self.databases:
            if db.getId() == db_id:
                return db

        new_db = Database(db_id)
        self.databases.append(new_db)
        return new_db

    def processFile(self, file_name):
        with open(file_name, 'r') as fin:
            lines = fin.readlines()
            for line in lines:
                line = line.strip().split()
                command = line[0]
                match command:
                    case "A":
                        db = self.getDb(line[1])
                        key = line[2]
                        value = " ".join(line[3:])
                        add = AddCommand(db, key, value)
                        if self.macro_stack:
                            self.macro_stack[-1].commands.append(add)
                        else:
                            self.commands.append(add)

                    case "B":
                        macro = MacroCommand()
                        self.macro_stack.append(macro)

                    case "E":
                        completed_macro = self.macro_stack.pop()
                        if self.macro_stack:
                            self.macro_stack[-1].commands.append(completed_macro)
                        else:
                            self.commands.append(completed_macro)

                    case "R":
                        db = self.getDb(line[1])
                        key = line[2]
                        remove = RemoveCommand(db, key)
                        if self.macro_stack:
                            self.macro_stack[-1].commands.append(remove)
                        else:
                            self.commands.append(remove)

                    case "U":
                        db = self.getDb(line[1])
                        key = line[2]
                        value = " ".join(line[3:])
                        update = UpdateCommand(db, key, value)
                        if self.macro_stack:
                            self.macro_stack[-1].commands.append(update)
                        else:
                            self.commands.append(update)

    def undoAll(self):
        for command in reversed(self.commands):
            command.undo()

    def executeAll(self):
        for command in self.commands:
            command.execute()
def main():
    invoker = Invoker()
    file_name = sys.argv[1]
    invoker.processFile(file_name)
    invoker.executeAll()
    invoker.printDatabases()
    invoker.undoAll()
    invoker.printDatabases()

if __name__ == "__main__":
    main()
