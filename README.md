# delta_analyser
Takes the exported positions CSV from the Interactive Brokers Trader Workstation (TWS) and calcs. delta pos.

This is a little project to help me work out an overall market exposure for a set of positions at my brokers.

It works on a csv file exported from Interactive Brokers Trader Workstation. For obvious reasons, I haven't uploaded my positions, 
(there is an encrypted version tho').

I am not a Python expert, but any means, and this is largely a learning exercise for me.

There are several source files. The only one I have done much work on is the calc_delta.py, which works out the overall market exposure. 

I took some data (by hand) from the amazing resource that is [unicorn bay](https://unicornbay.com/tools/asset-correlations).
