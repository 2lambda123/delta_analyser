import csv
import random
import locale
locale.setlocale( locale.LC_ALL, 'en_US.UTF-8' )  # so you can interpret e.g. "1,000.0" as a number

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

def read_positions():
    positions = [] # each entry will be of type dict
    with open('full_positions1.csv', newline = '') as csvfile:
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

known_betas={'RUT':1, 'SX7P':1, 'SI':0, 'ROKU':2, 'ZAR':0, 'NG':0, 'LK':0.2,
             'HCC':0.5, 'ZM':1.7, 'FTMIB':1, 'ESTX50':1, 'ES':1, 'EMB':0, 'CVNA':1.5, 'CL':0,
             'BNDX':1.8, 'BTP':0, 'BKLN':0}

def main():
    betas = read_betas()
    # can display_betas to check
    positions = read_positions()
    #display_positions(positions)
    aggregate_delta = 0
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
        print("{0:}, {1:.0f}".format(i['Financial Instrument'], delta_pos))            
        aggregate_delta += delta_pos
                      
##        if beta.isnumeric() and delta.isnumeric():
##            print("Beta: {0:}, Delta Dollars: {1:}".format(beta , delta))
##            

    print("Overall exposure: {0:.0f}".format(aggregate_delta))
    

main()        
