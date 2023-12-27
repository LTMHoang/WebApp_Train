from flask import Flask
from urllib.parse import quote
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import cloudinary

app = Flask(__name__)

app.secret_key = "14124512B3JKB12IBTIB3214TNY23KLBJ4TB3JKT3B4TUB3T43%%#%^46%$#^#$%@$%2"
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:%s@localhost/train_webapp?charset=utf8mb4" % quote('Admin@123')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["PAGE_SIZE"] = 1

db = SQLAlchemy(app=app)
login = LoginManager(app=app)

cloudinary.config(
    cloud_name="dvsnl4nsh",
    api_key="672181655553596",
    api_secret="4ve100xmuA2kUAOvcmfWC9xSM1c"
)