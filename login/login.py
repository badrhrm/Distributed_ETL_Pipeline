from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        # Add authentication logic here
        if email == "admin@example.com" and password == "admin":
            return "Logged in successfully!"
        else:
            return "Invalid credentials!"
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
