class Output():
    def write(self, stream):
        pass


class StreamOutput(Output):
    def __init__(self, stream):
        self.sink = stream


    def write(self, stream):
        with open("StreamOutput.txt", "w") as fout:
            for line in stream:
                fout.write(f"{line}")


class Decorator(Output):
    def __init__(self, decorated):
        self.decorated = decorated
        #self.sink = self.decorated.sink

    def write(self, stream):
        pass


class BracketOutput(Decorator):
    def write(self, stream):
        new_sink = []
        for line in stream:
            new_line = f"[{line.strip()}]\n"
            new_sink.append(new_line)
        
        #self.decorated.sink = new_sink
        self.decorated.write(new_sink)


class NumberedOutput(Decorator):
    def write(self, stream):
        new_sink = []
        line_num = 1
        for line in stream:
            new_sink.append(f"{str(line_num).rjust(5)}: {line.strip()}")
            line_num += 1

        #self.decorated.sink = new_sink
        self.decorated.write(new_sink)


class TeeOutput(Decorator):
    def write(self, stream):
        new_sink = []
        new_fin = input("Please enter a file name, with a suffix of .txt, to tee the output too: ")
        with open(new_fin, 'w') as fout:
            for line in stream:
                fout.write(line)
                new_sink.append(line)
        
        print("Current stream written to ", new_fin)
        self.decorated.write(new_sink)


class FilterOutput(Decorator):
    def write(self, stream):
        new_sink = []
        choice = input("""
        Please select a filter:

        [1] Only write lines with parenthesis
        [2] Only write lines with the word "Python"

        ENTER CHOICE: """)

        if choice == '1':
            for line in stream:
                if '(' in line or ')' in line:
                    new_sink.append(line)

        else:
            for line in stream:
                if "Python" in line:
                    new_sink.append(line)
        
        print("\nFilter applied\n")
        self.decorated.write(new_sink)

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
        
        [1] Write Stream
        [2] Add Brackets
        [3] Add Line Numbers
        [4] Tee Output
        [5] Filter Output
        [6] Quit
                        
        ENTER CHOICE: ''')

        if choice == '1':
            stream_obj.write(stream_in)
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

        elif choice == '4':
            tee = TeeOutput(stream_obj)
            stream_obj = tee
            print('\nOutput Tee Created\n')

        elif choice == '5':
            filtered = FilterOutput(stream_obj)
            stream_obj = filtered
            print("\nFilter Created\n")

        else:
            print("\nGoodbye!\n")
            return False


main()

