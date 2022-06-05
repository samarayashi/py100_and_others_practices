from pyspark import SparkConf, SparkContext
from pyspark.sql import SparkSession

spark = SparkSession.builder.config(conf=SparkConf()).getOrCreate()
df1 = spark.read.csv("data_set/a_lvr_land_a.csv")
df2 = spark.read.csv("data_set/b_lvr_land_a.csv")
df1.show()
