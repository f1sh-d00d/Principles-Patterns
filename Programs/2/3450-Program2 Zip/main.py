class StockSubject():
    '''Interface for stock monitoring subjects'''
    
    def __init__(self):
        pass


    def addObserver(self):
        pass


    def removeObserver(self):
        pass


    def notifyObserver(self):
        pass


class StockObserver():
    '''interfaec for stock observer'''

    def __init__(self):
        pass


    def update(self):
        pass


class LocalStocks(StockSubject):
    '''Concrete implementation of StockSubject'''
    
    def __init__(self):
        self.observers = []


    def addObserver(self, observer):
        self.observers.append(observer)


    def removeObserver(self, observer):
        if observer in self.observers:
            self.observers.remove(observer)

    
    def monitorStocks(self):
        with open("Ticker.dat", "r") as fin:
            stock_data = fin.readlines()

            notify_data = []
            blanks = 0
            blocks = 0

            for line in stock_data:
                if "Last updated" in line:
                    last_was_blank = False
                    notify_data = []
                    blanks = 0
                    blocks += 1
                    notify_data.append(line.strip())
                
                elif line.strip():                              #if the line isn't blank
                    parse = line.split(" ")
                    stock_info = {'company':" ".join(parse[:-10]), "symbol":parse[-10], "price":parse[-9], "change$":parse[-8], "change%":parse[-6], "YTDchange":parse[-5], "52high":parse[-4], "52low":parse[-3], "ratio":parse[-2]}
                    notify_data.append(stock_info)                
            
                elif last_was_blank == False:                                           #if the line is blank, we can notify our observers because we have finished receiving new stock data
                    self.notifyObserver(notify_data)
                    last_was_blank = True

    
    def notifyObserver(self, notify_data):
        #FIXME - pass notify data to observer and have the observer process the data however it needs
        for observer in self.observers:
            observer.update(notify_data)


class AverageObserver(StockObserver):
    '''conrete StockObserver implementation for calculating average stock prices'''
    def __init__(self, subject):
        self.subject = subject


    def update(self, notify_data):
        prices = []
        date = " ".join(notify_data.pop(0).split(" ")[2:])
        for row in notify_data:
            prices.append(float(row["price"]))

        avg_price = sum(prices) / len(prices)
        
        with open("Average.dat", "a") as fout:
            fout.write(f"{date}, Average Price: {round(avg_price, 10)}\n")


def main():
    stockMonitor = LocalStocks()
    avgObserver = AverageObserver(stockMonitor)
    stockMonitor.addObserver(avgObserver)
    stockMonitor.monitorStocks()


main()
