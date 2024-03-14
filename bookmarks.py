import requests
from bs4 import BeautifulSoup
import logging
import time
import os

def read_bookmarks_file(file_path):
    """Reads the bookmark.html file and extracts URLs."""
    urls = []
    with open(file_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')
        for link in soup.find_all('a'):
            urls.append(link.get('href'))
    return urls

def test_url(url):
    """Tests if a URL is still operational by making a GET request."""
    try:
        response = requests.get(url, timeout=5, allow_redirects=True)
        if response.status_code == 200:
            logging.info(f"Successfully accessed: {response.url}")
        else:
            logging.warning(f"Failed to access {response.url}. Status code: {response.status_code}")
    except requests.RequestException as e:
        logging.error(f"Failed to access {url}: {e}")

def main():
    # Ask for the location of the bookmarks file
    bookmark_file = input("Please enter the location of the bookmarks file (bookmark.html): ").strip()
    if not os.path.isfile(bookmark_file):
        print("Error: Invalid file path.")
        return
    
    # Extract directory path from the bookmarks file location
    log_dir = os.path.dirname(bookmark_file)
    
    # Set up logging
    log_file = os.path.join(log_dir, 'audit.log')
    logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')
    
    # Read URLs from bookmark.html
    urls = read_bookmarks_file(bookmark_file)
    
    # Test each URL
    for url in urls:
        test_url(url)
        # Add a small delay between requests to be respectful to the servers
        time.sleep(1)

if __name__ == "__main__":
    main()
