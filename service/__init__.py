from flask import Flask

app = Flask(__name__)

# Import the routes after the Flask app is created
from service import routes, models