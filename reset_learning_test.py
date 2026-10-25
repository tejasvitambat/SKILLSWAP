from app import app
from extensions import db
from models import (
    TopicProgress,
    TaskEvaluation,
    TaskSubmission,
    TopicTask,
    RoadmapTopic,
)

with app.app_context():

    print("=" * 60)
    print("SKILLSWAP - RESET LEARNING TEST DATA")
    print("=" * 60)

    # 1. Delete task evaluations first
    evaluations = TaskEvaluation.query.delete(
        synchronize_session=False
    )
    print(f"Task evaluations deleted: {evaluations}")

    # 2. Delete task submissions
    submissions = TaskSubmission.query.delete(
        synchronize_session=False
    )
    print(f"Task submissions deleted: {submissions}")

    # 3. Delete topic progress
    progress = TopicProgress.query.delete(
        synchronize_session=False
    )
    print(f"Topic progress deleted: {progress}")

    # 4. Delete generated topic tasks
    tasks = TopicTask.query.delete(
        synchronize_session=False
    )
    print(f"Topic tasks deleted: {tasks}")

    db.session.commit()

    print()
    print("Learning test data reset successfully.")
    print("Users / Skills / Assessments were NOT deleted.")
    print("=" * 60)