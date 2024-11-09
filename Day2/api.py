from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

#  function to connect to the database
def get_db_connection():
    conn = sqlite3.connect('todos.db')
    conn.row_factory = sqlite3.Row  # This enables dict-like row access
    return conn

# Route to add a new task (Create)
@app.route('/tasks', methods=['POST'])
def add_task():
    data = request.get_json()
    task = data.get('task')
    status = data.get('status', 'Pending')

    if not task:
        return jsonify({'error': 'Task description is required'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO todos (task, status) VALUES (?, ?)", (task, status))
    conn.commit()
    task_id = cursor.lastrowid
    conn.close()

    return jsonify({'id': task_id, 'task': task, 'status': status}), 201

# Route to delete a task by ID (Delete)
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM todos WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()

    if cursor.rowcount == 0:  # cursor.rowcount will return no. of rows changed so we can use it to know if the row is deleted or not
        return jsonify({'error': 'Task not found'}), 404

    return jsonify({'message': 'Task deleted'}), 200

# Route to update a task by ID (Update)
@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.get_json()
    task = data.get('task')
    status = data.get('status')

    if not task and not status:
        return jsonify({'error': 'No update data provided'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE todos
        SET task = COALESCE(?, task), status = COALESCE(?, status)
        WHERE id = ?
    """, (task, status, task_id))
    conn.commit()
    conn.close()

    if cursor.rowcount == 0:
        return jsonify({'error': 'Task not found'}), 404

    return jsonify({'message': 'Task updated'}), 200

if __name__ == '__main__':
    app.run(debug=True)
