import subprocess
import json
import argparse
from pymongo import MongoClient


def run_katana(url):
    """
    Runs the Katana web crawler and collects the output in JSON format.
    """
    command = [
        "katana",
        "-u", url,  # Use the provided URL
        "-jsonl",   # Output results in JSON format
        "-d", '4'
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


def write_to_mongodb(mongo_uri, database_name, collection_name, crawled_data):
    """
    Writes the crawled data to a MongoDB database.
    """
    try:
        # Initialize MongoDB client
        client = MongoClient(mongo_uri)
        db = client[database_name]
        collection = db[collection_name]

        # Insert the data into the collection
        if crawled_data:
            result = collection.insert_many(crawled_data)
            print(f"Inserted {len(result.inserted_ids)} documents into MongoDB collection '{collection_name}'.")
        else:
            print("No data to insert into MongoDB.")
    except Exception as e:
        print(f"Error writing to MongoDB: {e}")
    finally:
        client.close()


def main():
    # Argument parser setup
    parser = argparse.ArgumentParser(description="Run Katana crawler and store data into MongoDB.")
    parser.add_argument("url", help="The URL to crawl.")
    parser.add_argument("mongo_uri", help="MongoDB connection URI.")
    parser.add_argument("database_name", help="MongoDB database name.")
    parser.add_argument("collection_name", help="MongoDB collection name.")

    args = parser.parse_args()

    print(f"Starting Katana web crawler for URL: {args.url}")
    crawled_data = run_katana(args.url)

    if crawled_data:
        print(f"Crawled {len(crawled_data)} pages. Storing data to MongoDB...")
        write_to_mongodb(args.mongo_uri, args.database_name, args.collection_name, crawled_data)
        print("Crawling and data storage completed.")
    else:
        print("No data crawled. Exiting.")


if __name__ == "__main__":
    main()
