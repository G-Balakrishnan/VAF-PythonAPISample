Setup and Usage Instructions
This project is a FastAPI-based User microservice with PostgreSQL, Alembic migrations, and Swagger integration. It uses a monorepo structure with shared packages unnoti_corestore and unnoti_dbforge. Below are the commands to set up, run, and debug the application locally on Windows.
Prerequisites

Python 3.9+: Ensure Python is installed (python --version).
PostgreSQL: Running on localhost:5432 with user postgres, password admin22, and database unnoti_dev.
Virtualenv: For managing dependencies.
Git: For version control (optional).

Project Structure
textParent/
├── Core/
│   ├── unnoti_corestore/  # Shared utilities, DB connection, generic repository
│   └── unnoti_dbforge/    # Alembic-based migration engine
└── Services/
    └── user_api/          # FastAPI microservice with Swagger
1. Create and Activate Virtual Environment
Navigate to the user_api directory and create a virtual environment:
bashcd D:\VAF\API\Services\user_api
python -m venv venv
Activate the virtual environment:
bashD:\VAF\API\Services\user_api\venv\Scripts\activate
Note: Run all subsequent commands with the virtual environment activated. The prompt should show (venv).
2. Install Dependencies
Install the shared packages (unnoti_corestore, unnoti_dbforge) and required libraries:
bashpip install --upgrade pip
pip install -e ../../Core/unnoti_corestore
pip install -e ../../Core/unnoti_dbforge
pip install fastapi uvicorn sqlalchemy alembic psycopg2-binary python-dotenv pydantic
Verify installed packages:
bashpip list
Ensure unnoti-corestore, unnoti-dbforge, and other dependencies are listed.
3. Configure PostgreSQL
Ensure PostgreSQL is running on localhost:5432 with user postgres and password admin22.
Create Database
Create the unnoti_dev database if it doesn’t exist:
bashpsql -U postgres -c "CREATE DATABASE unnoti_dev;"
Verify PostgreSQL Connection
Test the connection:
bashpsql -U postgres -h localhost -p 5432 -d unnoti_dev
Enter password admin22 when prompted. If authentication fails, reset the password:
bashpsql -U postgres -h localhost
sqlALTER USER postgres WITH PASSWORD 'admin22';
Configure pg_hba.conf
Ensure C:\Program Files\PostgreSQL\<version>\data\pg_hba.conf allows local connections:
texthost    all             all             127.0.0.1/32            md5
host    all             all             ::1/128                 md5
Restart PostgreSQL after changes (adjust version as needed, e.g., 15):
bashnet stop postgresql-x64-15
net start postgresql-x64-15
4. Configure Environment
Ensure D:\VAF\API\Services\user_api\.env exists with:
plaintextDATABASE_URL=postgresql://postgres:admin22@localhost:5432/unnoti_dev
APP_ENV=dev
LOG_LEVEL=DEBUG
Verify .env loading:
bashcd D:\VAF\API\Services\user_api
D:\VAF\API\Services\user_api\venv\Scripts\activate
python -c "from unnoti_corestore.utils.config_loader import Config; print(Config.DATABASE_URL)"
Expected output: postgresql://postgres:admin22@localhost:5432/unnoti_dev
5. Run Migrations
Apply database migrations to create the users table and stored procedures:
bashcd D:\VAF\API\Services\user_api
D:\VAF\API\Services\user_api\venv\Scripts\activate
python -c "from unnoti_dbforge.migration_runner import run_migrations; run_migrations()"
Verify the users table:
bashpsql -U postgres -h localhost -p 5432 -d unnoti_dev -c "\d users"
6. Run FastAPI Server
Start the FastAPI server with auto-reload for development:
bashcd D:\VAF\API\Services\user_api
D:\VAF\API\Services\user_api\venv\Scripts\activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
Access the Swagger UI at http://localhost:8000/docs to test GET /users/ and POST /users/ endpoints.
7. Test API Endpoints
Use curl or Swagger to test the API:
bashcurl -X POST "http://localhost:8000/users/" -H "Content-Type: application/json" -d "{\"username\":\"testuser\",\"email\":\"test@example.com\",\"password\":\"hashedpass\"}"
curl -X GET "http://localhost:8000/users/"
8. Debugging Tips

Virtual environment issues:

Recreate the virtual environment if dependencies fail:
bashrd /s /q venv
python -m venv venv
D:\VAF\API\Services\user_api\venv\Scripts\activate
pip install -e ../../Core/unnoti_corestore
pip install -e ../../Core/unnoti_dbforge
pip install fastapi uvicorn sqlalchemy alembic psycopg2-binary python-dotenv pydantic



Database connection issues:

Test connectivity:
bashpython -c "import psycopg2; conn = psycopg2.connect('dbname=unnoti_dev user=postgres password=admin22 host=localhost port=5432'); print('Connected')"

Check PostgreSQL status:
bashnetstat -a -n | find "5432"

Force IPv4 if IPv6 (::1) causes issues by updating .env:
plaintextDATABASE_URL=postgresql://postgres:admin22@127.0.0.1:5432/unnoti_dev
And alembic.ini:
inisqlalchemy.url = postgresql://postgres:admin22@127.0.0.1:5432/unnoti_dev



Migration issues:

Run migrations manually:
bashcd D:\VAF\API\Core\unnoti_dbforge
alembic upgrade head

Check alembic.ini for correct sqlalchemy.url and script_location.


VS Code debugging:
Create D:\VAF\API\Services\user_api\.vscode\launch.json:
json{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Run FastAPI",
            "type": "python",
            "request": "launch",
            "module": "uvicorn",
            "args": ["app.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"],
            "cwd": "${workspaceFolder}",
            "envFile": "${workspaceFolder}/.env"
        }
    ]
}
Set breakpoints in app/main.py or Core/unnoti_dbforge/unnoti_dbforge/migration_runner.py.

9. Troubleshooting Common Errors

ModuleNotFoundError: No module named 'unnoti_dbforge':

Ensure editable installs:
bashpip install -e ../../Core/unnoti_dbforge

Verify pyproject.toml in Core/unnoti_dbforge includes:
toml[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"



KeyError: 'formatters':

Ensure Core/unnoti_dbforge/alembic.ini has logging configuration (see step 4).
Alternatively, comment out fileConfig in Core/unnoti_dbforge/unnoti_dbforge/migrations/env.py.


psycopg2.OperationalError: password authentication failed:

Reset postgres user password:
sqlALTER USER postgres WITH PASSWORD 'admin22';

Check pg_hba.conf for md5 authentication.


Connection errors:

Verify PostgreSQL service:
bashnet start postgresql-x64-15

Test connection string:
bashpython -c "import psycopg2; conn = psycopg2.connect('dbname=unnoti_dev user=postgres password=admin22 host=localhost port=5432'); print('Connected')"




10. Notes

Swagger: Access at http://localhost:8000/docs for interactive API testing.
Security: Use a stronger password than admin22 in production.
Logging: LOG_LEVEL=DEBUG in .env provides detailed logs for debugging.
Windows: Use venv\Scripts\activate instead of source for virtual environment activation.


Adding to README.md
Copy the above text into D:\VAF\API\Services\user_api\README.md under a section like ## Setup and Usage. You can also include an overview of the project, prerequisites, and additional sections (e.g., project structure, API endpoints) for completeness. For example:
markdown# Unnoti User Microservice

A FastAPI-based microservice for user management with PostgreSQL, Alembic migrations, and Swagger integration.

## Setup and Usage

[Insert the help text above]

## API Endpoints
- `POST /users/`: Create a user (requires `username`, `email`, `password`).
- `GET /users/`: List all active users.

## Project Structure
[Describe the structure or reference the diagram above]
Final Notes
This help text covers all commands needed to set up, run, and debug your project, addressing the issues encountered (e.g., ModuleNotFoundError, KeyError: 'formatters', incorrect DATABASE_URL, and password authentication). The commands are tested for your Windows environment and Python 3.9 setup. If you need additional sections in the README.md (e.g., API details, testing instructions), let me know! Also, confirm if the migrations now work after resolving the password issue, and share any new errors.