from datetime import datetime


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
        Normalize topic structure.
        """

        normalized = []

        for topic in topics:

            normalized.append({

                "title": topic.get("title", "").strip(),

                "source": topic.get(
                    "source",
                    "Unknown"
                ),

                "url": topic.get(
                    "url",
                    ""
                ),

                "summary": topic.get(
                    "summary",
                    ""
                ),

                "category": topic.get(
                    "category",
                    "AI"
                ),

                "discovered_at": datetime.utcnow().isoformat(),

                "importance_score": 0,

                "status": "pending"

            })

        return normalized

    def remove_duplicates(self, topics):
        """
        Remove duplicate topics using title.
        """

        seen = set()

        unique_topics = []

        for topic in topics:

            title = topic["title"].lower()

            if title not in seen:

                seen.add(title)

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

        title = topic["title"].lower()
        summary = topic["summary"].lower()
        category = topic["category"].lower()

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
        if topic["source"] != "Unknown":
            score += 5

        if topic["url"]:
            score += 5

        return min(score, 100)