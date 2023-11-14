from flask import Flask
from flask_cors import CORS


app = Flask(__name__,static_folder='utils/em',static_url_path='/em')
app.json.ensure_ascii = False # 解决中文乱码问题
CORS(app)