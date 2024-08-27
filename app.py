from flask import Flask, jsonify, request, render_template, redirect, url_for
from recommendation import recommend_connections

app = Flask(__name__)

# Simulated user data
users = {'testuser': {'password': 'password123', 'role': 'student'}}

# Endpoint to get user details
@app.route('/api/users/<username>', methods=['GET'])
def get_user(username):
    user = users.get(username)
    if user:
        return jsonify({'username': username, 'role': user['role']}), 200
    return jsonify({'error': 'User not found'}), 404

# Endpoint to create a new user
@app.route('/api/users', methods=['POST'])
def create_user():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    role = data.get('role', 'student')

    if username in users:
        return jsonify({'error': 'User already exists'}), 400

    users[username] = {'password': password, 'role': role}
    return jsonify({'message': 'User created successfully'}), 201

# Endpoint to update user details
@app.route('/api/users/<username>', methods=['PUT'])
def update_user(username):
    if username not in users:
        return jsonify({'error': 'User not found'}), 404

    data = request.json
    users[username].update(data)
    return jsonify({'message': 'User updated successfully'}), 200

# Endpoint to delete a user
@app.route('/api/users/<username>', methods=['DELETE'])
def delete_user(username):
    if username in users:
        del users[username]
        return jsonify({'message': 'User deleted successfully'}), 200
    return jsonify({'error': 'User not found'}), 404

# Endpoint to get recommendations
@app.route('/api/recommendations/<username>', methods=['GET'])
def get_recommendations(username):
    recommendations = recommend_connections(username)
    if 'error' in recommendations:
        return jsonify(recommendations), 404
    return jsonify(recommendations), 200

# Existing routes...
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = users.get(username)
        if user and user['password'] == password:
            return redirect(url_for('dashboard', username=username))
        else:
            return "Invalid credentials, try again.", 401
    return render_template('login.html')

@app.route('/dashboard/<username>')
def dashboard(username):
    return render_template('dashboard.html', user={'username': username})

@app.route('/logout')
def logout():
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
