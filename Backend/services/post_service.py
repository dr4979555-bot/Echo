from agents.publishing_engine import PublishingEngine


class PostService:

    def __init__(self, db):
        self.db = db
        self.publisher = PublishingEngine(db)

    def create_post(self, topic, rationale):

        return self.publisher.publish(
            topic,
            rationale
        )