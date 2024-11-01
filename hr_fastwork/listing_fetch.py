import re

import requests
from bs4 import BeautifulSoup
import time
import random
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def crawl_fastwork_pages(base_url, output_file="details_urls.txt", buffer_size=10, max_retries=3):
    """
    Crawls Fastwork pages, extracting article URLs and saving them to a file.

    Args:
        base_url: The base URL for the Fastwork pages.
        output_file: The file to save URLs to.
        buffer_size: Number of URLs to accumulate before writing.
        max_retries: Maximum number of retries for failed requests.
    """

    urls = []
    page_num = 1

    while True:
        url = f"{base_url}{page_num}/"
        logging.info(f"Processing page {page_num}: {url}")

        for attempt in range(max_retries):
            try:
                response = requests.get(url, timeout=10)
                response.raise_for_status()
                break
            except requests.exceptions.RequestException as e:
                retry_count = attempt + 1
                logging.warning(f"Request failed for {url} (attempt {retry_count}/{max_retries}): {e}. Retrying...")
                if retry_count >= max_retries:
                    logging.error(f"Giving up on {url} after {max_retries} attempts.")
                    return False
                time.sleep(2**attempt)

        else:
            logging.warning(f"Failed to reach page {page_num} after {max_retries} attempts")
            return False


        soup = BeautifulSoup(response.content, 'html.parser')

        articles = soup.find_all('article', id=re.compile(r'^post-\d+')) # Select all articles with IDs starting with 'post-'

        if not articles:
            logging.info(f"No more articles found on page {page_num}.")
            break


        for article in articles:
            try:
                link_element = article.select_one('div.post-header a')
                if link_element:
                    article_url = link_element.get('href')
                    if article_url and article_url.startswith('https://fastwork.vn/'):
                        urls.append(article_url)
                    else:
                        logging.warning(f"Invalid or missing article URL: {article_url}")
                else:
                    logging.warning(f"Missing <a> tag for article: {article['id']}") # Catch cases where there is no valid <a> element

            except Exception as e:
                logging.error(f"Error processing article {article['id']}: {e}")


        if len(urls) >= buffer_size:
            try:
                with open(output_file, "a", encoding="utf-8") as f:
                    for url in urls:
                        f.write(url + "\n")
                logging.info(f"Wrote {len(urls)} URLs to {output_file}")
                urls = []
            except Exception as e:
                logging.error(f"Error writing to file: {e}")

        page_num += 1
        time.sleep(random.uniform(1, 10))


    if urls:
        try:
            with open(output_file, "a", encoding="utf-8") as f:
                for url in urls:
                    f.write(url + "\n")
            logging.info(f"Wrote the remaining {len(urls)} URLs to {output_file}")
        except Exception as e:
            logging.error(f"Error writing remaining URLs to file: {e}")

    return True


if __name__ == "__main__":
    base_url = "https://fastwork.vn/kien-thuc/nhan-su/page/"
    success = crawl_fastwork_pages(base_url)

    if success:
        print("Crawling completed successfully.")
    else:
        print("Crawling failed.")