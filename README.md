# Backend Development Template
### Tech Stack
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white)](https://www.sqlalchemy.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)

[![Flask-Admin](https://img.shields.io/badge/Flask_Admin-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask-admin.readthedocs.io/)
[![Pipenv](https://img.shields.io/badge/Pipenv-2C8EBB?style=for-the-badge&logo=pipenv&logoColor=white)](https://pipenv.pypa.io/)
[![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/)

This is a **template for Flask-based backend applications**. It provides a fast and efficient starting point for building modern RESTful APIs with a well-structured architecture, database integration, and administrative interface.

## Features
- 🚀 **Flask-powered**: Fast and lightweight framework for API development.
- 📦 **SQLAlchemy ORM**: Simple yet powerful database integration.
- 🔐 **Admin Panel**: Built-in admin interface for database management.

- 🛠️ **Clean Architecture**: Organized in services, repositories, and controllers.
- 🔄 **Database Migrations**: Easy database schema management with Flask-Migrate.
- 🔒 **CORS Support**: Cross-Origin Resource Sharing enabled for frontend integration.
- 🧪 **Testing Ready**: Configured for pytest integration.

## Architecture Overview

### Clean Architecture
- **Models:**  
  Data models defined in `app/models` using SQLAlchemy ORM.
  
- **Repositories:**  
  Data access layer in `app/repositories` handling all database operations.
  
- **Services:**  
  Business logic layer in `app/services` implementing application features.
  
- **Controllers:**  
  API endpoints and route handlers in `app/controllers`.



### Database Integration
- **SQLAlchemy:**  
  ORM for database operations with model definitions.
  
- **Flask-Migrate:**  
  Database migration tool based on Alembic.
  
- **PostgreSQL:**  
  Primary database, configurable through environment variables.

### Admin Interface
- **Flask-Admin:**  
  Administrative interface for database CRUD operations.
  
- **Model Views:**  
  Auto-generated views for all models.

## Getting Started

Follow these steps to set up and run the project:

### 1. Prerequisites
Ensure you have the following installed:
- Python 3.9 or higher
- PostgreSQL (or another database of your choice)
- Pipenv (for dependency management)

### 2. Clone the Repository
Clone the repository to your local machine:
```bash
git clone https://github.com/yourusername/flask-backend-template.git
cd flask-backend-template
```

### 3. Set Up Environment Variables
Create a `.env` file in the root directory based on the provided `.env.example`:
```bash
cp .env.example .env
```
Update the `.env` file with your database credentials and other configuration:
```
DATABASE_URL=postgresql+psycopg2://username:password@localhost:5432/dbname
SECRET_KEY=your-secret-key
CORS_ORIGINS=http://localhost:5173
```

### 4. Install Dependencies
Install all required dependencies using Pipenv:
```bash
pipenv install
```

For development dependencies, add the `--dev` flag:
```bash
pipenv install --dev
```

### 5. Initialize the Database
Set up the database with migrations:
```bash
pipenv run setup
pipenv run migrate
pipenv run upgrade
```

### 6. Start the Development Server
Run the development server:
```bash
pipenv run start
```
Or alternatively:
```bash
pipenv shell
flask run --debug --reload
```

### 7. Access the API
Once the server is running, access:
- API at: `http://localhost:5001/api/v1`
- Admin panel at: `http://localhost:5001/admin`
- Health check at: `http://localhost:5001/ping`

## Available Commands

The project includes several useful Pipenv commands defined in the `Pipfile`:

### `pipenv run start`
Starts the development server with debug and auto-reload.

### `pipenv run serve`
Runs the server on port 3000 (useful for production-like testing).

### `pipenv run setup`
Initializes the database.

### `pipenv run migrate`
Creates a new migration based on model changes.

### `pipenv run upgrade`
Applies migrations to the database.

### `pipenv run downgrade`
Reverts the last migration.

### `pipenv run resetdb`
Drops and recreates all database tables.

### `pipenv run test`
Runs the test suite.

### `pipenv run seed`
Seeds the database with sample data.

## Project Structure
```
├── app
│   ├── __init__.py          # Application factory
│   ├── admin.py             # Admin panel configuration
│   ├── config.py            # Configuration settings
│   ├── extensions.py        # Flask extensions
│   ├── error_handlers.py    # Global error handlers
│   ├── models               # Data models
│   │   ├── __init__.py
│   │   └── example.py       # Example model (User)
│   ├── controllers          # API route handlers
│   │   ├── __init__.py
│   │   └── example.py       # Example routes
│   ├── repositories         # Data access layer
│   │   ├── __init__.py
│   │   └── example.py       # Example repository
│   ├── services             # Business logic
│   │   ├── __init__.py
│   │   └── example.py       # Example service
│   └── utils                # Utility functions
│       └── __init__.py
├── migrations               # Database migrations
│   └── .gitkeep
├── .env.example             # Environment variables template
├── .flaskenv                # Flask configuration
├── .gitignore               # Git ignore file
├── LICENSE                  # License file
├── Pipfile                  # Dependencies definition
├── Pipfile.lock             # Locked dependencies
├── reset_db.py              # Database reset script
└── run.py                   # Application runner
```

## Customization

### Adding New Models
1. Create a new file in the `app/models` directory
2. Define your model class using SQLAlchemy
3. Import the model in `app/models/__init__.py`
4. Add model to admin panel in `app/admin.py`
5. Create migration with `pipenv run migrate`
6. Apply migration with `pipenv run upgrade`

### Creating New Endpoints
1. Create or modify files in `app/controllers` directory
2. Define routes using Flask's Blueprint
3. Register your Blueprint in `app/__init__.py`

### Implementing Business Logic
1. Create repositories in `app/repositories` for database operations
2. Implement service layer in `app/services` for business rules
3. Connect services to controllers 

### Database Configuration
1. Update `DATABASE_URL` in your `.env` file
2. For a different database engine, modify the SQLAlchemy URI and install the required driver

## Testing
The project is configured for testing with pytest. Write your tests in a `tests/` directory and run:
```bash
pipenv run test
```

## Deployment
For deployment, consider:
1. Setting `FLASK_ENV=production` in your environment
2. Using a WSGI server like Gunicorn
3. Setting up proper database credentials
4. Configuring proper CORS settings
5. Setting a strong SECRET_KEY

## Contributing
If you'd like to contribute to this template, feel free to fork the repository and submit a pull request.

## License
This project is licensed under the [MIT License](LICENSE).

---

This project has been created by **Dmytro Chobotar**.

Happy coding! 🎉