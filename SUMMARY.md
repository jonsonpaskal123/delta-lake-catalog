# خلاصه پروژه Delta Lake Catalog

پروژه `delta-lake-catalog` یک محیط کامل برای کار با **Delta Lake** با استفاده از **Apache Spark** و **Docker** فراهم می‌کند.

## هدف اصلی

هدف این پروژه نمایش چگونگی مدیریت متادیتای جداول Delta به صورت متمرکز با استفاده از **Hive Metastore** است.

## اجزای اصلی

*   **Spark:** برای پردازش داده‌ها (شامل یک Master و چند Worker).
*   **Hive Metastore:** برای مدیریت مرکزی متادیتا (اسکیما، پارتیشن‌بندی و...).
*   **PostgreSQL:** به عنوان پایگاه داده پشتیبان برای Hive Metastore.
*   **MinIO:** یک ذخیره‌ساز object storage سازگار با S3 برای نگهداری فایل‌های Delta Lake.
*   **Elasticsearch/Kibana:** به عنوان منبع داده برای یک خط لوله ETL.
*   **Indexer:** سرویسی که داده‌های اولیه را وارد Elasticsearch می‌کند.

## سناریوی کاربردی

پروژه یک خط لوله **ETL** (Extract, Transform, Load) را پیاده‌سازی می‌کند که:

1.  **Extract:** داده‌ها را از Elasticsearch استخراج می‌کند.
2.  **Transform:** داده‌ها را در Spark پردازش و تبدیل می‌کند.
3.  **Load:** داده‌های نهایی را به عنوان یک جدول Delta در MinIO ذخیره کرده و متادیتای آن را در Hive Metastore ثبت می‌کند.

## نقاط قوت

*   **مستندسازی خوب:** فایل `README.md` به فارسی و با توضیحات کامل، معماری و نحوه اجرا را شرح داده است.
*   **محیط کامل:** با یک دستور `docker-compose up` تمامی سرویس‌های لازم راه‌اندازی می‌شوند.
*   **کاربردی بودن:** یک سناریوی واقعی (ETL از Elasticsearch به Delta Lake) را پیاده‌سازی کرده که مفاهیم را به خوبی نشان می‌دهد.

به طور خلاصه، این یک پروژه عالی برای یادگیری و تست Delta Lake و مدیریت کاتالوگ آن در یک محیط کامل و ایزوله شده است.
