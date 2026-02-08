from flask import Flask
from config import Config
from models import db
from routes import main
import os


def create_app(config_class=Config):
    """Application factory pattern"""
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions
    db.init_app(app)
    
    # Register blueprints
    app.register_blueprint(main)
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app


if __name__ == '__main__':
    app = create_app()
    
    print("=" * 60)
    print(" NoteMaster AI-V1 is starting...")
    print("=" * 60)
    
    # Check API key
    if app.config['GEMINI_API_KEY']:
        print("The Gemini API Key has been detected")
        print("Program is now running.")
        print("The program is now taking off motherfuckers! HAHAHAHA")
    else:
        print("Web app is not utilizing proper API key configuration, make sure to check and properly diagnose the issue.")
        print("Program is not running. Please make sure to check the config or routes files.")
        
    print("=" * 60)
    print("Open your browser and go to: http://127.0.0.1:5000")
    print("=" * 60)
    print()
    
    app.run(debug=True, host='0.0.0.0', port=5000)
