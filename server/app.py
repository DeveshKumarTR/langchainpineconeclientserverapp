from flask import Flask, jsonify
from flask.cli import with_appcontext
import click
import os
import sys

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from server.config import config
from server.routes import documents_bp, search_bp

def create_app(config_name=None):
    """Application factory pattern"""
    
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')
    
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Register blueprints
    app.register_blueprint(documents_bp, url_prefix='/api')
    app.register_blueprint(search_bp, url_prefix='/api')
    
    # Register CLI commands
    app.cli.add_command(init_db_command)
    
    # Health check endpoint
    @app.route('/health')
    def health_check():
        return jsonify({
            'status': 'healthy',
            'service': 'langchain-pinecone-server'
        })
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Not found'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'error': 'Internal server error'}), 500
    
    return app

@click.command()
@with_appcontext
def init_db_command():
    """Initialize the Pinecone index."""
    from server.models.vector_store import VectorStoreManager
    
    try:
        manager = VectorStoreManager()
        manager.init_index()
        click.echo('Initialized Pinecone index successfully.')
    except Exception as e:
        click.echo(f'Error initializing Pinecone index: {str(e)}')

if __name__ == '__main__':
    app = create_app()
    app.run(
        host=app.config['HOST'],
        port=app.config['PORT'],
        debug=app.config['DEBUG']
    )
