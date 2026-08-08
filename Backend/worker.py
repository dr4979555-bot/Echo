from scheduler.scheduler import Scheduler

from database.database import SessionLocal
from services.news_service import NewsService
from agents.orchestrator import Orchestrator


AGENT_ID = "6d2cc51b-6b78-426b-9c43-0f51dad83cdf"


def run_agent_cycle():

    db = SessionLocal()

    try:

        news_service = NewsService()

        orchestrator = Orchestrator(
            news_service,
            db
        )

        result = orchestrator.run(
            AGENT_ID
        )

        print("\n=== Echo Mind Cycle ===")
        print(result)

    except Exception as e:

        print("Worker Error:", e)

    finally:

        db.close()


scheduler = Scheduler(
    callback=run_agent_cycle,
    interval=300
)


print("Echo Mind Scheduler started.")

scheduler.start()


try:

    while True:
        pass

except KeyboardInterrupt:

    print("\nStopping Echo Mind Scheduler...")

    scheduler.stop()