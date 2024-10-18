from pyspark.sql.functions import col
import os
from aux_files.get_spark import get_spark



def create_sample_dataframe(spark, start=1, end=6):
    df = spark.range(start, end).toDF("number")
    return df.withColumn("square", col("number") * col("number"))

def calculate_sums(df):
    result = df.agg({"number": "sum", "square": "sum"}).collect()[0]
    return result[0], result[1]  # sum of numbers, sum of squares

def main():
    """
    This function creates a Spark session, generates a sample DataFrame,
    calculates the sum of numbers and squares, and displays the results.
    """
    storage_account_name = os.getenv('STORAGE_ACCOUNT_NAME', "salakefrandev")
    storage_account_key = os.getenv('STORAGE_ACCOUNT_KEY')
    spark = get_spark(storage_account_name=storage_account_name, storage_account_key=storage_account_key)    
    

    print("Spark Version:", spark.version)
    
    df = create_sample_dataframe(spark)
    
    print("Sample DataFrame:")
    df.show()
    
    sum_numbers, sum_squares = calculate_sums(df)
    print("Sum of numbers:", sum_numbers)
    print("Sum of squares:", sum_squares)
    
    spark.stop()

if __name__ == "__main__":
    main()