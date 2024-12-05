import subprocess
import json
import argparse
from elasticsearch import Elasticsearch, helpers

def run_katana(url):
    """
    Runs the Katana web crawler and collects the output in JSON format.
    """
    command = [
        "katana",
        "-u", url,  # Use the provided URL
        "-jsonl",      # Output results in JSON format
        "-d", '1'
    ]
    print(command)
    try:
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        stdout, stderr = process.communicate()

        if process.returncode != 0:
            raise RuntimeError(f"Katana failed with error: {stderr}")

        # Parse JSON output
        data = [json.loads(line) for line in stdout.strip().split("\n") if line.strip()]
        return data

    except Exception as e:
        print(f"Error running Katana: {e}")
        return []

def index_to_elasticsearch(api_key, es_host, index_name, crawled_data):
    """
    Indexes the crawled data into Elasticsearch.
    """
    # Initialize Elasticsearch client with API Key
    es = Elasticsearch(
        es_host,
        api_key=api_key,
    )

    # Ensure the index exists
    if not es.indices.exists(index=index_name):
        es.indices.create(index=index_name)

    # Prepare and bulk index the data
    actions = [
        {
            "_index": index_name,
            "_source": data,
        }
        for data in crawled_data
    ]
    helpers.bulk(es, actions[0:9])
    print(f"Indexed {len(crawled_data)} documents into Elasticsearch.")

def main():
    # Argument parser setup
    parser = argparse.ArgumentParser(description="Run Katana crawler and index data into Elasticsearch.")
    parser.add_argument("url", help="The URL to crawl.")
    parser.add_argument("api_key", help="Elasticsearch API key.")
    parser.add_argument("es_host", help="Elasticsearch host URL.")
    parser.add_argument("index_name", help="Elasticsearch index name.")

    args = parser.parse_args()

    print(f"Starting Katana web crawler for URL: {args.url}")
    crawled_data = run_katana(args.url)

    if crawled_data:
        print(f"Crawled {len(crawled_data)} pages. Indexing to Elasticsearch...")
        index_to_elasticsearch(args.api_key, args.es_host, args.index_name, crawled_data)
        print("Crawling and indexing completed.")
    else:
        print("No data crawled. Exiting.")

if __name__ == "__main__":
    main()
