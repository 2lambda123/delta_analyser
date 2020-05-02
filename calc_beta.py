#!/usr/bin/python

# ALPHAVANTAGE_API_KEY
my_key='71N6UTNGSMQXQFWU'

from alpha_vantage.timeseries import TimeSeries

ts = TimeSeries(key=my_key)

import csv
# import random
import locale
locale.setlocale( locale.LC_ALL, 'en_US.UTF-8' )  # so you can interpret e.g. "1,000.0" as a number

import openpyxl as opx
import datetime

import sys 
import getopt

import json
import time

from matplotlib import pyplot

verbose = False

def quiet_print(*args):
    if verbose:
        print(args)


def usage(prog):
    print(sys.argv[0],"calc_deltas --symbol=<e.g. IBM> --index=<e.g. SPX>", end='')

def later():    # commented out
    for i in symbol_timeseries:
        print(i)

        input()
        sp[i] = symbol_timeseries[i]['4. close']
        try:
            index[i] = index_timeseries[i]['4. close']
        except KeyError:
            print("Missing index close on {0:}".format(i))
        count -= 1
        if count <= 0: break

    print(sp)

def main(argv):
    verbose=1
    symbol='IBM'
    index='SPY'
    print(sys.argv)
#    quiet_print("argv[1]={0:}".format(sys.argv[1]))
#    quiet_print("argv[2]={0:}".format(sys.argv[2]))
    
    try:
        opts, args = getopt.getopt(sys.argv, "hvs:i:",["verbose", "symbol=", "index="])
    except getopt.GetoptError as err:
        print(err)
        usage()
        sys.exit(2)
    output = None
    verbose = False
    for o, a in opts:
        if o in ("-v", "--verbose"):
            verbose = True
        elif o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-s", "--symbol"):
            symbol = a
        elif o in ("-i", "--index"):
            index = a
        else:
            assert False, "unhandled option"

    symbol_timeseries=ts.get_monthly_adjusted(symbol=symbol)
    # time series[0] is actual price data
    time.sleep(15)
    index_timeseries=ts.get_monthly_adjusted(symbol=index)

    cleaned_data = {} # will be {'date': {'symbol': sp, 'indx': ip}}
    # the price series is in timeseries[0] as a dict, keyed by date.
    for i in symbol_timeseries[0]:
        if i in index_timeseries[0]:
            cleaned_data[i] = {symbol:symbol_timeseries[0][i]['4. close'],
                                   index:index_timeseries[0][i]['4. close']}
    
    print(cleaned_data)
    data_as_json_string = json.dumps(cleaned_data)
    
    with open("{0:}_{1:}.json".format(symbol, index),"w") as jsonfile:
        jsonfile.write(data_as_json_string)







if __name__ == "__main__":
   main(sys.argv[1:])
