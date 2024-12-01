class Iterator:
    '''Generic Iterator Class'''

    def first(self):
        '''Get the first item in the sequence.'''
        pass

    def next(self):
        '''Get the next item in the sequence'''
        pass

    def isDone(self):
        '''Bool - indicates end of sequence'''
        pass

    def current(self):
        '''Get current element in sequence'''
        pass


class Iterable:
    '''Generic Iterable Class'''

    def getIterator(self):
        '''return an Iterator object specific to the iterable'''
        pass


class Sequence:
    '''Generic Sequence Class'''

    def add(self, val):
        '''Add value to sequence'''
        pass

    def size(self):
        '''Return Sequence size (Fixed)'''
        pass

    def capacity(self):
        '''Get number of elements in Sequence'''
        pass

    def get(self, index):
        '''get element at specific index'''
        pass


class IterableSequence(Iterable, Sequence):
    '''Concrete Iterable Sequence'''

    def __init__(self, size):
        self.size = size
        self.array = [None for i in range(size)]
        self.get_index = 0
        self.add_index = 0


class MyArray(IterableSequence):
    '''Concrete Iterable Sequence'''
    def __init__(self, size):
        super().__init__(size)

    def add(self, val):
        if self.add_index < self.size:                          # as long as there is space for one more element
            self.array[self.add_index] = val
            self.add_index += 1
        else:
            print("Array is full; unable to add more values")

    def size(self):
        return self.size

    def capacity(self):
        return self.add_index

    def get(self, index):
        if index < self.size:
            return self.array[index]
        else:
            print("Index out of range")
            return None

    def getIterator(self):
        return MyIterator(self)


class MyIterator(Iterator):
    '''Concrete Iterator'''
    def __init__(self, iterable):
        self.sequence = iterable
        self.array = self.sequence.array
        self.sequence.get_index = 0                             #ensure starting from the beginning

    def first(self):
        return self.sequence.get(0)

    def next(self):
        if not self.isDone():
            current_element = self.sequence.get(self.sequence.get_index)
            self.sequence.get_index += 1
            return current_element
        return None

    def isDone(self):
        return self.sequence.get_index >= self.sequence.add_index

    def current(self):
        if not self.isDone():
            return self.sequence.get(self.sequence.get_index)
        return None


class FilterIterator(Iterator):
    '''Decorator that filters items in an Iterator based on a predicate function'''

    def __init__(self, iterator, predicate):
        self.iterator = iterator
        self.predicate = predicate
        self.array = []
        self.get_index = 0

        for val in self.iterator.array:
            if predicate(val):
                self.array.append(val)
        
    def filterArray(self, array):
        new_array = []
        for val in array:
            if self.predicate(val):
                new_array.append(val)
        return new_array

    def first(self):
        return self.array[0]

    def next(self):
        if not self.isDone():
            val = self.array[self.get_index]
            self.get_index += 1
            return val

    def isDone(self):
        if self.get_index >= len(self.array):
            return True
        else:
            return False

    def current(self):
        return self.array[self.get_index]


class ReverseIterator(Iterator):
    '''Decorator that iterates through items in an Iterator in reverse order'''

    def __init__(self, iterator):
        self.iterator = iterator
        self.array = []
        self.get_index = 0

        for val in iterator.array[::-1]:
            if val is not None:
                self.array.append(val)

    def first(self):
        return self.array[0]

    def next(self):
        if not self.isDone():
            val = self.array[self.get_index]
            self.get_index += 1
            return val

    def isDone(self):
        if self.get_index >= len(self.array):
            return True
        else:
            return False

    def current(self):
        return self.array[self.get_index]


def main():
    int_array = MyArray(10)
    int_array.add(10)
    int_array.add(20)
    int_array.add(31)
    int_array.add(40)
    int_array.add(51)
    int_array.add(100)

    #create iterator 
    int_iterator = int_array.getIterator()
    print("Full IntArray:")
    while int_iterator.isDone() == False:
        print(int_iterator.next())
    print()

    str_array = MyArray(5)
    str_array.add("I")
    str_array.add("Am")
    str_array.add("A")
    str_array.add("String")
    str_array.add("Array")
    str_iterator = str_array.getIterator()
    
    print("Full Str Array:")
    while str_iterator.isDone() == False:
        print(str_iterator.next())
    print()
    
    print("1. Over two types of elements (int and str)")
    even_filter = FilterIterator(int_iterator, lambda x: True if x != None and x % 2 == 0 else False)
    print("FilterIterator (Even Numbers):")
    while even_filter.isDone() == False:
        print(even_filter.next())
    print()

    len_filter = FilterIterator(str_iterator, lambda x: True if len(x) > 3 else False)
    print("FilterIterator (Strings > 3 Characters):")
    while len_filter.isDone() == False:
        print(len_filter.next())
    print()

    print("2. A FilterIterator that filters results from another FilterIterator")
    print("Filtering numbers < 50 from even numbers")
    less_filter = FilterIterator(even_filter, lambda x: True if x < 50 else False)
    while less_filter.isDone() == False:
        print(less_filter.next())
    print()

    print("3. FilterIterator that filters out everything")
    null_filter = FilterIterator(str_iterator, lambda x: False)
    while null_filter.isDone() == False:
        print(null_filter.next())
    print("\n")

    print("4. A Reverse Iterator")
    reverse_iterator = ReverseIterator(str_iterator)
    print("ReverseIterator:")
    while reverse_iterator.isDone() == False:
        print(reverse_iterator.next())
    print()

    print("5. ReverseIterator that takes a FilterIterator (Even numbers in reverse order)")
    reverse_even_filter = ReverseIterator(even_filter)
    while reverse_even_filter.isDone() == False:
        print(reverse_even_filter.next())
    print()

main()
