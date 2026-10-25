import os
import uuid
import ast
import subprocess
import sys
import tempfile
import os
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from datetime import datetime,timedelta
from types import SimpleNamespace

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash,
    send_from_directory
)

from werkzeug.utils import secure_filename

from extensions import db
from flask_migrate import Migrate
from universal_evaluator import evaluate_submission

from models import (
    User,
    Skill,
    UserSkill,
    Assessment,
    AssessmentQuestion,
    AssessmentResult,
    Roadmap,
    RoadmapTopic,
    TopicProgress,
    Connection,
    Message,
    Session,
    Session as LearningSession,
    Review,
    Certificate,
    Notification,
    TopicTask,
    TaskSubmission,
    TaskEvaluation,
)

# ============================================================
# APP CONFIGURATION
# ============================================================

app = Flask(__name__)

app.config["SECRET_KEY"] = "skillswap-secret-key-change-later"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///skillswap.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

print("SKILLSWAP DATABASE URI:", app.config["SQLALCHEMY_DATABASE_URI"])
print("SKILLSWAP INSTANCE PATH:", app.instance_path)


db.init_app(app)
migrate = Migrate(app, db)


@app.context_processor
def inject_current_user():
    user_id = session.get("user_id")
    unread_count = 0

    if user_id:
        user = User.query.get(user_id)

        if user:
            unread_count = Notification.query.filter_by(
                user_id=user_id,
                is_read=False
            ).count()

            return {
                "current_user": user,
                "nav_unread_count": unread_count,
                "flask_session": session
            }

    return {
        "current_user": SimpleNamespace(
            is_authenticated=False,
            id=None
        ),
        "nav_unread_count": unread_count,
        "flask_session": session
    }

@app.template_filter("ist_time")
def ist_time(value):
    if value is None:
        return ""

    return (value + timedelta(hours=5, minutes=30)).strftime("%I:%M %p")

@app.template_filter("profile_image")
def profile_image(photo_path):
    if not photo_path:
        return ""

    # Normalize paths saved in the database
    photo_path = str(photo_path).replace("\\", "/").strip()
    photo_path = photo_path.lstrip("/")

    # Remove "static/" if it was saved in the database
    if photo_path.startswith("static/"):
        photo_path = photo_path[len("static/"):]

    candidates = [photo_path]

    # Also check common profile-photo folders
    if "/" not in photo_path:
        candidates.extend([
            f"uploads/{photo_path}",
            f"profile_photos/{photo_path}",
        ])

    for candidate in candidates:
        full_path = os.path.join(
            app.static_folder,
            *candidate.split("/")
        )

        if os.path.isfile(full_path):
            return url_for("static", filename=candidate)

    return ""



# ============================================================
# PROFILE PHOTO UPLOAD CONFIGURATION
# ============================================================

app.config["UPLOAD_FOLDER"] = os.path.join(
    app.root_path,
    "static",
    "uploads"
)

os.makedirs(
    app.config["UPLOAD_FOLDER"],
    exist_ok=True
)

# ============================================================
# GLOBAL TEMPLATE DATA
# ============================================================

@app.context_processor
def inject_global_data():
    return {
        "current_year": datetime.now().year
    }


# ============================================================
# HOME
# ============================================================

@app.route("/")
def home():
    return render_template("home.html")


# ============================================================
# HOW IT WORKS
# ============================================================

@app.route("/how-it-works")
def how_it_works():
    return render_template("how_it_works.html")

# ============================================================
# LOGIN
# ============================================================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get(
            "email",
            ""
        ).strip()

        password = request.form.get(
            "password",
            ""
        )

        # ----------------------------------------------------
        # VALIDATION
        # ----------------------------------------------------

        if not email or not password:

            flash(
                "Please enter your email and password.",
                "error"
            )

            return redirect(
                url_for("login")
            )

        # ----------------------------------------------------
        # FIND USER
        # ----------------------------------------------------

        user = User.query.filter_by(
            email=email
        ).first()

        if not user:

            flash(
                "Invalid email or password.",
                "error"
            )

            return redirect(
                url_for("login")
            )

        # ----------------------------------------------------
        # ACCOUNT STATUS
        # ----------------------------------------------------

        if hasattr(user, "is_active") and not user.is_active:

            flash(
                "Your account is currently inactive.",
                "error"
            )

            return redirect(
                url_for("login")
            )

        # ----------------------------------------------------
        # PASSWORD CHECK
        # ----------------------------------------------------
        # Current project stores password in password_hash.
        # Hashing can be upgraded later without changing
        # the login flow.

        if user.password_hash != password:

            flash(
                "Invalid email or password.",
                "error"
            )

            return redirect(
                url_for("login")
            )

        # ----------------------------------------------------
        # LOGIN SESSION
        # ----------------------------------------------------

        session.clear()

        session["user_id"] = user.id

        flash(
            "Welcome back!",
            "success"
        )

        # Existing users go directly to dashboard.
        return redirect(
            url_for("dashboard")
        )

    # --------------------------------------------------------
    # LOGIN PAGE
    # --------------------------------------------------------

    return render_template(
        "login.html"
    )


# ============================================================
# SIGNUP
# ============================================================

@app.route("/signup", methods=["GET", "POST"])
def signup():

    if request.method == "POST":

        # ----------------------------------------------------
        # FORM DATA
        # ----------------------------------------------------

        full_name = request.form.get(
            "full_name",
            ""
        ).strip()

        username = request.form.get(
            "username",
            ""
        ).strip()

        email = request.form.get(
            "email",
            ""
        ).strip()

        password = request.form.get(
            "password",
            ""
        )

        # ----------------------------------------------------
        # REQUIRED FIELD VALIDATION
        # ----------------------------------------------------

        if (
            not full_name
            or not username
            or not email
            or not password
        ):

            flash(
                "Please fill all required fields.",
                "error"
            )

            return redirect(
                url_for("signup")
            )

        # ----------------------------------------------------
        # EMAIL DUPLICATE CHECK
        # ----------------------------------------------------

        existing_email = User.query.filter_by(
            email=email
        ).first()

        if existing_email:

            flash(
                "Email already registered.",
                "error"
            )

            return redirect(
                url_for("signup")
            )

        # ----------------------------------------------------
        # USERNAME DUPLICATE CHECK
        # ----------------------------------------------------

        existing_username = User.query.filter_by(
            username=username
        ).first()

        if existing_username:

            flash(
                "Username already taken.",
                "error"
            )

            return redirect(
                url_for("signup")
            )

        # ----------------------------------------------------
        # CREATE USER
        # ----------------------------------------------------

        user = User(
            full_name=full_name,
            username=username,
            email=email,
            password_hash=password,
            is_active=True
        )

        db.session.add(user)

        try:

            db.session.commit()

        except Exception:

            db.session.rollback()

            flash(
                "Something went wrong while creating your account.",
                "error"
            )

            return redirect(
                url_for("signup")
            )

        # ----------------------------------------------------
        # CREATE LOGIN SESSION
        # ----------------------------------------------------

        session.clear()

        session["user_id"] = user.id

        flash(
            "Account created successfully!",
            "success"
        )

        # New user must complete profile first.
        return redirect(
            url_for("profile_setup")
        )

    # --------------------------------------------------------
    # SIGNUP PAGE
    # --------------------------------------------------------

    return render_template(
        "signup.html"
    )


# ============================================================
# LOGOUT
# ============================================================

@app.route("/logout", methods=["GET", "POST"])
def logout():

    session.clear()

    flash(
        "You have been logged out.",
        "success"
    )

    return redirect(
        url_for("home")
    )


# ============================================================
# FORGOT PASSWORD
# ============================================================

@app.route(
    "/forgot-password",
    methods=["GET", "POST"]
)
def forgot_password():

    if request.method == "POST":

        email = request.form.get(
            "email",
            ""
        ).strip()

        # ----------------------------------------------------
        # EMAIL VALIDATION
        # ----------------------------------------------------

        if not email:

            errors = {
                "email":
                    "Please enter your email address."
            }

            return render_template(
                "forgot_password.html",
                errors=errors,
                reset_sent=False
            )

        # ----------------------------------------------------
        # FIND USER
        # ----------------------------------------------------

        user = User.query.filter_by(
            email=email
        ).first()

        if not user:

            errors = {
                "email":
                    "No account found with this email address."
            }

            return render_template(
                "forgot_password.html",
                errors=errors,
                reset_sent=False
            )

        # ----------------------------------------------------
        # STORE USER TEMPORARILY
        # ----------------------------------------------------

        session["reset_user_id"] = user.id

        # Go to reset password page.
        return redirect(
            url_for("reset_password")
        )

    return render_template(
        "forgot_password.html",
        errors={},
        reset_sent=False
    )


# ============================================================
# RESET PASSWORD
# ============================================================

@app.route(
    "/reset-password",
    methods=["GET", "POST"]
)
def reset_password():

    # --------------------------------------------------------
    # USER MUST COME THROUGH FORGOT PASSWORD
    # --------------------------------------------------------

    if "reset_user_id" not in session:

        flash(
            "Please request a password reset first.",
            "error"
        )

        return redirect(
            url_for("forgot_password")
        )

    user = User.query.get(
        session["reset_user_id"]
    )

    if not user:

        session.pop(
            "reset_user_id",
            None
        )

        flash(
            "Unable to reset password.",
            "error"
        )

        return redirect(
            url_for("forgot_password")
        )

    # --------------------------------------------------------
    # RESET PASSWORD
    # --------------------------------------------------------

    if request.method == "POST":

        password = request.form.get(
            "password",
            ""
        )

        confirm_password = request.form.get(
            "confirm_password",
            ""
        )

        errors = {}

        # ----------------------------------------------------
        # VALIDATION
        # ----------------------------------------------------

        if not password:

            errors["password"] = (
                "Please enter a new password."
            )

        if not confirm_password:

            errors["confirm_password"] = (
                "Please confirm your password."
            )

        if password and confirm_password:

            if password != confirm_password:

                errors["confirm_password"] = (
                    "Passwords do not match."
                )

        # ----------------------------------------------------
        # SHOW ERRORS
        # ----------------------------------------------------

        if errors:

            return render_template(
                "reset_password.html",
                errors=errors
            )

        # ----------------------------------------------------
        # SAVE NEW PASSWORD
        # ----------------------------------------------------

        user.password_hash = password

        try:

            db.session.commit()

        except Exception:

            db.session.rollback()

            flash(
                "Unable to reset your password.",
                "error"
            )

            return redirect(
                url_for("forgot_password")
            )

        # ----------------------------------------------------
        # CLEAR RESET SESSION
        # ----------------------------------------------------

        session.pop(
            "reset_user_id",
            None
        )

        flash(
            "Password reset successfully. Please sign in.",
            "success"
        )

        return redirect(
            url_for("login")
        )

    return render_template(
        "reset_password.html",
        errors={}
    )


# ============================================================
# GOOGLE LOGIN PLACEHOLDER
# ============================================================

@app.route("/google-login")
def google_login():

    flash(
        "Google login will be connected later.",
        "info"
    )

    return redirect(
        url_for("login")
    )


# ============================================================
# PROFILE SETUP
# ============================================================

@app.route("/profile-setup", methods=["GET", "POST"])
def profile_setup():

    # --------------------------------------------------------
    # LOGIN CHECK
    # --------------------------------------------------------

    if "user_id" not in session:
        return redirect(url_for("login"))

    user = User.query.get(session["user_id"])

    if not user:
        session.clear()
        return redirect(url_for("login"))

    # --------------------------------------------------------
    # SAVE PROFILE
    # --------------------------------------------------------

    if request.method == "POST":

        user.bio = request.form.get(
            "bio",
            ""
        ).strip()

        user.city = request.form.get(
            "city",
            ""
        ).strip()

        user.country = request.form.get(
            "country",
            ""
        ).strip()

        user.learning_preference = request.form.get(
            "learning_preference",
            ""
        ).strip()

        user.availability = request.form.get(
            "availability",
            ""
        ).strip()

        # ----------------------------------------------------
        # PROFILE PHOTO
        # ----------------------------------------------------

        profile_photo = request.files.get(
            "profile_photo"
        )

        if profile_photo and profile_photo.filename:

            original_filename = secure_filename(
                profile_photo.filename
            )

            extension = os.path.splitext(
                original_filename
            )[1].lower()

            allowed_extensions = {
                ".jpg",
                ".jpeg",
                ".png",
                ".webp"
            }

            if extension not in allowed_extensions:

                flash(
                    "Please upload a JPG, JPEG, PNG or WEBP image.",
                    "error"
                )

                return redirect(
                    url_for("profile_setup")
                )

            # Unique filename
            unique_filename = (
                f"{uuid.uuid4().hex}{extension}"
            )

            profile_photo.save(
                os.path.join(
                    app.config["UPLOAD_FOLDER"],
                    unique_filename
                )
            )

            user.profile_photo = unique_filename

        # ----------------------------------------------------
        # SAVE
        # ----------------------------------------------------

        db.session.commit()

        flash(
            "Profile setup completed!",
            "success"
        )

        return redirect(
            url_for("dashboard")
        )

    # --------------------------------------------------------
    # GET
    # --------------------------------------------------------

    return render_template(
        "profile_setup.html",
        user=user
    )


# ============================================================
# SERVE UPLOADED PROFILE PHOTOS
# ============================================================

@app.route("/uploads/<filename>")
def uploaded_file(filename):

    return send_from_directory(
        app.config["UPLOAD_FOLDER"],
        filename
    )
# ============================================================
# DASHBOARD
# ============================================================
@app.route("/dashboard")
def dashboard():

    # ========================================================
    # LOGIN CHECK
    # ========================================================

    if "user_id" not in session:
        return redirect(url_for("login"))

    user = User.query.get(session["user_id"])

    if not user:
        session.clear()
        return redirect(url_for("login"))

    # ========================================================
    # PROFILE COMPLETION
    # ========================================================

    profile_fields = [
        user.full_name,
        user.username,
        user.bio,
        user.city,
        user.country,
        user.learning_preference,
        user.availability,
        user.profile_photo
    ]

    completed_profile_fields = sum(
        1
        for field in profile_fields
        if field
    )

    profile_percentage = int(
        (
            completed_profile_fields
            / len(profile_fields)
        ) * 100
    )

    # ========================================================
    # USER SKILLS
    # ========================================================

    user_skills = UserSkill.query.filter_by(
        user_id=user.id
    ).all()

    teach_user_skills = [
        item
        for item in user_skills
        if item.skill_type == "teach"
    ]

    learn_user_skills = [
        item
        for item in user_skills
        if item.skill_type == "learn"
    ]

    teach_skills = [
        item.skill
        for item in teach_user_skills
        if item.skill
    ]

    learn_skills = [
        item.skill
        for item in learn_user_skills
        if item.skill
    ]

    # ========================================================
    # CONNECTIONS
    # ========================================================

    user_connections = Connection.query.filter(
        db.or_(
            Connection.sender_id == user.id,
            Connection.receiver_id == user.id
        ),
        Connection.status == "accepted"
    ).order_by(
        Connection.accepted_at.desc()
    ).all()

    total_connections = len(user_connections)

    active_connection = (
        user_connections[0]
        if user_connections
        else None
    )

    # ========================================================
    # SESSIONS
    # ========================================================

    connection_ids = [
        connection.id
        for connection in user_connections
    ]

    upcoming_session = None
    total_sessions = 0
    total_learning_hours = 0

    if connection_ids:

        sessions = Session.query.filter(
            Session.connection_id.in_(connection_ids)
        ).order_by(
            Session.scheduled_at.asc()
        ).all()

        total_sessions = len(sessions)

        # ----------------------------------------------------
        # COMPLETED LEARNING HOURS
        # ----------------------------------------------------

        for learning_session in sessions:

            if learning_session.status == "completed":

                if learning_session.duration_minutes:
                    total_learning_hours += (
                        learning_session.duration_minutes / 60
                    )

        # ----------------------------------------------------
        # UPCOMING SESSION
        # ----------------------------------------------------

        now = datetime.utcnow()

        upcoming = [
            item
            for item in sessions
            if (
                item.scheduled_at
                and item.scheduled_at >= now
                and item.status not in [
                    "cancelled",
                    "declined",
                    "completed"
                ]
            )
        ]

        if upcoming:
            upcoming_session = upcoming[0]

    # ========================================================
    # LEARNING ROADMAP PROGRESS
    # ========================================================

    skill_progress = []

    for user_skill in learn_user_skills:

        skill = user_skill.skill

        if not skill:
            continue

        # ----------------------------------------------------
        # FIND ACTIVE ROADMAP
        # ----------------------------------------------------

        roadmap_obj = Roadmap.query.filter_by(
            skill_id=skill.id,
            is_active=True
        ).first()

        if not roadmap_obj:
            continue

        topics = sorted(
            list(roadmap_obj.topics),
            key=lambda topic: topic.order_index
        )

        if not topics:
            continue

        topic_ids = [
            topic.id
            for topic in topics
        ]

        # ----------------------------------------------------
        # USER TOPIC PROGRESS
        # ----------------------------------------------------

        progress_records = TopicProgress.query.filter(
            TopicProgress.user_id == user.id,
            TopicProgress.topic_id.in_(topic_ids)
        ).all()

        progress_by_topic = {
            record.topic_id: record
            for record in progress_records
        }

        # ----------------------------------------------------
        # COMPLETED TOPICS
        # ----------------------------------------------------

        completed_topic_ids = set()

        for topic in topics:

            progress_record = progress_by_topic.get(
                topic.id
            )

            if not progress_record:
                continue

            has_task = bool(
                topic.task_description
                and topic.task_description.strip()
            )

            # Topic has practical task
            if has_task:

                if (
                    progress_record.learned
                    and progress_record.practiced
                    and progress_record.task_completed
                ):
                    completed_topic_ids.add(
                        topic.id
                    )

            # Topic has no practical task
            else:

                if (
                    progress_record.learned
                    and progress_record.practiced
                ):
                    completed_topic_ids.add(
                        topic.id
                    )

        # ----------------------------------------------------
        # PROGRESS
        # ----------------------------------------------------

        total_topics = len(topics)

        completed_count = len(
            completed_topic_ids
        )

        percentage = int(
            (
                completed_count
                / total_topics
            ) * 100
        )

        # ----------------------------------------------------
        # CURRENT / NEXT TOPIC
        # ----------------------------------------------------

        next_topic = None

        for topic in topics:

            if topic.id not in completed_topic_ids:
                next_topic = topic
                break

        # ----------------------------------------------------
        # CURRENT TOPIC PROGRESS
        # ----------------------------------------------------

        current_progress = None

        if next_topic:

            current_progress = progress_by_topic.get(
                next_topic.id
            )

        # ----------------------------------------------------
        # LEARNING STATUS
        # ----------------------------------------------------

        if percentage >= 100:

            learning_status = "Completed"

        elif not current_progress:

            learning_status = "Not Started"

        elif not current_progress.learned:

            learning_status = "Learning"

        elif not current_progress.practiced:

            learning_status = "Practice Pending"

        elif (
            next_topic
            and next_topic.task_description
            and not current_progress.task_completed
        ):

            learning_status = "Task Pending"

        else:

            learning_status = "Learning"

        # ----------------------------------------------------
        # DASHBOARD PROGRESS OBJECT
        # ----------------------------------------------------

        skill_progress.append(
            SimpleNamespace(
                skill_name=skill.name,
                skill_slug=skill.slug,
                category=skill.category,

                percentage=percentage,

                completed_count=completed_count,
                total_topics=total_topics,

                next_topic=next_topic,
                current_progress=current_progress,

                learning_status=learning_status,

                level=(
                    user_skill.earned_level
                    or "Learning"
                )
            )
        )

    # ========================================================
    # RENDER DASHBOARD
    # ========================================================

    return render_template(
        "dashboard.html",

        # User
        user=user,
        current_user=user,

        # Profile
        profile_percentage=profile_percentage,

        # Skills
        teach_skills=teach_skills,
        learn_skills=learn_skills,
        teach_user_skills=teach_user_skills,
        learn_user_skills=learn_user_skills,

        # Matches
        matched_users=[],
        total_matches=0,

        # Connections
        user_connections=user_connections,
        active_connection=active_connection,
        total_connections=total_connections,

        # Sessions
        upcoming_session=upcoming_session,
        total_sessions=total_sessions,
        total_learning_hours=round(
            total_learning_hours,
            1
        ),

        # Learning
        skill_progress=skill_progress
    )
# ============================================================
# PROFILE
# ============================================================

@app.route("/profile")
def profile():

    if "user_id" not in session:
        return redirect(
            url_for("login")
        )

    user = User.query.get(
        session["user_id"]
    )

    if not user:
        session.clear()
        return redirect(
            url_for("login")
        )

    # --------------------------------------------------------
    # USER SKILLS
    # --------------------------------------------------------

    user_skills = UserSkill.query.filter_by(
        user_id=user.id
    ).all()

    # --------------------------------------------------------
    # TEACHING SKILLS
    # --------------------------------------------------------

    teach_skills = []

    for user_skill in user_skills:

        if user_skill.skill_type != "teach":
            continue

        if not user_skill.skill:
            continue

        # Latest assessment result for this skill
        latest_result = (
            AssessmentResult.query
            .filter_by(
                user_id=user.id,
                skill_id=user_skill.skill_id
            )
            .order_by(
                AssessmentResult.completed_at.desc()
            )
            .first()
        )

        # ----------------------------------------------------
        # CORRECT ANSWER COUNT
        # ----------------------------------------------------

        correct_count = 0

        if latest_result:

            stored_correct_answers = (
                latest_result.correct_answers
            )

            # Database may contain integer
            if isinstance(
                stored_correct_answers,
                int
            ):

                correct_count = (
                    stored_correct_answers
                )

            else:

                stored_correct_answers = str(
                    stored_correct_answers or ""
                )

                # Older data may contain:
                # "1,2,3,4"
                answer_parts = (
                    stored_correct_answers
                    .split(",")
                )

                correct_count = len([
                    answer_id
                    for answer_id in answer_parts
                    if answer_id.strip()
                ])

        # ----------------------------------------------------
        # ADD TEACHING SKILL
        # ----------------------------------------------------

        teach_skills.append(
            SimpleNamespace(

                name=user_skill.skill.name,

                category=user_skill.skill.category,

                level=(
                    user_skill.earned_level
                    or "Not assessed"
                ),

                assessment_score=(
                    user_skill.assessment_score
                    if user_skill.assessment_score
                    is not None
                    else 0
                ),

                correct_answers=correct_count,

                total_questions=(
                    latest_result.total_questions
                    if latest_result
                    else 0
                ),

                assessment_completed=(
                    user_skill.assessment_completed
                )
            )
        )

    # --------------------------------------------------------
    # LEARNING SKILLS
    # --------------------------------------------------------

    learn_skills = []

    for user_skill in user_skills:

        if user_skill.skill_type != "learn":
            continue

        if not user_skill.skill:
            continue

        learn_skills.append(
            SimpleNamespace(

                name=user_skill.skill.name,

                category=user_skill.skill.category

            )
        )

    # --------------------------------------------------------
    # PROFILE
    # --------------------------------------------------------

    return render_template(
        "profile.html",

        user=user,

        teach_skills=teach_skills,

        learn_skills=learn_skills
    )
# ============================================================
# SKILLS
# ============================================================

@app.route("/skills", methods=["GET", "POST"])
def skills():

    if "user_id" not in session:
        return redirect(url_for("login"))

    current_user = User.query.get(session["user_id"])

    if not current_user:
        session.clear()
        return redirect(url_for("login"))

    # --------------------------------------------------------
    # LOAD ALL ACTIVE SKILLS
    # --------------------------------------------------------

    all_skills = Skill.query.filter_by(
        is_active=True
    ).order_by(
        Skill.category,
        Skill.name
    ).all()

    skill_map = {
        skill.slug: skill
        for skill in all_skills
    }

    # --------------------------------------------------------
    # SAVE SELECTED SKILLS
    # --------------------------------------------------------

    if request.method == "POST":

        selected_teach = list(
            dict.fromkeys(
                request.form.getlist("teach_skills")
            )
        )

        selected_learn = list(
            dict.fromkeys(
                request.form.getlist("learn_skills")
            )
        )

        # ----------------------------------------------------
        # ONLY ONE TEACHING SKILL
        # ----------------------------------------------------

        if len(selected_teach) > 1:

            flash(
                "You can teach only one skill at a time.",
                "error"
            )

            return redirect(
                url_for("skills")
            )

        # ----------------------------------------------------
        # AT LEAST ONE SKILL
        # ----------------------------------------------------

        if not selected_teach and not selected_learn:

            flash(
                "Please select at least one skill.",
                "error"
            )

            return redirect(
                url_for("skills")
            )

        # ----------------------------------------------------
        # SAME SKILL CANNOT BE TEACH + LEARN
        # ----------------------------------------------------

        both = set(selected_teach) & set(selected_learn)

        if both:

            flash(
                "A skill cannot be selected for both teaching and learning.",
                "error"
            )

            return redirect(
                url_for("skills")
            )

        # ----------------------------------------------------
        # VALIDATE SKILLS
        # ----------------------------------------------------

        selected_slugs = (
            set(selected_teach) |
            set(selected_learn)
        )

        invalid_skills = (
            selected_slugs -
            set(skill_map.keys())
        )

        if invalid_skills:

            flash(
                "One or more selected skills are invalid.",
                "error"
            )

            return redirect(
                url_for("skills")
            )

        # ----------------------------------------------------
        # GET EXISTING USER SKILLS
        # ----------------------------------------------------

        existing = UserSkill.query.filter_by(
            user_id=current_user.id
        ).all()

        existing_map = {
            (
                item.skill_id,
                item.skill_type
            ): item
            for item in existing
        }

        selected_pairs = set()

        # Teaching skills
        for slug in selected_teach:

            selected_pairs.add(
                (
                    skill_map[slug].id,
                    "teach"
                )
            )

        # Learning skills
        for slug in selected_learn:

            selected_pairs.add(
                (
                    skill_map[slug].id,
                    "learn"
                )
            )

        # ----------------------------------------------------
        # REMOVE SKILLS THAT WERE UNSELECTED
        # ----------------------------------------------------

        for key, item in existing_map.items():

            if key not in selected_pairs:

                db.session.delete(item)

        # ----------------------------------------------------
        # ADD NEW SKILLS
        # ----------------------------------------------------

        for skill_id, skill_type in selected_pairs:

            if (skill_id, skill_type) not in existing_map:

                db.session.add(
                    UserSkill(
                        user_id=current_user.id,
                        skill_id=skill_id,
                        skill_type=skill_type,
                        earned_level=None,
                        assessment_score=None,
                        assessment_completed=False
                    )
                )

        # ----------------------------------------------------
        # SAVE TO DATABASE
        # ----------------------------------------------------

        try:

            db.session.commit()

        except Exception:

            db.session.rollback()

            flash(
                "Something went wrong while saving your skills.",
                "error"
            )

            return redirect(
                url_for("skills")
            )

        # ====================================================
        # LEARN YOURSELF
        # ====================================================
        #
        # If user selected a learning skill and no teaching
        # skill, open THAT SKILL'S roadmap directly.
        #
        # Example:
        # Python selected
        #       ↓
        # /roadmap/python
        #
        # ====================================================

        if selected_learn and not selected_teach:

            learning_skill = skill_map[
                selected_learn[0]
            ]

            flash(
                f"{learning_skill.name} saved. Start learning!",
                "success"
            )

            return redirect(
                url_for(
                    "roadmap",
                    skill=learning_skill.slug
                )
            )

        # ====================================================
        # SKILL EXCHANGE / TEACHING SKILL
        # ====================================================

        if selected_teach:

            teach_skill = skill_map[
                selected_teach[0]
            ]

            assessment_obj = Assessment.query.filter_by(
                skill_id=teach_skill.id
            ).first()

            # Teaching skill must be assessed first.
            if assessment_obj:

                flash(
                    "Teaching skill saved. Start your assessment.",
                    "success"
                )

                return redirect(
                    url_for(
                        "assessment",
                        skill_id=teach_skill.id
                    )
                )

            # If assessment doesn't exist yet
            flash(
                "Teaching skill saved successfully.",
                "success"
            )

            return redirect(
                url_for("dashboard")
            )

        # ----------------------------------------------------
        # FALLBACK
        # ----------------------------------------------------

        flash(
            "Your skills have been saved successfully!",
            "success"
        )

        return redirect(
            url_for("dashboard")
        )

    # ========================================================
    # GET CURRENT USER SKILLS
    # ========================================================

    user_skills = UserSkill.query.filter_by(
        user_id=current_user.id
    ).all()

    teach_skills = [
        item.skill.slug
        for item in user_skills
        if item.skill_type == "teach"
        and item.skill
    ]

    learn_skills = [
        item.skill.slug
        for item in user_skills
        if item.skill_type == "learn"
        and item.skill
    ]

    # ========================================================
    # RENDER SKILLS PAGE
    # ========================================================

    return render_template(
        "skills.html",
        skills=all_skills,
        teach_skills=teach_skills,
        learn_skills=learn_skills
    )

# ============================================================
# EXPLORE
# ============================================================
@app.route("/explore")
def explore():

    if "user_id" not in session:
        return redirect(url_for("login"))

    current_user = User.query.get(session["user_id"])

    if not current_user:
        session.clear()
        return redirect(url_for("login"))

    selected_skill = request.args.get(
        "skill",
        ""
    ).strip()

    # --------------------------------------------------------
    # FIND USERS WHO CAN TEACH SKILLS
    # Current SkillSwap system uses UserSkill + Skill.
    # --------------------------------------------------------

    teacher_skill_records = (
        UserSkill.query
        .filter_by(skill_type="teach")
        .join(Skill, UserSkill.skill_id == Skill.id)
        .all()
    )

    # Group teachable skills by user.
    teacher_map = {}

    for record in teacher_skill_records:

        if not record.user or not record.skill:
            continue

        user_id = record.user.id

        if user_id not in teacher_map:
            teacher_map[user_id] = {
                "user": record.user,
                "skills": []
            }

        teacher_map[user_id]["skills"].append(
            record.skill.name
        )

    # --------------------------------------------------------
    # FILTER BY SELECTED SKILL
    # --------------------------------------------------------

    users = []

    for data in teacher_map.values():

        person = data["user"]
        skill_names = data["skills"]

        if selected_skill:

            selected_lower = selected_skill.lower()

            matches = any(
                selected_lower == skill_name.lower()
                or selected_lower == Skill.query.filter_by(
                    name=skill_name
                ).first().slug.lower()
                for skill_name in skill_names
            )

            if not matches:
                continue

        # The existing explore.html expects
        # person.skills_to_teach.
        # This creates that display value temporarily
        # without changing the User model/database.
        person.skills_to_teach = ", ".join(skill_names)

        users.append(person)

    return render_template(
        "explore.html",
        users=users,
        selected_skill=selected_skill,
        current_user=current_user
    )
    
# ============================================================
# ASSESSMENT
# ============================================================

@app.route("/assessment/<int:skill_id>")
def assessment(skill_id):

    if "user_id" not in session:
        return redirect(url_for("login"))

    current_user = User.query.get(session["user_id"])

    if not current_user:
        session.clear()
        return redirect(url_for("login"))

    skill = Skill.query.get_or_404(skill_id)

    # --------------------------------------------------------
    # USER MUST HAVE THIS SKILL AS TEACHING SKILL
    # --------------------------------------------------------

    user_skill = UserSkill.query.filter_by(
        user_id=current_user.id,
        skill_id=skill.id,
        skill_type="teach"
    ).first()

    if not user_skill:
        flash(
            "You can only take an assessment for your teaching skill.",
            "error"
        )
        return redirect(url_for("skills"))

    # --------------------------------------------------------
    # FIND ASSESSMENT
    # --------------------------------------------------------

    assessment_obj = Assessment.query.filter_by(
        skill_id=skill.id
    ).first()

    if not assessment_obj:
        flash(
            "Assessment is not available yet.",
            "info"
        )
        return redirect(url_for("skills"))

    # --------------------------------------------------------
    # LOAD QUESTIONS
    # --------------------------------------------------------

    questions = AssessmentQuestion.query.filter_by(
        assessment_id=assessment_obj.id
    ).all()

    # Beginner → Intermediate → Pro
    difficulty_order = {
        "Beginner": 0,
        "Intermediate": 1,
        "Pro": 2
    }

    questions.sort(
        key=lambda q: difficulty_order.get(
            q.difficulty,
            3
        )
    )

    if not questions:
        flash(
            "No questions are available for this assessment.",
            "error"
        )
        return redirect(url_for("skills"))

    # --------------------------------------------------------
    # START NEW ASSESSMENT
    # --------------------------------------------------------

    if (
        session.get("assessment_skill_id") != skill.id
        or session.get("assessment_assessment_id") != assessment_obj.id
    ):

        session["assessment_skill_id"] = skill.id
        session["assessment_assessment_id"] = assessment_obj.id
        session["assessment_question_ids"] = [
            question.id for question in questions
        ]
        session["assessment_index"] = 0
        session["assessment_answers"] = {}
        session["assessment_correct_ids"] = []

    # --------------------------------------------------------
    # CURRENT QUESTION
    # --------------------------------------------------------

    question_ids = session.get(
        "assessment_question_ids",
        []
    )

    current_index = session.get(
        "assessment_index",
        0
    )

    # Safety check
    if current_index >= len(question_ids):
        return redirect(
            url_for(
                "assessment",
                skill_id=skill.id
            )
        )

    current_question = AssessmentQuestion.query.get(
        question_ids[current_index]
    )

    if not current_question:
        flash(
            "Assessment question could not be loaded.",
            "error"
        )

        session.pop("assessment_skill_id", None)
        session.pop("assessment_assessment_id", None)
        session.pop("assessment_question_ids", None)
        session.pop("assessment_index", None)
        session.pop("assessment_answers", None)
        session.pop("assessment_correct_ids", None)

        return redirect(url_for("skills"))

    # --------------------------------------------------------
    # SHOW ONE QUESTION
    # --------------------------------------------------------

    return render_template(
        "assessment.html",
        skill=skill,
        assessment=assessment_obj,
        question=current_question,
        current_question_number=current_index + 1,
        total_questions=len(question_ids),
        completed_count=current_index
    )
# ============================================================
# SUBMIT ASSESSMENT
# ============================================================

@app.route(
    "/assessment/<int:skill_id>/submit",
    methods=["POST"]
)
def submit_assessment(skill_id):

    # --------------------------------------------------------
    # LOGIN CHECK
    # --------------------------------------------------------

    if "user_id" not in session:
        return redirect(url_for("login"))

    current_user_id = session["user_id"]

    current_user = User.query.get(
        current_user_id
    )

    if not current_user:
        session.clear()
        return redirect(url_for("login"))

    # --------------------------------------------------------
    # GET SKILL
    # --------------------------------------------------------

    skill = Skill.query.get_or_404(
        skill_id
    )

    # --------------------------------------------------------
    # VERIFY TEACHING SKILL
    # --------------------------------------------------------

    user_skill = UserSkill.query.filter_by(
        user_id=current_user_id,
        skill_id=skill.id,
        skill_type="teach"
    ).first()

    if not user_skill:

        flash(
            "This assessment is only for your teaching skill.",
            "error"
        )

        return redirect(
            url_for("skills")
        )

    # --------------------------------------------------------
    # FIND ASSESSMENT
    # --------------------------------------------------------

    assessment_obj = Assessment.query.filter_by(
        skill_id=skill.id
    ).first()

    if not assessment_obj:

        flash(
            "Assessment not found.",
            "error"
        )

        return redirect(
            url_for("skills")
        )

    # --------------------------------------------------------
    # VERIFY ASSESSMENT SESSION
    # --------------------------------------------------------

    if (
        session.get("assessment_skill_id")
        != skill.id
    ):

        flash(
            "Assessment session expired. Please start again.",
            "error"
        )

        return redirect(
            url_for(
                "assessment",
                skill_id=skill.id
            )
        )

    # --------------------------------------------------------
    # GET QUESTION IDS
    # --------------------------------------------------------

    question_ids = session.get(
        "assessment_question_ids",
        []
    )

    current_index = session.get(
        "assessment_index",
        0
    )

    # --------------------------------------------------------
    # SAFETY CHECK
    # --------------------------------------------------------

    if not question_ids:

        flash(
            "Assessment session expired. Please start again.",
            "error"
        )

        return redirect(
            url_for(
                "assessment",
                skill_id=skill.id
            )
        )

    if current_index >= len(question_ids):

        flash(
            "Assessment session is no longer active.",
            "error"
        )

        return redirect(
            url_for(
                "assessment",
                skill_id=skill.id
            )
        )

    # --------------------------------------------------------
    # GET CURRENT QUESTION
    # --------------------------------------------------------

    current_question = AssessmentQuestion.query.get(
        question_ids[current_index]
    )

    if not current_question:

        flash(
            "Assessment question could not be found.",
            "error"
        )

        return redirect(
            url_for(
                "assessment",
                skill_id=skill.id
            )
        )

    # --------------------------------------------------------
    # GET USER ANSWER
    # --------------------------------------------------------

    submitted_answer = request.form.get(
        f"question_{current_question.id}",
        ""
    ).strip()

    # --------------------------------------------------------
    # EMPTY ANSWER
    #
    # Empty answer does NOT end assessment.
    # Same question will remain open.
    # --------------------------------------------------------

    if not submitted_answer:

        flash(
            "Please enter your answer.",
            "error"
        )

        return redirect(
            url_for(
                "assessment",
                skill_id=skill.id
            )
        )

    # --------------------------------------------------------
    # NORMALIZE ANSWER
    # --------------------------------------------------------

    def normalize(value):

        return " ".join(
            (value or "")
            .strip()
            .lower()
            .split()
        )

    submitted_normalized = normalize(
        submitted_answer
    )

    # --------------------------------------------------------
    # GET ACCEPTED ANSWERS
    #
    # Database can contain:
    #
    # answer one | answer two | answer three
    # --------------------------------------------------------

    accepted_answers = [

        normalize(answer)

        for answer in (
            current_question.correct_answer or ""
        ).split("|")

        if normalize(answer)

    ]

    # ========================================================
    # ❌ WRONG ANSWER
    #
    # IMPORTANT:
    #
    # Wrong answer immediately ends assessment.
    #
    # No next question.
    # No retry.
    # Current wrong answer is NOT counted.
    # Remaining questions are NOT answered.
    # Result is calculated from previous correct answers.
    # ========================================================

    if submitted_normalized not in accepted_answers:

        # ----------------------------------------------------
        # GET PREVIOUS CORRECT ANSWERS
        # ----------------------------------------------------

        correct_ids = session.get(
            "assessment_correct_ids",
            []
        )

        # Remove duplicates just in case
        correct_ids = list(
            dict.fromkeys(
                correct_ids
            )
        )

        # ----------------------------------------------------
        # TOTAL QUESTIONS
        # ----------------------------------------------------

        total_questions = len(
            question_ids
        )

        # ----------------------------------------------------
        # CORRECT COUNT
        # ----------------------------------------------------

        correct_count = len(
            correct_ids
        )

        # ----------------------------------------------------
        # CALCULATE LEVEL
        #
        # 0-4  = Beginner
        # 5-7  = Intermediate
        # 8-10 = Pro
        # ----------------------------------------------------

        if correct_count >= 8:

            earned_level = "Pro"

        elif correct_count >= 5:

            earned_level = "Intermediate"

        else:

            earned_level = "Beginner"

        # ----------------------------------------------------
        # SCORE %
        # ----------------------------------------------------

        if total_questions > 0:

            score = round(
                (
                    correct_count
                    / total_questions
                ) * 100,
                2
            )

        else:

            score = 0

        # ----------------------------------------------------
        # SAVE ASSESSMENT RESULT
        # ----------------------------------------------------

        result = AssessmentResult(

            user_id=current_user_id,

            skill_id=skill.id,

            assessment_id=assessment_obj.id,

            score=score,

            correct_answers=",".join(
                str(question_id)
                for question_id in correct_ids
            ),

            total_questions=total_questions,

            earned_level=earned_level

        )

        db.session.add(
            result
        )

        # ----------------------------------------------------
        # UPDATE USER TEACHING SKILL
        # ----------------------------------------------------

        user_skill.earned_level = earned_level

        user_skill.assessment_score = score

        user_skill.assessment_completed = True

        # ----------------------------------------------------
        # SAVE DATABASE
        # ----------------------------------------------------

        try:

            db.session.commit()

        except Exception:

            db.session.rollback()

            flash(
                "Something went wrong while saving your assessment result.",
                "error"
            )

            return redirect(
                url_for(
                    "assessment",
                    skill_id=skill.id
                )
            )

        # ----------------------------------------------------
        # CLEAR ASSESSMENT SESSION
        # ----------------------------------------------------

        session.pop(
            "assessment_skill_id",
            None
        )

        session.pop(
            "assessment_assessment_id",
            None
        )

        session.pop(
            "assessment_question_ids",
            None
        )

        session.pop(
            "assessment_index",
            None
        )

        session.pop(
            "assessment_answers",
            None
        )

        session.pop(
            "assessment_correct_ids",
            None
        )

        # ----------------------------------------------------
        # WRONG ANSWER MESSAGE
        # ----------------------------------------------------

        flash(
            f"❌ Assessment ended. "
            f"You got {correct_count}/{total_questions} correct "
            f"and earned {earned_level} level.",
            "error"
        )

        # ----------------------------------------------------
        # OPEN RESULT PAGE
        # ----------------------------------------------------

        return redirect(
            url_for(
                "assessment_result",
                result_id=result.id
            )
        )

    # ========================================================
    # ✅ CORRECT ANSWER
    # ========================================================

    correct_ids = session.get(
        "assessment_correct_ids",
        []
    )

    question_id_string = str(
        current_question.id
    )

    # --------------------------------------------------------
    # SAVE CORRECT QUESTION
    # --------------------------------------------------------

    if question_id_string not in correct_ids:

        correct_ids.append(
            question_id_string
        )

    session["assessment_correct_ids"] = (
        correct_ids
    )

    # --------------------------------------------------------
    # SAVE ANSWER
    # --------------------------------------------------------

    answers = session.get(
        "assessment_answers",
        {}
    )

    answers[question_id_string] = (
        submitted_answer
    )

    session["assessment_answers"] = (
        answers
    )

    # --------------------------------------------------------
    # MOVE TO NEXT QUESTION
    # --------------------------------------------------------

    next_index = (
        current_index + 1
    )

    session["assessment_index"] = (
        next_index
    )

    # --------------------------------------------------------
    # MORE QUESTIONS AVAILABLE
    # --------------------------------------------------------

    if next_index < len(question_ids):

        flash(
            "✓ Correct answer!",
            "success"
        )

        return redirect(
            url_for(
                "assessment",
                skill_id=skill.id
            )
        )

    # ========================================================
    # ASSESSMENT COMPLETED
    #
    # User answered every question correctly.
    # ========================================================

    total_questions = len(
        question_ids
    )

    correct_count = len(
        set(correct_ids)
    )

    # --------------------------------------------------------
    # FINAL LEVEL
    # --------------------------------------------------------

    if correct_count >= 8:

        earned_level = "Pro"

    elif correct_count >= 5:

        earned_level = "Intermediate"

    else:

        earned_level = "Beginner"

    # --------------------------------------------------------
    # SCORE %
    # --------------------------------------------------------

    if total_questions > 0:

        score = round(
            (
                correct_count
                / total_questions
            ) * 100,
            2
        )

    else:

        score = 0

    # --------------------------------------------------------
    # SAVE FINAL RESULT
    # --------------------------------------------------------

    result = AssessmentResult(

        user_id=current_user_id,

        skill_id=skill.id,

        assessment_id=assessment_obj.id,

        score=score,

        correct_answers=",".join(
            str(question_id)
            for question_id in correct_ids
        ),

        total_questions=total_questions,

        earned_level=earned_level

    )

    db.session.add(
        result
    )

    # --------------------------------------------------------
    # UPDATE USER TEACHING SKILL
    # --------------------------------------------------------

    user_skill.earned_level = (
        earned_level
    )

    user_skill.assessment_score = (
        score
    )

    user_skill.assessment_completed = (
        True
    )

    # --------------------------------------------------------
    # SAVE DATABASE
    # --------------------------------------------------------

    try:

        db.session.commit()

    except Exception:

        db.session.rollback()

        flash(
            "Something went wrong while saving your assessment result.",
            "error"
        )

        return redirect(
            url_for(
                "assessment",
                skill_id=skill.id
            )
        )

    # --------------------------------------------------------
    # CLEAR ASSESSMENT SESSION
    # --------------------------------------------------------

    session.pop(
        "assessment_skill_id",
        None
    )

    session.pop(
        "assessment_assessment_id",
        None
    )

    session.pop(
        "assessment_question_ids",
        None
    )

    session.pop(
        "assessment_index",
        None
    )

    session.pop(
        "assessment_answers",
        None
    )

    session.pop(
        "assessment_correct_ids",
        None
    )

    # --------------------------------------------------------
    # SUCCESS MESSAGE
    # --------------------------------------------------------

    flash(
        f"Assessment complete! "
        f"You got {correct_count}/{total_questions} correct "
        f"and earned {earned_level} level.",
        "success"
    )

    # --------------------------------------------------------
    # RESULT PAGE
    # --------------------------------------------------------

    return redirect(
        url_for(
            "assessment_result",
            result_id=result.id
        )
    )


# ============================================================
# RESTART ASSESSMENT
# ============================================================

@app.route(
    "/assessment/<int:skill_id>/restart",
    methods=["POST"]
)
def restart_assessment(skill_id):

    if "user_id" not in session:
        return redirect(
            url_for("login")
        )

    skill = Skill.query.get_or_404(
        skill_id
    )

    # --------------------------------------------------------
    # VERIFY TEACHING SKILL
    # --------------------------------------------------------

    user_skill = UserSkill.query.filter_by(
        user_id=session["user_id"],
        skill_id=skill.id,
        skill_type="teach"
    ).first()

    if not user_skill:

        flash(
            "You can only restart an assessment for your teaching skill.",
            "error"
        )

        return redirect(
            url_for("skills")
        )

    # --------------------------------------------------------
    # CLEAR ASSESSMENT SESSION
    # --------------------------------------------------------

    session.pop(
        "assessment_skill_id",
        None
    )

    session.pop(
        "assessment_assessment_id",
        None
    )

    session.pop(
        "assessment_question_ids",
        None
    )

    session.pop(
        "assessment_index",
        None
    )

    session.pop(
        "assessment_answers",
        None
    )

    session.pop(
        "assessment_correct_ids",
        None
    )

    # --------------------------------------------------------
    # START ASSESSMENT AGAIN
    # --------------------------------------------------------

    return redirect(
        url_for(
            "assessment",
            skill_id=skill.id
        )
    )
# ============================================================
# ASSESSMENT RESULT
# ============================================================
@app.route("/assessment-result/<int:result_id>")
def assessment_result(result_id):

    if "user_id" not in session:
        return redirect(url_for("login"))

    result = AssessmentResult.query.get_or_404(result_id)

    if result.user_id != session["user_id"]:
        return "Unauthorized", 403

    skill = Skill.query.get(result.skill_id)

    # correct_answers is stored as an integer count
    correct_count = result.correct_answers or 0

    return render_template(
        "assessment_result.html",

        result=result,
        skill=skill,

        skill_name=skill.name if skill else "Skill",

        score=result.score,

        correct_answers=correct_count,

        total_questions=result.total_questions,

        earned_level=result.earned_level
    )
# ============================================================
# SMART MATCHES
# ============================================================

@app.route("/matches")
def matches():

    # --------------------------------------------------------
    # LOGIN CHECK
    # --------------------------------------------------------

    if "user_id" not in session:
        return redirect(url_for("login"))

    current_user = User.query.get(
        session["user_id"]
    )

    if not current_user:
        session.clear()
        return redirect(url_for("login"))

    # --------------------------------------------------------
    # FILTERS
    # --------------------------------------------------------

    selected_category = request.args.get(
        "category",
        ""
    ).strip().lower()

    minimum_match = request.args.get(
        "minimum_match",
        ""
    ).strip()

    try:
        minimum_match_value = (
            int(minimum_match)
            if minimum_match
            else 0
        )
    except ValueError:
        minimum_match_value = 0
        minimum_match = ""

    # --------------------------------------------------------
    # CURRENT USER SKILLS
    # --------------------------------------------------------

    current_user_skills = UserSkill.query.filter_by(
        user_id=current_user.id
    ).all()

    current_teach_ids = {
        item.skill_id
        for item in current_user_skills
        if item.skill_type == "teach"
    }

    current_learn_ids = {
        item.skill_id
        for item in current_user_skills
        if item.skill_type == "learn"
    }

    current_teach_skills = (
        Skill.query.filter(
            Skill.id.in_(current_teach_ids)
        ).all()
        if current_teach_ids
        else []
    )

    current_learn_skills = (
        Skill.query.filter(
            Skill.id.in_(current_learn_ids)
        ).all()
        if current_learn_ids
        else []
    )

    # --------------------------------------------------------
    # FIND ALL ACTIVE USERS
    #
    # Only users who have completed at least one
    # teaching-skill assessment are eligible to appear.
    # --------------------------------------------------------

    all_active_users = User.query.filter(
        User.id != current_user.id,
        User.is_active == True
    ).all()

    matches_list = []

    for other_user in all_active_users:

        # ----------------------------------------------------
        # USER'S SKILLS
        # ----------------------------------------------------

        other_user_skills = UserSkill.query.filter_by(
            user_id=other_user.id
        ).all()

        other_teach = [
            item
            for item in other_user_skills
            if item.skill_type == "teach"
        ]

        other_learn = [
            item
            for item in other_user_skills
            if item.skill_type == "learn"
        ]

        # ----------------------------------------------------
        # USER MUST HAVE COMPLETED ASSESSMENT
        # ----------------------------------------------------

        completed_assessment = any(
            item.assessment_completed
            for item in other_teach
        )

        if not completed_assessment:
            continue

        # ----------------------------------------------------
        # SKILL IDs
        # ----------------------------------------------------

        other_teach_ids = {
            item.skill_id
            for item in other_teach
        }

        other_learn_ids = {
            item.skill_id
            for item in other_learn
        }

        # ----------------------------------------------------
        # WHAT YOU CAN LEARN FROM THEM
        # ----------------------------------------------------

        skills_you_can_learn_ids = (
            current_learn_ids
            & other_teach_ids
        )

        # ----------------------------------------------------
        # WHAT THEY CAN LEARN FROM YOU
        # ----------------------------------------------------

        skills_they_can_learn_ids = (
            current_teach_ids
            & other_learn_ids
        )

        # ----------------------------------------------------
        # SKILL OBJECTS
        # ----------------------------------------------------

        skills_you_can_learn = (
            Skill.query.filter(
                Skill.id.in_(
                    skills_you_can_learn_ids
                )
            ).all()
            if skills_you_can_learn_ids
            else []
        )

        skills_they_can_learn = (
            Skill.query.filter(
                Skill.id.in_(
                    skills_they_can_learn_ids
                )
            ).all()
            if skills_they_can_learn_ids
            else []
        )

        # ----------------------------------------------------
        # CATEGORY FILTER
        # ----------------------------------------------------

        if selected_category:

            other_skill_ids = (
                other_teach_ids
                | other_learn_ids
            )

            other_skills = (
                Skill.query.filter(
                    Skill.id.in_(other_skill_ids)
                ).all()
                if other_skill_ids
                else []
            )

            has_category = any(
                (
                    skill.category
                    or ""
                ).lower()
                == selected_category
                for skill in other_skills
            )

            if not has_category:
                continue

        # ----------------------------------------------------
        # MATCH PERCENTAGE
        #
        # User still appears even when match is 0%.
        # ----------------------------------------------------

        total_possible = (
            len(current_teach_ids)
            + len(current_learn_ids)
        )

        matched_count = (
            len(skills_you_can_learn_ids)
            + len(skills_they_can_learn_ids)
        )

        if total_possible > 0:

            match_percentage = round(
                (
                    matched_count
                    / total_possible
                ) * 100
            )

        else:

            match_percentage = 0

        # ----------------------------------------------------
        # MATCH STRENGTH FILTER
        # ----------------------------------------------------

        if (
            minimum_match_value > 0
            and match_percentage
            < minimum_match_value
        ):
            continue

        # ----------------------------------------------------
        # EARNED LEVELS
        # ----------------------------------------------------

        earned_levels = []

        for user_skill in other_teach:

            if not user_skill.earned_level:
                continue

            skill = Skill.query.get(
                user_skill.skill_id
            )

            if not skill:
                continue

            earned_levels.append(
                {
                    "skill": skill.name,
                    "level": user_skill.earned_level
                }
            )

        # ----------------------------------------------------
        # CREATE TEMPLATE OBJECT
        # ----------------------------------------------------

        match = SimpleNamespace(

            user=other_user,

            match_percentage=match_percentage,

            skills_you_can_learn=[
                skill.name
                for skill in skills_you_can_learn
            ],

            skills_they_can_learn=[
                skill.name
                for skill in skills_they_can_learn
            ],

            earned_levels=earned_levels
        )

        matches_list.append(match)

    # --------------------------------------------------------
    # SORT
    #
    # Highest compatibility first.
    # Users with 0% still remain at the bottom.
    # --------------------------------------------------------

    matches_list.sort(
        key=lambda item: item.match_percentage,
        reverse=True
    )

    # --------------------------------------------------------
    # RENDER
    # --------------------------------------------------------

    return render_template(

        "matches.html",

        current_user=current_user,

        matches=matches_list,

        user_teach_skills=current_teach_skills,

        user_learn_skills=current_learn_skills,

        selected_category=selected_category,

        minimum_match=minimum_match
    )

   # ============================================================
# VIEW OTHER USER PROFILE
# ============================================================

@app.route("/profile/<username>")
def view_profile(username):

    if "user_id" not in session:
        return redirect(url_for("login"))

    current_user = User.query.get(session["user_id"])

    if not current_user:
        session.clear()
        return redirect(url_for("login"))

    user = User.query.filter_by(
        username=username,
        is_active=True
    ).first_or_404()

    user_skills = UserSkill.query.filter_by(
        user_id=user.id
    ).all()

    teach_user_skills = [
        item for item in user_skills
        if item.skill_type == "teach"
    ]

    learn_user_skills = [
        item for item in user_skills
        if item.skill_type == "learn"
    ]

    teach_skills = []

    for item in teach_user_skills:
        skill = Skill.query.get(item.skill_id)

        if skill:
            teach_skills.append({
                "skill": skill,
                "level": item.earned_level,
                "assessment_completed": item.assessment_completed
            })

    learn_skills = []

    for item in learn_user_skills:
        skill = Skill.query.get(item.skill_id)

        if skill:
            learn_skills.append({
                "skill": skill,
                "level": item.earned_level
            })

    return render_template(
        "profile.html",
        user=user,
        current_user=current_user,
        teach_skills=teach_skills,
        learn_skills=learn_skills
    )
# ============================================================
# CONNECTIONS
# ============================================================
@app.route("/connections")
def connections():

    if "user_id" not in session:
        return redirect(url_for("login"))

    user_id = session["user_id"]

    # --------------------------------------------------------
    # INCOMING PENDING REQUESTS
    # --------------------------------------------------------

    incoming_requests = Connection.query.filter(
        Connection.receiver_id == user_id,
        Connection.status == "pending"
    ).order_by(
        Connection.created_at.desc()
    ).all()


    # --------------------------------------------------------
    # SENT PENDING REQUESTS
    # --------------------------------------------------------

    sent_requests = Connection.query.filter(
        Connection.sender_id == user_id,
        Connection.status == "pending"
    ).order_by(
        Connection.created_at.desc()
    ).all()


    # --------------------------------------------------------
    # ACTIVE / ACCEPTED CONNECTIONS
    # --------------------------------------------------------

    active_connections = Connection.query.filter(
        (
            (Connection.sender_id == user_id) |
            (Connection.receiver_id == user_id)
        ),
        Connection.status == "accepted"
    ).order_by(
        Connection.accepted_at.desc()
    ).all()


    # --------------------------------------------------------
    # CURRENT USER
    # --------------------------------------------------------

    current_user = User.query.get_or_404(user_id)


    # --------------------------------------------------------
    # RENDER
    # --------------------------------------------------------

    return render_template(
        "connections.html",
        current_user=current_user,
        incoming_requests=incoming_requests,
        sent_requests=sent_requests,
        active_connections=active_connections
    )
# ============================================================
# SEND CONNECTION REQUEST
# ============================================================

@app.route(
    "/connections/send/<int:user_id>",
    methods=["POST"]
)
def send_connection_request(user_id):

    if "user_id" not in session:
        return redirect(url_for("login"))

    sender_id = session["user_id"]

    # Cannot connect with yourself
    if sender_id == user_id:
        flash(
            "You cannot connect with yourself.",
            "error"
        )
        return redirect(url_for("matches"))

    receiver = User.query.get_or_404(user_id)

    # Check whether any connection already exists
    existing = Connection.query.filter(
        db.or_(
            db.and_(
                Connection.sender_id == sender_id,
                Connection.receiver_id == user_id
            ),
            db.and_(
                Connection.sender_id == user_id,
                Connection.receiver_id == sender_id
            )
        )
    ).first()

    if existing:

        if existing.status == "pending":
            flash(
                "A connection request is already pending.",
                "info"
            )

        elif existing.status == "accepted":
            flash(
                "You are already connected with this user.",
                "info"
            )

        elif existing.status == "declined":
            flash(
                "A previous connection request already exists.",
                "info"
            )

        elif existing.status == "cancelled":
            flash(
                "A previous connection request already exists.",
                "info"
            )

        return redirect(url_for("matches"))

    # Create new request
    connection = Connection(
        sender_id=sender_id,
        receiver_id=receiver.id,
        status="pending",
        message=request.form.get(
            "message",
            ""
        ).strip()
    )

    db.session.add(connection)

    try:
        db.session.commit()

        flash(
            "Connection request sent!",
            "success"
        )

    except Exception:
        db.session.rollback()

        flash(
            "Something went wrong. Please try again.",
            "error"
        )

    return redirect(url_for("matches"))

# ============================================================
# ACCEPT CONNECTION
# ============================================================

@app.route(
    "/connections/<int:connection_id>/accept",
    methods=["POST"]
)
def accept_connection_request(connection_id):

    if "user_id" not in session:
        return redirect(url_for("login"))

    connection = Connection.query.get_or_404(
        connection_id
    )

    if connection.receiver_id != session["user_id"]:
        return "Unauthorized", 403

    connection.status = "accepted"
    connection.accepted_at = datetime.utcnow()

    db.session.commit()

    flash(
        "Connection accepted!",
        "success"
    )

    return redirect(url_for("connections"))


# ============================================================
# DECLINE CONNECTION
# ============================================================

@app.route(
    "/connections/<int:connection_id>/decline",
    methods=["POST"]
)
def decline_connection_request(connection_id):

    if "user_id" not in session:
        return redirect(url_for("login"))

    connection = Connection.query.get_or_404(
        connection_id
    )

    if connection.receiver_id != session["user_id"]:
        return "Unauthorized", 403

    connection.status = "declined"

    db.session.commit()

    return redirect(url_for("connections"))


# ============================================================
# CANCEL CONNECTION
# ============================================================

@app.route(
    "/connections/<int:connection_id>/cancel",
    methods=["POST"]
)
def cancel_connection_request(connection_id):

    if "user_id" not in session:
        return redirect(url_for("login"))

    connection = Connection.query.get_or_404(
        connection_id
    )

    if connection.sender_id != session["user_id"]:
        return "Unauthorized", 403

    connection.status = "cancelled"

    db.session.commit()

    return redirect(url_for("connections"))

# ============================================================
# CHAT
# ============================================================

@app.route("/chat")
@app.route("/chat/<int:connection_id>")
def chat(connection_id=None):

    # --------------------------------------------------------
    # LOGIN CHECK
    # --------------------------------------------------------

    if "user_id" not in session:
        return redirect(url_for("login"))

    current_user_id = session["user_id"]

    # Default values
    connection = None
    messages = []
    partner = None
    upcoming_session = None

    skills_you_learn = []
    skills_you_teach = []

    # --------------------------------------------------------
    # CHAT WITHOUT CONNECTION
    # --------------------------------------------------------

    if connection_id is None:

        return render_template(
            "chat.html",
            connection=None,
            messages=[],
            partner=None,
            skills_you_learn=[],
            skills_you_teach=[],
            upcoming_session=None
        )

    # --------------------------------------------------------
    # GET CONNECTION
    # --------------------------------------------------------

    connection = Connection.query.get_or_404(
        connection_id
    )

    # --------------------------------------------------------
    # SECURITY CHECK
    # --------------------------------------------------------

    if current_user_id not in [
        connection.sender_id,
        connection.receiver_id
    ]:
        return "Unauthorized", 403

    # --------------------------------------------------------
    # CONNECTION MUST BE ACCEPTED
    # --------------------------------------------------------

    if connection.status != "accepted":

        flash(
            "You can chat only after the connection is accepted.",
            "error"
        )

        return redirect(
            url_for("connections")
        )

    # --------------------------------------------------------
    # FIND PARTNER
    # --------------------------------------------------------

    if connection.sender_id == current_user_id:

        partner = connection.receiver

    else:

        partner = connection.sender

    # Safety check
    if not partner:

        return "Partner not found", 404

    # --------------------------------------------------------
    # GET MESSAGES
    # --------------------------------------------------------

    messages = Message.query.filter_by(
        connection_id=connection.id
    ).order_by(
        Message.created_at.asc()
    ).all()

    # --------------------------------------------------------
    # CURRENT USER SKILLS
    # --------------------------------------------------------

    current_user_skills = UserSkill.query.filter_by(
        user_id=current_user_id
    ).all()

    # --------------------------------------------------------
    # SKILLS YOU WANT TO LEARN
    # --------------------------------------------------------

    for user_skill in current_user_skills:

        if not user_skill.skill:
            continue

        if user_skill.skill_type == "learn":

            skills_you_learn.append(
                user_skill.skill.name
            )

    # --------------------------------------------------------
    # SKILLS YOU CAN TEACH
    # --------------------------------------------------------

    for user_skill in current_user_skills:

        if not user_skill.skill:
            continue

        if user_skill.skill_type == "teach":

            skills_you_teach.append(
                user_skill.skill.name
            )

    # Remove duplicates
    skills_you_learn = list(
        dict.fromkeys(skills_you_learn)
    )

    skills_you_teach = list(
        dict.fromkeys(skills_you_teach)
    )

    # --------------------------------------------------------
    # UPCOMING SESSION
    # --------------------------------------------------------
    # IMPORTANT:
    # Your actual model is Session, NOT LearningSession.
    # --------------------------------------------------------

    upcoming_session = Session.query.filter(
        Session.connection_id == connection.id,
        Session.status.in_([
            "pending",
            "scheduled",
            "confirmed"
        ]),
        Session.scheduled_at >= datetime.utcnow()
    ).order_by(
        Session.scheduled_at.asc()
    ).first()

    # --------------------------------------------------------
    # RENDER CHAT
    # --------------------------------------------------------

    return render_template(
        "chat.html",
        connection=connection,
        messages=messages,
        partner=partner,
        skills_you_learn=skills_you_learn,
        skills_you_teach=skills_you_teach,
        upcoming_session=upcoming_session
    )

# ============================================================
# SEND MESSAGE
# ============================================================

@app.route(
    "/chat/<int:connection_id>/send",
    methods=["POST"]
)
def send_message(connection_id):

    # --------------------------------------------------------
    # LOGIN CHECK
    # --------------------------------------------------------

    if "user_id" not in session:
        return redirect(url_for("login"))

    current_user_id = session["user_id"]

    # --------------------------------------------------------
    # GET CONNECTION
    # --------------------------------------------------------

    connection = Connection.query.get_or_404(
        connection_id
    )

    # --------------------------------------------------------
    # SECURITY CHECK
    # --------------------------------------------------------

    if current_user_id not in [
        connection.sender_id,
        connection.receiver_id
    ]:
        return "Unauthorized", 403

    # --------------------------------------------------------
    # CONNECTION MUST BE ACCEPTED
    # --------------------------------------------------------

    if connection.status != "accepted":

        flash(
            "You can send messages only after the connection is accepted.",
            "error"
        )

        return redirect(
            url_for(
                "chat",
                connection_id=connection.id
            )
        )

    # --------------------------------------------------------
    # GET MESSAGE FROM FORM
    # --------------------------------------------------------

    message_text = request.form.get(
        "message",
        ""
    ).strip()

    # --------------------------------------------------------
    # EMPTY MESSAGE CHECK
    # --------------------------------------------------------

    if not message_text:

        flash(
            "Please enter a message.",
            "error"
        )

        return redirect(
            url_for(
                "chat",
                connection_id=connection.id
            )
        )

    # --------------------------------------------------------
    # CREATE MESSAGE
    # --------------------------------------------------------

    new_message = Message(
        connection_id=connection.id,
        sender_id=current_user_id,
        message=message_text,
        is_read=False
    )

    # --------------------------------------------------------
    # SAVE MESSAGE
    # --------------------------------------------------------

    try:

        db.session.add(
            new_message
        )

        db.session.commit()

    except Exception:

        db.session.rollback()

        flash(
            "Something went wrong while sending the message.",
            "error"
        )

    # --------------------------------------------------------
    # BACK TO CHAT
    # --------------------------------------------------------

    return redirect(
        url_for(
            "chat",
            connection_id=connection.id
        )
    )
# ============================================================
# SESSIONS
# ============================================================
@app.route("/sessions")
def sessions():

    if "user_id" not in session:
        return redirect(url_for("login"))

    user_id = session["user_id"]

    # 1. Get ONLY accepted connections involving this user
    accepted_connections = Connection.query.filter(
        (
            (Connection.sender_id == user_id) |
            (Connection.receiver_id == user_id)
        ) &
        (Connection.status == "accepted")
    ).all()

    connection_ids = [
        connection.id
        for connection in accepted_connections
    ]

    # 2. Fetch sessions belonging only to those connections
    learning_sessions = []

    if connection_ids:
        learning_sessions = Session.query.filter(
            Session.connection_id.in_(connection_ids)
        ).order_by(
            Session.scheduled_at.asc()
        ).all()

    # 3. Separate sessions by status
    upcoming_sessions = []
    pending_sessions = []
    completed_sessions = []

    for item in learning_sessions:
        status = (item.status or "").strip().lower()

        if status == "completed":
            completed_sessions.append(item)

        elif status in ("pending", "requested"):
            pending_sessions.append(item)

        elif status in (
            "scheduled",
            "accepted",
            "confirmed",
            "approved"
        ):
            upcoming_sessions.append(item)

    # 4. Calculate learning hours from completed sessions
    total_minutes = sum(
        (item.duration_minutes or 0)
        for item in completed_sessions
    )

    total_learning_hours = round(total_minutes / 60, 1)

    # 5. Render the page
    return render_template(
        "sessions.html",
        sessions=learning_sessions,
        upcoming_sessions=upcoming_sessions,
        pending_sessions=pending_sessions,
        completed_sessions=completed_sessions,
        total_learning_hours=total_learning_hours
    )


#=================================================
# SESSION DETAIL
# ============================================================


@app.route("/sessions/<int:session_id>")
def session_detail(session_id):
    if "user_id" not in session:
        return redirect(url_for("login"))

    current_user_id = session["user_id"]

    learning_session = Session.query.get_or_404(session_id)

    connection = Connection.query.get(learning_session.connection_id)

    if not connection:
        return "Connection not found", 404

    if current_user_id not in [
        connection.sender_id,
        connection.receiver_id
    ]:
        return "Unauthorized", 403

    # Find the other user in this connection
    if connection.sender_id == current_user_id:
        partner = connection.receiver
    else:
        partner = connection.sender

    return render_template(
        "session_detail.html",
        session=learning_session,
        connection=connection,
        partner=partner
    )

# ============================================================
# SCHEDULE SESSION
# ============================================================

@app.route(
    "/sessions/schedule/<int:connection_id>",
    methods=["GET", "POST"]
)
def schedule_session(connection_id):

    # --------------------------------------------------------
    # AUTHENTICATION
    # --------------------------------------------------------
    if "user_id" not in session:
        return redirect(url_for("login"))

    current_user_id = session["user_id"]
    current_user = User.query.get(current_user_id)

    if not current_user:
        session.clear()
        return redirect(url_for("login"))

    # --------------------------------------------------------
    # CONNECTION ACCESS
    # --------------------------------------------------------
    connection = Connection.query.get_or_404(connection_id)

    if current_user_id not in [
        connection.sender_id,
        connection.receiver_id
    ]:
        return "Unauthorized", 403

    if connection.status != "accepted":
        flash(
            "You can schedule a session only with an accepted skill partner.",
            "error"
        )
        return redirect(url_for("connections"))

    # --------------------------------------------------------
    # FIND PARTNER
    # --------------------------------------------------------
    if connection.sender_id == current_user_id:
        partner = connection.receiver
    else:
        partner = connection.sender

    if not partner:
        flash("Your skill partner could not be found.", "error")
        return redirect(url_for("connections"))

    # --------------------------------------------------------
    # GET BOTH USERS' SKILLS
    # --------------------------------------------------------
    current_user_skills = UserSkill.query.filter_by(
        user_id=current_user_id
    ).all()

    partner_skills = UserSkill.query.filter_by(
        user_id=partner.id
    ).all()

    current_user_teaches = []
    current_user_learns = []
    partner_teaches = []
    partner_learns = []

    for user_skill in current_user_skills:
        if not user_skill.skill:
            continue

        skill_name = user_skill.skill.name

        if user_skill.skill_type == "teach":
            current_user_teaches.append(skill_name)
        elif user_skill.skill_type == "learn":
            current_user_learns.append(skill_name)

    for user_skill in partner_skills:
        if not user_skill.skill:
            continue

        skill_name = user_skill.skill.name

        if user_skill.skill_type == "teach":
            partner_teaches.append(skill_name)
        elif user_skill.skill_type == "learn":
            partner_learns.append(skill_name)

    # Partner teaches OR current user teaches
    exchange_skills = sorted(set(
        partner_teaches + current_user_teaches
    ))

    # --------------------------------------------------------
    # HANDLE FORM SUBMISSION
    # --------------------------------------------------------
    if request.method == "POST":

        session_date = request.form.get(
            "session_date", ""
        ).strip()

        session_time = request.form.get(
            "session_time", ""
        ).strip()

        skill = request.form.get(
            "skill", ""
        ).strip()

        topic = request.form.get(
            "topic", ""
        ).strip()

        duration = request.form.get(
            "duration", ""
        ).strip()

        mode = request.form.get(
            "mode", ""
        ).strip()

        notes = request.form.get(
            "notes", ""
        ).strip()

        meeting_url = request.form.get(
            "meeting_url", ""
        ).strip()

        # -------------------------
        # VALIDATE REQUIRED FIELDS
        # -------------------------
        if not session_date or not session_time:
            flash("Please select a date and time.", "error")
            return redirect(url_for(
                "schedule_session",
                connection_id=connection.id
            ))

        if not skill or skill not in exchange_skills:
            flash("Please select a valid skill for this connection.", "error")
            return redirect(url_for(
                "schedule_session",
                connection_id=connection.id
            ))

        if not duration:
            flash("Please select a duration.", "error")
            return redirect(url_for(
                "schedule_session",
                connection_id=connection.id
            ))

        if not mode:
            flash("Please select a session mode.", "error")
            return redirect(url_for(
                "schedule_session",
                connection_id=connection.id
            ))

        # -------------------------
        # VALIDATE MEETING LINK
        # -------------------------
        if meeting_url:
            from urllib.parse import urlparse

            parsed_url = urlparse(meeting_url)

            if (
                parsed_url.scheme not in ("http", "https")
                or not parsed_url.netloc
            ):
                flash(
                    "Please enter a valid Zoom or Google Meet URL.",
                    "error"
                )
                return redirect(url_for(
                    "schedule_session",
                    connection_id=connection.id
                ))

        # -------------------------
        # PARSE DATE AND TIME
        # -------------------------
        try:
            scheduled_at = datetime.fromisoformat(
                f"{session_date}T{session_time}"
            )
        except (ValueError, TypeError):
            flash("Please select a valid date and time.", "error")
            return redirect(url_for(
                "schedule_session",
                connection_id=connection.id
            ))

        # -------------------------
        # VALIDATE DURATION
        # -------------------------
        duration_map = {
            "30 Minutes": 30,
            "1 Hour": 60,
            "1.5 Hours": 90,
            "2 Hours": 120
        }

        duration_minutes = duration_map.get(duration)

        if duration_minutes is None:
            flash("Please select a valid duration.", "error")
            return redirect(url_for(
                "schedule_session",
                connection_id=connection.id
            ))

        # -------------------------
        # CREATE AND SAVE SESSION
        # -------------------------
        try:
            learning_session = Session(
                connection_id=connection.id,
                title=f"{skill} Learning Session",
                skill=skill,
                topic=topic or None,
                description=None,
                scheduled_at=scheduled_at,
                duration_minutes=duration_minutes,
                session_type=mode,
                meeting_url=meeting_url or None,
                status="pending",
                message=notes or None
            )

            db.session.add(learning_session)
            db.session.flush()

          
            partner_notification = Notification(
                user_id=partner.id,
                notification_type="session_request",
                title="New Learning Session Scheduled",
                message=(
                    f"{current_user.full_name} scheduled a "
                    f"{skill} session"
                    f"{' about ' + topic if topic else ''} "
                    f"on {scheduled_at.strftime('%d %b %Y at %I:%M %p')}."
                ),
                action_url=url_for(
                    "session_detail",
                    session_id=learning_session.id
                ),
                category="session"
            )

            db.session.add(partner_notification)
            db.session.commit()

                
            db.session.add(partner_notification)
            db.session.commit()

            flash("Session scheduled successfully!", "success")
            return redirect(url_for("sessions"))

        except Exception:
            db.session.rollback()

            app.logger.exception(
                "Error scheduling session or creating notification"
            )

            flash(
                "Something went wrong while scheduling the session.",
                "error"
            )
            return redirect(url_for(
                "schedule_session",
                connection_id=connection.id
            ))

    # --------------------------------------------------------
    # GET REQUEST: DISPLAY THE FORM
    # IMPORTANT: This return is outside the POST block.
    # --------------------------------------------------------
    return render_template(
        "schedule_session.html",
        connection=connection,
        partner=partner,
        current_user=current_user,
        exchange_skills=exchange_skills,
        current_user_teaches=current_user_teaches,
        current_user_learns=current_user_learns,
        partner_teaches=partner_teaches,
        partner_learns=partner_learns
    )

# ============================================================
# ROADMAP
# ============================================================

@app.route("/roadmap")
@app.route("/roadmap/<skill>")
def roadmap(skill=None):

    if "user_id" not in session:
        return redirect(url_for("login"))

    selected_skill = None
    roadmap_obj = None
    roadmap_sections = []

    # ========================================================
    # FIND SELECTED SKILL
    # ========================================================

    if skill:

        selected_skill = Skill.query.filter(
            db.or_(
                Skill.slug == skill,
                Skill.name == skill
            )
        ).first()

        if selected_skill:

            roadmap_obj = Roadmap.query.filter_by(
                skill_id=selected_skill.id,
                is_active=True
            ).first()

    # ========================================================
    # NO ROADMAP
    # ========================================================

    if not selected_skill or not roadmap_obj:

        return render_template(
            "roadmap.html",
            skill=selected_skill,
            roadmap=roadmap_obj,
            roadmap_sections=[],
            total_topics=0,
            completed_topics=0,
            remaining_topics=0,
            progress_percentage=0,
            earned_level="Learning"
        )
     

    # ========================================================
    # ROADMAP TOPICS
    # ========================================================

    roadmap_topics = list(
        roadmap_obj.topics
    )

    current_user_id = session["user_id"]

    # ========================================================
    # USER PROGRESS
    # ========================================================

    topic_ids = [
        topic.id
        for topic in roadmap_topics
    ]

    progress_records = {}

    if topic_ids:

        records = TopicProgress.query.filter(
            TopicProgress.user_id == current_user_id,
            TopicProgress.topic_id.in_(topic_ids)
        ).all()

        progress_records = {
            record.topic_id: record
            for record in records
        }

    # ========================================================
    # BUILD ROADMAP TOPICS
    # ========================================================

    roadmap_topic_views = []

    previous_topic_completed = True

    completed_topics = 0

    for index, topic in enumerate(roadmap_topics):

        progress = progress_records.get(
            topic.id
        )

        learned = (
            progress.learned
            if progress
            else False
        )

        practiced = (
            progress.practiced
            if progress
            else False
        )

        task_completed = (
            progress.task_completed
            if progress
            else False
        )

        # ----------------------------------------------------
        # Does this topic actually have a practical task?
        # ----------------------------------------------------

        has_task = bool(
            topic.task_description
        )

        # ----------------------------------------------------
        # Completion
        # ----------------------------------------------------

        if has_task:

            topic_completed = (
                learned
                and practiced
                and task_completed
            )

        else:

            topic_completed = (
                learned
                and practiced
            )

        # ----------------------------------------------------
        # Unlock logic
        # ----------------------------------------------------

        if index == 0:

            topic_unlocked = True

        else:

            topic_unlocked = (
                previous_topic_completed
            )

        # ----------------------------------------------------
        # Count completed topics
        # ----------------------------------------------------

        if topic_completed:

            completed_topics += 1

        # ----------------------------------------------------
        # Topic description
        #
        # Current RoadmapTopic model has explanation,
        # not description.
        # ----------------------------------------------------

        topic_description = (
            topic.explanation
            if topic.explanation
            else topic.task_description
        )

        # ----------------------------------------------------
        # Topic view for roadmap.html
        # ----------------------------------------------------

        roadmap_topic_views.append(
            SimpleNamespace(
                id=topic.id,

                title=topic.title,

                description=topic_description,

                completed=topic_completed,

                unlocked=topic_unlocked,

                locked=not topic_unlocked,

                learned=learned,

                practiced=practiced,

                task_completed=task_completed,

                has_task=has_task,

                order_index=topic.order_index
            )
        )

        # ----------------------------------------------------
        # Next topic depends ONLY on actual completion
        # ----------------------------------------------------

        previous_topic_completed = (
            topic_completed
        )

    # ========================================================
    # OVERALL PROGRESS
    # ========================================================

    total_topics = len(
        roadmap_topics
    )

    remaining_topics = max(
        total_topics - completed_topics,
        0
    )

    if total_topics:

        progress_percentage = int(
            (
                completed_topics
                / total_topics
            ) * 100
        )

    else:

        progress_percentage = 0

    # ========================================================
    # EARNED LEVEL
    # ========================================================

    earned_level = "Learning"

    user_skill = UserSkill.query.filter_by(
        user_id=current_user_id,
        skill_id=selected_skill.id,
        skill_type="learn"
    ).first()

    if user_skill and user_skill.earned_level:

        earned_level = (
            user_skill.earned_level
        )

    # ========================================================
    # ONE ROADMAP STAGE
    #
    # Current Roadmap model does not have a separate
    # Stage/Section table, so we keep the existing topics
    # inside one structured stage.
    # ========================================================

    roadmap_sections = [
        SimpleNamespace(
            title=roadmap_obj.title,

            description=(
                roadmap_obj.description
                or
                f"Follow the structured {selected_skill.name} "
                f"learning path step by step."
            ),

            topics=roadmap_topic_views
        )
    ]

    # ========================================================
    # RENDER
    # ========================================================

    return render_template(
        "roadmap.html",

        skill=selected_skill,

        skill_name=selected_skill.name,

        roadmap=roadmap_obj,

        roadmap_sections=roadmap_sections,

        total_topics=total_topics,

        completed_topics=completed_topics,

        remaining_topics=remaining_topics,

        progress_percentage=progress_percentage,

        earned_level=earned_level
    )


# ============================================================
# TOPIC LEARNING
# ============================================================

@app.route("/topic/<int:topic_id>")
def topic_learning(topic_id):

    if "user_id" not in session:
        return redirect(url_for("login"))

    current_user_id = session["user_id"]

    topic = RoadmapTopic.query.get_or_404(
        topic_id
    )

    # ========================================================
    # SKILL + ROADMAP
    # ========================================================

    roadmap_obj = topic.roadmap

    if not roadmap_obj:
        return "Roadmap not found for this topic.", 404

    skill_obj = roadmap_obj.skill

    if not skill_obj:
        return "Skill not found for this topic.", 404

    skill = skill_obj.slug
    skill_name = skill_obj.name

    # ========================================================
    # ALL ROADMAP TOPICS
    # ========================================================

    roadmap_topics = list(
        roadmap_obj.topics
    )

    current_index = next(
        (
            index
            for index, roadmap_topic
            in enumerate(roadmap_topics)
            if roadmap_topic.id == topic.id
        ),
        None
    )

    if current_index is None:
        return "Topic does not belong to this roadmap.", 404

    # ========================================================
    # CURRENT TOPIC PROGRESS
    # ========================================================

    progress = TopicProgress.query.filter_by(
        user_id=current_user_id,
        topic_id=topic.id
    ).first()

    learning_completed = (
        progress.learned
        if progress
        else False
    )

    practice_completed = (
        progress.practiced
        if progress
        else False
    )

    task_completed = (
        progress.task_completed
        if progress
        else False
    )

    # ========================================================
    # TOPIC TASK
    # ========================================================

    has_task = bool(
        topic.task_description
    )

    # ========================================================
    # CURRENT TOPIC COMPLETION
    # ========================================================

    if has_task:

        topic_completed = (
            learning_completed
            and practice_completed
            and task_completed
        )

    else:

        topic_completed = (
            learning_completed
            and practice_completed
        )

    # ========================================================
    # CHECK PREVIOUS TOPIC
    # ========================================================

    previous_topic = None
    next_topic = None

    if current_index > 0:

        previous_topic = roadmap_topics[
            current_index - 1
        ]

        previous_progress = TopicProgress.query.filter_by(
            user_id=current_user_id,
            topic_id=previous_topic.id
        ).first()

        previous_has_task = bool(
            previous_topic.task_description
        )

        if previous_progress:

            if previous_has_task:

                previous_completed = (
                    previous_progress.learned
                    and
                    previous_progress.practiced
                    and
                    previous_progress.task_completed
                )

            else:

                previous_completed = (
                    previous_progress.learned
                    and
                    previous_progress.practiced
                )

        else:

            previous_completed = False

        topic_unlocked = (
            previous_completed
        )

    else:

        topic_unlocked = True

    # ========================================================
    # PROTECT LOCKED TOPICS
    # ========================================================

    if not topic_unlocked:

        flash(
            "Complete the previous topic first to unlock this topic.",
            "info"
        )

        return redirect(
            url_for(
                "roadmap",
                skill=skill
            )
        )

    # ========================================================
    # TOPIC STATUS
    # ========================================================

    if topic_completed:

        topic_status = "completed"

    elif (
        learning_completed
        or practice_completed
        or task_completed
    ):

        topic_status = "current"

    else:

        topic_status = "available"

    # ========================================================
    # TOPIC VIEW
    #
    # Only use fields that actually exist in
    # RoadmapTopic. Missing future fields stay None.
    # ========================================================

    topic_view = SimpleNamespace(

        id=topic.id,

        title=topic.title,

        description=getattr(
            topic,
            "description",
            None
        ),

        explanation=topic.explanation,

        example=getattr(
            topic,
            "example",
            None
        ),

        code_example=topic.code_example,

        code_language=getattr(
            topic,
            "code_language",
            None
        ),

        practice_instructions=getattr(
            topic,
            "practice_instructions",
            None
        ),

        task_title=getattr(
            topic,
            "task_title",
            None
        ),

        task_instructions=getattr(
            topic,
            "task_instructions",
            None
        ),

        task_description=topic.task_description,

        task_type=topic.task_type,

        has_task=has_task,

        estimated_minutes=getattr(
            topic,
            "estimated_minutes",
            None
        ),

        order_index=topic.order_index,

        status=topic_status
    )

    # ========================================================
    # NEXT TOPIC
    # ========================================================

    if (
        topic_completed
        and
        current_index < len(roadmap_topics) - 1
    ):

        next_topic = roadmap_topics[
            current_index + 1
        ]

    # ========================================================
    # TOPIC PROGRESS %
    # ========================================================

    completed_steps = 0

    if learning_completed:
        completed_steps += 1

    if practice_completed:
        completed_steps += 1

    if has_task:

        if task_completed:
            completed_steps += 1

        total_steps = 3

    else:

        total_steps = 2

    topic_progress_percentage = int(
        (
            completed_steps
            / total_steps
        ) * 100
    )

    # ========================================================
    # EARNED LEVEL
    # ========================================================

    user_skill = UserSkill.query.filter_by(
        user_id=current_user_id,
        skill_id=skill_obj.id,
        skill_type="learn"
    ).first()

    earned_level = None

    if user_skill:

        earned_level = (
            user_skill.earned_level
        )

    # ========================================================
    # ASSESSMENT
    # ========================================================

    assessment_available = (
        Assessment.query.filter_by(
            skill_id=skill_obj.id
        ).first()
        is not None
    )

    # ========================================================
    # TASK SUBMISSION
    # ========================================================

    task_submission = None
    task_error = None

    # ========================================================
    # RENDER
    # ========================================================
    return render_template(
    "topic_learning.html",

    topic=topic_view,

    progress=progress,

    skill=skill,
    skill_id=skill_obj.id,
    skill_name=skill_name,

    topic_progress_percentage=(
        topic_progress_percentage
    ),

    learning_completed=(
        learning_completed
    ),

    practice_completed=(
        practice_completed
    ),

    task_completed=(
        task_completed
    ),

    previous_topic=previous_topic,
    next_topic=next_topic,

    earned_level=earned_level,

    assessment_available=(
        assessment_available
    ),

    task_submission=task_submission,
    task_error=task_error
)

# ============================================================
# MARK TOPIC LEARNED
# ============================================================

@app.route(
    "/topic/<int:topic_id>/learned",
    methods=["POST"]
)
def mark_topic_learned(topic_id):

    if "user_id" not in session:
        return redirect(url_for("login"))

    topic = RoadmapTopic.query.get_or_404(
        topic_id
    )

    current_user_id = session["user_id"]

    # ========================================================
    # CHECK TOPIC UNLOCK
    # ========================================================

    roadmap_obj = topic.roadmap

    roadmap_topics = list(
        roadmap_obj.topics
    )

    current_index = next(
        (
            index
            for index, roadmap_topic
            in enumerate(roadmap_topics)
            if roadmap_topic.id == topic.id
        ),
        None
    )

    if current_index is None:
        return redirect(url_for("dashboard"))

    if current_index > 0:

        previous_topic = roadmap_topics[
            current_index - 1
        ]

        previous_progress = TopicProgress.query.filter_by(
            user_id=current_user_id,
            topic_id=previous_topic.id
        ).first()

        if not previous_progress:

            flash(
                "Complete the previous topic first.",
                "info"
            )

            return redirect(
                url_for(
                    "roadmap",
                    skill=roadmap_obj.skill.slug
                )
            )

        previous_has_task = bool(
            previous_topic.task_description
        )

        if previous_has_task:

            previous_completed = (
                previous_progress.learned
                and
                previous_progress.practiced
                and
                previous_progress.task_completed
            )

        else:

            previous_completed = (
                previous_progress.learned
                and
                previous_progress.practiced
            )

        if not previous_completed:

            flash(
                "Complete the previous topic first.",
                "info"
            )

            return redirect(
                url_for(
                    "roadmap",
                    skill=roadmap_obj.skill.slug
                )
            )

    # ========================================================
    # GET / CREATE PROGRESS
    # ========================================================

    progress = TopicProgress.query.filter_by(
        user_id=current_user_id,
        topic_id=topic.id
    ).first()

    if not progress:

        progress = TopicProgress(
            user_id=current_user_id,
            topic_id=topic.id,
            status="available"
        )

        db.session.add(progress)

    # ========================================================
    # MARK LEARNED
    # ========================================================

    progress.learned = True

    # Do not mark topic completed here.
    # Practice + practical task are still required.
    # ========================================================

    if (
        progress.practiced
        and
        progress.task_completed
    ):

        progress.status = "completed"

        if not progress.completed_at:

            progress.completed_at = datetime.utcnow()

    else:

        progress.status = "current"

    db.session.commit()

    return redirect(
        url_for(
            "topic_learning",
            topic_id=topic.id
        )
    )


# ============================================================
# MARK TOPIC PRACTICED
# ============================================================

@app.route(
    "/topic/<int:topic_id>/practiced",
    methods=["POST"]
)
def mark_topic_practiced(topic_id):

    if "user_id" not in session:
        return redirect(url_for("login"))

    topic = RoadmapTopic.query.get_or_404(
        topic_id
    )

    current_user_id = session["user_id"]
        # ========================================================
    # CHECK TOPIC UNLOCK
    # ========================================================

    roadmap_obj = topic.roadmap

    if not roadmap_obj:
        return "Roadmap not found for this topic.", 404

    roadmap_topics = list(
        roadmap_obj.topics
    )

    current_index = next(
        (
            index
            for index, roadmap_topic
            in enumerate(roadmap_topics)
            if roadmap_topic.id == topic.id
        ),
        None
    )

    if current_index is None:
        return "Topic does not belong to this roadmap.", 404

    # --------------------------------------------------------
    # Previous topic must be completed
    # --------------------------------------------------------

    if current_index > 0:

        previous_topic = roadmap_topics[
            current_index - 1
        ]

        previous_progress = TopicProgress.query.filter_by(
            user_id=current_user_id,
            topic_id=previous_topic.id
        ).first()

        if not previous_progress:

            flash(
                "Complete the previous topic first.",
                "info"
            )

            return redirect(
                url_for(
                    "roadmap",
                    skill=roadmap_obj.skill.slug
                )
            )

        previous_has_task = bool(
            previous_topic.task_description
        )

        if previous_has_task:

            previous_completed = (
                previous_progress.learned
                and
                previous_progress.practiced
                and
                previous_progress.task_completed
            )

        else:

            previous_completed = (
                previous_progress.learned
                and
                previous_progress.practiced
            )

        if not previous_completed:

            flash(
                "Complete the previous topic first.",
                "info"
            )

            return redirect(
                url_for(
                    "roadmap",
                    skill=roadmap_obj.skill.slug
                )
            )

    # ========================================================
    # GET / CREATE PROGRESS
    # ========================================================

    progress = TopicProgress.query.filter_by(
        user_id=current_user_id,
        topic_id=topic.id
    ).first()

    if not progress:

        progress = TopicProgress(
            user_id=current_user_id,
            topic_id=topic.id,
            status="available"
        )

        db.session.add(progress)

    # ========================================================
    # PRACTICE REQUIRES LEARNING FIRST
    # ========================================================

    if not progress.learned:

        db.session.rollback()

        flash(
            "Please complete the learning step first.",
            "info"
        )

        return redirect(
            url_for(
                "topic_learning",
                topic_id=topic.id
            )
        )

    # ========================================================
    # MARK PRACTICED
    # ========================================================

    progress.practiced = True

    # ========================================================
    # TOPIC COMPLETION
    # ========================================================

    has_task = bool(
        topic.task_description
    )

    if has_task:

        if (
            progress.learned
            and
            progress.practiced
            and
            progress.task_completed
        ):

            progress.status = "completed"

            if not progress.completed_at:

                progress.completed_at = datetime.utcnow()

        else:

            progress.status = "current"

    else:

        if (
            progress.learned
            and
            progress.practiced
        ):

            progress.status = "completed"

            if not progress.completed_at:

                progress.completed_at = datetime.utcnow()

        else:

            progress.status = "current"

    db.session.commit()

    return redirect(
        url_for(
            "topic_learning",
            topic_id=topic.id
        )
    )
# ============================================================
# PYTHON TASK EVALUATOR
# ============================================================

def evaluate_python_task(topic, submission):
    """
    Evaluate Python practical tasks for the first 5 Python topics.

    Returns:
        passed: bool
        score: float
        feedback: str
    """

    code = submission.strip()

    if not code:
        return False, 0, "Please write your solution before submitting."

    # --------------------------------------------------------
    # 1. Check whether submitted code is valid Python
    # --------------------------------------------------------

    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        return (
            False,
            0,
            f"Your Python code contains a syntax error: {e.msg}."
        )

    # --------------------------------------------------------
    # 2. Identify the topic number
    # --------------------------------------------------------

    topic_number = topic.order_index

    # --------------------------------------------------------
    # Topic 1
    # Python Setup & First Program
    # --------------------------------------------------------

    if topic_number == 1:

        result = run_python_submission(code)

        if not result["success"]:
            return False, 0, result["feedback"]

        output = result["output"].strip()

        if not output:
            return (
                False,
                0,
                "Your program runs, but it does not produce any output."
            )

        return (
            True,
            100,
            "Correct! Your first Python program runs successfully and produces output."
        )

    # --------------------------------------------------------
    # Topic 2
    # Python Syntax & Indentation
    # --------------------------------------------------------

    if topic_number == 2:

        has_comment = any(
            isinstance(node, ast.Expr)
            and isinstance(node.value, ast.Constant)
            and isinstance(node.value.value, str)
            for node in ast.walk(tree)
        ) or "#" in code

        has_variable = any(
            isinstance(node, ast.Assign)
            for node in ast.walk(tree)
        )

        has_indented_block = any(
            isinstance(node, (ast.If, ast.For, ast.While, ast.FunctionDef))
            for node in ast.walk(tree)
        )

        result = run_python_submission(code)

        if not result["success"]:
            return False, 0, result["feedback"]

        if not has_comment:
            return (
                False,
                40,
                "Add at least one comment explaining part of your program."
            )

        if not has_variable:
            return (
                False,
                50,
                "Create and use at least one variable in your program."
            )

        if not has_indented_block:
            return (
                False,
                60,
                "Your task requires correctly indented statements. Add a suitable indented block such as an if, loop, or function."
            )

        return (
            True,
            100,
            "Correct! Your program has valid Python syntax, variables, comments and an indented block."
        )

    # --------------------------------------------------------
    # Topic 3
    # Variables & Naming
    # --------------------------------------------------------

    if topic_number == 3:

        assignments = [
            node
            for node in ast.walk(tree)
            if isinstance(node, ast.Assign)
        ]

        if not assignments:
            return (
                False,
                0,
                "No variables were created. Create variables for student information."
            )

        variable_names = []

        for assignment in assignments:
            for target in assignment.targets:
                if isinstance(target, ast.Name):
                    variable_names.append(target.id)

        if not variable_names:
            return (
                False,
                30,
                "Create meaningful variable names for the student information."
            )

        generic_names = {
            "a",
            "b",
            "c",
            "x",
            "y",
            "z",
            "var",
            "data"
        }

        meaningful_names = [
            name
            for name in variable_names
            if name.lower() not in generic_names
        ]

        if len(meaningful_names) < 2:
            return (
                False,
                60,
                "Use meaningful variable names such as student_name, age, city, course, etc."
            )

        result = run_python_submission(code)

        if not result["success"]:
            return False, 0, result["feedback"]

        return (
            True,
            100,
            "Correct! Your program creates and uses meaningful variables for student information."
        )

    # --------------------------------------------------------
    # Topic 4
    # Data Types
    # --------------------------------------------------------

    if topic_number == 4:

        result = run_python_submission(code)

        if not result["success"]:
            return False, 0, result["feedback"]

        output = result["output"]

        type_names = set()

        for node in ast.walk(tree):

            if isinstance(node, ast.Constant):

                if isinstance(node.value, bool):
                    type_names.add("bool")

                elif isinstance(node.value, int):
                    type_names.add("int")

                elif isinstance(node.value, float):
                    type_names.add("float")

                elif isinstance(node.value, str):
                    type_names.add("str")

        required_types = {
            "int",
            "float",
            "str",
            "bool"
        }

        missing = required_types - type_names

        if missing:
            return (
                False,
                60,
                "Your program must use at least four Python data types: int, float, string and boolean."
            )

        if not output.strip():
            return (
                False,
                80,
                "Create the data-type variables and display their values."
            )

        return (
            True,
            100,
            "Correct! Your program uses int, float, string and boolean data types and produces output."
        )

    # --------------------------------------------------------
    # Topic 5
    # Input & Output
    # --------------------------------------------------------

    if topic_number == 5:

        input_calls = [
            node
            for node in ast.walk(tree)
            if isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == "input"
        ]

        if len(input_calls) < 3:
            return (
                False,
                50,
                "Your program must accept three inputs: name, age and city."
            )

        result = run_python_submission(
            code,
            input_data="Tejasvi\n20\nPune\n"
        )

        if not result["success"]:
            return False, 0, result["feedback"]

        output = result["output"].lower()

        required_output_values = [
            "tejasvi",
            "20",
            "pune"
        ]

        missing = [
            value
            for value in required_output_values
            if value not in output
        ]

        if missing:
            return (
                False,
                70,
                "Your program accepts input, but the final introduction should display the name, age and city."
            )

        return (
            True,
            100,
            "Correct! Your program accepts name, age and city and displays them in the introduction."
        )

    # --------------------------------------------------------
    # Topics without an evaluator yet
    # --------------------------------------------------------

    return (
        False,
        0,
        "This topic's automatic evaluator has not been implemented yet."
    )


def run_python_submission(code, input_data=""):
    """
    Run submitted Python code with a short timeout.

    This is a development evaluator only.
    A production deployment must use a properly isolated sandbox.
    """

    temp_path = None

    try:

        with tempfile.NamedTemporaryFile(
            mode="w",
            suffix=".py",
            delete=False,
            encoding="utf-8"
        ) as temp_file:

            temp_file.write(code)
            temp_path = temp_file.name

        completed = subprocess.run(
            [sys.executable, temp_path],
            input=input_data,
            text=True,
            capture_output=True,
            timeout=3
        )

        if completed.returncode != 0:

            error = completed.stderr.strip()

            return {
                "success": False,
                "output": completed.stdout,
                "feedback": (
                    "Your program could not run successfully.\n\n"
                    + error[:1000]
                )
            }

        return {
            "success": True,
            "output": completed.stdout,
            "feedback": ""
        }

    except subprocess.TimeoutExpired:

        return {
            "success": False,
            "output": "",
            "feedback": "Your program took too long to finish. Check for an infinite loop."
        }

    except Exception as e:

        return {
            "success": False,
            "output": "",
            "feedback": f"Evaluation error: {str(e)}"
        }

    finally:

        if temp_path and os.path.exists(temp_path):

            try:
                os.remove(temp_path)
            except OSError:
                pass

# ============================================================
# SUBMIT TOPIC TASK
# ============================================================
# ============================================================
# SUBMIT TOPIC TASK
# ============================================================

@app.route(
    "/topic/<int:topic_id>/task",
    methods=["POST"]
)
def submit_topic_task(topic_id):

    if "user_id" not in session:
        return redirect(url_for("login"))

    topic = RoadmapTopic.query.get_or_404(topic_id)

    # --------------------------------------------------------
    # Get / create topic progress
    # --------------------------------------------------------

    progress = TopicProgress.query.filter_by(
        user_id=session["user_id"],
        topic_id=topic.id
    ).first()

    if not progress:

        progress = TopicProgress(
            user_id=session["user_id"],
            topic_id=topic.id,
            status="available"
        )

        db.session.add(progress)
        db.session.flush()

    # --------------------------------------------------------
    # Learning sequence protection
    # --------------------------------------------------------

    if not progress.learned:

        flash(
            "Complete the learning step before submitting the task.",
            "error"
        )

        return redirect(
            url_for(
                "topic_learning",
                topic_id=topic.id
            )
        )

    if not progress.practiced:

        flash(
            "Complete the practice step before submitting the task.",
            "error"
        )

        return redirect(
            url_for(
                "topic_learning",
                topic_id=topic.id
            )
        )

    # --------------------------------------------------------
    # Get submission
    # IMPORTANT: HTML uses name="answer"
    # --------------------------------------------------------

    submission_text = request.form.get(
        "answer",
        ""
    ).strip()

    if not submission_text:

        flash(
            "Please write your solution before submitting.",
            "error"
        )

        return redirect(
            url_for(
                "topic_learning",
                topic_id=topic.id
            )
        )

    # --------------------------------------------------------
    # Find / create task configuration
    # --------------------------------------------------------

    task = TopicTask.query.filter_by(
        topic_id=topic.id
    ).first()

    evaluation_mode_map = {
        "coding": "universal_coding",
        "speaking": "universal_language",
        "creative": "universal_creative",
        "marketing": "universal_marketing",
        "practical": "universal_practical"
    }

    task_type = (
        topic.task_type
        or "practical"
    ).strip().lower()

    evaluation_mode = evaluation_mode_map.get(
        task_type,
        "universal_practical"
    )

    if not task:

        task = TopicTask(
            topic_id=topic.id,
            task_type=task_type,
            evaluation_mode=evaluation_mode,
            instructions=topic.task_description or "",
            is_active=True
        )

        db.session.add(task)
        db.session.flush()

    else:

        # Existing tasks created by the old Python evaluator
        # must also move to the universal evaluator.

        task.task_type = task_type
        task.evaluation_mode = evaluation_mode
        task.instructions = topic.task_description or ""
        task.is_active = True

    # --------------------------------------------------------
    # Save submission
    # --------------------------------------------------------

    submission = TaskSubmission(
        task_id=task.id,
        user_id=session["user_id"],
        submission=submission_text,
        status="evaluating"
    )

    db.session.add(submission)
    db.session.flush()

    # --------------------------------------------------------
    # UNIVERSAL EVALUATION
    # --------------------------------------------------------

    passed, score, feedback = evaluate_submission(
        topic,
        submission_text
    )

    # --------------------------------------------------------
    # Save evaluation result
    # --------------------------------------------------------

    evaluation = TaskEvaluation(
        submission_id=submission.id,
        passed=passed,
        score=score,
        feedback=feedback
    )

    db.session.add(evaluation)

    # --------------------------------------------------------
    # TASK PASSED
    # --------------------------------------------------------

    if passed:

        submission.status = "passed"

        progress.task_completed = True
        progress.status = "completed"
        progress.completed_at = datetime.utcnow()

        flash(
            f"Task passed! Score: {score}/100. "
            "Next topic is now unlocked.",
            "success"
        )

    # --------------------------------------------------------
    # TASK FAILED
    # --------------------------------------------------------

    else:

        submission.status = "failed"

        # Failed task must NEVER complete the topic.
        progress.task_completed = False

        flash(
            f"Task not passed ({score}/100). {feedback}",
            "error"
        )

    db.session.commit()

    return redirect(
        url_for(
            "topic_learning",
            topic_id=topic.id
        )
    )
# ============================================================
# PROGRESS
# ============================================================
@app.route("/progress")
def progress():

    if "user_id" not in session:
        return redirect(url_for("login"))

    progress_records = TopicProgress.query.filter_by(
        user_id=session["user_id"]
    ).all()

    return render_template(
        "progress.html",
        progress_records=progress_records
    )
# ============================================================
# CERTIFICATES
# ============================================================
@app.route("/certificates")
def certificates():

    if "user_id" not in session:
        return redirect(url_for("login"))

    user_certificates = Certificate.query.filter_by(
        user_id=session["user_id"]
    ).order_by(
        Certificate.issued_at.desc()
    ).all()

    return render_template(
        "certificates.html",
        certificates=user_certificates
    )
# ============================================================
# SINGLE CERTIFICATE
# ============================================================
@app.route("/certificate/<int:certificate_id>")
def certificate(certificate_id):

    certificate_obj = Certificate.query.get_or_404(
        certificate_id
    )

    return render_template(
        "certificate.html",
        certificate=certificate_obj
    )
# ============================================================
# REVIEWS
# ============================================================
@app.route("/reviews")
def reviews():

    if "user_id" not in session:
        return redirect(url_for("login"))

    user = User.query.get(
        session["user_id"]
    )

    received_reviews = Review.query.filter_by(
        reviewee_id=user.id
    ).order_by(
        Review.created_at.desc()
    ).all()

    given_reviews = Review.query.filter_by(
        reviewer_id=user.id
    ).order_by(
        Review.created_at.desc()
    ).all()

    return render_template(
        "reviews.html",
        received_reviews=received_reviews,
        given_reviews=given_reviews
    )
# ============================================================
# CREATE REVIEW
# ============================================================
@app.route(
    "/reviews/create/<int:session_id>",
    methods=["GET", "POST"]
)
def create_review(session_id):

    if "user_id" not in session:
        return redirect(url_for("login"))

    learning_session = LearningSession.query.get_or_404(
        session_id
    )

    connection = learning_session.connection

    current_user_id = session["user_id"]

    if current_user_id not in [
        connection.sender_id,
        connection.receiver_id
    ]:
        return "Unauthorized", 403

    if current_user_id == connection.sender_id:
        reviewee_id = connection.receiver_id
    else:
        reviewee_id = connection.sender_id

    if request.method == "POST":

        rating = int(
            request.form.get(
                "rating",
                5
            )
        )

        comment = request.form.get(
            "comment",
            ""
        ).strip()

        review = Review(
            session_id=learning_session.id,
            reviewer_id=current_user_id,
            reviewee_id=reviewee_id,
            rating=rating,
            comment=comment
        )

        db.session.add(review)
        db.session.commit()

        flash(
            "Review submitted!",
            "success"
        )

        return redirect(
            url_for("reviews")
        )

    return render_template(
        "create_review.html",
        session=learning_session
    )
# ============================================================
# NOTIFICATIONS
# ============================================================

@app.route("/notifications")
def notifications():
    if "user_id" not in session:
        return redirect(url_for("login"))

    user_id = session["user_id"]

    notification_list = Notification.query.filter_by(
        user_id=user_id
    ).order_by(
        Notification.created_at.desc()
    ).all()

    unread_count = Notification.query.filter_by(
        user_id=user_id,
        is_read=False
    ).count()

    total_notifications = Notification.query.filter_by(
        user_id=user_id
    ).count()

    return render_template(
        "notifications.html",
        notifications=notification_list,
        unread_count=unread_count,
        total_notifications=total_notifications
    )

    
# ============================================================
# MARK NOTIFICATION READ
# ============================================================
@app.route(
    "/notifications/<int:notification_id>/read",
    methods=["POST"]
)
def mark_notification_read(notification_id):

    if "user_id" not in session:
        return redirect(url_for("login"))

    notification = Notification.query.get_or_404(
        notification_id
    )

    if notification.user_id != session["user_id"]:
        return "Unauthorized", 403

    notification.is_read = True

    db.session.commit()

    return redirect(
        url_for("notifications")
    )
# ============================================================
# MARK ALL NOTIFICATIONS READ
# ============================================================
@app.route(
    "/notifications/read-all",
    methods=["POST"]
)
def mark_all_notifications_read():

    if "user_id" not in session:
        return redirect(url_for("login"))

    Notification.query.filter_by(
        user_id=session["user_id"],
        is_read=False
    ).update(
        {
            Notification.is_read: True
        }
    )

    db.session.commit()

    return redirect(
        url_for("notifications")
    )
# ============================================================
# TERMS
# ============================================================
@app.route("/terms")
def terms():
    return render_template("terms.html")
# ============================================================
# PRIVACY
# ============================================================
@app.route("/privacy")
def privacy():
    return render_template("privacy.html")
# ============================================================
# 404
# ============================================================
@app.errorhandler(404)
def page_not_found(error):

    return render_template(
        "404.html"
    ), 404
# ============================================================
# 403
# ============================================================
@app.errorhandler(403)
def forbidden(error):

    return render_template(
        "403.html"
    ), 403
# ============================================================
# 400
# ============================================================
@app.errorhandler(400)
def bad_request(error):

    return render_template(
        "400.html"
    ), 400
# ============================================================
# 500
# ============================================================
@app.errorhandler(500)
def internal_server_error(error):

    db.session.rollback()

    return render_template(
        "500.html"
    ), 500
# ============================================================
# DATABASE
# ============================================================
with app.app_context():
    db.create_all()
# ============================================================
# RUN
# ============================================================
if __name__ == "__main__":
    app.run(
       debug=True
    )