from flask import Flask
from flask_bcrypt import Bcrypt


app = Flask('app')
bcrypt = Bcrypt(app)
