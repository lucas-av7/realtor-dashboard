from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def home():
    return 'home'

if __name__ == '__main__':
    app.secret_key=os.environ.get("SECRET_KEY")
    app.run(debug=os.environ.get("FLASK_DEBUG"))