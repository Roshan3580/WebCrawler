# Modular Interactive Web Crawler

## Project Overview
This project is a modular, interactive web crawler and URL extractor. It allows users to explore the web starting from any URL, with customizable options for domain and file type filtering, crawl depth, and politeness delay. The crawler traverses web pages, extracts all valid links, and provides real-time feedback and statistics.

## Technologies Used
- **Python 3**
- **requests**: For making HTTP requests and downloading web pages
- **beautifulsoup4**: For parsing HTML and extracting links and text

## What the Project Returns
- Prints each crawled URL and every extracted link in real time
- Displays the longest page by word count
- Shows the top 10 most frequent words found during the crawl

## What the Project Asks the User For
When you run the crawler, you will be prompted for:
- The starting URL to crawl
- (Optional) Domains to restrict crawling to
- (Optional) File extensions to block (as a regex)
- (Optional) Maximum crawl depth
- (Optional) Politeness delay (seconds between requests)

## How to Use
1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
2. Run the crawler:
   ```
   python main.py
   ```
3. Follow the interactive prompts to configure your crawl and view results in real time.

## Contact
For questions or feedback, contact:
**Roshan Raj**  
roshanraj@uci.edu
