from flask import Flask

def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)

    with app.app_context():
        # Import and register the Blueprint
        from .routes import main
        app.register_blueprint(main)

    return app
