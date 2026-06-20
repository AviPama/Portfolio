# Avneet Pama — Personal Portfolio (Flask)

A personal portfolio website built with Flask, Jinja2, and SQLite,
featuring a light/dark theme toggle and a working contact form.

## Project Structure
```
portfolio/
├── app.py                  # Main Flask app: routes, data, contact form logic
├── wsgi.py                 # Production entry point (waitress/gunicorn)
├── requirements.txt
├── Dockerfile
├── templates/               # Jinja2 HTML templates
│   ├── base.html
│   ├── index.html
│   ├── about.html
│   ├── skills.html
│   ├── experience.html
│   ├── projects.html
│   └── contact.html
└── static/
    ├── css/style.css
    ├── js/main.js
    ├── images/             
    └── files/               
```

## 1. Setup (local development)

```bash
# Clone / unzip the project, then cd into it
cd portfolio

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## 2. Set up the database

```bash
export FLASK_APP=app.py         # Windows (cmd): set FLASK_APP=app.py
flask db init
flask db migrate -m "initial migration"
flask db upgrade
```
This creates `portfolio.db` (SQLite) and a `migrations/` folder.

## 3. Run the app locally

```bash
python app.py
```
Visit **http://127.0.0.1:5000** in your browser.

## 4. Add your photo

Drop a photo named `profile.jpg` into `static/images/`. If it's missing,
the homepage will show a placeholder image instead of breaking.


## 5. Email notifications on contact form

By default, contact form messages are saved to the database only.

   ```


## Notes for beginners
- Every route in `app.py` is documented with comments explaining what it does.
- All your personal content (bio, skills, experience, projects) lives in Python
  dictionaries/lists near the top of `app.py` — edit those directly to update
  your site, no HTML editing required.
- The contact form validates input server-side and stores submissions in the
  `ContactMessage` table — you can view them anytime with a small script or
  a SQLite browser tool like [DB Browser for SQLite](https://sqlitebrowser.org/).
