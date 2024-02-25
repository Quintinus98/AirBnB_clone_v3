#!/usr/bin/python3
from flask import Flask
from models import storage
from api.v1.views import app_views

app = Flask(__name__)
app.url_map.strict_slashes = False

app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_storage():
    """Teardown storage"""
    storage.close()


if __name__ == "__main__":
    app.run('0.0.0.0', 5000, threaded=True, debug=True)
