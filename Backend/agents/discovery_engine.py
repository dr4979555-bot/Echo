from datetime import datetime
import re
from html import unescape


class DiscoveryEngine:

    def __init__(self, news_service):
        self.news_service = news_service

    def discover_topics(self):
        """
        Fetch, normalize, deduplicate and rank technology topics.
        """

        topics = self.news_service.fetch_topics()

        topics = self.normalize_topics(topics)

        topics = self.remove_duplicates(topics)

        topics = self.score_topics(topics)

        return topics

    def normalize_topics(self, topics):
        """
        Normalize topic structure and clean incoming text/URLs.
        """

        normalized = []

        for topic in topics:

            title = self.clean_text(
                topic.get("title", "")
            )

            source = self.clean_text(
                topic.get("source", "Unknown")
            )

            url = self.clean_url(
                topic.get("url", "")
            )

            summary = self.clean_text(
                topic.get("summary", "")
            )

            category = self.clean_text(
                topic.get("category", "AI")
            )

            normalized.append({

                "title": title,

                "source": source or "Unknown",

                "url": url,

                "summary": summary,

                "category": category or "AI",

                "discovered_at": datetime.utcnow().isoformat(),

                "importance_score": 0,

                "status": "pending"

            })

        return normalized

    def remove_duplicates(self, topics):
        """
        Remove duplicate topics using normalized title and URL.
        """

        seen_titles = set()
        seen_urls = set()

        unique_topics = []

        for topic in topics:

            title = self.normalize_key(
                topic.get("title", "")
            )

            url = self.normalize_key(
                topic.get("url", "")
            )

            # Prefer URL as the strongest duplicate key.
            if url and url in seen_urls:
                continue

            # Also prevent duplicate titles.
            if title and title in seen_titles:
                continue

            if title:
                seen_titles.add(title)

            if url:
                seen_urls.add(url)

            unique_topics.append(topic)

        return unique_topics

    def score_topics(self, topics):
        """
        Calculate importance score for every topic.
        """

        for topic in topics:

            topic["importance_score"] = (
                self.calculate_importance(topic)
            )

        topics.sort(
            key=lambda topic: topic["importance_score"],
            reverse=True
        )

        return topics

    def calculate_importance(self, topic):
        """
        Calculate topic importance based on
        relevance, category and available information.
        """

        score = 0

        title = topic.get("title", "").lower()
        summary = topic.get("summary", "").lower()
        category = topic.get("category", "").lower()

        # AI relevance
        if "ai" in title:
            score += 20

        if "ai" in summary:
            score += 15

        if "ai" in category:
            score += 20

        # Agent relevance
        if "agent" in title:
            score += 15

        if "agent" in summary:
            score += 10

        # Technology keywords
        keywords = [
            "model",
            "automation",
            "developer",
            "technology",
            "machine learning",
            "artificial intelligence"
        ]

        for keyword in keywords:

            if keyword in title:
                score += 5

            if keyword in summary:
                score += 3

        # Source and URL availability
        if topic.get("source") and topic["source"] != "Unknown":
            score += 5

        if topic.get("url"):
            score += 5

        return min(score, 100)

    def clean_text(self, value):
        """
        Remove HTML markup and escaped HTML from incoming text.
        """

        if not value:
            return ""

        value = str(value)

        # Decode HTML entities such as &amp; and &#x27;
        value = unescape(value)

        # Remove HTML tags.
        value = re.sub(
            r"<[^>]+>",
            " ",
            value
        )

        # Remove markdown-style links:
        # [text](url)
        # Remove markdown links completely.
        value = re.sub( r"\[([^\]]+)\]\([^)]+\)", "", value)

        # Remove excessive whitespace.
        value = re.sub(
            r"\s+",
            " ",
            value
        )

        return value.strip()

    def clean_url(self, value):
        """
        Return a clean URL without HTML or markdown wrappers.
        """

        if not value:
            return ""

        value = unescape(str(value)).strip()

        # Handle markdown URL:
        # [https://example.com](https://example.com)
        markdown_match = re.search(
            r"\]\((https?://[^)]+)\)",
            value
        )

        if markdown_match:
            return markdown_match.group(1).strip()

        # Handle HTML href:
        # <a href="https://example.com">
        href_match = re.search(
            r'href=["\'](https?://[^"\']+)["\']',
            value
        )

        if href_match:
            return href_match.group(1).strip()

        # Extract plain URL if additional text exists.
        url_match = re.search(
            r"https?://[^\s<>\"']+",
            value
        )

        if url_match:
            return url_match.group(0).strip()

        return value

    def normalize_key(self, value):
        """
        Create a stable key for duplicate detection.
        """

        value = self.clean_text(value)

        value = value.lower()

        value = re.sub(
            r"\s+",
            " ",
            value
        )

        return value.strip()