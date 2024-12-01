#FIXME -- make write take a streamable argument

class Output():
    def write(self):
        pass


class StreamOutput(Output):
    def __init__(self, stream):
        self.sink = stream


    def write(self):
        with open("StreamOutput.txt", "w") as fout:
            for line in self.sink:
                fout.write(f"{line}")


class Decorator(Output):
    def __init__(self, decorated):
        self.decorated = decorated
        self.sink = self.decorated.sink

    def write(self):
        pass


class BracketOutput(Decorator):
    def write(self):
        new_sink = []
        for line in self.sink:
            new_line = f"[{line.strip()}]\n"
            new_sink.append(new_line)
        
        self.decorated.sink = new_sink
        self.decorated.write()


class NumberedOutput(Decorator):
    def write(self):
        new_sink = []
        line_num = 1
        for line in self.sink:
            new_sink.append(f"{str(line_num).rjust(5)}: {line.strip()}")
            line_num += 1

        self.decorated.sink = new_sink
        self.decorated.write()


def main():

    fin_name = input("Please input a file name: ")
    stream_in = []
    
    with open(fin_name, 'r') as fin:
        fin_list = list(fin)
        for line in fin_list:
            stream_in.append(line.strip())

    #print(stream_in)
    stream_obj = StreamOutput(stream_in)
    print("File uploaded")

    while True:
        choice = input('''
        What would you like to do?
        
        [1] Write stream
        [2] Add Brackets
        [3] Add Line Numbers
        [4] Quit
                        
        ENTER CHOICE: ''')

        if choice == '1':
            stream_obj.write()
            print("\nOuptut written to StreamOutput.txt")
            return False

        elif choice == '2':
            brackets = BracketOutput(stream_obj)
            stream_obj = brackets
            print("\nBrackets added\n")

        elif choice == '3':
            line_nums = NumberedOutput(stream_obj)
            stream_obj = line_nums
            print('\nLine Numbers Added\n')

        else:
            print("\nGoodbye!\n")
            return False


main()

