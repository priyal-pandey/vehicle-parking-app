from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

import config
import models
import routes as routes


if __name__ == "__main__":
    app.run(debug=True)