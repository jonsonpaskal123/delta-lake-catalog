
from pyspark.sql import SparkSession

# 1. راه‌اندازی SparkSession
print("Initializing SparkSession...")
spark = (
    SparkSession.builder
    .appName("DeltaLakeWithHiveCatalog")
    .enableHiveSupport()
    .getOrCreate()
)

# 2. ایجاد یک دیتابیس
print("Creating database 'my_delta_db'...")
spark.sql("CREATE DATABASE IF NOT EXISTS my_delta_db")

# 3. ایجاد و ذخیره یک جدول Delta
print("Creating a sample DataFrame...")
data = [("Alice", 1), ("Bob", 2), ("Charlie", 3)]
columns = ["name", "id"]
df = spark.createDataFrame(data, columns)

table_name = "my_delta_db.users"
# Note: Ensure the 'my-bucket' exists in MinIO
table_path = "s3a://my-bucket/users"

print(f"Writing DataFrame to Delta table: {table_name} at path: {table_path}")
df.write.format("delta").mode("overwrite").option("path", table_path).saveAsTable(table_name)
print("Write operation successful.")

# 4. خواندن داده از جدول Delta
print(f"Reading data from table: {table_name}")
df_read = spark.read.table(table_name)
df_read.show()

# 5. مشاهده جدول در کاتالوگ
print(f"Verifying table in Hive Metastore...")
spark.sql(f"SHOW TABLES IN {table_name.split('.')[0]}").show()

# 6. پاک کردن
print("Stopping SparkSession.")
spark.stop()
