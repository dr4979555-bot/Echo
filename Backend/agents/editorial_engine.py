import re

from agents.persona_engine import PersonaEngine


class EditorialEngine:

    def __init__(self):

        self.persona = PersonaEngine().get_persona()

    # ==================================================
    # MAIN EDITORIAL EVALUATION
    # ==================================================

    def evaluate(self, topic):

        score = 0

        title = str(
            topic.get("title", "")
        ).strip()

        summary = str(
            topic.get("summary", "")
        ).strip()

        category = str(
            topic.get("category", "")
        ).strip()

        source = str(
            topic.get("source", "Unknown")
        ).strip()

        discovery_score = topic.get(
            "importance_score",
            0
        )

        memory_context = topic.get(
            "memory_context"
        )

        title_lower = title.lower()
        summary_lower = summary.lower()
        category_lower = category.lower()

        # --------------------------------
        # CLEAN SUMMARY
        # --------------------------------

        clean_summary = self.clean_text(
            summary
        )

        clean_summary_lower = clean_summary.lower()

        # --------------------------------
        # REJECT UNWANTED TOPICS
        # --------------------------------

        for reject in self.persona.reject_topics:

            reject_text = str(
                reject
            ).strip().lower()

            if (
                reject_text
                and (
                    reject_text in title_lower
                    or reject_text in clean_summary_lower
                )
            ):

                return {
                    "approved": False,
                    "score": 0,
                    "reason": (
                        f"Rejected because it matches "
                        f"the unwanted topic '{reject}'."
                    ),
                    "take": ""
                }

        # --------------------------------
        # PERSONA INTEREST
        # --------------------------------

        interest_match = False

        for interest in self.persona.interests:

            interest_text = str(
                interest
            ).strip().lower()

            if (
                interest_text
                and (
                    interest_text in title_lower
                    or interest_text in clean_summary_lower
                    or interest_text in category_lower
                )
            ):

                interest_match = True
                score += 25
                break

        # --------------------------------
        # AI RELEVANCE
        # --------------------------------

        ai_keywords = [
            "ai",
            "artificial intelligence",
            "machine learning",
            "llm",
            "large language model",
            "generative ai",
            "deep learning",
            "neural network",
            "foundation model",
            "multimodal",
            "computer vision",
            "natural language processing",
            "nlp",
            "robotics",
            "intelligent system"
        ]

        ai_match = self.contains_keyword(
            title_lower,
            clean_summary_lower,
            category_lower,
            ai_keywords
        )

        if ai_match:
            score += 20

        # --------------------------------
        # AI AGENT RELEVANCE
        # --------------------------------

        agent_keywords = [
            "agent",
            "ai agent",
            "ai agents",
            "agentic",
            "agentic ai",
            "autonomous agent",
            "agent tools",
            "coding agent",
            "ai assistant",
            "autonomous ai",
            "agent framework"
        ]

        agent_match = self.contains_keyword(
            title_lower,
            clean_summary_lower,
            category_lower,
            agent_keywords
        )

        if agent_match:
            score += 15

        # --------------------------------
        # DEVELOPER / TECHNOLOGY RELEVANCE
        # --------------------------------

        technology_keywords = [
            "developer",
            "developers",
            "coding",
            "software",
            "programming",
            "developer tools",
            "automation",
            "model",
            "api",
            "cloud",
            "technology",
            "framework",
            "platform",
            "database",
            "cybersecurity",
            "security",
            "infrastructure",
            "open source",
            "software engineering"
        ]

        technology_match = self.contains_keyword(
            title_lower,
            clean_summary_lower,
            category_lower,
            technology_keywords
        )

        if technology_match:
            score += 10

        # --------------------------------
        # INDUSTRY IMPACT
        # --------------------------------

        impact_keywords = [
            "launch",
            "launched",
            "launches",
            "release",
            "released",
            "announces",
            "announced",
            "new",
            "breakthrough",
            "study",
            "research",
            "acquisition",
            "investment",
            "security",
            "hack",
            "hacked",
            "breach",
            "update",
            "upgrade",
            "competition",
            "partnership",
            "unveils",
            "unveiled"
        ]

        impact_match = self.contains_keyword(
            title_lower,
            clean_summary_lower,
            category_lower,
            impact_keywords
        )

        if impact_match:
            score += 5

        # --------------------------------
        # DISCOVERY IMPORTANCE
        # --------------------------------

        try:

            discovery_score = int(
                discovery_score
            )

        except (
            TypeError,
            ValueError
        ):

            discovery_score = 0

        if discovery_score >= 70:

            score += 15

        elif discovery_score >= 50:

            score += 10

        elif discovery_score >= 30:

            score += 5

        # --------------------------------
        # SUMMARY QUALITY
        # --------------------------------

        if len(clean_summary) >= 150:

            score += 5

        elif len(clean_summary) >= 60:

            score += 3

        # --------------------------------
        # SOURCE QUALITY
        # --------------------------------

        if (
            source
            and source.lower() != "unknown"
        ):

            score += 5

        # --------------------------------
        # MEMORY CONTEXT
        # --------------------------------

        memory_edges = []

        if isinstance(
            memory_context,
            dict
        ):

            memory_edges = memory_context.get(
                "edges",
                []
            )

        if memory_edges:

            score += 5

        # --------------------------------
        # FINAL SCORE
        # --------------------------------

        score = min(
            score,
            100
        )

        # --------------------------------
        # EDITORIAL APPROVAL
        # --------------------------------

        approved = (
            score >= 60
            and ai_match
        )

        # --------------------------------
        # DECISION REASON
        # --------------------------------

        if not ai_match:

            reason = (
                "Rejected because the topic "
                "does not have sufficient AI relevance."
            )

        elif approved and memory_edges:

            reason = (
                "Topic passed editorial review "
                "with strong AI relevance and "
                "supporting context from agent memory."
            )

        elif approved and interest_match:

            reason = (
                "Topic passed editorial review "
                "because it matches the agent's "
                "interests and has strong AI relevance."
            )

        elif approved and agent_match:

            reason = (
                "Topic passed editorial review "
                "because it has strong relevance "
                "to AI agents and technology."
            )

        elif approved and impact_match:

            reason = (
                "Topic passed editorial review "
                "because it represents a meaningful "
                "AI or technology development."
            )

        elif approved:

            reason = (
                "Topic passed editorial review "
                "with sufficient AI and technology relevance."
            )

        else:

            reason = (
                "Topic quality or relevance "
                "was below the publishing threshold."
            )

        # --------------------------------
        # ECHO MIND TAKE
        # --------------------------------

        take = self.generate_take(
            topic,
            agent_match=agent_match,
            technology_match=technology_match,
            impact_match=impact_match,
            memory_edges=memory_edges
        )

        return {
            "approved": approved,
            "score": score,
            "reason": reason,
            "take": take
        }

    # ==================================================
    # HELPER: KEYWORD MATCH
    # ==================================================

    def contains_keyword(
        self,
        title,
        summary,
        category,
        keywords
    ):

        for keyword in keywords:

            keyword = str(
                keyword
            ).strip().lower()

            if (
                keyword
                and (
                    keyword in title
                    or keyword in summary
                    or keyword in category
                )
            ):

                return True

        return False

    # ==================================================
    # CLEAN RSS / HTML TEXT
    # ==================================================

    def clean_text(
        self,
        text
    ):

        text = str(
            text or ""
        )

        text = re.sub(
            r"<script.*?>.*?</script>",
            " ",
            text,
            flags=re.IGNORECASE | re.DOTALL
        )

        text = re.sub(
            r"<style.*?>.*?</style>",
            " ",
            text,
            flags=re.IGNORECASE | re.DOTALL
        )

        text = re.sub(
            r"<[^>]+>",
            " ",
            text
        )

        text = re.sub(
            r"https?://\S+",
            " ",
            text
        )

        replacements = {
            "&nbsp;": " ",
            "&amp;": "&",
            "&quot;": '"',
            "&#39;": "'",
            "&apos;": "'",
            "&lt;": "<",
            "&gt;": ">",
        }

        for old, new in replacements.items():

            text = text.replace(
                old,
                new
            )

        text = re.sub(
            r"\s+",
            " ",
            text
        )

        return text.strip()

    # ==================================================
    # EXTRACT FIRST USEFUL SENTENCE
    # ==================================================

    def extract_key_sentence(
        self,
        summary
    ):

        if not summary:

            return ""

        sentences = re.split(
            r"(?<=[.!?])\s+",
            summary
        )

        sentences = [
            sentence.strip()
            for sentence in sentences
            if sentence.strip()
        ]

        if not sentences:

            return summary[:300].strip()

        # Prefer a reasonably informative sentence.
        for sentence in sentences:

            if len(sentence) >= 60:

                return (
                    sentence[:300]
                    .strip()
                    .rstrip(".")
                )

        return (
            sentences[0][:300]
            .strip()
            .rstrip(".")
        )

    # ==================================================
    # DETECT TOPIC TYPE
    # ==================================================

    def detect_topic_type(
        self,
        title,
        summary
    ):

        text = (
            f"{title} {summary}"
        ).lower()

        # Security
        security_keywords = [
            "hack",
            "hacked",
            "hacking",
            "cybersecurity",
            "cyber attack",
            "security",
            "breach",
            "credential",
            "infostealer",
            "malware",
            "zero trust",
            "vulnerability"
        ]

        if any(
            keyword in text
            for keyword in security_keywords
        ):

            return "security"

        # Coding / developer tools
        coding_keywords = [
            "coding",
            "developer",
            "developers",
            "programming",
            "code",
            "coding tools",
            "developer tools",
            "software engineering",
            "ide",
            "ai coding"
        ]

        if any(
            keyword in text
            for keyword in coding_keywords
        ):

            return "coding"

        # Research
        research_keywords = [
            "study",
            "research",
            "researchers",
            "scientists",
            "university",
            "paper",
            "experiment",
            "findings"
        ]

        if any(
            keyword in text
            for keyword in research_keywords
        ):

            return "research"

        # Product / launch
        launch_keywords = [
            "launch",
            "launched",
            "launches",
            "release",
            "released",
            "announced",
            "announces",
            "unveils",
            "new tool",
            "new model"
        ]

        if any(
            keyword in text
            for keyword in launch_keywords
        ):

            return "launch"

        # Business / competition
        business_keywords = [
            "acquisition",
            "investment",
            "partnership",
            "competition",
            "competitor",
            "market",
            "startup",
            "company"
        ]

        if any(
            keyword in text
            for keyword in business_keywords
        ):

            return "business"

        return "general"

    # ==================================================
    # ECHO MIND TAKE
    # ==================================================

    def generate_take(
        self,
        topic,
        agent_match=False,
        technology_match=False,
        impact_match=False,
        memory_edges=None
    ):

        title = self.clean_text(
            topic.get(
                "title",
                ""
            )
        )

        summary = self.clean_text(
            topic.get(
                "summary",
                ""
            )
        )

        category = self.clean_text(
            topic.get(
                "category",
                ""
            )
        )

        if not title:

            title = "This development"

        # --------------------------------
        # GET REAL ARTICLE SENTENCE
        # --------------------------------

        key_sentence = self.extract_key_sentence(
            summary
        )

        # --------------------------------
        # DETECT ARTICLE TYPE
        # --------------------------------

        topic_type = self.detect_topic_type(
            title,
            summary
        )

        # --------------------------------
        # SECURITY TAKE
        # --------------------------------

        if topic_type == "security":

            if key_sentence:

                return (
                    f"{title} highlights an important "
                    f"AI security development. "
                    f"{key_sentence}."
                )

            return (
                f"{title} highlights the growing "
                f"importance of security as AI systems "
                f"become more capable."
            )

        # --------------------------------
        # CODING TAKE
        # --------------------------------

        if topic_type == "coding":

            if key_sentence:

                return (
                    f"{title} shows how AI is changing "
                    f"the way developers build software. "
                    f"{key_sentence}."
                )

            return (
                f"{title} reflects the growing role "
                f"of AI-powered tools in software development."
            )

        # --------------------------------
        # AI AGENT TAKE
        # --------------------------------

        if agent_match:

            if key_sentence:

                return (
                    f"{title} is particularly relevant "
                    f"to the evolution of AI agents. "
                    f"{key_sentence}."
                )

            return (
                f"{title} reflects the continued evolution "
                f"of AI agents and autonomous software."
            )

        # --------------------------------
        # RESEARCH TAKE
        # --------------------------------

        if topic_type == "research":

            if key_sentence:

                return (
                    f"{title} adds new research insight "
                    f"to the AI landscape. "
                    f"{key_sentence}."
                )

            return (
                f"{title} highlights how ongoing research "
                f"is expanding the capabilities of AI."
            )

        # --------------------------------
        # PRODUCT / LAUNCH TAKE
        # --------------------------------

        if topic_type == "launch":

            if key_sentence:

                return (
                    f"{title} signals a new development "
                    f"in the AI technology landscape. "
                    f"{key_sentence}."
                )

            return (
                f"{title} signals continued development "
                f"and competition in AI technology."
            )

        # --------------------------------
        # BUSINESS TAKE
        # --------------------------------

        if topic_type == "business":

            if key_sentence:

                return (
                    f"{title} could influence the direction "
                    f"of the AI technology market. "
                    f"{key_sentence}."
                )

            return (
                f"{title} reflects the growing business "
                f"importance of AI technology."
            )

        # --------------------------------
        # TECHNOLOGY TAKE
        # --------------------------------

        if technology_match:

            if key_sentence:

                return (
                    f"{title} represents a notable "
                    f"technology development. "
                    f"{key_sentence}."
                )

            return (
                f"{title} shows how AI and technology "
                f"continue to evolve across the industry."
            )

        # --------------------------------
        # MEMORY-AWARE TAKE
        # --------------------------------

        if memory_edges:

            if key_sentence:

                return (
                    f"{title} connects with themes Echo Mind "
                    f"has encountered before. "
                    f"{key_sentence}."
                )

            return (
                f"{title} connects with topics previously "
                f"encountered in Echo Mind's memory."
            )

        # --------------------------------
        # GENERAL AI TAKE
        # --------------------------------

        if key_sentence:

            return (
                f"{title} is relevant to the broader "
                f"AI and technology landscape. "
                f"{key_sentence}."
            )

        # --------------------------------
        # FINAL FALLBACK
        # --------------------------------

        return (
            f"{title} is a development worth monitoring "
            f"in the broader "
            f"{category or 'AI and technology'} space."
        )