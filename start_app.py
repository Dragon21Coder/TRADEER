#!/usr/bin/env python3
"""
Simple launcher for SUDNAXI Trading Platform
Perfect for PyCharm and other IDEs
"""
import subprocess
import sys
import os

def main():
    """Launch the Streamlit app"""
    print("🚀 Starting SUDNAXI Trading Platform...")
    print("📊 Your professional trading intelligence system")
    print("=" * 50)
    
    # Change to the script directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    try:
        # Launch Streamlit
        print("🌐 Opening your browser...")
        print("📍 App will be available at: http://localhost:8501")
        print("🔄 Press Ctrl+C to stop the server")
        print("=" * 50)
        
        subprocess.run([
            sys.executable, '-m', 'streamlit', 'run', 'app.py',
            '--server.port=8501',
            '--server.address=localhost'
        ])
        
    except KeyboardInterrupt:
        print("\n👋 Shutting down SUDNAXI Trading Platform...")
        print("💡 Thanks for using SUDNAXI!")
        
    except FileNotFoundError:
        print("❌ Error: Streamlit not found!")
        print("💡 Install it with: pip install streamlit")
        print("💡 Or run: pip install -r production_requirements.txt")
        
    except Exception as e:
        print(f"❌ Error starting app: {e}")
        print("💡 Make sure you're in the right directory")
        print("💡 Try: pip install -r production_requirements.txt")

if __name__ == "__main__":
    main()