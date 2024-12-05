import subprocess
import json
import argparse
from pymongo import MongoClient


def run_katana_and_write_to_db(url, mongo_uri, database_name, collection_name):
    """
    Runs the Katana web crawler and writes each output line to MongoDB.
    """
    command = [
        "katana",
        "-u", url,  # Use the provided URL
        "-jsonl",   # Output results in JSON Lines format
        "-d", '4'
    ]
    print(f"Running command: {' '.join(command)}")
    try:
        # Initialize MongoDB client
        client = MongoClient(mongo_uri)
        db = client[database_name]
        collection = db[collection_name]

        # Start the Katana process
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,  # Line-buffered
            universal_newlines=True
        )

        # Read stdout line by line
        for line in iter(process.stdout.readline, ''):
            line = line.strip()
            if line:
                try:
                    data = json.loads(line)
                    # Write data to MongoDB
                    collection.insert_one(data)
                    print(f"Inserted document into MongoDB collection '{collection_name}'.")
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON: {e}")
                except Exception as e:
                    print(f"Error inserting into MongoDB: {e}")

        # Wait for the process to complete
        process.stdout.close()
        process.wait()

        if process.returncode != 0:
            stderr_output = process.stderr.read()
            raise RuntimeError(f"Katana failed with error: {stderr_output}")

    except Exception as e:
        print(f"Error running Katana: {e}")
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
    run_katana_and_write_to_db(args.url, args.mongo_uri, args.database_name, args.collection_name)
    print("Crawling and data storage completed.")


if __name__ == "__main__":
    main()
