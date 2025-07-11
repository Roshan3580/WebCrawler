from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import re

STOPWORDS = {"the", "and", "to", "of", "a", "in", "that", "it", "is", "was", "for", "on", "with", "as", "he", "she",
             "at", "by", "an", "be", "this", "which", "or", "from", "but", "not", "are", "were", "his", "her", "they",
             "their", "have", "has", "had", "if", "then", "than"}

def extract_links(base_url, html, allowed_domains=None, blocked_extensions=None):
    soup = BeautifulSoup(html, "html.parser")
    links = set()
    for tag in soup.find_all("a", href=True):
        full_link = urljoin(base_url, tag["href"])
        full_link = full_link.split("#")[0]
        if is_valid_url(full_link, allowed_domains, blocked_extensions):
            links.add(full_link)
    return links

def is_valid_url(url, allowed_domains=None, blocked_extensions=None):
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"}:
        return False
    if allowed_domains is not None and parsed.hostname not in allowed_domains:
        return False
    if blocked_extensions is None:
        blocked_extensions = (
            r'\.(css|js|bmp|gif|jpeg|jpg|ico|png|tiff|mp3|mp4|wav|avi|mov|mpeg|m4v|mkv|ogg|pdf'
            r'|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|exe|bz2|tar|msi|bin|7z|psd|dmg|iso|epub'
            r'|dll|cnf|tgz|sha1|thmx|mso|arff|rtf|jar|csv|rm|wmv|swf|wma|zip|rar|gz)$'
        )
    return not re.search(blocked_extensions, parsed.path.lower())

def tokenize(text):
    words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
    return [word for word in words if word not in STOPWORDS]

def get_word_stats(html, url, stats):
    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text()
    words = tokenize(text)
    word_count = len(words)
    if word_count > stats["longest_page"]["word_count"]:
        stats["longest_page"] = {"url": url, "word_count": word_count}
    for word in words:
        stats["word_frequencies"][word] = stats["word_frequencies"].get(word, 0) + 1
