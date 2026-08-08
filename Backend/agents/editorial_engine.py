from agents.persona_engine import PersonaEngine


class EditorialEngine:

    def __init__(self):

        self.persona = PersonaEngine().get_persona()

    def evaluate(self, topic):

        score = 0

        title = topic.get(
            "title",
            ""
        ).lower()

        summary = topic.get(
            "summary",
            ""
        )

        category = topic.get(
            "category",
            ""
        ).lower()

        source = topic.get(
            "source",
            "Unknown"
        )

        # --------------------------------
        # Interest Matching
        # --------------------------------

        for interest in self.persona.interests:

            if interest.lower() in title:

                score += 20

        # --------------------------------
        # Reject Unwanted Topics
        # --------------------------------

        for reject in self.persona.reject_topics:

            if reject.lower() in title:

                return {
                    "approved": False,
                    "score": 0,
                    "reason": (
                        f"Rejected because it matches "
                        f"'{reject}'."
                    )
                }

        # --------------------------------
        # AI / Technology Relevance
        # --------------------------------

        if category in [
            "ai",
            "llm",
            "machine learning",
            "developer tools",
            "ai agents"
        ]:

            score += 40

        # --------------------------------
        # Summary Quality
        # --------------------------------

        if len(summary) > 30:

            score += 20

        # --------------------------------
        # Source Quality
        # --------------------------------

        if source != "Unknown":

            score += 20

        # --------------------------------
        # Breeth Context
        # --------------------------------

        memory_context = topic.get(
            "memory_context"
        )

        if memory_context:

            edges = memory_context.get(
                "edges",
                []
            )

            if edges:

                score += 10

        # --------------------------------
        # Final Score
        # --------------------------------

        score = min(
            score,
            100
        )

        approved = score >= 60

        # --------------------------------
        # Decision Reason
        # --------------------------------

        if memory_context and memory_context.get("edges"):

            reason = (
                "Topic passed editorial review "
                "with supporting historical context "
                "from agent memory."
            )

        elif approved:

            reason = (
                "Topic passed editorial review."
            )

        else:

            reason = (
                "Topic quality below publishing threshold."
            )

        return {

            "approved": approved,

            "score": score,

            "reason": reason
        }