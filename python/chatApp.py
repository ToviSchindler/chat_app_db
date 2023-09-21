from flask import Flask, render_template, request, redirect, session, jsonify
import csv
import os
import base64
import mysql.connector
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Set a secret key for session management
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"


# Retrieve the room files path from environment variable
room_files_path = os.getenv('ROOM_FILES_PATH')
users_path = os.getenv('USERS_PATH')
#room_files_path = "rooms/"
print(room_files_path)


# Helper functions for user authentication
def encode_password(password):
    encoded_bytes = base64.b64encode(password.encode('utf-8'))
    return encoded_bytes.decode('utf-8')

 
def decode_password(encoded_password):
    decoded_bytes = base64.b64decode(encoded_password.encode('utf-8'))
    return decoded_bytes.decode('utf-8')


def check_user_credentials(username, password):
    with open(users_path, 'r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == username and decode_password(row[1]) == password:
                return True
    return False

def is_exist(user):
    cursor.execute("select * from users where UserName={user.username} and password={user.password}")
    data = cursor.fetchall()
    if data:
        return True
    return False

# Routes
@app.route('/')
def logOut():
    try:
        connection = mysql.connector.connect(
            user='root',
            password='root',
            host='mysql-db',
            port=3306,
            database='chat_app_db'
        )
        cursor = connection.cursor()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users")
        data = cursor.fetchall()
        # Process the retrieved data
        return "Data: " + str(data)
    except mysql.connector.Error as err:
        return f"Error: {err}"


@app.route('/register', methods=['GET', 'POST'])
def register():
    user = {
    'username': request.form['username'],
    'password': request.form['password']
    } 
    if(is_exist(user)):
        return redirect('/login')

    # if request.method == 'POST':
    #     username = request.form['username']
    #     password = request.form['password']
    #     encoded_password = encode_password(password)
        
    #     # Save user details to the CSV file
    #     with open(users_path, 'a', newline='') as file:
    #         writer = csv.writer(file)
    #         writer.writerow([username, encoded_password])
        
    #     return redirect('/login')
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if check_user_credentials(username, password):
            session['username'] = username
            return redirect('/lobby')
        else:
            return "Invalid credentials. Please try again."
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/login')


@app.route('/lobby', methods=['GET', 'POST'])
def lobby():
    if 'username' in session:
        if request.method == 'POST':
            room_name = request.form['new_room']
            try:
                with open(f'{room_files_path}{room_name}.txt', 'x') as f:
                    f.write('')
            except FileNotFoundError:
                print("The given room name already exists")
            print("CREATED NEW ROOM NAMED: " + room_name )
        rooms = os.listdir(f'{room_files_path}')
        new_rooms = [x[:-4] for x in rooms]
        return render_template('lobby.html', rooms=new_rooms)  
    else:
        return redirect('/login')


@app.route('/chat/<room>', methods=['GET', 'POST'])
def chat(room):
    if 'username' in session:
        return render_template('chat.html', room=room)
    else:
        return redirect('/login')


@app.route('/api/chat/<room>', methods=['GET','POST'])
def update_chat(room):
    if request.method == 'POST':
        message = request.form['msg']
        username = session['username']

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Append the message to the room's unique .txt file
        with open(f'{room_files_path}{room}.txt', 'a', newline='') as file:
            file.write(f'[{timestamp}] {username}: {message}\n')           
    with open(f'{room_files_path}{room}.txt', 'r' ) as file:
        file.seek(0)
        messages = file.read()
    
    
    #return [session['username'],messages.split('\n')]
    return str([session['username'], str(messages.split('\n'))])


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)