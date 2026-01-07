import psycopg2

def get_db():
    # !!! IMPORTANT: Replace with your actual PostgreSQL connection details !!!
    return psycopg2.connect(
        host="localhost",
        database="your_db",
        user="your_user",
        password="your_password"
    )

create_table_sql = """
CREATE TABLE goal_progress_history (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    goal_id INT NOT NULL,
    previous_amount NUMERIC(12,2),
    new_amount NUMERIC(12,2),
    change_amount NUMERIC(12,2),
    source VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_goal
        FOREIGN KEY (goal_id) REFERENCES goals(id) ON DELETE CASCADE,

    CONSTRAINT fk_user
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
"""

conn = None
cur = None
try:
    conn = get_db()
    cur = conn.cursor()
    cur.execute(create_table_sql)
    conn.commit()
    print("Table 'goal_progress_history' created successfully.")
except psycopg2.Error as e:
    print(f"Error creating table: {e}")
finally:
    if cur:
        cur.close()
    if conn:
        conn.close()