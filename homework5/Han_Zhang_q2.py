from pyspark import SparkContext
import sys

likes_loc = sys.argv[1]
frequents_loc = sys.argv[2]
save_loc = sys.argv[3]

sc = SparkContext()

likes = sc.textFile(likes_loc).map(lambda x: x.split(',')[0]).distinct()
frequents = sc.textFile(frequents_loc).map(lambda x: x.split(',')[0]).distinct()

output = likes.subtract(frequents)

with open(save_loc, 'wb') as save_f:
    save_f.writelines('Drinker\n')
    for s in output.collect():
        save_f.writelines(s+'\n')