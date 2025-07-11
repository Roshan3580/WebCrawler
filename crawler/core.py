import time
import requests
from collections import defaultdict
from crawler.filters import normalize_url, VisitedSet
from extract.links import extract_links, get_word_stats

def crawl(start_url, allowed_domains=None, blocked_extensions=None, crawl_depth=2, politeness=0.5):
    queue = [(start_url, 0)]
    visited = VisitedSet()
    stats = {"longest_page": {"url": "", "word_count": 0}, "word_frequencies": defaultdict(int)}

    while queue:
        url, depth = queue.pop(0)
        norm_url = normalize_url(url)
        if norm_url in visited or depth > crawl_depth:
            continue
        visited.add(norm_url)
        try:
            resp = requests.get(url, timeout=10)
            if resp.status_code != 200 or not resp.content:
                continue
            html = resp.content
            print(f"Crawled: {url}")
            get_word_stats(html, url, stats)
            links = extract_links(url, html, allowed_domains, blocked_extensions)
            for link in links:
                print(f"  Extracted: {link}")
                queue.append((link, depth + 1))
            time.sleep(politeness)
        except Exception as e:
            print(f"Error crawling {url}: {e}")
    print("\nCrawling complete.")
    print(f"Longest page: {stats['longest_page']['url']} ({stats['longest_page']['word_count']} words)")
    print("Top 10 words:")
    top_words = sorted(stats["word_frequencies"].items(), key=lambda x: -x[1])[:10]
    for word, count in top_words:
        print(f"  {word}: {count}")
