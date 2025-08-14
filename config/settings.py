"""
Global configuration settings for the LangChain Pinecone application
"""

import os
from typing import Dict, Any

# Default configuration values
DEFAULT_CONFIG = {
    # Server settings
    'DEFAULT_HOST': '127.0.0.1',
    'DEFAULT_PORT': 5000,
    
    # Vector database settings
    'DEFAULT_CHUNK_SIZE': 1000,
    'DEFAULT_CHUNK_OVERLAP': 200,
    'DEFAULT_SEARCH_RESULTS': 5,
    
    # File processing settings
    'MAX_FILE_SIZE_MB': 16,
    'SUPPORTED_EXTENSIONS': ['.pdf', '.txt', '.docx', '.xlsx'],
    
    # API settings
    'DEFAULT_TIMEOUT': 30,
    'MAX_RETRIES': 3,
}

def get_config() -> Dict[str, Any]:
    """Get merged configuration from defaults and environment variables"""
    
    config = DEFAULT_CONFIG.copy()
    
    # Override with environment variables if present
    env_mappings = {
        'FLASK_HOST': 'DEFAULT_HOST',
        'FLASK_PORT': 'DEFAULT_PORT',
        'CHUNK_SIZE': 'DEFAULT_CHUNK_SIZE',
        'CHUNK_OVERLAP': 'DEFAULT_CHUNK_OVERLAP',
        'MAX_FILE_SIZE': 'MAX_FILE_SIZE_MB',
        'API_TIMEOUT': 'DEFAULT_TIMEOUT',
    }
    
    for env_var, config_key in env_mappings.items():
        env_value = os.environ.get(env_var)
        if env_value:
            # Convert to appropriate type
            if config_key in ['DEFAULT_PORT', 'DEFAULT_CHUNK_SIZE', 'DEFAULT_CHUNK_OVERLAP', 
                             'MAX_FILE_SIZE_MB', 'DEFAULT_TIMEOUT', 'MAX_RETRIES']:
                try:
                    config[config_key] = int(env_value)
                except ValueError:
                    pass  # Keep default value
            else:
                config[config_key] = env_value
    
    return config

def validate_environment() -> Dict[str, str]:
    """Validate that required environment variables are set"""
    
    required_vars = [
        'PINECONE_API_KEY',
        'OPENAI_API_KEY',
    ]
    
    optional_vars = [
        'PINECONE_ENVIRONMENT',
        'PINECONE_INDEX_NAME',
    ]
    
    issues = {}
    
    # Check required variables
    for var in required_vars:
        if not os.environ.get(var):
            issues[var] = 'Required environment variable not set'
    
    # Check optional variables (warnings only)
    for var in optional_vars:
        if not os.environ.get(var):
            issues[var] = f'Optional environment variable not set (using default)'
    
    return issues

def print_config_status():
    """Print current configuration status"""
    
    print("Configuration Status:")
    print("=" * 50)
    
    config = get_config()
    for key, value in config.items():
        print(f"{key}: {value}")
    
    print("\nEnvironment Variables:")
    print("=" * 50)
    
    issues = validate_environment()
    for var, status in issues.items():
        env_value = os.environ.get(var, 'Not set')
        status_icon = "✅" if "Required" not in status else "❌"
        print(f"{status_icon} {var}: {env_value}")
        if "Required" in status:
            print(f"   └─ {status}")

if __name__ == "__main__":
    print_config_status()
