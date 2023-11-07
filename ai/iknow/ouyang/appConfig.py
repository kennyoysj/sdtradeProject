from flask import Flask
from flask_cors import CORS


app = Flask(__name__,static_folder='utils/em',static_url_path='/em')
CORS(app)