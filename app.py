import flask
from flask import jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from models.constants import ENVIRONMENT
from config import app_config
from views.auth import auth
from views.payments import payment



app = flask.Flask(__name__)
CORS(app)

app.config.from_object(app_config[ENVIRONMENT])
jwt = JWTManager(app)

app.register_blueprint(auth)
app.register_blueprint(payment)

### swagger specific ###
### end swagger specific ###

@app.route('/', methods=['GET'])
def home():
    return '''<h1>Kari Hotel | v2</h1>
            <p>Accomodation at ts best.</p>'''


@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404

@app.errorhandler(400)
def bad_request(e):
    return jsonify(error=str(e.description)), 400

if __name__ == "__main__":
    app.run()
