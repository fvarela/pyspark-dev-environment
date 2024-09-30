from pyspark.sql import SparkSession
from pyspark.sql.functions import collect_list, struct, udf
from pyspark.sql.types import StringType
import random
import json

spark = SparkSession.builder.appName("Simple Category Processing").getOrCreate()

def generate_dummy_data():
    categories = ["A", "B", "C"]
    data = [(i, f"name_{i}", random.randint(20, 60), random.choice(categories)) for i in range(10)]
    return spark.createDataFrame(data, ["id", "name", "age", "category"])

@udf(returnType=StringType())
def process_category(group_data):
    return json.dumps([{"name": person['name'], "age": person['age']} for person in group_data])

def run():
    df = generate_dummy_data()
    result_df = df.groupBy("category").agg(
        process_category(collect_list(struct("name", "age"))).alias("people")
    )
    result_df.show(truncate=False)

if __name__ == "__main__":
    run()
    spark.stop()