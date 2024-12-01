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
        self.sequence.get_index = 0  # Ensure starting from the beginning

    def first(self):
        self.sequence.get_index = 0
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
        self.find_next_valid()

    def find_next_valid(self):
        '''Advance to the next valid element that satisfies the predicate'''
        while not self.iterator.isDone() and not self.predicate(self.iterator.current()):
            self.iterator.next()

    def first(self):
        self.iterator.first()
        self.find_next_valid()
        return self.current()

    def next(self):
        current_value = self.current()
        self.iterator.next()
        self.find_next_valid()
        return current_value

    def isDone(self):
        return self.iterator.isDone()

    def current(self):
        return self.iterator.current()


class ReverseIterator(Iterator):
    '''Decorator that iterates through items in an Iterator in reverse order'''

    def __init__(self, iterator):
        self.stack = []
        # Load all elements into the stack
        while not iterator.isDone():
            self.stack.append(iterator.current())
            iterator.next()
        self.index = len(self.stack) - 1

    def first(self):
        self.index = len(self.stack) - 1
        return self.stack[self.index] if self.index >= 0 else None

    def next(self):
        if not self.isDone():
            element = self.stack[self.index]
            self.index -= 1
            return element
        return None

    def isDone(self):
        return self.index < 0

    def current(self):
        return self.stack[self.index] if self.index >= 0 else None


def main():
    # Create a MyArray instance and add some elements
    my_array = MyArray(10)
    my_array.add(10)
    my_array.add(20)
    my_array.add(30)
    my_array.add(40)
    my_array.add(50)

    # Original iterator
    iterator = my_array.getIterator()

    # 1. FilterIterator with predicate to filter even numbers
    even_filter = FilterIterator(iterator, lambda x: x is not None and x % 2 == 0)
    print("FilterIterator (Even Numbers):")
    while not even_filter.isDone():
        print(even_filter.next())

    # Reset iterator
    iterator = my_array.getIterator()

    # 2. FilterIterator filtering another FilterIterator (e.g., filter > 20 after filtering evens)
    greater_than_20_filter = FilterIterator(FilterIterator(iterator, lambda x: x is not None and x % 2 == 0), lambda x: x > 20)
    print("\nFilterIterator (Even Numbers > 20):")
    while not greater_than_20_filter.isDone():
        print(greater_than_20_filter.next())

    # Reset iterator
    iterator = my_array.getIterator()

    # 3. FilterIterator that filters out everything (returns None)
    null_filter = FilterIterator(iterator, lambda x: False)
    print("\nFilterIterator (Filters Out Everything):")
    while not null_filter.isDone():
        print(null_filter.next())  # Should print None or not print at all

    # Reset iterator
    iterator = my_array.getIterator()

    # 4. ReverseIterator
    reverse_iterator = ReverseIterator(iterator)
    print("\nReverseIterator:")
    while not reverse_iterator.isDone():
        print(reverse_iterator.next())

    # 5. ReverseIterator that takes a FilterIterator (Even numbers in reverse order)
    iterator = my_array.getIterator()  # Reset iterator
    even_filter = FilterIterator(iterator, lambda x: x is not None and x % 2 == 0)
    reverse_even_filter = ReverseIterator(even_filter)
    print("\nReverseIterator with FilterIterator (Even Numbers in Reverse):")
    while not reverse_even_filter.isDone():
        print(reverse_even_filter.next())


main()
