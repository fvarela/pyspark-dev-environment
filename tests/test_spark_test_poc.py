import unittest
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, LongType
import sys
import os

# Add the app directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'app')))

import spark_test_poc

class TestSparkTestPOC(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.spark = spark_test_poc.create_spark_session("TestSparkTestPOC")

    @classmethod
    def tearDownClass(cls):
        cls.spark.stop()

    def test_create_sample_dataframe(self):
        df = spark_test_poc.create_sample_dataframe(self.spark, 1, 6)
        
        # Check the schema
        expected_schema = StructType([
            StructField("number", LongType(), False),
            StructField("square", LongType(), False)  # Changed to False
        ])
        self.assertEqual(df.schema, expected_schema)
        
        # Check the number of rows
        self.assertEqual(df.count(), 5)
        
        # Check the content
        expected_data = [(1, 1), (2, 4), (3, 9), (4, 16), (5, 25)]
        self.assertEqual(df.collect(), expected_data)

    def test_calculate_sums(self):
        df = spark_test_poc.create_sample_dataframe(self.spark, 1, 6)
        sum_numbers, sum_squares = spark_test_poc.calculate_sums(df)
        
        self.assertEqual(sum_numbers, 15)  # Sum of numbers
        self.assertEqual(sum_squares, 55)  # Sum of squares

if __name__ == '__main__':
    unittest.main()