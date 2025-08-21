import os
from app import create_app

if __name__ == "__main__":
    env = os.getenv("FLASK_ENV", "development")
    app = create_app(env)
    app.run(debug=(env == "development"))