Setup and Usage Instructions

This project is a FastAPI-based User microservice using PostgreSQL, Alembic migrations, and Swagger integration.
It follows a monorepo structure with shared packages: unnoti_corestore and unnoti_dbforge.
The following steps describe how to set up, run, and debug the application on Windows.

PREREQUISITES

Python 3.9+ : Verify with → python --version

PostgreSQL : Host=localhost, Port=5432, User=postgres, Password=admin22, Database=unnoti_dev

Virtualenv : For isolated dependencies

Git (optional) : For version control

PROJECT STRUCTURE

Parent/
├── Core/
│ ├── unnoti_corestore/ → Shared utilities, DB connection, generic repository
│ └── unnoti_dbforge/ → Alembic-based migration engine
└── Services/
└── user_api/ → FastAPI microservice with Swagger integration

CREATE AND ACTIVATE VIRTUAL ENVIRONMENT

cd D:\VAF\API\Services\user_api
python -m venv venv
D:\VAF\API\Services\user_api\venv\Scripts\activate

Note: Ensure "(venv)" is visible in your prompt before continuing.

INSTALL DEPENDENCIES

pip install --upgrade pip
pip install -e ../../Core/unnoti_corestore
pip install -e ../../Core/unnoti_dbforge
pip install fastapi uvicorn sqlalchemy alembic psycopg2-binary python-dotenv pydantic

Verify installation:
pip list
(Ensure unnoti-corestore and unnoti-dbforge are listed.)

CONFIGURE POSTGRESQL

Create Database:
psql -U postgres -c "CREATE DATABASE unnoti_dev;"

Test Connection:
psql -U postgres -h localhost -p 5432 -d unnoti_dev

If authentication fails, reset password:
ALTER USER postgres WITH PASSWORD 'admin22';

Update pg_hba.conf (located in PostgreSQL data folder):
host all all 127.0.0.1/32 md5
host all all ::1/128 md5

Restart PostgreSQL service:
net stop postgresql-x64-15
net start postgresql-x64-15

CONFIGURE ENVIRONMENT

Create file: D:\VAF\API\Services\user_api.env

DATABASE_URL=postgresql://postgres:admin22@localhost:5432/unnoti_dev
APP_ENV=dev
LOG_LEVEL=DEBUG

Verify environment variables:
python -c "from unnoti_corestore.utils.config_loader import Config; print(Config.DATABASE_URL)"
Expected Output: postgresql://postgres:admin22@localhost:5432/unnoti_dev

RUN DATABASE MIGRATIONS

python -c "from unnoti_dbforge.migration_runner import run_migrations; run_migrations()"

Verify:
psql -U postgres -h localhost -p 5432 -d unnoti_dev -c "\d users"

START FASTAPI SERVER

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

Access Swagger UI:
http://localhost:8000/docs

TEST API ENDPOINTS

Create a user:
curl -X POST "http://localhost:8000/users/
" -H "Content-Type: application/json" -d "{"username":"testuser","email":"test@example.com
","password":"hashedpass"}"

List users:
curl -X GET "http://localhost:8000/users/
"

DEBUGGING AND TROUBLESHOOTING

VIRTUAL ENVIRONMENT ISSUES:

If dependencies fail, recreate environment:
rd /s /q venv
python -m venv venv
D:\VAF\API\Services\user_api\venv\Scripts\activate
pip install -e ../../Core/unnoti_corestore
pip install -e ../../Core/unnoti_dbforge
pip install fastapi uvicorn sqlalchemy alembic psycopg2-binary python-dotenv pydantic

DATABASE CONNECTION ISSUES:

Test connectivity:
python -c "import psycopg2; conn = psycopg2.connect('dbname=unnoti_dev user=postgres password=admin22 host=localhost port=5432'); print('Connected')"

Check if PostgreSQL is listening:
netstat -a -n | find "5432"

If IPv6 (::1) causes issues, use IPv4:
DATABASE_URL=postgresql://postgres:admin22@127.0.0.1:5432/unnoti_dev

MIGRATION ISSUES:

Run manually if auto fails:
cd D:\VAF\API\Core\unnoti_dbforge
alembic upgrade head

Check alembic.ini for correct sqlalchemy.url

VS CODE DEBUGGING:
Create file: D:\VAF\API\Services\user_api.vscode\launch.json
{
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

COMMON ERRORS AND FIXES

Error: ModuleNotFoundError: No module named 'unnoti_dbforge'
Fix: pip install -e ../../Core/unnoti_dbforge

Error: KeyError: 'formatters'
Fix: Ensure alembic.ini has logging config or comment out fileConfig in env.py

Error: psycopg2.OperationalError (password authentication failed)
Fix: ALTER USER postgres WITH PASSWORD 'admin22'

Error: Connection refused
Fix: Verify PostgreSQL service using → net start postgresql-x64-15

ADDITIONAL NOTES

Swagger UI available at http://localhost:8000/docs

Use strong passwords in production (not admin22)

Set LOG_LEVEL=DEBUG only for development

Use venv\Scripts\activate instead of 'source' on Windows