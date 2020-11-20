# mv  positions.csv positions.csv.tmp
# busybox iconv -t ASCII  positions.csv.tmp >positions.csv
./calc_delta.py --exclude 'FI,FX,COM'

