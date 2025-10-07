"""Initial users table and stored procedures"""
from alembic import op

revision = '0001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        username VARCHAR(100) NOT NULL UNIQUE,
        email VARCHAR(255) NOT NULL UNIQUE,
        password_hash VARCHAR(255) NOT NULL,
        is_active BOOLEAN DEFAULT TRUE,
        created_at TIMESTAMP DEFAULT NOW(),
        updated_at TIMESTAMP DEFAULT NOW()
    );
    """)
    op.execute("""
    CREATE OR REPLACE FUNCTION sp_get_users()
    RETURNS TABLE(id INT, username TEXT, email TEXT) AS $$  
    BEGIN
        RETURN QUERY SELECT id, username, email FROM users WHERE is_active = TRUE;
    END;
      $$ LANGUAGE plpgsql;
    """)
    op.execute("""
    CREATE OR REPLACE FUNCTION sp_create_user(p_username TEXT, p_email TEXT, p_password TEXT)
    RETURNS INT AS $$  
    DECLARE new_id INT;
    BEGIN
        INSERT INTO users (username, email, password_hash)
        VALUES (p_username, p_email, p_password)
        RETURNING id INTO new_id;
        RETURN new_id;
    END;
      $$ LANGUAGE plpgsql;
    """)

def downgrade():
    op.execute("DROP FUNCTION IF EXISTS sp_create_user(TEXT, TEXT, TEXT);")
    op.execute("DROP FUNCTION IF EXISTS sp_get_users();")
    op.execute("DROP TABLE IF EXISTS users;")