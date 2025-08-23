"""
WSGI entry point for the Flask application.
This file is used by WSGI servers like Gunicorn for deployment.
"""

from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run()
