import sqlite3
from datetime import datetime
from typing import Literal
import streamlit as st
from pydantic import BaseModel
import streamlit_pydantic as sp

con = sqlite3.connect("todoapp.sqlite", isolation_level=None)
cur = con.cursor()

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY,
        name TEXT,
        description TEXT,
        state TEXT,
        created_at DATETIME,
        created_by TEXT,
        category TEXT
    )
    """
)

class Task(BaseModel):
    name: str
    description: str
    state: Literal["in progress", "done"]
    created_by: str
    category: str

def toggle_state(state, row):
    con = sqlite3.connect("todoapp.sqlite", isolation_level=None)
    cur = con.cursor()
    new_state = 'in progress' if state else 'done'
    cur.execute(
        """
        UPDATE tasks SET state = ? WHERE id = ?
        """,
        (new_state, row[0]),
    )


def main():
    st.title("Todo App")
    data = sp.pydantic_form(key="task_form", model=Task)
    if data:
        # Automatically set the current timestamp for created_at
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cur.execute(
            """
            INSERT INTO tasks (name, description, state, created_at, created_by, category)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (data.name, data.description, data.state, current_time, data.created_by, data.category),
        )

    data = cur.execute(
        """
        SELECT * FROM tasks
        """
    ).fetchall()

    cols = st.columns(6)
    cols[0].write("State")
    cols[1].write("Name")
    cols[2].write("Description")
    cols[3].write("Created By")
    cols[4].write("Created At")
    cols[5].write("Category")

    for row in data:
        cols = st.columns(6)
        state_checkbox = cols[0].checkbox('state', row[3] == 'done', label_visibility='hidden', key=row[0], on_change=toggle_state, args=('done' if row[3] != 'done' else 'in-progress', row))
        cols[0].write(row[3] if not state_checkbox else ('done' if row[3] != 'done' else 'in progress'))
        cols[1].write(row[1])
        cols[2].write(row[2])
        cols[3].write(row[5])
        cols[4].write(row[4])
        cols[5].write(row[6])


main()
