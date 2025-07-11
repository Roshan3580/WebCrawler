def get_user_settings():
    print("Welcome to the Modular Interactive Web Crawler!\n")
    start_url = input("Enter the starting URL to crawl: ").strip()
    if not start_url:
        raise ValueError("A starting URL is required.")

    allowed_domains_input = input("Restrict to specific domains? (comma-separated, leave blank for any): ").strip()
    allowed_domains = set(d.strip() for d in allowed_domains_input.split(",") if d.strip()) if allowed_domains_input else None

    blocked_ext_input = input("Blocked file extensions (regex, leave blank for default): ").strip()
    blocked_extensions = blocked_ext_input if blocked_ext_input else None

    try:
        crawl_depth = int(input("Crawl depth (default 2): ").strip() or 2)
    except ValueError:
        crawl_depth = 2

    try:
        politeness = float(input("Politeness delay in seconds (default 0.5): ").strip() or 0.5)
    except ValueError:
        politeness = 0.5

    return {
        "start_url": start_url,
        "allowed_domains": allowed_domains,
        "blocked_extensions": blocked_extensions,
        "crawl_depth": crawl_depth,
        "politeness": politeness
    }
