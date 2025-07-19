#!/usr/bin/env python3
"""
Setup script for UW Directory Scraping and Email Automation Tool
"""

import os
import sys
import subprocess
import shutil

def print_banner():
    """Print the setup banner."""
    print("="*60)
    print("UW Directory Scraping and Email Automation Tool - Setup")
    print("="*60)

def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 7):
        print("❌ Python 3.7 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True

def install_dependencies():
    """Install required dependencies."""
    print("\n📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def setup_config():
    """Set up configuration file."""
    print("\n⚙️  Setting up configuration...")

    if os.path.exists('config.py'):
        response = input("Configuration file already exists. Overwrite? (y/N): ")
        if response.lower() != 'y':
            print("Skipping configuration setup")
            return True

    if not os.path.exists('config.example.py'):
        print("❌ config.example.py not found")
        return False

    try:
        shutil.copy('config.example.py', 'config.py')
        print("✅ Configuration file created")
        print("\n📝 Please edit config.py with your credentials:")
        print("   - UW_USERNAME: Your UW NetID (used for both directory and email)")
        print("   - UW_PASSWORD: Your UW password (used for both directory and email)")
        return True
    except Exception as e:
        print(f"❌ Failed to create configuration file: {e}")
        return False

def check_chromedriver():
    """Check if ChromeDriver is available."""
    print("\n🔍 Checking ChromeDriver...")
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options

        # Test if ChromeDriver works with simple setup
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        # This will test if ChromeDriver is available
        test_driver = webdriver.Chrome(options=chrome_options)
        test_driver.quit()

        print("✅ ChromeDriver is working correctly")
        return True
    except Exception as e:
        print(f"❌ ChromeDriver check failed: {e}")
        print("Please ensure ChromeDriver is installed and in your PATH")
        print("Download from: https://chromedriver.chromium.org/")
        return False

def create_directories():
    """Create necessary directories."""
    print("\n📁 Creating directories...")
    directories = ['logs', 'reports']

    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"✅ Created directory: {directory}")
        else:
            print(f"✅ Directory exists: {directory}")

    # Create a .gitkeep file in empty directories to ensure they're tracked by git
    for directory in directories:
        gitkeep_file = os.path.join(directory, '.gitkeep')
        if not os.path.exists(gitkeep_file):
            with open(gitkeep_file, 'w') as f:
                f.write('# This file ensures the directory is tracked by git\n')
            print(f"✅ Added .gitkeep to {directory}")

def show_next_steps():
    """Show next steps for the user."""
    print("\n" + "="*60)
    print("🎉 Setup completed successfully!")
    print("="*60)
    print("\nNext steps:")
    print("1. Edit config.py with your credentials")
    print("2. Run the tool: python main.py")
    print("3. Choose option 1 for complete workflow")
    print("\nFor help, see README.md")

def main():
    """Main setup function."""
    print_banner()

    # Check Python version
    if not check_python_version():
        return

    # Install dependencies
    if not install_dependencies():
        return

    # Setup configuration
    if not setup_config():
        return

    # Check ChromeDriver
    if not check_chromedriver():
        print("⚠️  ChromeDriver setup incomplete. You may need to install it manually.")

    # Create directories
    create_directories()

    # Show next steps
    show_next_steps()

if __name__ == "__main__":
    main()