import cloudinary
from flask import Flask
from flask_admin import Admin
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.secret_key = 'ASDL@#@!(#&*(&&(^()*^!@#%^D*&^()!@#$!@MADAGASCANS'
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://root:H29012003@localhost/SaleAppV1db?charset=utf8mb4"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['PAGE_SIZE'] = 4

db = SQLAlchemy(app=app)

admin = Admin(app=app, name='E-commerce Administration', template_mode='bootstrap4')

cloudinary.config(
    cloud_name="dtthwldgs",
    api_key="295661242477252",
    api_secret="xKPY2fG-4h1mtZl2_PRvxsSfgtA"
)

login = LoginManager(app=app)
