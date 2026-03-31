from flask import Flask, render_template, request

app = Flask(__name__)

# Home page
@app.route('/')
def home():
    return render_template('index.html')

# Form submit
@app.route('/submit', methods=['POST'])
def submit():
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')

    print("New Contact:")
    print("Name:", name)
    print("Email:", email)
    print("Message:", message)

    return "<h2>Form submitted successfully!</h2><a href='/'>Go Back</a>"

# Run app
if __name__ == '__main__':
    app.run(debug=True)