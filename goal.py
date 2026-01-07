from fastapi import FastAPI, HTTPException
import psycopg2
from psycopg2.extras import RealDictCursor

app = FastAPI()

def get_db():
    return psycopg2.connect(
        host="localhost",
        database="your_db",
        user="your_user",
        password="your_password"
    )

# -------------------------------
# UPDATE GOAL PROGRESS
# -------------------------------
@app.put("/goals/{goal_id}/progress")
def update_goal_progress(goal_id: int, user_id: int, new_amount: float):
    conn = get_db()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    # Get current amount
    cur.execute(
        "SELECT current_amount FROM goals WHERE id=%s AND user_id=%s",
        (goal_id, user_id)
    )
    goal = cur.fetchone()

    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")

    previous_amount = goal["current_amount"]
    change_amount = new_amount - previous_amount

    # Update goal
    cur.execute(
        "UPDATE goals SET current_amount=%s WHERE id=%s AND user_id=%s",
        (new_amount, goal_id, user_id)
    )

    # Insert history
    cur.execute("""
        INSERT INTO goal_progress_history
        (user_id, goal_id, previous_amount, new_amount, change_amount, source)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (
        user_id,
        goal_id,
        previous_amount,
        new_amount,
        change_amount,
        "manual_update"
    ))

    conn.commit()
    cur.close()
    conn.close()

    return {"message": "Goal progress updated successfully"}

# -------------------------------
# FETCH PROGRESS HISTORY
# -------------------------------
@app.get("/goals/{goal_id}/progress-history")
def get_progress_history(goal_id: int, user_id: int):
    conn = get_db()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    cur.execute("""
        SELECT previous_amount, new_amount, change_amount, created_at
        FROM goal_progress_history
        WHERE goal_id=%s AND user_id=%s
        ORDER BY created_at DESC
    """, (goal_id, user_id))

    history = cur.fetchall()
    cur.close()
    conn.close()

    return history
