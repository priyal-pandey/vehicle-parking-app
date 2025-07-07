from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

import config
import routes

if __name__ == "__main__":
    app.run(debug=True)