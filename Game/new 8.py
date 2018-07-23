# lines = []

# with open('testfile.csv') as f: 
    # for line in f:
        # transaction = line.split(',')
        # lines.append((transaction[1],transaction[4]))
        

import re
import datetime	
import csv
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import mplcursors

lines =[]
with open('testfile.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, dialect = 'excel')
    for line in spamreader:
	    #print(row)
        #print(', '.join(row))
        #transaction = line.split(',')
        #print(line[0])
        lines.append((line[1],line[4]))
lines.pop(0)
lines = [[x[0],float(x[1])] for x in lines]		
current = -1776.48
#for l in lines:
#    print(l)
	
def makeDate(date):
    '''
    Returns
    : param ...:
    : return :
    '''
    l = re.compile("-").split(date)
    #print(l)
    y = int(l[0])
    m = int(l[1])
    d = int(l[2])
    return datetime.date(y,m,d)	
	
week_sequence = (4, 5, 4, 5, 4, 4, 5, 4, 4, 5, 4)

datetime.timedelta(weeks = 4)
start_date = datetime.date(2018,1,7)
date_sequence = []#[datetime.timedelta(weeks = x) for x in week_sequence]
next_date = start_date
date_sequence.append(next_date)
for period in week_sequence:
    next_date = next_date +  datetime.timedelta(weeks = period)
    date_sequence.append(next_date)
    
#print(date_sequence)
def divideTransactions(transactions, date_sequence):
    '''
    Returns bins of sorted transactions.
    :param transactions: list of (string date, float amount)
    :param date_sequence: list of datetime startdates for periods.
    :return : list of bins, where each bin is a list of transactions for that period, and the period is the bin index, where bin[0] contains all transactions before the considered periods.
    
    '''
    #need
    datePairs = periodNumber(date_sequence)
    tbins = [[] for x in range(len(datePairs))]
    for t in transactions:
        p = setTransaction(t,datePairs)
        if p!=0:
            tbins[p].append(t)
        #((matplotlib.dates.date2num(datetime.datetime.combine(makeDate(t[0]), datetime.datetime.min.time()))),t[1]))
    for b in tbins:
        b.sort()
    #so what do I want from this and now I'm thinking, perhaps what I want is list of
    #lists, so use list comprehension and range of datepairs len. then add to it
    return tbins

def setTransaction(transaction, datePairs):
    '''
    Returns the period number, period 0 contains un-perioded data.
    : param transaction: (string date, float amount) date in yyyy-mm-dd format.
    : param datePairs: list of list of start and end dates for periods.
    : return int periodnumber:
    '''
    for i, d in enumerate(datePairs, 1):
        if makeDate(transaction[0])<(d[1]+datetime.timedelta(days=1)) and (makeDate(transaction[0])+datetime.timedelta(days=1))>d[0]:
            return i
            
        if makeDate(transaction[0])==d[1] or makeDate(transaction[0])==d[0]:
            print("the same")
            return i
    return 0
    
def periodNumber(date_sequence):
    '''
    Returns
    : param ...:
    : return :
    '''
    #want to set bounds from the date_sequence
    #number bounds
    #find
    datePairs = boundMaker(date_sequence)#[0:setCurrentPeriod(
    datePairs = datePairs[0:setCurrentPeriod(datePairs)]
    return datePairs
    
    
def boundMaker(date_sequence):
    '''
    Returns
    : param ...:
    : return :
    '''
    datePairs = []
    for i in range(len(date_sequence )- 1):
        datePairs.append((date_sequence[i],date_sequence[i+1]))
    return datePairs
    
def setCurrentPeriod(datePairs):
    '''
    Returns
    : param ...:
    : return :
    '''
    pNo = 0
    for i,d in enumerate(datePairs):
        if d[1] > datetime.date.today() or d[1] == datetime.date.today():
            pNo = i
            
def calibrate(tbins, current):
    '''
    Returns
    : param ...:
    : return :
    '''
    #somehow need to go backwards through them all. mwahahaha.
    #use reverse ranges perhaps, so pretty easy then really.
    #but also need to replace the number with the right one really.
    for i in range(len(tbins)-1, -1, -1):
        #print(tbins[i])
        for x in range(len(tbins[i])-1, -1, -1):
            print("x", tbins[i][x][1])
            t = current
            current = current - tbins[i][x][1]
            tbins[i][x][1] = current
            
    return tbins
print(divideTransactions(lines, date_sequence)[7])
tbins = calibrate(divideTransactions(lines, date_sequence),current)    
print(tbins[7])
for t in tbins:
    plt.plot([d[0] for d in t], [d[1] for d in t], solid_joinstyle='miter', solid_capstyle ='butt')
    #plt.set_('round')
#plt.plot([d[0] for d in tbins[6]], [d[1] for d in tbins[6]])
mplcursors.cursor(hover=True)
plt.show()
#so days from beginnig and the amount. and each one a differnt plot.
            
#print(l[0])

#print(makeDate(l[0]))
end_date = datetime.date.today

