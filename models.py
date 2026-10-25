from datetime import datetime

from extensions import db


# ============================================================
# USER
# ============================================================

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    full_name = db.Column(db.String(120), nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)

    profile_photo = db.Column(db.String(255), nullable=True)
    bio = db.Column(db.Text, nullable=True)

    city = db.Column(db.String(100), nullable=True)
    country = db.Column(db.String(100), nullable=True)

    learning_preference = db.Column(db.String(30), nullable=True)
    availability = db.Column(db.String(30), nullable=True)

    is_active = db.Column(db.Boolean, default=True, nullable=False)

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )

    # --------------------------------------------------------
    # Relationships
    # --------------------------------------------------------

    user_skills = db.relationship(
        "UserSkill",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    sent_connections = db.relationship(
        "Connection",
        foreign_keys="Connection.sender_id",
        back_populates="sender",
        cascade="all, delete-orphan"
    )

    received_connections = db.relationship(
        "Connection",
        foreign_keys="Connection.receiver_id",
        back_populates="receiver",
        cascade="all, delete-orphan"
    )

    sent_messages = db.relationship(
        "Message",
        foreign_keys="Message.sender_id",
        back_populates="sender",
        cascade="all, delete-orphan"
    )

    reviews_given = db.relationship(
        "Review",
        foreign_keys="Review.reviewer_id",
        back_populates="reviewer",
        cascade="all, delete-orphan"
    )

    reviews_received = db.relationship(
        "Review",
        foreign_keys="Review.reviewee_id",
        back_populates="reviewee",
        cascade="all, delete-orphan"
    )

    notifications = db.relationship(
        "Notification",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    progress_records = db.relationship(
        "TopicProgress",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    certificates = db.relationship(
        "Certificate",
        back_populates="user",
        cascade="all, delete-orphan"
    )


# ============================================================
# SKILL
# ============================================================

class Skill(db.Model):
    __tablename__ = "skills"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), unique=True, nullable=False)
    slug = db.Column(db.String(100), unique=True, nullable=False)

    category = db.Column(db.String(50), nullable=False)

    description = db.Column(db.Text, nullable=True)

    is_active = db.Column(db.Boolean, default=True, nullable=False)

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    user_skills = db.relationship(
        "UserSkill",
        back_populates="skill",
        cascade="all, delete-orphan"
    )

    assessments = db.relationship(
        "Assessment",
        back_populates="skill",
        cascade="all, delete-orphan"
    )

    roadmaps = db.relationship(
        "Roadmap",
        back_populates="skill",
        cascade="all, delete-orphan"
    )


# ============================================================
# USER SKILL
# ============================================================

class UserSkill(db.Model):
    __tablename__ = "user_skills"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    skill_id = db.Column(
        db.Integer,
        db.ForeignKey("skills.id"),
        nullable=False
    )

    # teach = skill user can teach
    # learn = skill user wants to learn
    skill_type = db.Column(
        db.String(20),
        nullable=False
    )

    # IMPORTANT:
    # Level is earned from assessment.
    # It is NOT selected during signup.
    earned_level = db.Column(
        db.String(30),
        nullable=True
    )

    assessment_score = db.Column(
        db.Float,
        nullable=True
    )

    assessment_completed = db.Column(
        db.Boolean,
        default=False,
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    user = db.relationship(
        "User",
        back_populates="user_skills"
    )

    skill = db.relationship(
        "Skill",
        back_populates="user_skills"
    )

    __table_args__ = (
        db.UniqueConstraint(
            "user_id",
            "skill_id",
            "skill_type",
            name="unique_user_skill_type"
        ),
    )


# ============================================================
# ASSESSMENT
# ============================================================

class Assessment(db.Model):
    __tablename__ = "assessments"

    id = db.Column(db.Integer, primary_key=True)

    skill_id = db.Column(
        db.Integer,
        db.ForeignKey("skills.id"),
        nullable=False
    )

    title = db.Column(
        db.String(150),
        nullable=False
    )

    description = db.Column(
        db.Text,
        nullable=True
    )

    passing_score = db.Column(
        db.Float,
        default=60,
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    skill = db.relationship(
        "Skill",
        back_populates="assessments"
    )

    questions = db.relationship(
        "AssessmentQuestion",
        back_populates="assessment",
        cascade="all, delete-orphan"
    )


# ============================================================
# ASSESSMENT QUESTION
# ============================================================

class AssessmentQuestion(db.Model):
    __tablename__ = "assessment_questions"

    id = db.Column(db.Integer, primary_key=True)

    assessment_id = db.Column(
        db.Integer,
        db.ForeignKey("assessments.id"),
        nullable=False
    )

    question = db.Column(
        db.Text,
        nullable=False
    )

    option_a = db.Column(db.String(255), nullable=False)
    option_b = db.Column(db.String(255), nullable=False)
    option_c = db.Column(db.String(255), nullable=False)
    option_d = db.Column(db.String(255), nullable=False)

    correct_answer = db.Column(
        db.Text,
        nullable=False
    )

    difficulty = db.Column(
        db.String(30),
        nullable=True
    )

    # TEXT / OUTPUT / CODE
    question_type = db.Column(
        db.String(30),
        nullable=False,
        default="text"
    )

    assessment = db.relationship(
        "Assessment",
        back_populates="questions"
    )

# ============================================================
# ASSESSMENT RESULT
# ============================================================

class AssessmentResult(db.Model):
    __tablename__ = "assessment_results"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    skill_id = db.Column(
        db.Integer,
        db.ForeignKey("skills.id"),
        nullable=False
    )

    assessment_id = db.Column(
        db.Integer,
        db.ForeignKey("assessments.id"),
        nullable=False
    )

    score = db.Column(
        db.Float,
        nullable=False
    )

    correct_answers = db.Column(
        db.Text,
        nullable=False
    )

    total_questions = db.Column(
        db.Integer,
        nullable=False
    )

    earned_level = db.Column(
        db.String(30),
        nullable=False
    )

    completed_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )


# ============================================================
# ROADMAP
# ============================================================

class Roadmap(db.Model):
    __tablename__ = "roadmaps"

    id = db.Column(db.Integer, primary_key=True)

    skill_id = db.Column(
        db.Integer,
        db.ForeignKey("skills.id"),
        nullable=False
    )

    title = db.Column(
        db.String(150),
        nullable=False
    )

    description = db.Column(
        db.Text,
        nullable=True
    )

    is_active = db.Column(
        db.Boolean,
        default=True,
        nullable=False
    )

    skill = db.relationship(
        "Skill",
        back_populates="roadmaps"
    )

    topics = db.relationship(
        "RoadmapTopic",
        back_populates="roadmap",
        cascade="all, delete-orphan",
        order_by="RoadmapTopic.order_index"
    )


# ============================================================
# ROADMAP TOPIC
# ============================================================
class RoadmapTopic(db.Model):
    __tablename__ = "roadmap_topics"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    roadmap_id = db.Column(
        db.Integer,
        db.ForeignKey("roadmaps.id"),
        nullable=False
    )

    title = db.Column(
        db.String(150),
        nullable=False
    )

    explanation = db.Column(
        db.Text,
        nullable=False
    )

    code_example = db.Column(
        db.Text,
        nullable=True
    )

    task_description = db.Column(
        db.Text,
        nullable=True
    )

    task_type = db.Column(
        db.String(30),
        nullable=True
    )

    order_index = db.Column(
        db.Integer,
        nullable=False
    )

    roadmap = db.relationship(
        "Roadmap",
        back_populates="topics"
    )

    progress_records = db.relationship(
        "TopicProgress",
        back_populates="topic",
        cascade="all, delete-orphan"
    )

    task = db.relationship(
        "TopicTask",
        back_populates="topic",
        uselist=False,
        cascade="all, delete-orphan"
    )
# ============================================================
# TOPIC TASK
# ============================================================

class TopicTask(db.Model):
    __tablename__ = "topic_tasks"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    topic_id = db.Column(
        db.Integer,
        db.ForeignKey("roadmap_topics.id"),
        nullable=False,
        unique=True
    )

    task_type = db.Column(
        db.String(30),
        nullable=False
    )

    evaluation_mode = db.Column(
        db.String(50),
        nullable=False,
        default="manual"
    )

    instructions = db.Column(
        db.Text,
        nullable=False
    )

    is_active = db.Column(
        db.Boolean,
        default=True,
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )

    topic = db.relationship(
        "RoadmapTopic",
        back_populates="task"
    )

    submissions = db.relationship(
        "TaskSubmission",
        back_populates="task",
        cascade="all, delete-orphan"
    )


# ============================================================
# TASK SUBMISSION
# ============================================================

class TaskSubmission(db.Model):
    __tablename__ = "task_submissions"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    task_id = db.Column(
        db.Integer,
        db.ForeignKey("topic_tasks.id"),
        nullable=False
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    submission = db.Column(
        db.Text,
        nullable=False
    )

    status = db.Column(
        db.String(30),
        nullable=False,
        default="submitted"
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    task = db.relationship(
        "TopicTask",
        back_populates="submissions"
    )

    user = db.relationship(
        "User"
    )

    evaluation = db.relationship(
        "TaskEvaluation",
        back_populates="submission",
        uselist=False,
        cascade="all, delete-orphan"
    )


# ============================================================
# TASK EVALUATION
# ============================================================

class TaskEvaluation(db.Model):
    __tablename__ = "task_evaluations"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    submission_id = db.Column(
        db.Integer,
        db.ForeignKey("task_submissions.id"),
        nullable=False,
        unique=True
    )

    passed = db.Column(
        db.Boolean,
        nullable=False,
        default=False
    )

    score = db.Column(
        db.Float,
        nullable=True
    )

    feedback = db.Column(
        db.Text,
        nullable=True
    )

    evaluated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    submission = db.relationship(
        "TaskSubmission",
        back_populates="evaluation"
    )

# ============================================================
# TOPIC PROGRESS
# ============================================================

class TopicProgress(db.Model):
    __tablename__ = "topic_progress"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    topic_id = db.Column(
        db.Integer,
        db.ForeignKey("roadmap_topics.id"),
        nullable=False
    )

    status = db.Column(
        db.String(30),
        default="available",
        nullable=False
    )

    learned = db.Column(
        db.Boolean,
        default=False,
        nullable=False
    )

    practiced = db.Column(
        db.Boolean,
        default=False,
        nullable=False
    )

    task_completed = db.Column(
        db.Boolean,
        default=False,
        nullable=False
    )

    completed_at = db.Column(
        db.DateTime,
        nullable=True
    )

    user = db.relationship(
        "User",
        back_populates="progress_records"
    )

    topic = db.relationship(
        "RoadmapTopic",
        back_populates="progress_records"
    )

    __table_args__ = (
        db.UniqueConstraint(
            "user_id",
            "topic_id",
            name="unique_user_topic_progress"
        ),
    )


# ============================================================
# CONNECTION
# ============================================================

class Connection(db.Model):
    __tablename__ = "connections"

    id = db.Column(db.Integer, primary_key=True)

    sender_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    receiver_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    status = db.Column(
        db.String(30),
        default="pending",
        nullable=False
    )

    message = db.Column(
        db.Text,
        nullable=True
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    accepted_at = db.Column(
        db.DateTime,
        nullable=True
    )

    sender = db.relationship(
        "User",
        foreign_keys=[sender_id],
        back_populates="sent_connections"
    )

    receiver = db.relationship(
        "User",
        foreign_keys=[receiver_id],
        back_populates="received_connections"
    )

    messages = db.relationship(
        "Message",
        back_populates="connection",
        cascade="all, delete-orphan"
    )

    sessions = db.relationship(
        "Session",
        back_populates="connection",
        cascade="all, delete-orphan"
    )


# ============================================================
# MESSAGE
# ============================================================

# ============================================================
# MESSAGE
# ============================================================

class Message(db.Model):
    __tablename__ = "messages"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    connection_id = db.Column(
        db.Integer,
        db.ForeignKey("connections.id"),
        nullable=False
    )

    sender_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    message = db.Column(
        db.Text,
        nullable=False
    )

    is_read = db.Column(
        db.Boolean,
        default=False,
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    connection = db.relationship(
        "Connection",
        back_populates="messages"
    )

    sender = db.relationship(
        "User",
        foreign_keys=[sender_id],
        back_populates="sent_messages"
    )


# ============================================================
# SESSION
# ============================================================


class Session(db.Model):
    __tablename__ = "sessions"

    id = db.Column(db.Integer, primary_key=True)

    connection_id = db.Column(
        db.Integer,
        db.ForeignKey("connections.id"),
        nullable=False
    )

    title = db.Column(
        db.String(150),
        nullable=False
    )

    skill = db.Column(
        db.String(100),
        nullable=True
    )

    topic = db.Column(
        db.String(150),
        nullable=True
    )

    description = db.Column(
        db.Text,
        nullable=True
    )

    scheduled_at = db.Column(
        db.DateTime,
        nullable=False
    )

    duration_minutes = db.Column(
        db.Integer,
        nullable=False
    )

    session_type = db.Column(
        db.String(30),
        nullable=False
    )

    # Zoom or other online meeting link
    meeting_url = db.Column(
        db.String(500),
        nullable=True
    )

    status = db.Column(
        db.String(30),
        default="pending",
        nullable=False
    )

    message = db.Column(
        db.Text,
        nullable=True
    )

    completion_note = db.Column(
        db.Text,
        nullable=True
    )

    completed_at = db.Column(
        db.DateTime,
        nullable=True
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    connection = db.relationship(
        "Connection",
        back_populates="sessions"
    )


# ============================================================
# REVIEW
# ============================================================

class Review(db.Model):
    __tablename__ = "reviews"

    id = db.Column(db.Integer, primary_key=True)

    session_id = db.Column(
        db.Integer,
        db.ForeignKey("sessions.id"),
        nullable=False
    )

    reviewer_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    reviewee_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    rating = db.Column(
        db.Integer,
        nullable=False
    )

    comment = db.Column(
        db.Text,
        nullable=True
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    reviewer = db.relationship(
        "User",
        foreign_keys=[reviewer_id],
        back_populates="reviews_given"
    )

    reviewee = db.relationship(
        "User",
        foreign_keys=[reviewee_id],
        back_populates="reviews_received"
    )


# ============================================================
# CERTIFICATE
# ============================================================

class Certificate(db.Model):
    __tablename__ = "certificates"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    skill_id = db.Column(
        db.Integer,
        db.ForeignKey("skills.id"),
        nullable=False
    )

    skill_name = db.Column(
        db.String(100),
        nullable=False
    )

    earned_level = db.Column(
        db.String(30),
        nullable=False
    )

    certificate_number = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )

    issued_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    completed_at = db.Column(
        db.DateTime,
        nullable=True
    )

    user = db.relationship(
        "User",
        back_populates="certificates"
    )


# ============================================================
# NOTIFICATION
# ============================================================

class Notification(db.Model):
    __tablename__ = "notifications"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    notification_type = db.Column(
        db.String(50),
        nullable=False
    )

    title = db.Column(
        db.String(150),
        nullable=False
    )

    message = db.Column(
        db.Text,
        nullable=False
    )

    action_url = db.Column(
        db.String(255),
        nullable=True
    )

    category = db.Column(
        db.String(50),
        nullable=True
    )

    is_read = db.Column(
        db.Boolean,
        default=False,
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    user = db.relationship(
        "User",
        back_populates="notifications"
    )