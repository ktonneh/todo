from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')

##app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:smartcode@localhost/flask_microblog'
##app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/flask_microblog'
db = SQLAlchemy(app)

from app import views, models