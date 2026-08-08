import feedparser

from typing import List, Dict


class NewsService:

    def __init__(self):

        self.feeds = [
            {
                "name": "Google News AI",
                "url": (
                    "https://news.google.com/rss/"
                    "search?q=artificial+intelligence"
                    "&hl=en-US&gl=US&ceid=US:en"
                ),
                "category": "AI"
            },
            {
                "name": "Google News AI Agents",
                "url": (
                    "https://news.google.com/rss/"
                    "search?q=AI+agents"
                    "&hl=en-US&gl=US&ceid=US:en"
                ),
                "category": "AI Agents"
            },
            {
                "name": "Google News Machine Learning",
                "url": (
                    "https://news.google.com/rss/"
                    "search?q=machine+learning"
                    "&hl=en-US&gl=US&ceid=US:en"
                ),
                "category": "Machine Learning"
            },
            {
                "name": "Google News Developer AI",
                "url": (
                    "https://news.google.com/rss/"
                    "search?q=AI+developer+tools"
                    "&hl=en-US&gl=US&ceid=US:en"
                ),
                "category": "Developer Tools"
            }
        ]

    def fetch_topics(self) -> List[Dict]:
        """
        Fetch real AI and technology topics
        from RSS feeds.
        """

        topics = []

        for feed_config in self.feeds:

            try:

                feed = feedparser.parse(
                    feed_config["url"]
                )

                for entry in feed.entries[:10]:

                    title = entry.get(
                        "title",
                        ""
                    ).strip()

                    summary = entry.get(
                        "summary",
                        ""
                    ).strip()

                    url = entry.get(
                        "link",
                        ""
                    ).strip()

                    if not title:
                        continue

                    topics.append({

                        "title": title,

                        "summary": summary,

                        "source": feed_config["name"],

                        "url": url,

                        "category": feed_config["category"]

                    })

            except Exception as e:

                print(
                    f"RSS Error "
                    f"({feed_config['name']}):",
                    e
                )

        return self.remove_duplicates(
            topics
        )

    def remove_duplicates(
        self,
        topics: List[Dict]
    ) -> List[Dict]:
        """
        Remove duplicate articles
        using normalized titles.
        """

        seen = set()

        unique_topics = []

        for topic in topics:

            normalized_title = (
                topic["title"]
                .lower()
                .strip()
            )

            if normalized_title in seen:
                continue

            seen.add(
                normalized_title
            )

            unique_topics.append(
                topic
            )

        return unique_topics