import re
from urllib.parse import urlparse, urljoin
from collections import Counter
from bs4 import BeautifulSoup

STOPWORDS = {"the", "and", "to", "of", "a", "in", "that", "it", "is", "was", "for", "on", "with", "as", "he", "she",
             "at", "by", "an", "be", "this", "which", "or", "from", "but", "not", "are", "were", "his", "her", "they",
             "their", "have", "has", "had", "if", "then", "than"}

stats = {
    "longest_page": {"url": "", "word_count": 0},
    "word_frequencies": Counter(),
    "visited_urls": set()
}


def scrape_links(url, resp, allowed_domains=None, blocked_extensions=None):
    if resp.status != 200 or not resp.raw_response:
        return []
    links = extract_links(url, resp, allowed_domains, blocked_extensions)
    analyze_page_content(url, resp)
    return links


def extract_links(url, resp, allowed_domains=None, blocked_extensions=None):
    extracted_links = set()
    try:
        soup = BeautifulSoup(resp.raw_response.content, "html.parser")

        for tag in soup.find_all("a", href=True):
            full_link = urljoin(url, tag["href"])
            full_link = full_link.split("#")[0]

            if is_valid_url(full_link, allowed_domains, blocked_extensions):
                extracted_links.add(full_link)

    except Exception as e:
        print(f"Error extracting links from {url}: {e}")

    return list(extracted_links)


def analyze_page_content(url, resp):
    try:
        soup = BeautifulSoup(resp.raw_response.content, "html.parser")
        text = soup.get_text()
        words = tokenize(text)

        word_count = len(words)
        if word_count > stats["longest_page"]["word_count"]:
            stats["longest_page"] = {"url": url, "word_count": word_count}
        stats["word_frequencies"].update(words)

    except Exception as e:
        print(f"Error processing text from {url}: {e}")


def tokenize(text):
    words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
    return [word for word in words if word not in STOPWORDS]


def is_valid_url(url, allowed_domains=None, blocked_extensions=None):
    """
    Determines if a URL should be crawled based on scheme and file types.
    Optionally restricts by domain and file extension.
    Args:
        url (str): The URL to validate.
        allowed_domains (set, optional): If provided, only allow these domains.
        blocked_extensions (str, optional): Regex string of blocked file extensions.
    Returns:
        bool: True if the URL is valid for crawling, False otherwise.
    """
    try:
        parsed = urlparse(url)
        if parsed.scheme not in {"http", "https"}:
            return False
        if allowed_domains is not None:
            if parsed.hostname not in allowed_domains:
                return False
        # Default blocked extensions (non-HTML content)
        if blocked_extensions is None:
            blocked_extensions = (
                r'\.(css|js|bmp|gif|jpeg|jpg|ico|png|tiff|mp3|mp4|wav|avi|mov|mpeg|m4v|mkv|ogg|pdf'
                r'|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|exe|bz2|tar|msi|bin|7z|psd|dmg|iso|epub'
                r'|dll|cnf|tgz|sha1|thmx|mso|arff|rtf|jar|csv|rm|wmv|swf|wma|zip|rar|gz)$'
            )
        return not re.search(blocked_extensions, parsed.path.lower())
    except TypeError:
        return False
