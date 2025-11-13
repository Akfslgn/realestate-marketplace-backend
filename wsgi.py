"""
WSGI entry point for the Flask application.
This file is used by WSGI servers like Gunicorn for deployment.
"""

from app import create_app
import os

print(f"Creating Flask app with FLASK_ENV: {os.getenv('FLASK_ENV')}")
app = create_app()
print(f"Flask app created successfully. Available routes:")
for rule in app.url_map.iter_rules():
    if '/health' in rule.rule or '/ping' in rule.rule or '/seed' in rule.rule:
        print(f"  {rule.rule} [{list(rule.methods)}]")

if __name__ == "__main__":
    app.run()
