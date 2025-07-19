# راهنمای پیکربندی نهایی پروژه

این سند، پیکربندی نهایی و تست‌شده‌ای را که منجر به اجرای موفقیت‌آمیز خط لوله ETL (از Elasticsearch به Delta Lake) شد، مستند می‌کند. هدف این است که از تکرار خطاها در آینده جلوگیری شود.

## معماری و دلیل انتخاب رویکرد نهایی

پس از چندین بار تلاش و خطا، مشخص شد که بهترین و پایدارترین روش برای اجرای یک Spark Job در محیط Docker Compose، ایجاد یک **سرویس اختصاصی و ایزوله** برای آن کار است. تلاش برای اجرای `spark-submit` از طریق `docker-compose exec` درون سرویس `spark-master` منجر به مشکلات متعدد در شناسایی مسیرها (Paths) و پکیج‌ها (Class Not Found) می‌شد.

رویکرد نهایی، تعریف یک سرویس به نام `etl-job` در فایل `docker-compose.yml` است. این سرویس ویژگی‌های کلیدی زیر را دارد:

1.  **ایزوله بودن:** این سرویس فقط یک وظیفه دارد: اجرای اسکریپت ETL. پس از اتمام کار، خاموش می‌شود.
2.  **مدیریت وابستگی صریح:** با استفاده از `depends_on`، این سرویس منتظر می‌ماند تا سرویس‌های پیش‌نیاز مانند `spark-master` و `indexer` به طور کامل آماده شوند.
3.  **پیکربندی شفاف:** تمام پکیج‌های Maven مورد نیاز (مانند کانکتورهای Delta Lake و Elasticsearch) به طور مستقیم در `command` سرویس و از طریق آرگومان `--packages` به `spark-submit` داده می‌شوند. این روش، تمام پیچیدگی‌های مربوط به `classpath` را از بین می‌برد.

## پیکربندی‌های کلیدی

در ادامه، بخش‌های اصلی پیکربندی که برای کارکرد صحیح سیستم ضروری هستند، آمده است.

### ۱. سرویس `etl-job` در `docker-compose.yml`

این سرویس، قلب تپنده اجرای خط لوله ماست.

```yaml
etl-job:
  image: bitnami/spark:3
  container_name: etl-job
  user: root # برای جلوگیری از خطای Permission Denied
  volumes:
    - ./work:/app/work
    - ./conf:/opt/bitnami/spark/conf
  command: >
    /opt/bitnami/spark/bin/spark-submit 
    --master spark://spark-master:7077 
    --packages io.delta:delta-core_2.12:2.4.0,org.apache.hadoop:hadoop-aws:3.3.4,org.elasticsearch:elasticsearch-spark-30_2.12:8.5.1 
    /app/work/etl_elastic_to_delta.py
  depends_on:
    spark-master:
      condition: service_started
    indexer:
      condition: service_completed_successfully
  networks:
    - delta_network
```

**نکات مهم:**
*   `user: root`: برای حل مشکل دسترسی به فایل‌ها.
*   `--packages`: تمام وابستگی‌ها به صورت شفاف و مستقیم به Spark معرفی می‌شوند.
*   `depends_on`: تضمین می‌کند که این سرویس فقط زمانی اجرا شود که پیش‌نیازهای آن آماده باشند.

### ۲. سرویس `indexer` و `healthcheck`

برای اطمینان از اینکه `etl-job` قبل از آماده شدن Elasticsearch اجرا نمی‌شود، یک `healthcheck` برای سرویس `elasticsearch` و یک شرط `service_completed_successfully` برای `indexer` تعریف شده است.

```yaml
elasticsearch:
  # ... (سایر تنظیمات)
  healthcheck:
    test: ["CMD", "curl", "-f", "http://localhost:9200/_cluster/health?wait_for_status=yellow&timeout=5s"]
    interval: 10s
    timeout: 10s
    retries: 5

indexer:
  build:
    context: ./indexer
  depends_on:
    elasticsearch:
      condition: service_healthy
  # ... (سایر تنظیمات)
```

### ۳. فایل `conf/spark-defaults.conf`

این فایل اکنون فقط شامل تنظیمات مربوط به Delta Lake و اتصال به MinIO است و هیچ اطلاعاتی در مورد پکیج‌ها ندارد.

```properties
spark.sql.extensions io.delta.sql.DeltaSparkSessionExtension
spark.sql.catalog.spark_catalog org.apache.spark.sql.delta.catalog.DeltaCatalog
spark.hadoop.fs.s3a.endpoint http://minio:9000
spark.hadoop.fs.s3a.access.key admin
spark.hadoop.fs.s3a.secret.key password
spark.hadoop.fs.s3a.path.style.access true
spark.hadoop.fs.s3a.impl org.apache.hadoop.fs.s3a.S3AFileSystem
```

## نحوه اجرای نهایی

برای اجرای کامل خط لوله از ابتدا (شامل ساختن سرویس `indexer` و اجرای `etl-job`)، از دستور زیر استفاده کنید:

```bash
docker-compose up --build -d
```

برای اجرای مجدد `etl-job` بدون نیاز به ساخت مجدد، از دستور زیر استفاده کنید:

```bash
docker-compose up --force-recreate etl-job
```

برای مشاهده خروجی کار، لاگ‌های سرویس `etl-job` را بررسی کنید:

```bash
docker-compose logs etl-job
```
