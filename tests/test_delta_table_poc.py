import unittest
from pyspark.sql import SparkSession
import sys
import os
import shutil

# Add the app directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'app')))

import delta_table_poc

class TestDeltaTablePOC(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.spark = delta_table_poc.create_spark_session("TestDeltaTablePOC")
        cls.delta_table_path = "tmp/test_delta_table_poc"

    @classmethod
    def tearDownClass(cls):
        cls.spark.stop()
        # Clean up the test Delta table
        shutil.rmtree(cls.delta_table_path, ignore_errors=True)

    def test_create_sample_dataframe(self):
        df = delta_table_poc.create_sample_dataframe(self.spark, num_rows=5)
        
        # Check the number of rows
        self.assertEqual(df.count(), 5)
        
        # Check the schema
        self.assertEqual(df.columns, ["id", "name", "age"])
        
        # Check data types
        self.assertEqual(df.schema["id"].dataType.simpleString(), "bigint")
        self.assertEqual(df.schema["name"].dataType.simpleString(), "string")
        self.assertEqual(df.schema["age"].dataType.simpleString(), "int")

    def test_write_and_read_delta_table(self):
        # Create sample data
        data = delta_table_poc.create_sample_dataframe(self.spark, num_rows=10)
        
        # Write the Delta table
        delta_table_poc.write_delta_table(data, self.delta_table_path)
        
        # Read the Delta table
        read_df = delta_table_poc.read_delta_table(self.spark, self.delta_table_path)
        
        # Check the number of rows
        self.assertEqual(read_df.count(), 10)
        
        # Check the schema
        self.assertEqual(read_df.columns, ["id", "name", "age"])
        
        # Check data types
        self.assertEqual(read_df.schema["id"].dataType.simpleString(), "bigint")
        self.assertEqual(read_df.schema["name"].dataType.simpleString(), "string")
        self.assertEqual(read_df.schema["age"].dataType.simpleString(), "int")

if __name__ == '__main__':
    unittest.main()