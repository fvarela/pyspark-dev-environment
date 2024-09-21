from pyspark.sql import SparkSession
from delta import configure_spark_with_delta_pip
from pyspark.sql.functions import lit, rand, concat, col

# Configure Spark with Delta Lake
builder = SparkSession.builder.appName("DeltaTablePOC") \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")

# Configure for pip-installed Delta Lake
spark = configure_spark_with_delta_pip(builder).getOrCreate()

# Create a simple DataFrame
data = spark.range(10) \
    .withColumn("name", concat(lit("Person_"), col("id").cast("string"))) \
    .withColumn("age", (rand() * 42 + 18).cast("int"))


# Specify the path for the Delta table
delta_table_path = "tmp/delta_table_poc"

# Write the DataFrame as a Delta table
data.write.format("delta").mode("overwrite").save(delta_table_path)

print(f"Delta table created at: {delta_table_path}")

# Read and show the Delta table
spark.read.format("delta").load(delta_table_path).show(5)

spark.stop()