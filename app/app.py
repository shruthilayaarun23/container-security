from flask import Flask, request, render_template_string, jsonify
import sqlite3
import os
import subprocess

app = Flask(__name__)

# Vulnerability 1: Hard-coded secret key
app.secret_key = "super-secret-key-123"

# Vulnerability 2: Debug mode enabled in production
app.config['DEBUG'] = True

# Initialize SQLite database 
def init_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            email TEXT
        )
    ''')
   
    cursor.execute("INSERT OR REPLACE INTO users (id, username, password, email) VALUES (1, 'admin', 'password123', 'admin@example.com')")
    cursor.execute("INSERT OR REPLACE INTO users (id, username, password, email) VALUES (2, 'user', 'user123', 'user@example.com')")
    conn.commit()
    conn.close()

@app.route('/')
def home():
    return '''
    <h1>Vulnerable Demo Application</h1>
    <p>This application contains intentional security vulnerabilities for testing purposes.</p>
    <ul>
        <li><a href="/login">Login (SQL Injection Test)</a></li>
        <li><a href="/search?q=test">Search (XSS Test)</a></li>
        <li><a href="/execute?cmd=ls">Command Execution (RCE Test)</a></li>
        <li><a href="/file?name=../../etc/passwd">File Access (Path Traversal Test)</a></li>
    </ul>
    '''

# Vulnerability 3: SQL Injection
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
    
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
        
        try:
            cursor.execute(query)
            user = cursor.fetchone()
            conn.close()
            
            if user:
                return f"<h2>Welcome {user[1]}!</h2><p>Login successful</p>"
            else:
                return "<h2>Login failed</h2><p>Invalid credentials</p>"
        except Exception as e:
            return f"<h2>Database Error:</h2><p>{str(e)}</p>"
    
    return '''
    <form method="post">
        <h2>Login</h2>
        <p>Username: <input type="text" name="username"></p>
        <p>Password: <input type="password" name="password"></p>
        <p><input type="submit" value="Login"></p>
        <p><small>Try: admin' OR '1'='1' -- as username</small></p>
    </form>
    '''

# Vulnerability 4: Cross-Site Scripting (XSS)
@app.route('/search')
def search():
    query = request.args.get('q', '')
    template = f'''
    <h2>Search Results</h2>
    <p>You searched for: {query}</p>
    <p>No results found.</p>
    <a href="/">Back to Home</a>
    '''
    return render_template_string(template)

# Vulnerability 5: Command Injection
@app.route('/execute')
def execute_command():
    cmd = request.args.get('cmd', 'whoami')
    try:
        result = subprocess.check_output(cmd, shell=True, text=True, timeout=5)
        return f"<h2>Command Output:</h2><pre>{result}</pre><a href='/'>Back</a>"
    except subprocess.TimeoutExpired:
        return "<h2>Command timed out</h2>"
    except Exception as e:
        return f"<h2>Error:</h2><p>{str(e)}</p>"

# Vulnerability 6: Path Traversal
@app.route('/file')
def read_file():
    filename = request.args.get('name', 'welcome.txt')
    try:
        with open(filename, 'r') as f:
            content = f.read()
        return f"<h2>File Content:</h2><pre>{content}</pre><a href='/'>Back</a>"
    except Exception as e:
        return f"<h2>Error reading file:</h2><p>{str(e)}</p>"

# Vulnerability 7: Information Disclosure
@app.route('/admin/config')
def show_config():
    config_info = {
        "database_path": "users.db",
        "secret_key": app.secret_key,
        "debug_mode": app.config['DEBUG'],
        "environment_vars": dict(os.environ)
    }
    return jsonify(config_info)

@app.route('/health')
def health_check():
    return jsonify({"status": "healthy", "version": "1.0.0"})

if __name__ == '__main__':
    init_db()
    # Vulnerability 8: Running on all interfaces with debug mode
    app.run(host='0.0.0.0', port=5000, debug=True)