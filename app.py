from flask import Flask, request, jsonify, redirect, url_for, session, render_template
from flask_cors import CORS
from views import auth_views
from models.auth import login_required

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.register_blueprint(auth_views, url_prefix='/auth')
cors = CORS(app, resources={r"/*": {"origins": "*"}})

# Custom error handler for 403 Forbidden
@app.errorhandler(403)
def forbidden_error(error):
    return jsonify({'error': 'Access to the requested resource is restricted.'}), 403

if __name__ == '__main__':
    app.run(debug=True)
