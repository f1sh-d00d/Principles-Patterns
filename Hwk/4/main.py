class Factory:
    def createDisplayDriver(self):
        pass

    def printPrintDriver(self):
        pass


class HighResFactory(Factory):
    def createDisplayDriver(self):
        driver = HighResDisplayDriver()
        return driver

    def createPrintDriver(self):
        driver = HighResPrintDriver()
        return driver


class LowResFactory(Factory):
    def createDisplayDriver(self):
        driver = LowResDisplayDriver()
        return driver

    def createPrintDriver(self):
        driver = LowResPrintDriver()
        return driver

class PrintDriver:
    def createDocument(self):
        pass


class HighResPrintDriver(PrintDriver):
    def createDocument(self):
        new_doc = Document("High Resolution")
        new_doc.print_doc()


class LowResPrintDriver(PrintDriver):
    def createDocument(self):
        new_doc = Document("Low Resolution")
        new_doc.print_doc()


class DisplayDriver:
    def createWidget(self):
        pass


class HighResDisplayDriver(DisplayDriver):
    def createWidget(self):
        new_widget = Widget("High Resolution")
        new_widget.draw()


class LowResDisplayDriver(DisplayDriver):
    def createWidget(self):
        new_widget = Widget("Low Resolution")
        new_widget.draw()


class Widget:
    def __init__(self, setting):
        self.setting = setting

    def draw(self):
        print(f"Drawing a {self.setting} widget")


class Document:
    def __init__(self, setting):
        self.setting = setting

    def print_doc(self):
        print(f"Printing a {self.setting} document")


class WorkStation:
    '''Having a separate object for each work station ensures that there is only 1 copy each driver type exists per work station'''
    def __init__(self, resolution):
        self.resolution = resolution
        self.widget_driver = None
        self.print_driver = None


def main():
    #create factories
    hi_factory = HighResFactory()
    low_factory = LowResFactory()

    stations = []
    
    #create work station objects
    print("Creating High Resolution Work Station")
    hi_station = WorkStation("High")
    stations.append(hi_station)
    
    print("Creating Low Resolution Work Station")
    low_station = WorkStation("Low")
    stations.append(low_station)

    for station in stations:
        if station.resolution == "High":
            station.widget_driver = hi_factory.createDisplayDriver()
            station.print_driver = hi_factory.createPrintDriver()
        else:
            station.widget_driver = low_factory.createDisplayDriver()
            station.print_driver = low_factory.createPrintDriver()

        station.widget_driver.createWidget()
        station.print_driver.createDocument()


main()
