#!/usr/bin/env python3
"""
Production launcher for the SUDNAXI Trading Platform
"""
import os
import sys
import subprocess
from pathlib import Path

def setup_environment():
    """Set up the production environment"""
    # Add current directory to Python path
    current_dir = Path(__file__).parent
    sys.path.insert(0, str(current_dir))
    
    # Create .env file if it doesn't exist
    env_file = current_dir / '.env'
    env_example = current_dir / '.env.example'
    
    if not env_file.exists() and env_example.exists():
        print("Creating .env file from .env.example...")
        env_file.write_text(env_example.read_text())
        print("Please edit .env file with your configuration before running again.")
        return False
    
    return True

def install_dependencies():
    """Install required dependencies"""
    requirements_file = Path(__file__).parent / 'production_requirements.txt'
    
    if requirements_file.exists():
        print("Installing dependencies...")
        subprocess.run([
            sys.executable, '-m', 'pip', 'install', '-r', str(requirements_file)
        ], check=True)
    else:
        print("Warning: production_requirements.txt not found")

def run_app():
    """Run the Streamlit application"""
    print("Starting SUDNAXI Trading Platform...")
    
    # Set Streamlit configuration
    os.environ['STREAMLIT_SERVER_PORT'] = '8501'
    os.environ['STREAMLIT_SERVER_ADDRESS'] = '0.0.0.0'
    os.environ['STREAMLIT_SERVER_HEADLESS'] = 'true'
    
    # Run the app
    subprocess.run([
        sys.executable, '-m', 'streamlit', 'run', 'app.py',
        '--server.port=8501',
        '--server.address=0.0.0.0',
        '--server.headless=true'
    ])

def main():
    """Main function"""
    print("SUDNAXI Trading Platform - Production Setup")
    print("=" * 50)
    
    if not setup_environment():
        sys.exit(1)
    
    try:
        install_dependencies()
        run_app()
    except KeyboardInterrupt:
        print("\nShutting down gracefully...")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()