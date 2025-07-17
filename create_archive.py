#!/usr/bin/env python3
"""
Create downloadable archive of SUDNAXI Trading Platform
"""
import os
import shutil
import zipfile
from pathlib import Path

def create_production_archive():
    """Create a production-ready archive"""
    
    # Files to include in the archive
    files_to_include = [
        'app.py',
        'config.py',
        'run_production.py',
        'setup.py',
        'production_requirements.txt',
        '.env.example',
        'README.md',
        'download_instructions.md',
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
        '.streamlit/config.toml'
    ]
    
    # Create archive
    archive_name = 'sudnaxi-trading-platform.zip'
    
    with zipfile.ZipFile(archive_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file_path in files_to_include:
            if os.path.exists(file_path):
                # Add file to archive with proper directory structure
                zipf.write(file_path, f'sudnaxi-trading/{file_path}')
                print(f"Added: {file_path}")
            else:
                print(f"Warning: {file_path} not found")
    
    print(f"\n✓ Archive created: {archive_name}")
    print(f"✓ Size: {os.path.getsize(archive_name) / 1024 / 1024:.2f} MB")
    return archive_name

def create_file_list():
    """Create a comprehensive file list"""
    
    file_list = """# SUDNAXI Trading Platform - Complete File List

## Core Application Files
- app.py (Main Streamlit application)
- config.py (Configuration settings)  
- run_production.py (Production launcher)
- setup.py (Automated setup script)
- production_requirements.txt (Python dependencies)
- .env.example (Environment template)
- README.md (Complete documentation)

## Database Module
- database/models.py (Database models and setup)

## Utility Modules  
- utils/data_fetcher.py (Stock data retrieval)
- utils/chart_generator.py (Chart visualization)
- utils/news_sentiment.py (News analysis)
- utils/backtesting_engine.py (Strategy testing)
- utils/enhanced_backtesting.py (Advanced backtesting)
- utils/real_time_learning.py (ML adaptation)
- utils/help_system.py (Help and tooltips)

## Machine Learning
- ml/adaptive_strategy.py (ML trading strategies)
- ml/reinforcement_learning.py (RL components)

## Configuration
- .streamlit/config.toml (Streamlit settings)

## Deployment
- Dockerfile (Docker configuration)
- docker-compose.yml (Docker Compose setup)

## Total Files: 18 core files + documentation
## Complete, production-ready trading platform
"""
    
    with open('file_list.txt', 'w') as f:
        f.write(file_list)
    
    print("✓ File list created: file_list.txt")

if __name__ == "__main__":
    print("Creating SUDNAXI Trading Platform Archive")
    print("=" * 50)
    
    create_file_list()
    archive_name = create_production_archive()
    
    print("\n" + "=" * 50)
    print("DOWNLOAD READY!")
    print(f"Archive: {archive_name}")
    print("Complete production-ready trading platform")
    print("No Replit dependencies - runs anywhere!")