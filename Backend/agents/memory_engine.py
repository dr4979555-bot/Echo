from database.models import Memory
from services.breeth_service import BreethService


class MemoryEngine:

    def __init__(self, db):
        self.db = db
        self.breeth = BreethService()

    def topic_exists(
        self,
        agent_id,
        title: str
    ):
        """
        Check exact duplicates in local SQLite memory.
        """

        normalized_title = title.strip().lower()

        return (
            self.db
            .query(Memory)
            .filter(
                Memory.agent_id == agent_id,
                Memory.topic == normalized_title
            )
            .first()
        )

    def get_context(
        self,
        title: str
    ):
        """
        Retrieve related knowledge from Breeth.
        """

        try:

            result = self.breeth.search(
                title,
                limit=5
            )

            return result

        except Exception as e:

            print(
                "Breeth context retrieval failed:",
                e
            )

            return None

    def remember_topic(
        self,
        agent_id,
        title,
        decision,
        score,
        summary="",
        category="",
        source="Unknown"
    ):
        """
        Store topic in SQLite and Breeth.
        """

        normalized_title = title.strip().lower()

        # -------------------------
        # SQLite Memory
        # -------------------------

        memory = Memory(
            agent_id=agent_id,
            topic=normalized_title,
            decision=decision,
            importance_score=score
        )

        self.db.add(memory)

        self.db.commit()

        self.db.refresh(memory)

        # -------------------------
        # Breeth Memory
        # -------------------------

        try:

            result = self.breeth.save_topic_memory(
                agent_id=agent_id,
                title=title,
                summary=summary,
                category=category,
                source=source,
                decision=decision,
                score=score
            )

            print(
                "Breeth topic memory saved:",
                result
            )

        except Exception as e:

            print(
                "Breeth memory save failed:",
                e
            )

        return memory

    def get_all_memory(
        self,
        agent_id
    ):
        """
        Return memories of a specific agent.
        """

        return (
            self.db
            .query(Memory)
            .filter(
                Memory.agent_id == agent_id
            )
            .order_by(
                Memory.created_at.desc()
            )
            .all()
        )