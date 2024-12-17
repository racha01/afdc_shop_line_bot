
from flask import Flask, session
from itsdangerous import URLSafeTimedSerializer
    
import os

def create_app(config_class="config.LineConfig"):
    app = Flask(__name__)
    
    # # app.secret_key = 'REPLACE ME - this value is here as a placeholder.'
    
    app.config.from_object(config_class)
    
    app.config['SECRET_KEY'] = 'REPLACE ME - this value is here as a placeholder.'
    

    from app.routes.line_route import line_route_bp
    from app.routes.oauth_route import oauth_bp
    from app.routes.post_exchage_route import post_exchange_bp
    app.register_blueprint(oauth_bp)
    app.register_blueprint(line_route_bp)
    app.register_blueprint(post_exchange_bp)

    return app