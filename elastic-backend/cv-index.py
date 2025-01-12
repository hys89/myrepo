import pandas as pd
import time
import logging
from elasticsearch import Elasticsearch, helpers


# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Initialize the Elasticsearch client
es = Elasticsearch([{'host': 'localhost', 'port': 9200, 'scheme': "http"}])

# Check if the Elasticsearch server is running
if not es.ping():
    logger.error("Elasticsearch is not running!")
    raise ValueError("Elasticsearch is not running!")
else:
    logger.info("Elasticsearch is running.")

# Load CSV into pandas DataFrame
df = pd.read_csv('../asr/cv-valid-dev.csv')

# Fill NAs
df['generated_text'] = df['generated_text'].fillna('')
df['duration'] = df['duration'].astype(str).fillna('')
df['age'] = df['age'].fillna('')
df['gender'] = df['gender'].fillna('')
df['accent'] = df['accent'].fillna('')

# Define the index name
index_name = 'cv-transcriptions'

# Create index settings and mappings
index_config = {
    "settings": {
        "number_of_shards": 1,
        "number_of_replicas": 1
    },
    "mappings": {
        "properties": {
            "filename": {"type": "text"},
            "text": {"type": "text"},
            "up_votes": {"type": "integer"},
            "down_votes": {"type": "integer"},
            "age": {"type": "text"},
            "gender": {"type": "text"},
            "accent": {"type": "text"},
            "generated_text": {"type": "text"},
            "duration": {"type": "text"},
        }
    }
}

# Create the index if it doesn't exist
if not es.indices.exists(index=index_name):
    es.indices.create(index=index_name, body=index_config)
    logger.info(f"Index {index_name} created.")
else:
    logger.warning(f"Index {index_name} already exists. Re-creating it.")
    es.indices.delete(index=index_name)
    es.indices.create(index=index_name, body=index_config)
    logger.info(f"Index {index_name} created.")

# Prepare the data for indexing
def generate_documents(df):
    for _, row in df.iterrows():
        yield {
            "_op_type": "index",
            "_index": index_name,
            "_source": {
                "filename": row['filename'],
                "text": row['text'],
                "up_votes": row['up_votes'],
                "down_votes": row['down_votes'],
                "age": row['age'],
                "gender": row['gender'],
                "accent": row['accent'],
                "generated_text": row['generated_text'],
                "duration": row['duration'],
            }
        }

# Index the data
helpers.bulk(es, generate_documents(df), index_name)
logger.info(f"Data indexed to {index_name}.")

# Check no. of documents
time.sleep(2)
logger.info(f"No. of Documents: {es.cat.count(index=index_name, format='json')}")