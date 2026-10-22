import os
from dotenv import load_dotenv
load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_SECRET = os.getenv("REDDIT_SECRET")
MONGO_URI = os.getenv("MONGO_URI")
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = os.getenv("REDIS_PORT", 6379)
# config.py
"""
SEFORCSE Configuration
All crawlable websites are grouped by category.
New websites can be added without modifying any spider.
"""
SOURCES = {
    # ==========================================================
    # Documentation
    # ==========================================================
    "docs": [
        "https://react.dev",
        "https://developer.mozilla.org/en-US/",
        "https://docs.python.org/3/",
        "https://nodejs.org/en/docs",
        "https://go.dev/doc/",
        "https://learn.microsoft.com/",
        "https://docs.oracle.com/en/java/",
        "https://angular.dev",
        "https://vuejs.org",
        "https://docs.docker.com",
        "https://kubernetes.io/docs/",
        "https://flutter.dev/docs",
        "https://dart.dev/guides",
        "https://www.typescriptlang.org/docs/",
        "https://docs.djangoproject.com/",
        "https://flask.palletsprojects.com/",
        "https://fastapi.tiangolo.com/",
        "https://spring.io/projects",
        "https://laravel.com/docs",
        "https://rust-lang.org/learn"
    ],
    # ==========================================================
    # Technical Blogs
    # ==========================================================
    "blogs": [
        "https://dev.to",
        "https://hashnode.com",
        "https://www.freecodecamp.org/news/",
        "https://blog.logrocket.com/",
        "https://css-tricks.com",
        "https://martinfowler.com",
        "https://www.codeproject.com",
        "https://engineering.fb.com",
        "https://netflixtechblog.com",
        "https://engineering.atspotify.com",
        "https://aws.amazon.com/blogs/",
        "https://cloud.google.com/blog",
        "https://opensource.googleblog.com",
        "https://blog.jetbrains.com",
        "https://blog.cloudflare.com"
    ],
    # ==========================================================
    # Developer Forums
    # ==========================================================
    "forums": [
        "https://news.ycombinator.com/",
        "https://lobste.rs/"
    ],
    "qa": [
        "https://stackoverflow.com/questions",
        "https://superuser.com/questions",
        "https://serverfault.com/questions",
        "https://softwareengineering.stackexchange.com"
    ]
}
# ==============================================================
# API / Collector Based Sources
# (Not crawled by spiders)
# ==============================================================
COLLECTORS = {
    "stackoverflow": True,
    "github": True,
    "reddit": True,
    "wikipedia": True
}
# ==============================================================
# Crawl Settings
# ==============================================================
CRAWLER = {
    "max_pages_per_spider": 100,
    "crawl_depth": 3,
    "request_timeout": 10,
    "retry_attempts": 3,
    "user_agent": "SEFORCSE/1.0",
    "respect_robots_txt": True,
    "delay_between_requests": 1
}