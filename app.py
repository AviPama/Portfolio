"""
app.py
------
Main Flask application file.

This file:
1. Creates and configures the Flask app
2. Sets up a SQLite database (via Flask-SQLAlchemy) to store contact form messages
3. Defines all the page routes (Home, About, Skills, Projects, Experience, Contact)
4. Handles the contact form submission (validates input, saves to DB)

Beginner note: Flask works by mapping "routes" (URLs) to Python functions.
When a browser visits a URL, Flask runs the matching function and returns
whatever that function gives back (usually rendered HTML).
"""

from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
import os

# ----------------------------------------------------------------------
# 1. APP CONFIGURATION
# ----------------------------------------------------------------------
app = Flask(__name__)

# Secret key is required by Flask to securely sign session cookies and
# flash messages (the little "success!" / "error!" banners).
# In production, set this via an environment variable instead of hardcoding it.
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-secret-key-change-me")

# Configure SQLite database. The file "portfolio.db" will be created
# automatically inside the project folder the first time you run migrations.
basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "portfolio.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize the database and migration engine
db = SQLAlchemy(app)
migrate = Migrate(app, db)


# ----------------------------------------------------------------------
# 2. DATABASE MODEL
# ----------------------------------------------------------------------
class ContactMessage(db.Model):
    """
    Represents a single contact form submission.
    Each attribute below becomes a column in the 'contact_message' table.
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<ContactMessage {self.name} - {self.email}>"


# ----------------------------------------------------------------------
# 3. STATIC PORTFOLIO DATA
# ----------------------------------------------------------------------
# In a larger app this might live in the database or a separate config file,
# but for a personal portfolio, plain Python dictionaries/lists are simple
# and easy to edit.

PROFILE = {
    "name": "Avneet Pama",
    "title": "Full-Stack Developer / Cybersecurity Enthusiast",
    "location": "Seattle, WA",
    "email": "avneetpama@gmail.com",
    "github": "https://github.com/AviPama",
    "linkedin": "https://www.linkedin.com/in/avneet-pama/",
    "resume_file": "files/Avneet_Kaur_Pama_Resume_2026.pdf",
    "bio": (
        "Software engineer with a cybersecurity background (M.S. in IT Security, "
        "CompTIA Security+) and hands-on experience teaching coding and STEM "
        "concepts to elementary school students. Combines engineering fluency in "
        "Python, Java, and web technologies with the ability to design lesson "
        "plans, simplify technical concepts for young learners, and drive "
        "measurable improvements in student comprehension. Seeking part-time, "
        "remote opportunities teaching coding, STEM, or academic subjects to "
        "K-12 students."
    ),
}

EDUCATION = [
    {
        "degree": "Master of Information Technology Security",
        "school": "Ontario Tech University, Canada",
        "details": "GPA: 3.5 / 4.0",
        "years": "Sept 2022 – Aug 2024",
    },
    {
        "degree": "Bachelor of Technology in Computer Science",
        "school": "Institute of Engineering and Technology, India",
        "details": "CGPA: 8.63 / 10",
        "years": "July 2013 – April 2017",
    },
]

SKILLS = {
    "Programming & Web": ["Java", "Python", "C++", "JavaScript", "HTML", "CSS", "PHP", "MySQL", "Data Structures & Algorithms"],
    "Cloud & Security": ["AWS", "OWASP Top 10", "NIST", "ISO/IEC 27001", "Network Security (IDS/IPS)", "Penetration Testing (Burpsuite, Wireshark, Nessus)"],
    "Operating Systems": ["Windows", "Linux"],
    "Certifications": [
        "CompTIA Security+ (Oct 2023)",
        "Microsoft Certified: Security, Compliance and Identity Fundamentals (Oct 2023)",
        "AlgoExpert — 100 Data Structures & Algorithms Questions (Jan 2025)",
        "Preparing for Certified Ethical Hacker (CEH)",
    ],
}

EXPERIENCE = [
    {
        "role": "Elementary Tutor",
        "org": "West Woodland Elementary School, Seattle, USA",
        "years": "June 2025 – Present",
        "points": [
            "Deliver one-on-one and small-group English instruction to elementary grade students, adapting lessons to individual learning styles and pace.",
            "Evaluate student assignments and track progress to drive measurable academic achievement.",
        ],
    },
    {
        "role": "STEM Instructor",
        "org": "Kimball Elementary School, Seattle, USA",
        "years": "Feb 2025 – June 2025",
        "points": [
            "Taught foundational STEM concepts to elementary grade students through engaging, hands-on instruction.",
            "Evaluated assignments and tasks, enhancing efficiency and supporting student achievement.",
        ],
    },
    {
        "role": "Teaching Assistant (Blockchain)",
        "org": "Ontario Tech University, Canada",
        "years": "Jan 2024 – April 2024",
        "points": [
            "Developed 12+ interactive lesson plans, improving concept comprehension by 20% across 50+ students.",
            "Streamlined evaluation process for 200+ assignments, increasing grading efficiency and consistency.",
            "Provided personalized, one-on-one support to students struggling with technical concepts.",
        ],
    },
    {
        "role": "Security Engineer",
        "org": "SLK Software Services, India",
        "years": "May 2018 – Oct 2022",
        "points": [
            "Delivered 15+ secure banking applications by leading end-to-end security assessments.",
            "Reduced vulnerabilities by 70% through SAST/DAST scans; minimized exploitation risk by 75% addressing OWASP Top 10 vulnerabilities.",
            "Improved security posture for 25+ clients through detailed WebInspect/AppScan audits and CVSS-based risk insights.",
            "Embedded security protocols into the SDLC, reducing security gaps by 20% and achieving 95% defect detection.",
            "Recognized with the \u201cStellar Team Award\u201d for contributions across 5 team projects.",
        ],
    },
]

PROJECTS = [
    {
        "title": "Full-Stack Todo App",
        "tech": "JavaScript",
        "year": "2025",
        "description": "Built and deployed a full-stack task management web application, covering both front-end UI and back-end logic.",
        "github": "https://github.com/AviPama",
    },
    {
        "title": "Virtual Private Cloud (VPC) Setup",
        "tech": "AWS, Cloud Networking",
        "year": "2025",
        "description": "Designed a secure, segmented cloud network with public/private subnets and a bastion host for controlled access.",
        "github": "https://github.com/AviPama",
    },
    {
        "title": "RBAC Implementation in AWS IAM",
        "tech": "AWS, IAM",
        "year": "2025",
        "description": "Configured role-based access control policies to enforce least-privilege access across cloud resources.",
        "github": "https://github.com/AviPama",
    },
    {
        "title": "Metasploit Exploitation Lab",
        "tech": "Kali Linux",
        "year": "2024",
        "description": "Performed controlled exploitation of a vulnerable VM using the Metasploit Framework to demonstrate penetration testing methodology.",
        "github": "https://github.com/AviPama",
    },
    {
        "title": "Bias in Sentiment Classifiers",
        "tech": "Python, ML",
        "year": "2024",
        "description": "Evaluated bias in SVM, logistic regression, BERT, and RoBERTa sentiment models; applied debiasing techniques to improve accuracy.",
        "github": "https://github.com/AviPama",
    },
    {
        "title": "Motion Detector",
        "tech": "Python, OpenCV, Pandas",
        "year": "2024",
        "description": "Built a real-time object detection tool using a webcam, with automatic entry/exit logging to CSV.",
        "github": "https://github.com/AviPama",
    },
    {
        "title": "Blockchain-Based Product Tracking System",
        "tech": "Python, Blockchain",
        "year": "2023",
        "description": "Built a command-line blockchain application demonstrating block creation, transaction recording, and Proof of Work.",
        "github": "https://github.com/AviPama",
    },
]


# ----------------------------------------------------------------------
# 4. ROUTES
# ----------------------------------------------------------------------

@app.route("/")
def home():
    """Home page: hero section with name, title, bio, and quick links."""
    return render_template("index.html", profile=PROFILE)


@app.route("/about")
def about():
    """About page: bio + education."""
    return render_template("about.html", profile=PROFILE, education=EDUCATION)


@app.route("/skills")
def skills():
    """Skills page: categorized skill lists."""
    return render_template("skills.html", profile=PROFILE, skills=SKILLS)


@app.route("/experience")
def experience():
    """Experience page: work/teaching timeline."""
    return render_template("experience.html", profile=PROFILE, experience=EXPERIENCE)


@app.route("/projects")
def projects():
    """Projects page: grid of project cards."""
    return render_template("projects.html", profile=PROFILE, projects=PROJECTS)


@app.route("/contact", methods=["GET", "POST"])
def contact():
    """
    Contact page.

    GET  -> just show the empty contact form
    POST -> validate the submitted form, save it to the database,
            then redirect back to the contact page with a success/error message.
    """
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        message = request.form.get("message", "").strip()

        # --- Basic server-side validation ---
        if not name or not email or not message:
            flash("Please fill in all fields before submitting.", "error")
            return redirect(url_for("contact"))

        if "@" not in email or "." not in email:
            flash("Please enter a valid email address.", "error")
            return redirect(url_for("contact"))

        # --- Save to database ---
        new_message = ContactMessage(name=name, email=email, message=message)
        db.session.add(new_message)
        db.session.commit()

        # --- Optional: send yourself an email notification ---
        # Uncomment and configure the function below once you've set up
        # an app password for your email account. See README for instructions.
        # send_email_notification(name, email, message)

        flash("Thanks for reaching out! Your message has been received.", "success")
        return redirect(url_for("contact"))

    return render_template("contact.html", profile=PROFILE)


# ----------------------------------------------------------------------
# 5. OPTIONAL: EMAIL NOTIFICATION (using Python's built-in smtplib)
# ----------------------------------------------------------------------
def send_email_notification(name, email, message):
    """
    Sends an email to yourself whenever someone submits the contact form.
    Disabled by default — uncomment the call in the /contact route above
    to enable it, and fill in your own email credentials via environment
    variables (never hardcode passwords in code!).
    """
    import smtplib
    from email.message import EmailMessage

    sender_email = os.environ.get("MAIL_USERNAME")
    sender_password = os.environ.get("MAIL_PASSWORD")
    receiver_email = PROFILE["email"]

    if not sender_email or not sender_password:
        # Email isn't configured — silently skip instead of crashing the app.
        return

    msg = EmailMessage()
    msg["Subject"] = f"New portfolio contact from {name}"
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg.set_content(f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}")

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(sender_email, sender_password)
        smtp.send_message(msg)


# ----------------------------------------------------------------------
# 6. ENTRY POINT (for local development only — production uses wsgi.py)
# ----------------------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)
