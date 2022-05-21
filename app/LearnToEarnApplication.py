from flask import Flask, jsonify, request
from flask_cors import CORS
from src.database import DB
from src.routes.route import Routes

app = Flask(__name__)
app.register_blueprint(Routes.getBlueprint())
CORS(app)
DB()

if __name__ == "__main__":
    app.run()
