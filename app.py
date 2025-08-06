from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

# Vulnerable to XSS
@app.route('/greet/<name>')
def greet(name):
    return f'Hello, {name}!'  # unsanitized user input rendered directly in HTML

# Vulnerable to command injection (very dangerous)
@app.route('/ping')
def ping():
    ip = request.args.get('ip')
    import os
    response = os.popen(f"ping -c 1 {ip}").read()  # No input validation!
    return f"<pre>{response}</pre>"

# Vulnerable to server-side template injection (SSTI)
@app.route('/template')
def template():
    user_input = request.args.get('name', '')
    return app.jinja_env.from_string(f"Hello {{ {user_input} }}").render()
    # Allows template expressions like {{ 7*7 }} or worse

if __name__ == '__main__':
    app.run(debug=True)
