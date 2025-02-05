import os
import re
import hashlib
from urllib.parse import urlparse, urljoin
from collections import Counter
from bs4 import BeautifulSoup

STOPWORDS = {"the", "and", "to", "of", "a", "in", "that", "it", "is", "was", "for", "on", "with", "as", "he", "she",
             "at", "by", "an", "be", "this", "which", "or", "from", "but", "not", "are", "were", "his", "her", "they",
             "their", "have", "has", "had", "if", "then", "than"}

longest_page = {"url": "", "count": 0}
word_frequencies = Counter()
visited_urls = set()

SAVE_PAGES_DIR = "saved_pages"
if not os.path.exists(SAVE_PAGES_DIR):
    os.makedirs(SAVE_PAGES_DIR)

def scraper(url, resp):
    if resp.status != 200 or not resp.raw_response:
        return []
    save_page(url, resp)
    links = extract_next_links(url, resp)
    process_page_text(url, resp)
    return [link for link in links if is_valid(link)]

def extract_next_links(url, resp):
    try:
        soup = BeautifulSoup(resp.raw_response.content, "html.parser")
        links = set()

        for tag in soup.find_all("a", href=True):
            link = urljoin(url, tag["href"])
            link = link.split("#")[0]
            if is_valid(link):
                links.add(link)

        return list(links)
    except Exception as e:
        print(f"Error parsing {url}: {e}")
        return []

def process_page_text(url, resp):
    global longest_page, word_frequencies

    try:
        soup = BeautifulSoup(resp.raw_response.content, "html.parser")
        text = soup.get_text()
        words = re.findall(r'\b[a-zA-Z]{2,}\b', text.lower())

        word_count = len(words)
        if word_count > longest_page["count"]:
            longest_page = {"url": url, "count": word_count}

        filtered_words = [word for word in words if word not in STOPWORDS]
        word_frequencies.update(filtered_words)
    except Exception as e:
        print(f"Error processing text from {url}: {e}")

def is_valid(url):
    # Decide whether to crawl this url or not.
    # If you decide to crawl it, return True; otherwise return False.
    # There are already some conditions that return False.
    try:
        parsed = urlparse(url)
        if parsed.scheme not in {"http", "https"}:
            return False
        return not re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico"
            + r"|png|tiff?|mid|mp2|mp3|mp4"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
            + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1"
            + r"|thmx|mso|arff|rtf|jar|csv"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower())

    except TypeError:
        print ("TypeError for ", parsed)
        raise

def save_page(url, resp):
    try:
        url_hash = hashlib.md5(url.encode()).hexdigest()
        file_path = os.path.join(SAVE_PAGES_DIR, f"{url_hash}.html")
        with open(file_path, "wb") as f:
            f.write(resp.raw_response.content)
    except Exception as e:
        print(f"Error saving page {url}: {e}")