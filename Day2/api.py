from flask import Flask, request, jsonify
import sqlite3
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "secret-key"
app.config['SECRET_KEY'] = 'your-secret-key'

jwt = JWTManager(app)

def get_db_connection():
    conn = sqlite3.connect('todos.db')
    conn.row_factory = sqlite3.Row  
    return conn

@app.route('/register',methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    hashed_password = generate_password_hash(password)
    conn = get_db_connection()
    cursor = conn.cursor()
    if not username or not email or not password:
        return jsonify({"error":"field is empty"}),400
    
    cursor.execute("SELECT * FROM users WHERE username = ? OR email = ?",(username,email))
    existing_user = cursor.fetchone()
    if existing_user:
        conn.close()
        return jsonify({"error":"User already exists"}),409
    
    cursor.execute("INSERT INTO users (username,email,hashed_password) VALUES (?,?,?)",(username,email,hashed_password))
    conn.commit()
    conn.close()
    return jsonify({"message":"User registered"}),201


@app.route('/login',methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?",(username,))
    user = cursor.fetchone()
    conn.close()

    if user and check_password_hash(user['hashed_password'],password):
        access_token = create_access_token(identity=user['id'])
        return jsonify({"message": "Login successful", "access_token": access_token}), 200
    return jsonify({'error':'Invalid credentials'}),401
    

# Route to add a new task (Create)
@app.route('/tasks', methods=['POST'])
@jwt_required() # now only authenticated users can access this functioin
def add_task():
    current_user = get_jwt_identity()
    data = request.get_json()
    task = data.get('task')
    print(data)
    status = data.get('status', 'Pending')

    if not task:
        return jsonify({'error': 'Task description is required'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO todos (task, status, user_id) VALUES (?, ?, ?)", (task, status, current_user))
    conn.commit()
    task_id = cursor.lastrowid
    conn.close()

    return jsonify({'id': task_id, 'task': task, 'status': status}), 201

# Route to delete a task by ID (Delete)
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
@jwt_required()
def delete_task(task_id):
    current_user = get_jwt_identity()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM todos WHERE id = ? AND user_id = ?", (task_id,current_user))
    conn.commit()
    conn.close()

    if cursor.rowcount == 0:  # cursor.rowcount will return no. of rows changed so we can use it to know if the row is deleted or not
        return jsonify({'error': 'Task not found'}), 404

    return jsonify({'message': 'Task deleted'}), 200

# Route to update a task by ID (Update)
@app.route('/tasks/<int:task_id>', methods=['PUT'])
@jwt_required()
def update_task(task_id):
    current_user = get_jwt_identity()
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
        WHERE id = ? AND user_id = ?
    """, (task, status, task_id,current_user))
    conn.commit()
    conn.close()

    if cursor.rowcount == 0:
        return jsonify({'error': 'Task not found'}), 404

    return jsonify({'message': 'Task updated'}), 200

if __name__ == '__main__':
    app.run(debug=True)
