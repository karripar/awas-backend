from flask import Flask
from flask_cors import CORS
from database import init_db
from routes.auth import auth_bp
from routes.feed import feed_bp
from routes.admin import admin_bp

def create_app():
    """Application factory"""
    app = Flask(__name__)
    
    # Enable CORS
    CORS(app)
    
    # Initialize database
    init_db()
    
    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(feed_bp)
    app.register_blueprint(admin_bp)
    
    # Health check
    @app.route('/api/health', methods=['GET'])
    def health_check():
        from flask import jsonify
        return jsonify({'status': 'ok'}), 200
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='localhost', port=5000)
