from pyspark.sql import SparkSession
from delta import configure_spark_with_delta_pip
import os

def get_spark(storage_account_name=None, storage_account_key=None) -> SparkSession:
  try:
    from databricks.connect import DatabricksSession
    print("Databricks environment detected")
    return DatabricksSession.builder.getOrCreate()
  except:
      print("Local environment detected")
      builder = SparkSession.builder.appName("LocalETLJob")
      builder = configure_spark_with_delta_pip(builder)
      builder.config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
      builder.config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
      delta_version = "2.4.0"
      scala_version = "2.12"
      builder.config("spark.jars.packages", 
                      f"io.delta:delta-core_{scala_version}:{delta_version}," +
                      "org.apache.hadoop:hadoop-azure:3.3.1," +
                      "com.microsoft.azure:azure-storage:8.6.6")
      builder.config("spark.hadoop.fs.azure.account.auth.type", "SharedKey")
      builder.config(f"spark.hadoop.fs.azure.account.key.{storage_account_name}.dfs.core.windows.net", 
                      storage_account_key)
      return builder.getOrCreate()