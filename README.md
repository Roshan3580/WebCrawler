# Modular Interactive Web Crawler

This project is a fully refactored, modular, and interactive web crawler and URL extractor. It allows users to specify a starting URL and optional filters for domains, file types, and crawl depth. The crawler traverses the web, extracts all valid links, and prints them in real time.

## Features
- Interactive prompts for starting URL, allowed domains, file type filters, and crawl depth
- Crawls any website (not limited to specific domains)
- Extracts and prints all discovered URLs as it crawls
- Supports filtering by domain and file extension (customizable at runtime)
- Avoids revisiting URLs
- Politeness delay between requests
- Word statistics (longest page, word frequencies)
- Clean, modular codebase for easy extension

## Project Structure

```
webcrawler/
│
├── crawler/
│   ├── __init__.py
│   ├── core.py         # Main crawling logic (queue, visited, politeness, etc.)
│   └── filters.py      # Filtering logic (domains, extensions, etc.)
│
├── extract/
│   ├── __init__.py
│   └── links.py        # HTML parsing and link extraction
│
├── cli/
│   ├── __init__.py
│   └── interactive.py  # User prompts and argument parsing
│
├── main.py             # Entry point, glues everything together
├── README.md           # Project documentation
└── requirements.txt    # Python dependencies
```

## Usage

Run the crawler interactively:

```
python main.py
```

Follow the prompts to start crawling and extracting URLs!
