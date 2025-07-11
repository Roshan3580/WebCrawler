ABOUT
-------------------------
This is a general-purpose web crawler that uses a spacetime cache server to receive requests. It can crawl any website, not just UCI domains.

CONFIGURATION
-------------------------

### Step 1: Install dependencies

If you do not have Python 3.6+:

Windows: https://www.python.org/downloads/windows/

Linux: https://docs.python-guide.org/starting/install3/linux/

MAC: https://docs.python-guide.org/starting/install3/osx/

Check if pip is installed by opening up a terminal/command prompt and typing
`python3 -m pip`. This should show the help menu for all the commands possible with pip. If it does not, then get pip by following the
instructions at https://pip.pypa.io/en/stable/installing/

To install the dependencies for this project run the following two commands
after ensuring pip is installed for the version of python you are using.
Admin privileges might be required to execute the commands. Also make sure
that the terminal is at the root folder of this project.
```
python -m pip install packages/spacetime-2.1.1-py3-none-any.whl
python -m pip install -r packages/requirements.txt
```

### Step 2: Configuring config.ini

Set the options in the config.ini file. The following
configurations exist.

**USERAGENT**: Set the useragent to a unique string for your crawler.
It is important to set the useragent appropriately to get credit for
hitting the cache.

**HOST**: This is the host name of the caching server.

**PORT**: This is the port number of the caching server.

**SEEDURL**: The starting URL(s) that the crawler first starts downloading (comma-separated).

**POLITENESS**: The time delay each thread has to wait for after each download.

**SAVE**: The file that is used to save crawler progress. If you want to restart the
crawler from the seed url, you can simply delete this file.

**THREADCOUNT**: This can be a configuration used to increase the number of concurrent
threads used. Do not change it if you have not implemented multi-threading in
the crawler. The crawler, as it is, is deliberately not thread safe.

### Step 3: Scraper Function

The main scraping logic is in `scraper.py`:

```
def scrape_links(url: str, resp: utils.response.Response, allowed_domains=None, blocked_extensions=None) -> list:
    ...
```

- `url`: The URL that was added to the frontier and downloaded from the cache.
- `resp`: The response given by the caching server for the requested URL (see `utils/response.py`).
- `allowed_domains`: (Optional) Set of domains to restrict crawling to. If `None`, any domain is allowed.
- `blocked_extensions`: (Optional) Regex string of file extensions to block. Defaults to common non-HTML types.

**Return Value**

This function returns a list of URLs that are scraped from the response. These URLs will be
added to the Frontier and retrieved from the cache. These URLs are filtered so that URLs that
do not need to be downloaded are not added to the frontier.

The filtering is handled by the `is_valid_url` function in `scraper.py`, which you can customize.

ARCHITECTURE
-------------------------

### FLOW

The crawler receives a cache host and port from the spacetime servers
and instantiates the config.

It launches a crawler (defined in `crawler/__init__.py`) which creates a
Frontier and Worker(s) using the optional parameters `frontier_factory`, and
`worker_factory`.

When the crawler is started, workers are created that pick up an
undownloaded link from the frontier, download it from the cache server, and
pass the response to your scraper function. The links that are received by
the scraper are added to the list of undownloaded links in the frontier and
the URL that was downloaded is marked as complete. The cycle continues until
there are no more URLs to be downloaded in the frontier.

### REDEFINING THE FRONTIER:

You can make your own frontier to use with the crawler if they meet this
interface definition:
```
class Frontier:
    def __init__(self, config, restart):
        # Initializer.
        # config -> Config object (defined in utils/config.py)
        # restart -> A bool that is True if the crawler has to restart
        #           from the seed url and delete any current progress.

    def get_tbd_url(self):
        # Get one url that has to be downloaded.
        # Can return None to signify the end of crawling.

    def add_url(self, url):
        # Adds one url to the frontier to be downloaded later.
        # Checks can be made to prevent downloading duplicates.
    
    def mark_url_complete(self, url):
        # Mark a url as completed so that on restart, this url is not
        # downloaded again.
```
A sample reference is given in `utils/frontier.py`. Note that this
reference is not thread safe.

### REDEFINING THE WORKER

You can make your own worker to use with the crawler if they meet this
interface definition:
```
from scraper import scrape_links
from utils.download import download
class Worker(Thread): # Worker must inherit from Thread or Process.
    def __init__(self, worker_id, config, frontier):
        # worker_id -> a unique id for the worker to self identify.
        # config -> Config object (defined in utils/config.py)
        # frontier -> Frontier object created by the Crawler.
        self.config = config
        super().__init__(daemon=True)

    def run(self):
        In loop:
            > url = get one undownloaded link from frontier.
            > resp = download(url, self.config)
            > next_links = scrape_links(url, resp)
            > add next_links to frontier
            > sleep for self.config.time_delay
```
A sample reference is given in `utils/worker.py`.

THINGS TO KEEP IN MIND
-------------------------

1. It is important to filter out URLs that do not point to a webpage. For
   example, PDFs, PPTs, css, js, etc. The `is_valid_url` function filters a large number of
   such extensions, but you can customize it further.
2. You can restrict crawling to specific domains by passing `allowed_domains` to `scrape_links`.
3. It is important to maintain politeness to the cache server (on a per-domain basis).
4. Set the user agent in the config.ini correctly to get credit for hitting the cache servers.
5. Launching multiple instances of the crawler will download the same URLs in
   both. Mechanisms can be used to avoid that, however the politeness limits
   still apply and will be checked.
