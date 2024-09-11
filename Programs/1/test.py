from collections import deque
from abc import ABC, abstractmethod


class Queue():
    '''base class for queue'''
    def __init__(self, imp_obj):
        self.queue_imp = imp_obj


    def changeImp(self, new_imp):
        new_imp.clear
        for val in self.queue_imp.storage:
            new_imp.add(val)
        self.queue_imp = new_imp


    def add(self, val):
        self.queue_imp.add(val)


    def get(self):
        return self.queue_imp.get()


    def remove(self):
        self.queue_imp.remove()


    def size(self):
        self.queue_imp.size()


    def clear(self):
        self.queue_imp.clear()


    def __str__(self):  
        self.print_array = []
        for val in self.queue_imp.storage:
            self.print_array.append(val)
        return str(self.print_array)


class QueueImp():
    '''Interface for queue implementaion'''

    def __init__(self):
        pass

    
    def add(self, val):
        pass


    def get(self):
        pass


    def remove(self):
        pass


    def size(self):
        return int(0)


    def clear(self):
        pass


class PyList(QueueImp):
    '''class for array type queues'''
    def __init__(self):
        self.storage = []

    
    def add(self, val):
        self.storage.append(val)

    
    def get(self):
        return self.storage[0]


    def remove(self):
        self.storage.pop(0)


    def size(self):
        return len(self.storage)

    
    def clear(self):
        self.storage = []


class MyDeque(QueueImp):
    '''class for linked type queues'''
    def __init__(self):
        self.storage = deque()


    def add(self, val):
        self.storage.append(val)


    def get(self):
        first_ele = self.storage[0]
        #print(first_ele)
        #print(type(first_ele))
        return first_ele


    def remove(self):
        self.storage.popleft()


    def size(self):
        return len(self.storage)

    def clear(self):
        self.storage = deque([])
 


def string_queue():
    pylist = PyList()
    q1 = Queue(pylist)          #create a Queue from python's built in list
    q1.add("this")              #add via the list implementaion
    q1.add("is")
    q1.add("a")
    mydeque = MyDeque()
    q1.changeImp(mydeque)       #change to a deque
    q1.add("string")            #add via deque
    q1.add("queue")
    print(q1)
    first_ele = q1.get()
    print(first_ele)             #get via deque



def main():
  string_queue()


if __name__ == "__main__":
    main()
