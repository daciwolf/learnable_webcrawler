import subprocess
import json
import argparse
from pymongo import MongoClient #database we are using for storage
from collections import Counter
import math



def get_connecting_and_current(starting_url):
    try:
        # Run Katana command and capture the output
        result = subprocess.run(
            ["katana", "-u", starting_url, "-d", "1"],  # Adjust depth (-d) as needed
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        # Check for errors
        if result.returncode != 0:
            print("Error running Katana:")
            print(result.stderr)
            return []

        # Process the output and extract URLs
        urls = result.stdout.splitlines()
        print(f"Found {len(urls)} URLs:")
        for url in urls:
            print(url)

        return urls
    except Exception as e:
        print(f"An error occurred: {e}")
        return []


def similarity(keywords, document):
    # Frequency counts
    keywords_freq = Counter(keywords)
    document_freq = Counter(document)

    # Compute the numerator: dot product of frequencies
    numerator = sum(keywords_freq[t] * document_freq[t] for t in keywords if t in document)

    # Compute the denominator: product of vector magnitudes
    keywords_magnitude = math.sqrt(sum(f**2 for f in keywords_freq.values()))
    document_magnitude = math.sqrt(sum(f**2 for f in document_freq.values()))

    # Avoid division by zero
    if keywords_magnitude == 0 or document_magnitude == 0:
        return 0.0

    return numerator / (keywords_magnitude * document_magnitude)





