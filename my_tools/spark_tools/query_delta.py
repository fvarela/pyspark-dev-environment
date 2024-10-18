import os
from azure.storage.blob import BlobServiceClient
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from delta import configure_spark_with_delta_pip
from aux_files.get_spark import get_spark

def query_table(spark, delta_path):

    df = spark.read.format("delta").load(delta_path)
    df.show()

    spark.stop()

def main():
    delta_table = "bronze"

    # Use environment variables for configuration
    storage_account_name = os.getenv('DEV_STORAGE_ACCOUNT_NAME', "salakefrandev")
    storage_account_key = os.getenv('DEV_STORAGE_ACCOUNT_KEY')
    delta_container = os.getenv('DEV_STORAGE_DELTA_CONTAINER', "delta-lake")

    spark = get_spark(storage_account_name=storage_account_name, storage_account_key=storage_account_key)    

    delta_path = f"abfss://{delta_container}@{storage_account_name}.dfs.core.windows.net/{delta_table}"

    query_table(spark, delta_path)

    spark.stop()


if __name__ == "__main__":
    main()

