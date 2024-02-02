# TECHIN 510 Lab 3
## Overview
This is a todo list app that using Python for Data storage and retrieval.It has already been deployed on Azure: https://510todoapp.azurewebsites.net/

## how to run
first, use command to install the package list in reqirement

```bash
pip install -r requirements.txt
```

To run the streamliit app use the following command:

```bash
streamlit run app.py
```


## Lessons learned
- How does the SQLite database work in this app?
  - The app uses SQLite, a lightweight relational database, to store and manage the todo tasks. It creates a table named tasks to store information.
- What does the toggle_state function do?
  - The toggle_state function is responsible for toggling the state of a task between "planned" and "done" when the user interacts with the checkbox. It updates the state column in the database for the specified task.
- How does the app handle task deletion?
  - There is "Delete" button for each task. When user clicks the button, it triggers the delete_task function, which removes the selected task from the SQLite database.

## Future improvements

Some potential improvements could include adding user authentication, improving the visual design, implementing task due dates, Add Task Reminders and Notifications functions send emails or messages to users when task is due, and enhancing the filtering options.