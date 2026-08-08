from agents.discovery_engine import DiscoveryEngine
from agents.editorial_engine import EditorialEngine
from agents.memory_engine import MemoryEngine
from agents.publishing_engine import PublishingEngine


class Orchestrator:

    def __init__(
        self,
        news_service,
        db
    ):

        self.discovery = DiscoveryEngine(
            news_service
        )

        self.editorial = EditorialEngine()

        self.memory = MemoryEngine(
            db
        )

        self.publisher = PublishingEngine(
            db
        )

    def run(self, agent_id):
        """
        Run the complete Echo Mind autonomous workflow.
        """

        topics = self.discovery.discover_topics()

        results = []

        # Prevent duplicate topics
        # during the same run.
        processed_titles = set()

        for topic in topics:

            # --------------------------------
            # Normalize Title
            # --------------------------------

            normalized_title = (
                topic.get("title", "")
                .strip()
                .lower()
            )

            # --------------------------------
            # Current Run Duplicate Check
            # --------------------------------

            if normalized_title in processed_titles:

                results.append({
                    "title": topic.get("title", ""),
                    "status": "skipped",
                    "reason": (
                        "Duplicate topic in current run."
                    )
                })

                continue

            processed_titles.add(
                normalized_title
            )

            # --------------------------------
            # Local Memory Check
            # --------------------------------

            memory = self.memory.topic_exists(
                agent_id,
                topic["title"]
            )

            if memory:

                results.append({
                    "title": topic["title"],
                    "status": "skipped",
                    "reason": (
                        "Already exists in memory."
                    )
                })

                continue

            # --------------------------------
            # Retrieve Breeth Context
            # --------------------------------

            context = self.memory.get_context(
                topic["title"]
            )

            if context:

                topic["memory_context"] = context

            # --------------------------------
            # Editorial Decision
            # --------------------------------

            editorial_result = (
                self.editorial.evaluate(topic)
            )

            if not editorial_result["approved"]:

                # Store rejected decision
                self.memory.remember_topic(
                    agent_id=agent_id,
                    title=topic["title"],
                    decision="reject",
                    score=editorial_result["score"],
                    summary=topic.get(
                        "summary",
                        ""
                    ),
                    category=topic.get(
                        "category",
                        ""
                    ),
                    source=topic.get(
                        "source",
                        "Unknown"
                    )
                )

                results.append({
                    "title": topic["title"],
                    "status": "rejected",
                    "reason": editorial_result["reason"],
                    "score": editorial_result["score"]
                })

                continue

            # --------------------------------
            # Store Published Memory
            # --------------------------------

            self.memory.remember_topic(
                agent_id=agent_id,
                title=topic["title"],
                decision="publish",
                score=editorial_result["score"],
                summary=topic.get(
                    "summary",
                    ""
                ),
                category=topic.get(
                    "category",
                    ""
                ),
                source=topic.get(
                    "source",
                    "Unknown"
                )
            )

            # --------------------------------
            # Add Agent ID
            # --------------------------------

            topic["agent_id"] = agent_id

            # --------------------------------
            # Publish
            # --------------------------------

            post = self.publisher.publish(
                topic,
                editorial_result["reason"]
            )

            results.append({
                "title": topic["title"],
                "status": "published",
                "post_id": str(post.id),
                "score": editorial_result["score"]
            })

        # --------------------------------
        # Final Response
        # --------------------------------

        return {
            "agent_id": agent_id,
            "discovered": len(topics),
            "results": results
        }