from pyspark import SparkContext
import sys

load_loc = sys.argv[1]
save_loc = sys.argv[2]

sc = SparkContext()
lines = sc.textFile(load_loc)

def beerFilter(line):
    return line[1]!='Summerbrew' and line[0]!='bar'
   
output = lines.map(lambda x: x.split(',')).filter(beerFilter)\
.map(lambda x:(x[0], int(x[2]))).groupByKey()\
.filter(lambda x:len(x[1])>1).mapValues(list).mapValues(max)
outputFile = output.map(lambda x:x[0]+"\t"+str(x[1])+"\n")
with open(save_loc, 'wb') as save_f:
    save_f.writelines("Bar\tMax_Price\n")
    for s in outputFile.collect():
        save_f.writelines(s)