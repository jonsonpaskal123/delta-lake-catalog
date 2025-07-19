
import time
from elasticsearch import Elasticsearch
from faker import Faker

# Initialize Faker for generating dummy data
fake = Faker()

# Elasticsearch connection settings
ES_HOST = "elasticsearch"
ES_PORT = 9200
INDEX_NAME = "people"

# Function to create an Elasticsearch client
def get_es_client():
    for _ in range(10):  # Retry for 100 seconds
        try:
            client = Elasticsearch(
                hosts=[{"host": ES_HOST, "port": ES_PORT, "scheme": "http"}]
            )
            if client.ping():
                print("Successfully connected to Elasticsearch!")
                return client
        except Exception as e:
            print(f"Could not connect to Elasticsearch: {e}. Retrying in 10 seconds...")
            time.sleep(10)
    raise ConnectionError("Failed to connect to Elasticsearch after multiple retries.")

# Function to create the index with a specific mapping
def create_index(client):
    if not client.indices.exists(index=INDEX_NAME):
        mapping = {
            "properties": {
                "name": {"type": "text"},
                "email": {"type": "keyword"},
                "address": {"type": "text"},
                "job": {"type": "text"},
                "company": {"type": "text"},
                "birthdate": {"type": "date"}
            }
        }
        client.indices.create(index=INDEX_NAME, mappings=mapping)
        print(f"Index '{INDEX_NAME}' created with mapping.")
    else:
        print(f"Index '{INDEX_NAME}' already exists.")

# Function to generate and index dummy data
def index_data(client):
    # Check if the index is empty
    if client.count(index=INDEX_NAME)["count"] > 0:
        print("Data already exists in the index. Skipping data generation.")
        return

    print("Generating and indexing 1000 dummy documents...")
    actions = []
    for i in range(1000):
        doc = {
            "name": fake.name(),
            "email": fake.email(),
            "address": fake.address(),
            "job": fake.job(),
            "company": fake.company(),
            "birthdate": fake.date_of_birth(minimum_age=18, maximum_age=70).isoformat()
        }
        actions.append({"_index": INDEX_NAME, "_source": doc})

        # Bulk index every 100 documents
        if len(actions) == 100:
            from elasticsearch.helpers import bulk
            bulk(client, actions)
            actions = []
            print(f"Indexed {i+1}/1000 documents...")

    # Index any remaining actions
    if actions:
        from elasticsearch.helpers import bulk
        bulk(client, actions)
    
    print("Finished indexing all documents.")

if __name__ == "__main__":
    es_client = get_es_client()
    create_index(es_client)
    index_data(es_client)
