from pyspark import SparkContext
import sys

likes_loc = sys.argv[1]
frequents_loc = sys.argv[2]
sells_loc = sys.argv[3]
save_loc = sys.argv[4]

sc = SparkContext()

likes = sc.textFile(likes_loc).map(lambda x: x.split(',')).map(lambda x:(x[0],x[1]))
frequents = sc.textFile(frequents_loc).map(lambda x: x.split(',')).map(lambda x:(x[1],x[0]))
sells = sc.textFile(sells_loc).map(lambda x: x.split(',')).map(lambda x:(x[0],x[1]))

frequentsJoinSells = frequents.join(sells).map(lambda x:(x[1])).distinct()
output = likes.intersection(frequentsJoinSells)
OutputFile = output.map(lambda x:x[0]+"\t"+x[1]+"\n")
with open(save_loc, 'wb') as save_f:
    save_f.writelines('Drinker\tBeer\n')
    for s in OutputFile.collect():
        save_f.writelines(s)