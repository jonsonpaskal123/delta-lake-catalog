
from pyspark.sql import SparkSession

# 1. Initialize SparkSession
print("Initializing SparkSession for ETL...")
spark = (
    SparkSession.builder
    .appName("ElasticToDeltaETL")
    .enableHiveSupport()
    .getOrCreate()
)

# 2. Extract data from Elasticsearch
print("Extracting data from Elasticsearch index 'person_sabt'...")
es_df = (
    spark.read.format("elasticsearch")
    .option("es.nodes", "elasticsearch")
    .option("es.port", "9200")
    .option("es.resource", "person_sabt")
    .load()
)

print(f"Successfully extracted {es_df.count()} rows from Elasticsearch.")
es_df.printSchema()

# 3. Transform data (optional)
# For this example, we will just select the columns to ensure the schema
print("Transforming data...")
transformed_df = es_df.select("name", "email", "address", "job", "company", "birthdate", "national_code")

# 4. Load data into Delta Lake
print("Loading data into Delta Lake...")
database_name = "my_delta_db"
table_name = "person_sabt"
full_table_name = f"{database_name}.{table_name}"

# Ensure the database exists
spark.sql(f"CREATE DATABASE IF NOT EXISTS {database_name}")

# Define the path in MinIO
delta_path = f"s3a://my-bucket/{table_name}"

# Write to Delta Lake and register in Hive Metastore
transformed_df.write.format("delta").mode("overwrite").option("path", delta_path).saveAsTable(full_table_name)

print(f"Successfully loaded data into Delta table: {full_table_name}")

# 5. Verify the data in Delta Lake
print("Verifying data in Delta Lake...")
delta_df = spark.read.table(full_table_name)
delta_df.show(10)

print("ETL process finished successfully!")

# 6. Stop SparkSession
spark.stop()
