from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("SparkTestPOC") \
    .getOrCreate()

print("Spark Version:", spark.version)

df = spark.range(1, 6).toDF("number")
df = df.withColumn("square", df["number"] * df["number"])

print("Sample DataFrame:")
df.show()

result = df.agg({"number": "sum", "square": "sum"}).collect()[0]
print("Sum of numbers:", result[0])
print("Sum of squares:", result[1])

spark.stop()