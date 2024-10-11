from pyspark.sql import SparkSession
from delta import configure_spark_with_delta_pip
from pyspark.sql.functions import lit, rand, concat, col

def get_spark() -> SparkSession:
  try:
    from databricks.connect import DatabricksSession
    print("Databricks environment detected")
    return DatabricksSession.builder.getOrCreate()
  except:
    print("Local environment detected")
    return SparkSession.builder.getOrCreate()
  
def create_sample_dataframe(spark, num_rows=10):
    return spark.range(num_rows) \
        .withColumn("name", concat(lit("Person_"), col("id").cast("string"))) \
        .withColumn("age", (rand() * 42 + 18).cast("int"))

def write_delta_table(df, path, mode="overwrite"):
    df.write.format("delta").mode(mode).save(path)

def read_delta_table(spark, path):
    return spark.read.format("delta").load(path)

def main():
    """
    This function creates a Spark session, generates a sample DataFrame,
    writes it to a Delta table, reads it back, and displays the results.
    """

    spark = get_spark()
    data = create_sample_dataframe(spark)
    delta_table_path = "tmp/delta_table_poc"
    write_delta_table(data, delta_table_path)
    print(f"Delta table created at: {delta_table_path}")
    read_df = read_delta_table(spark, delta_table_path)
    read_df.show(5)
    
    spark.stop()

if __name__ == "__main__":
    main()