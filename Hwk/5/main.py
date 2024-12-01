class Shape:
    def __init__(self):
        self.name = None
        self.x = 0
        self.y = 0
        self.color = "Black"

    def setLocation(self, x, y):
        self.x = x
        self.y = y

    def getLocation(self):
        if self.x and self.y:
            print(f"{self.name} is located at ({self.x}, {self.y}")

    def display(self):
        pass

    def fill(self):
        pass

    def setColor(self, color):
        self.color = color

    def undisplay(self):
        pass


class Point(Shape):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def display(self):
        print(f"Displaying Point '{self.name}'")

    def fill(self):
        print(f"Filling Point '{self.name}' with {self.color}")

    def undisplay(self):
        print(f"Undisplaying Point '{self.name}'")


class Line(Shape):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def display(self):
        print(f"Displaying Line '{self.name}'")

    def fill(self):
        print(f"Filling Line '{self.name}' with {self.color}")

    def undisplay(self):
        print(f"Undisplaying Line '{self.name}'")


class Rectangle(Shape):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def display(self):
        print(f"Displaying Rectangle '{self.name}'")

    def fill(self):
        print(f"Filling Rectangle '{self.name}' with {self.color}")

    def undisplay(self):
        print(f"Undisplaying Rectangle '{self.name}'")



class CircleAdapter(Shape):
    def __init__(self, circle_obj):
        self.circ = circle_obj

    def setLocation(self, x, y):
        self.circ.setLocation(x, y)

    def getLocation(self):
        self.circ.getLocation()

    def display(self):
        self.circ.displayIt()

    def fill(self):
        self.circ.fillIt()

    def setColor(self, color):
        self.circ.setItsColor(color)

    def undisplay(self):
        self.circ.undisplayIt()


class XXCircle:
    def __init__(self, name):
        self.name = name
        self.x = 0
        self.y = 0
        self.color = "Black"

    def setLocation(self, x, y):
        self.x = x
        self.y = y

    def getLocation(self):
        print(f"{self.name} is at ({self.x}, {self.y})")

    def displayIt(self):
        print(f"Displaying Circle '{self.name}'")

    def fillIt(self):
        print(f"Filling Circle '{self.name}' with {self.color}")

    def setItsColor(self, color):
        self.color = color

    def undisplayIt(self):
        print(f"Undisplaying Circle '{self.name}'")


def main():
    rect = Rectangle("Rectangle 1")
    rect.setLocation(9, 10)
    rect.setColor("Blue")
    rect.getLocation()
    rect.display()
    rect.fill()
    rect.undisplay()
    print()

    line = Line("Line 1")
    line.setLocation(5, 10)
    line.setColor("Red")
    line.getLocation()
    line.display()
    line.fill()
    line.undisplay()
    print()

    point = Rectangle("Rectangle 1")
    point.setLocation(9, 14)
    point.setColor("Blue")
    point.getLocation()
    point.display()
    point.fill()
    point.undisplay()
    print()

    xcirc = XXCircle("Circle 1")

    circ = CircleAdapter(xcirc)
    circ.setLocation(3, 5)
    circ.setColor("Green")
    circ.getLocation()
    circ.display()
    circ.fill()
    circ.undisplay()


main()
