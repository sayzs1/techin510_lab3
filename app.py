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
    state: Literal["planned", "in progress"]
    created_by: str
    category: str

def toggle_state(row):
    con = sqlite3.connect("todoapp.sqlite", isolation_level=None)
    cur = con.cursor()
    new_state = "done" if row[3] != "done" else "planned"
    cur.execute(
        """
        UPDATE tasks SET state = ? WHERE id = ?
        """,
        (new_state, row[0]),
    )

def delete_task(row):
    con = sqlite3.connect("todoapp.sqlite", isolation_level=None)
    cur = con.cursor()
    cur.execute(
        """
        DELETE FROM tasks WHERE id = ?
        """,
        (row[0],),
    )

def main():
    st.title("Todo App")

    # Search Bar
    search_query = st.text_input("Search Task Names:")

    # Filter Dropdown
    selected_category = st.selectbox("Filter by Category:", ["All"] + cur.execute("SELECT DISTINCT category FROM tasks").fetchall())

    data = sp.pydantic_form(key="task_form", model=Task)
    if data:
        # Ensure the correct state value is retrieved
        state_value = 'in progress' if data.state == 'planned' else 'planned'
        # Automatically set the current timestamp for created_at
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cur.execute(
            """
            INSERT INTO tasks (name, description, state, created_at, created_by, category)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (data.name, data.description, state_value, current_time, data.created_by, data.category),
        )

    # Fetch and filter data
    query = """
        SELECT * FROM tasks
        WHERE (name LIKE ?) AND (? = 'All' OR category = ?)
    """
    # Ensure selected_category is a string
    selected_category_str = selected_category[0] if selected_category != "All" else "All"
    data = cur.execute(query, (f"%{search_query}%", selected_category_str, selected_category_str)).fetchall()

    cols = st.columns(7)
    cols[0].write("State")
    cols[1].write("Name")
    cols[2].write("Description")
    cols[3].write("Created By")
    cols[4].write("Created At")
    cols[5].write("Category")
    cols[6].write("Actions")

    for row in data:
        cols = st.columns(7)
        # Check if the state is 'done'
        is_done = row[3] == 'done'
        # Checkbox to toggle state
        state_checkbox = cols[0].checkbox('state', is_done, label_visibility='hidden', key=f"state_{row[0]}", on_change=toggle_state, args=(row,))
        # Set state based on checkbox
        new_state = 'done' if is_done else 'in progress' if row[3] == 'planned' else 'planned'
        cols[0].write(new_state)
        cols[1].write(row[1])
        cols[2].write(row[2])
        cols[3].write(row[5])
        cols[4].write(row[4])
        cols[5].write(row[6])

        # Delete button with unique key
        delete_key = f"delete_{row[0]}"
        if cols[6].button("Delete", key=delete_key):
            delete_task(row)

main()