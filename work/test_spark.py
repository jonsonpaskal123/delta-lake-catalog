

from pyspark.sql import SparkSession

print("\n" + "="*40)
print("Spark Test Script Started")
print("="*40 + "\n")

spark = SparkSession.builder.appName("TestApp").getOrCreate()

data = [("Testing Spark Submit", 1), ("This is a test", 2)]
df = spark.createDataFrame(data, ["message", "id"])

print("Spark test successful! DataFrame created:")
df.show()

print("\n" + "="*40)
print("Spark Test Script Finished")
print("="*40 + "\n")

spark.stop()

