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
        date = " ".join(notify_data[0].split(" ")[2:])
        for row in notify_data[1:]:
            prices.append(float(row["price"]))

        avg_price = sum(prices) / len(prices)
        
        with open("Average.dat", "a") as fout:
            fout.write(f"{date}, Average Price: {round(avg_price, 10)}\n")


class HighLowObserver(StockObserver):
    '''concrete StockObserver implementation for finding which companies closed within 1% of their 52 week high or low'''
    def __init__(self, subject):
        self.subject = subject


    def checkHigh(self, high, price):
        '''checks if a stock price is within 1% of the 52 week high or higher'''
        percent = float(high)/100
        
        if high == "0":
            if float(price) < 0.3:
                return True

        if float(price) >= (float(high) - percent):
            return True
        
        return False


    def checkLow(self, low, price):
        '''checks if a stock price is within 1% of the 52 week low or lower'''
        percent = float(low)/100

        if float(price) <= (float(low) + percent):
            return True

        return False


    def update(self, notify_data):
        with open("HighLow.dat", "a") as fout:        
            date = notify_data[0]
            fout.write(f"{date}\n")

            for row in notify_data[1:]:
                high = row["52high"]
                low = row["52low"]
                price = row["price"]
             
                if self.checkHigh(high, price) or self.checkLow(low, price):
                    fout.write(f'{row["symbol"]}: {price}, {high}, {low}\n')
            fout.write("\n")


class SelectionsObserver(StockObserver):
    '''concrete implementation to observe only certain stocks'''
    def __init__(self, subject):
        self.subject = subject


    def update(self, notify_data):
        symbols = ["ALL", "BA", "BC", "GBEL", "KFT", "MCD" "TR", "WAG"]
        
        with open("Selections.dat", "a") as fout:
            date = notify_data[0]
            fout.write(f"{date}\n")
            for row in notify_data[1:]:
                if row["symbol"] in symbols:
                    fout.write(f'{row["company"]}, {row["symbol"]}, {row["price"]}, {row["change$"]}, {row["change%"]}, {row["YTDchange"]}, {row["52high"]}, {row["52low"]}, {row["ratio"]}\n')
            fout.write("\n")

        


def main():
    stockMonitor = LocalStocks()
    
    avgObserver = AverageObserver(stockMonitor)
    highLow = HighLowObserver(stockMonitor)
    selectObs = SelectionsObserver(stockMonitor)

    stockMonitor.addObserver(avgObserver)
    stockMonitor.addObserver(highLow)
    stockMonitor.addObserver(selectObs)

    stockMonitor.monitorStocks()


main()
