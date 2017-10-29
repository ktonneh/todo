import os

WTF_CSRF_ENABLED = True
SECRET_KEY = 'm^@H2w;PLSZuc=dnDAaH3F@`KPU8BiGkPoirPBKU[TdcXOTd;biXviJXKo@Ov]:2'

basedir = os.path.abspath(os.path.dirname(__file__))

# SQLALCHEMY_DATABASE_URI = 'sqlite:////'+os.path.join(basedir,'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
# SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:smartcode@localhost/flask_microblog'
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root@localhost/python_flask_todo'

