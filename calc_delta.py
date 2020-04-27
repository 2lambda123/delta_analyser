import csv
# import random
import locale
locale.setlocale( locale.LC_ALL, 'en_US.UTF-8' )  # so you can interpret e.g. "1,000.0" as a number

import openpyxl as opx
import datetime

import sys


# cols in export from IB
ib_export = {'ticker':1, 'sec_type':2, 'exchange':3, 'datestr':4, 'strike':5, 'putcall':6, 'size':7}


# will hold beta for stock tickers as dict

tickers = dict()

def read_positions_old():
    positions = []
    with open("example.csv", newline='') as csvfile:
        position_reader = csv.reader(csvfile)
        for row in position_reader:
            positions.append(row)
    return positions

def read_positions(f):
    positions = [] # each entry will be of type dict
    with open(f, newline = '') as csvfile:
        header = [h.strip() for h in csvfile.readline().split(',')]
        reader = csv.DictReader(csvfile, fieldnames=header)
        for row in reader:
            positions.append(row)
    return positions

def create_betas():
    with open("betas.csv", 'w', newline = '') as betacsvfile:
        betawriter = csv.writer(betacsvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        
        for i in sorted(tickers):
            betawriter.writerow([i]+[1,2,3,4])

def read_betas(): # read csv file with betas in
    result = dict()
    with open("betas.csv", newline = '') as bcsv:
        breader = csv.reader(bcsv)
        for row in breader:
            result[row[0]] = row[1:]
    return result

def display_betas(betas):
    for i in betas:
        print(i, betas[i])

def display_positions(p):
    for i in p:
        print (i)

#known_betas={'RUT':1, 'SX7P':1, 'SI':0, 'ROKU':2, 'ZAR':0, 'NG':0, 'LK':0.2,
#             'HCC':0.5, 'ZM':1.7, 'FTMIB':1, 'ESTX50':1, 'ES':1, 'EMB':0, 'CVNA':1.5, 'CL':0,
#             'BNDX':1.8, 'BTP':0, 'BKLN':0}

def read_known_betas(f):  # read additional betas from excel worksheet
    wb = opx.load_workbook(f)
    ws = wb.active # there will be just one
    betavals = dict()
    for row in ws.rows:
        if (row[0].value == "Ticker"): # i.e. 1st row
            continue
        betavals[row[0].value] = row[1].value
    return betavals
    

def write_row(ws,row_number, col_start, lst):
    c = col_start
    for i in lst:
        ws.cell(row_number, c).value = i
        c += 1


def main():
    if len(sys.argv) > 1:
        beta_workbook = sys.argv[1]
    else:
        beta_workbook =     "betavals.xlsx"

    if len(sys.argv) > 2:
        positions_file = sys.argv[2]
    else:
        positions_file =    'full_positions1.csv'
    # betas = read_betas(beta_workbook)
    # can display_betas to check
    positions = read_positions(positions_file)
    
    known_betas = read_known_betas(beta_workbook)
    # print("known betas: {}".format(known_betas))
    #display_positions(positions)
    aggregate_delta = 0
    wb = opx.Workbook() # workbook
    ws = wb.create_sheet('Delta Calc', 0)
    excel_row = 1
    write_row(ws, excel_row, 1, ["Instrument", "Beta", "Delta", "SPX Equiv"])
    excel_row += 1
    for i in positions:
        beta = i['Beta']
        delta = i['Delta Dollars']
        # n.b. b & d are strings
#        print("{0:}, {1:}, {2:}".format(i['Financial Instrument'],beta, delta))
        try:
            betav = locale.atof(beta)
        except ValueError:
            underlying = i['Underlying']
            if underlying in known_betas:
                betav = known_betas[underlying]
            else:
                print("ignoring: {0:}".format(i))
        delta_pos = betav*locale.atof(delta)
        fi = i['Financial Instrument']
        print("{0:}, {1:.0f}".format(fi, delta_pos))
        if delta_pos != 0:
            write_row(ws, excel_row, 1, [fi, betav, delta, delta_pos])
            excel_row += 1
        
        aggregate_delta += delta_pos
                      
##        if beta.isnumeric() and delta.isnumeric():
##            print("Beta: {0:}, Delta Dollars: {1:}".format(beta , delta))
##            
    wb.save("Delta_Values_"+datetime.datetime.now().strftime("%H%M%S")+".xlsx")
    print("Overall exposure: {0:.0f}".format(aggregate_delta))    

main()        
