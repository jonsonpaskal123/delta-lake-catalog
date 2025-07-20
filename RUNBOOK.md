## Runbook: Ghadam be Ghadam

In file, tamami-e marahel-e raah-andazi-e proje va moshkelat-e ehtemali be hamrah-e raah-e hal zakhire mishe ta dar ayande raahat-tar bashe.

### Pish-niaz-ha

*   Docker
*   Docker Compose

### Moshkel-e Avalie: Khata-ye `docker-credential-gcloud`

Hangam-e ejra-ye `docker-compose up`, momken ast dar marhale-ye build-e service-e `indexer` be khata-ye `docker-credential-gcloud` barkhord konid. In moshkel be in dalil ast ke Docker Compose سعی darad az etelaat-e ehraz-e hoviat-e Google Cloud estefade konad.

### Raah-e Hal: Build-e Mostaghim-e Image

Baraye hal-e in moshkel, ma image-e `indexer` ro be soorat-e mostaghim ba `docker` build mikonim ta in marhale-ye ehraz-e hoviat dor zade shavad.

--- 

### Nahve-ye Ejra-ye Kamel (Baraye Ayande)

Baraye raah-andazi-e kamel-e proje, marahel-e zir ro donbal konid:

**Ghadam 1: Build-e service-e `indexer` (faghat yek bar ya dar soorat-e taghir)**

In dastoor image-e `indexer` ro misazad. Agar koda-ye `indexer` taghir nakarde, niazi be ejra-ye dobare nist.

```bash
docker build -t delta-lake-catalog_indexer ./indexer
```

**Ghadam 2: Raah-andazi-e hame-ye service-ha**

In dastoor hame-ye service-ha ro (ba estefade az image-e build shode dar ghadam-e ghabl) raah-andazi mikone.

```bash
docker-compose up -d
```

--- 

### Dastoorat-e Mofid

*   **Barresi-e vaz'iat-e service-ha:**
    ```bash
    docker-compose ps
    ```

*   **Motavaghef kardan-e hame-ye service-ha:**
    ```bash
    docker-compose down
    ```

*   **Ejra-ye yek script-e Spark (mesal):**
    ```bash
    docker-compose exec -T spark-master spark-submit /app/work/test_spark.py
    ```

*   **Ejra-ye pipeline-e ETL (az Elasticsearch be Delta Lake):**
    ```bash
    docker-compose exec -T spark-master spark-submit /app/work/etl_elastic_to_delta.py
    ```
