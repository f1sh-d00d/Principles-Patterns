from collections import deque


class Queue():
    '''base class for queue'''
    def __init__(self, imp_obj):
        self.queue_imp = imp_obj


    def changeImp(self, new_imp):
        new_imp.clear()
        for val in self.queue_imp.storage:
            new_imp.add(val)
        self.queue_imp = new_imp


    def add(self, val):
        self.queue_imp.add(val)


    def get(self):
        return self.queue_imp.get()


    def remove(self):
       return self.queue_imp.remove()


    def size(self):
        return self.queue_imp.size()


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
        pass

    def clear(self):
        pass


class PyList(QueueImp):
    '''class for array type queues. this functions as the list type build into python'''
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
    '''class for linked type queues. this fuctions as the deque type built into python collections'''
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
    print("STRING QUEUE")
    pylist = PyList()
    print("Created a PyList object")
    q1 = Queue(pylist)          #create a Queue from python's built in list
    print("Created a Queue object with a list as its implementation\n")
    q1.add("this")              #add via the list implementaion
    print('Added "this" to the queue')
    q1.add("is")
    print('Added "is" to the queue')
    q1.add("a")
    print('Added "a" to the queue\n')
    mydeque = MyDeque()
    print("Created a MyDeque object")
    q1.changeImp(mydeque)       #change to a deque
    print("Changed Queue implementation to a deque\n")
    q1.add("string")            #add via deque
    print('Added "string" to the queue')
    q1.add("queue")
    print('Added "queue" to the queue\n')
    print("Current Queue:")
    print(q1)
    print("\nqueue.get()")
    print(q1.get())             #get via deque
    q1.remove()                 #remove via deque
    print("\nRemoved first element from queue\nCurrent Queue:")
    print(q1,"\n")
    q1.changeImp(pylist)        #change back to pylist
    print("Change queue implementation back to pylist\n\nCurrent Queue size: ")
    print(q1.size(),"\n")       #size via pylist
    q1.clear()                  #clear via pylist
    print("Cleared Queue\nSize after clearing queue:")
    print(q1.size())            #check size after clear


def int_queue():
    print("\nINT QUEUE")
    mydeque = MyDeque()
    print("Created a MyDeque object")
    q2 = Queue(mydeque)
    print("Created a Queue object with a deque as its implementation")
    q2.add(1)
    print("\nAdded 1 to the queue")
    q2.add(2)
    print("Added 2 to the queue")
    q2.add(3)
    print("Added 3 to the queue\n")
    pylist = PyList()
    print("Created a PyList object")
    q2.changeImp(pylist)
    print("Changed Queue implementation to a pylist\n")
    q2.add(4)
    print("Added 4 to the queue")
    q2.add(5)
    print("Added 5 to the queue\n")
    print("Current Queue:")
    print(q2,"\n")
    print("queue.get()")
    print(q2.get())
    q2.remove()
    print("\nRemoved first element from the queue\nCurrent Queue:")
    print(q2)
    q2.changeImp(mydeque)
    print("\nChanged implementation back to deque\n\nCurrent Queue size:")
    print(q2.size())
    q2.clear()
    print("Cleared Queue\nSize after clearing queue:")
    print(q2.size())


def main():
    string_queue()
    int_queue()

if __name__ == "__main__":
    main()
