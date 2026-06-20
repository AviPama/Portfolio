"""
wsgi.py
-------
Entry point used by production WSGI servers (waitress, gunicorn, etc.)
Local development should use `python app.py` instead, which runs Flask's
built-in dev server with auto-reload and debug mode.

Example production run:
    waitress-serve --port=8080 wsgi:app
"""

from app import app

if __name__ == "__main__":
    app.run()
