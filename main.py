from cli.interactive import get_user_settings
from crawler.core import crawl

if __name__ == "__main__":
    settings = get_user_settings()
    crawl(
        start_url=settings["start_url"],
        allowed_domains=settings["allowed_domains"],
        blocked_extensions=settings["blocked_extensions"],
        crawl_depth=settings["crawl_depth"],
        politeness=settings["politeness"]
    )
