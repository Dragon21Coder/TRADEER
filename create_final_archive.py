#!/usr/bin/env python3
"""
Create final production archive for SUDNAXI Trading Platform
"""
import os
import zipfile
from pathlib import Path

def create_final_archive():
    """Create the final production-ready archive"""
    
    # Essential files for production
    essential_files = [
        'app.py',
        'start_app.py',
        'config.py',
        'constants.py',
        'version.py',
        'setup.py',
        'production_requirements.txt',
        '.env.example',
        'README.md',
        'Dockerfile',
        'docker-compose.yml',
        'database/models.py',
        'ml/adaptive_strategy.py',
        'ml/reinforcement_learning.py',
        'utils/data_fetcher.py',
        'utils/chart_generator.py',
        'utils/news_sentiment.py',
        'utils/backtesting_engine.py',
        'utils/enhanced_backtesting.py',
        'utils/real_time_learning.py',
        'utils/help_system.py',
        'core/__init__.py',
        'core/config.py',
        '.streamlit/config.toml'
    ]
    
    # Create optimized archive
    archive_name = 'SUDNAXI-Trading-Platform-v1.0.zip'
    
    with zipfile.ZipFile(archive_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file_path in essential_files:
            if os.path.exists(file_path):
                zipf.write(file_path, f'SUDNAXI-Trading-Platform/{file_path}')
                print(f"✓ Added: {file_path}")
            else:
                print(f"⚠ Missing: {file_path}")
    
    file_size = os.path.getsize(archive_name) / 1024
    print(f"\n✅ Production archive created: {archive_name}")
    print(f"📦 Size: {file_size:.1f} KB")
    print(f"🎯 Files included: {len(essential_files)}")
    
    return archive_name

if __name__ == "__main__":
    print("Creating SUDNAXI Trading Platform - Final Production Archive")
    print("=" * 60)
    create_final_archive()
    print("=" * 60)
    print("🚀 Ready for deployment anywhere!")
    print("💻 Compatible with PyCharm, VS Code, and all Python IDEs")
    print("🔧 No external dependencies beyond Python packages")