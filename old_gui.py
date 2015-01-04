from Tkinter import *
import numpy
import urllib2

class logic():
    def __init__(self):
        self.look_back = 30
        self.start = '2000'
        self.end = '2013'
        self.recent = '2014'
    def find_recent(self,stock):
        dates = stock[0]
        highs = self.find_highs(stock)
        last_month = []
        for high,num in zip(highs,range(len(highs))):
            last_month = dates[dates.index(high) - 20:dates.index(high)]
            count = 0
            for day in last_month:
                count += highs.count(day)
        return highs[-1],count

    def parse (self, symbol,end):
        """Create map from CSV"""
        url = 'http://www.google.com/finance/historical?q=' + symbol + \
              '&histperiod=daily&startdate=Jan+1%2C+'+ self.start + \
              '&enddate=Dec+31%2C+' + end + '&output=csv'
        f = urllib2.urlopen(url).read()
        points = f.replace('\n',',').split(',') # split csv
        #create map from date to point data.
        point_map = {}
        dates = []
        for i in range (6,len(points)-6,6):
            try:
                point_map[points[i]] = (float(points[i+1]),float(points[i+2]),\
                                        float(points[i+3]),float(points[i+4]),float(points[i+5]))
                dates.append(points[i])
            except:
                pass
        dates.reverse()
        stock = (dates,point_map)
        return stock
    def find_highs(self,stock):
        high = 1
        dates = stock[0]
        point_map = stock[1]
        ftw = 5*52

        year_highs = []
        highs = []
        for date in dates:
            highs.append(point_map[date][high])
        for i in range(ftw, len(dates)):
            if max(highs[i - ftw:i-1]) < highs[i]:
                year_highs.append(dates[i])
        return year_highs
    def high_numbers(self,dates,highs):
        counts = {}
        last_month = []
        for date in dates:
            count = 0
            try:
                last_month = dates[dates.index(date) - 20:dates.index(date)]
            except:
                pass
            for day in last_month:
                count += highs.count(day)
            if count in counts:
                counts[count] += 1
            else:
                counts[count] = 1
        return counts
    def back_and_forth(self,dates,highs):
        counts_back = {}
        counts_forth = {}
        last_month = []
        for high,num in zip(highs,range(len(highs))):
            last_month = dates[dates.index(high) - 20:dates.index(high)]
            count = 0
            for day in last_month:
                count += highs.count(day)
            if count in counts_back:
                counts_back[count] += 1
            else:
                counts_back [count] = 1
            try:
                counts_two = dates.index(highs[num+1]) - dates.index(highs[num])
            except:
                pass
            if count in counts_forth:
                counts_forth [count].append(counts_two)
            else:
                counts_forth[count] = [counts_two]
        for record in counts_forth.keys():
            counts_forth[record].sort()
        return counts_back.values(), counts_forth
        
                        
class gui():
    def __init__(self):
        self.column_labels = ['count','instances','occurrence','%max','mean return','min return',\
                              '25% return','50% return','75% return','max return',\
                              'std return','mean ttn', 'min ttn','25% ttn', '50% ttn','75% ttn',\
                              "max ttn", "std ttn"]
        self.symbol = 'junk'
        self.root = Tk()
        self.column_actuator = [IntVar() for i in range(len(self.column_labels))]
        self.row_actuator = IntVar()
        self.labels = []
        self.num_highs = 0
        self.time = IntVar()
        self.stock = []
        self.recent_stock = []
        self.old_symbol ="xxx"
        self.end = '2013'
        self.recent = '2014'
    def get_returns(self,stock,highs):
        time = self.time.get()
        close = 3
        returns = {}
        dates = stock[0]
        stock = stock[1]
        
        for high in highs:
            last_month = dates[dates.index(high) - 20: dates.index(high)]
            count = 0
            for day in last_month:
                count += highs.count(day)
            try:
                later = dates[dates.index(high) + time]
            except IndexError:
                later = dates[-1]
            value = ((stock[later][close] - stock[high][close])/stock[high][close]) #((y2 - y1) / y1)*100
            if count in returns:
                returns[count].append(value)
            else:
                returns[count] = [value]
        return returns.values()
            
    def calculate_occurences(self):
        instances = self.instances
        occurences = [0 for i in range(len(instances))]
        for i,instance in zip(range(len(instances)),instances):
            occurences[i] = sum(instances[i::])
        return occurences
    def make_rows(self):
        labels = range(self.num_highs)
        for label in labels:
            Radiobutton(self.root,text = str(label), variable = self.row_actuator, value = label,indicatoron = 0).grid(row = label + 12,column=0)
    def make_columns(self):
        for label,number,actuator in zip(self.column_labels,range(len(self.column_labels)), self.column_actuator):
            Checkbutton(self.root, text=label, variable = actuator).grid(row=10,column=number)
    def make_buttons(self):
        Button(self.root,text = "Populate",command = self.populate).grid(row = 0, column = 2)
        Button(self.root,text = "Run", command = self.run_program).grid(row=1,column=2)
        Button(self.root,text ="Quit",command = self.quit_button).grid(row=2,column=2)
    def make_symbol_entry(self):
        self.symbol_entry = Entry(self.root,textvariable=self.symbol)
        self.symbol_entry.grid(row=0,column=0)
    def make_instances(self):
        for i,instance in zip(range(len(self.instances)),self.instances):
            Label(self.root, text = str(instance)).grid(row = i + 12, column = 1)
    def make_occurences(self):
        occurences = self.calculate_occurences()
        self.occurences = occurences
        for i,instance in zip(range(len(occurences)),occurences):
            Label(self.root, text = str(instance)).grid(row = i + 12, column = 2)
    def make_percent_max(self):
        from operator import truediv
        percent_max = map(truediv,self.instances,self.occurences)
        for i,instance in zip(range(len(percent_max)),percent_max):
            Label(self.root, text = str(instance * 100)[:4] + '%').grid(row = i + 12, column = 3)
    def populate(self):
        global past
        for child in self.root.children.values():
            child.destroy()
        self.make()
        log = logic()
        if self.symbol_entry.get() != past:
            self.stock = log.parse(self.symbol_entry.get(),self.end)
            self.recent_stock = log.parse(self.symbol_entry.get(),self.recent)
            past = self.symbol_entry.get()
        self.make_recent(self.recent_stock)
        dates = self.stock[0]
        highs = log.find_highs(self.stock)
        counts = log.high_numbers(dates,highs)
        self.instances, self.ttn = log.back_and_forth(dates,highs)
        self.num_highs = len(self.instances)
        self.make_rows()
        self.make_instances()
        self.make_occurences()
        self.make_percent_max()
        self.make_returns(self.stock,highs)
        self.make_ttn()
    def make_recent(self,stock):
        log = logic()
        date,count = log.find_recent(stock)
        Label(self.root, text = date).grid(row = 0, column = 3)
        Label(self.root, text = str(count)).grid(row = 0, column = 4)
    def make_ttn(self):
        ttn = self.ttn.values()
        mean_ttn = [(sum(spread)/len(spread)) for spread in ttn]
        min_ttn = [min(spread) for spread in ttn]
        q1_ttn = [numpy.percentile(spread,25) for spread in ttn]
        q2_ttn = [numpy.percentile(spread,50) for spread in ttn]
        q3_ttn = [numpy.percentile(spread,75) for spread in ttn]
        max_ttn = [max(spread) for spread in ttn]
        stddev_ttn = [numpy.std(spread) for spread in ttn]
        for i,instance in zip(range(len(mean_ttn)),mean_ttn):
            Label(self.root, text = str(instance)[:4]).grid(row = i + 12, column = 11)
        for i,instance in zip(range(len(min_ttn)),min_ttn):
            Label(self.root, text = str(instance)[:4]).grid(row = i + 12, column = 12)
        for i,instance in zip(range(len(q1_ttn)),q1_ttn):
            Label(self.root, text = str(instance)[:4]).grid(row = i + 12, column = 13)
        for i,instance in zip(range(len(q2_ttn)),q2_ttn):
            Label(self.root, text = str(instance)[:4]).grid(row = i + 12, column = 14)
        for i,instance in zip(range(len(q3_ttn)),q3_ttn):
            Label(self.root, text = str(instance)[:4]).grid(row = i + 12, column = 15)
        for i,instance in zip(range(len(max_ttn)),max_ttn):
            Label(self.root, text = str(instance)[:4]).grid(row = i + 12, column = 16)
        for i,instance in zip(range(len(stddev_ttn)),stddev_ttn):
            Label(self.root, text = str(instance)[:4]).grid(row = i + 12, column = 117)
    def make_returns(self,stock,highs):
        returns = self.get_returns(stock,highs)
        mean_returns = [(sum(spread)/len(spread)) for spread in returns]
        min_returns = [min(spread) for spread in returns]
        q1_returns = [numpy.percentile(spread,25) for spread in returns]
        q2_returns = [numpy.percentile(spread,50) for spread in returns]
        q3_returns = [numpy.percentile(spread,75) for spread in returns]
        max_returns = [max(spread) for spread in returns]
        stddev_returns = [numpy.std(spread) for spread in returns]
        for i,instance in zip(range(len(mean_returns)),mean_returns):
            Label(self.root, text = str(instance * 100)[:4] + '%').grid(row = i + 12, column = 4)
        for i,instance in zip(range(len(min_returns)),min_returns):
            Label(self.root, text = str(instance * 100)[:4] + '%').grid(row = i + 12, column = 5)
        for i,instance in zip(range(len(q1_returns)),q1_returns):
            Label(self.root, text = str(instance * 100)[:4] + '%').grid(row = i + 12, column = 6)
        for i,instance in zip(range(len(q2_returns)),q2_returns):
            Label(self.root, text = str(instance * 100)[:4] + '%').grid(row = i + 12, column = 7)
        for i,instance in zip(range(len(q3_returns)),q3_returns):
            Label(self.root, text = str(instance * 100)[:4] + '%').grid(row = i + 12, column = 8)
        for i,instance in zip(range(len(max_returns)),max_returns):
            Label(self.root, text = str(instance * 100)[:4] + '%').grid(row = i + 12, column = 9)
        for i,instance in zip(range(len(stddev_returns)),stddev_returns):
            Label(self.root, text = str(instance * 100)[:4] + '%').grid(row = i + 12, column = 10)
    def run_program(self):
        
        high = self.row_actuator.get()
        self.populate()
##        self.labels = []
##        for i in range(len(self.column_labels)):
##            if (self.column_actuator[i].get()):
##                self.labels.append(Label(self.root,text = self.column_labels[i]))
##        for label,count in zip(self.labels, range(len(self.labels))):
##            label.grid(row = len(self.column_labels) + 15, column = count)
        if self.column_actuator[1]:
            pass
    def make_time_entry(self):
        labels = ["One Day", "One Week", "Two Weeks", "One Month", "Three Months", "One Year"]
        rows = range(len(labels))
        values = [1,5,10,20,60,240]

        for label,shift,days in zip(labels,rows,values):
            Radiobutton(self.root,text = label, variable = self.time, value = days,indicatoron = 0).grid(row = shift,column=1)
    def set_defaults(self):
        self.symbol_entry.insert(0,"car")
    def quit_button(self):
        self.root.destroy()
    def make(self):
        self.make_columns()
        self.make_buttons()
        self.make_symbol_entry()
        self.make_time_entry()
    def run(self):
        self.root.mainloop()
global past
past ="foo"
gui = gui()
gui.make()
gui.run()
