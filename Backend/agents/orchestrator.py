from agents.discovery_engine import DiscoveryEngine
from agents.editorial_engine import EditorialEngine
from agents.memory_engine import MemoryEngine
from agents.publishing_engine import PublishingEngine


class Orchestrator:

    def __init__(self, news_service, db):

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

    def run(self, objective, agent_id):

        print("\n==============================")
        print("ECHO MIND ORCHESTRATOR START")
        print("==============================")

        print(f"AGENT ID: {agent_id}")
        print(f"OBJECTIVE: {objective}")

        # --------------------------------
        # DISCOVERY
        # --------------------------------

        print("\n[1] DISCOVERY START")

        topics = self.discovery.discover_topics()

        print(
            f"[1] DISCOVERY COMPLETE - {len(topics)} topics found"
        )

        results = []

        processed_titles = set()

        # --------------------------------
        # PROCESS TOPICS
        # --------------------------------

        for index, topic in enumerate(topics, start=1):

            print(
                f"\n---------- TOPIC {index} ----------"
            )

            title = topic.get(
                "title",
                ""
            )

            print(
                f"TITLE: {title}"
            )

            normalized_title = (
                title
                .strip()
                .lower()
            )

            # --------------------------------
            # DUPLICATE CHECK
            # --------------------------------

            print("[2] CHECKING DUPLICATE")

            if normalized_title in processed_titles:

                print(
                    "[2] DUPLICATE - SKIPPING"
                )

                results.append({
                    "title": title,
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
            # MEMORY CHECK
            # --------------------------------

            print("[3] MEMORY CHECK START")

            memory = self.memory.topic_exists(
                agent_id,
                title
            )

            print(
                f"[3] MEMORY CHECK COMPLETE: {memory}"
            )

            if memory:

                print(
                    "[3] ALREADY EXISTS - SKIPPING"
                )

                results.append({
                    "title": title,
                    "status": "skipped",
                    "reason": (
                        "Already exists in memory."
                    )
                })

                continue

            # --------------------------------
            # MEMORY CONTEXT
            # --------------------------------

            print("[4] MEMORY CONTEXT START")

            context = self.memory.get_context(
                title
            )

            print(
                "[4] MEMORY CONTEXT COMPLETE"
            )

            if context:
                topic["memory_context"] = context

            # --------------------------------
            # ADD AGENT ID
            # --------------------------------

            topic["agent_id"] = agent_id

            # --------------------------------
            # EDITORIAL
            # --------------------------------

            print("[5] EDITORIAL START")

            editorial_result = (
                self.editorial.evaluate(topic)
            )

            print(
                "[5] EDITORIAL COMPLETE:",
                editorial_result
            )

            # --------------------------------
            # REJECTED
            # --------------------------------

            if not editorial_result["approved"]:

                print(
                    "[6] TOPIC REJECTED"
                )

                self.memory.remember_topic(
                    agent_id=agent_id,
                    title=title,
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
                    "title": title,
                    "status": "rejected",
                    "reason": editorial_result["reason"],
                    "score": editorial_result["score"]
                })

                continue

            # --------------------------------
            # SAVE MEMORY
            # --------------------------------

            print(
                "[6] SAVING TOPIC TO MEMORY"
            )

            self.memory.remember_topic(
                agent_id=agent_id,
                title=title,
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

            print(
                "[6] MEMORY SAVE COMPLETE"
            )

            # --------------------------------
            # PUBLISH
            # --------------------------------

            print(
                "[7] PUBLISH START"
            )

            topic["take"] = editorial_result.get("take","")
            post = self.publisher.publish(topic,editorial_result["reason"])

            print(
                f"[7] PUBLISH COMPLETE - POST ID: {post.id}"
            )

            results.append({
                "title": title,
                "status": "published",
                "post_id": str(post.id),
                "score": editorial_result["score"]
            })

        # --------------------------------
        # COMPLETE
        # --------------------------------

        print("\n==============================")
        print("ECHO MIND ORCHESTRATOR COMPLETE")
        print("==============================")

        return {
            "success": True,
            "agent_id": agent_id,
            "objective": objective,
            "discovered": len(topics),
            "results": results
        }