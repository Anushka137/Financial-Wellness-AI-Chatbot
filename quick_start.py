#!/usr/bin/env python3
"""
Quick Start Script for Financial Wellness AI Chatbot
Automates the setup and launch process
"""

import os
import sys
import subprocess
import asyncio
import time
from pathlib import Path

def run_command(command, description, check=True):
    """Run a shell command with error handling"""
    print(f"\n{description}...")
    try:
        result = subprocess.run(command, shell=True, check=check, capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        if e.stderr:
            print(f"Details: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 or higher is required")
        print(f"Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} is compatible")
    return True

def install_dependencies():
    """Install required dependencies"""
    print("\n📦 Installing dependencies...")
    
    # Install server dependencies
    if not run_command("pip install -r requirements.txt", "Installing server dependencies"):
        return False
    
    # Install client dependencies
    if not run_command("cd client && pip install -r requirements.txt", "Installing client dependencies"):
        return False
    
    print("✅ Dependencies installed successfully")
    return True

def setup_configuration():
    """Set up configuration if needed"""
    config_file = Path("config.json")
    
    if config_file.exists():
        print("✅ Configuration file already exists")
        return True
    
    print("\n⚙️  Setting up configuration...")
    print("You'll need to provide your Google Gemini API key.")
    print("Get one for free at: https://aistudio.google.com/")
    
    # Create basic config
    config_content = {
        "GOOGLE_API_KEY": "your-gemini-api-key-here",
        "API_KEY": "your-api-key-here",
        "API_URL": "http://localhost:8000"
    }
    
    with open(config_file, 'w') as f:
        import json
        json.dump(config_content, f, indent=2)
    
    print("✅ Configuration file created")
    print("⚠️  Please edit config.json with your actual API keys")
    return True

def start_server():
    """Start the API server"""
    print("\n🚀 Starting API server...")
    
    # Check if server is already running
    try:
        import httpx
        import asyncio
        
        async def check_server():
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.get("http://localhost:8000/", timeout=2)
                    return response.status_code == 200
            except:
                return False
        
        if asyncio.run(check_server()):
            print("✅ Server is already running")
            return True
    except:
        pass
    
    # Start server in background
    try:
        # Use subprocess.Popen to run server in background
        server_process = subprocess.Popen(
            [sys.executable, "api_server.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Wait a moment for server to start
        time.sleep(3)
        
        # Check if server started successfully
        if server_process.poll() is None:
            print("✅ Server started successfully")
            return True
        else:
            print("❌ Server failed to start")
            return False
            
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        return False

def test_system():
    """Run system tests"""
    print("\n🧪 Testing system...")
    
    if not run_command(f"{sys.executable} test_system.py", "Running system tests", check=False):
        print("⚠️  Some tests failed, but the system may still work")
        return True
    
    return True

def launch_client():
    """Launch the interactive client"""
    print("\n💬 Launching interactive client...")
    print("You can now chat with your financial wellness assistant!")
    print("Type 'help' for available commands, 'exit' to quit")
    print("-" * 50)
    
    try:
        subprocess.run([sys.executable, "client/universal_client.py"], check=True)
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Error launching client: {e}")

def main():
    """Main quick start function"""
    print("🎯 Financial Wellness AI Chatbot - Quick Start")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        return
    
    # Install dependencies
    if not install_dependencies():
        print("❌ Failed to install dependencies")
        return
    
    # Setup configuration
    if not setup_configuration():
        print("❌ Failed to setup configuration")
        return
    
    # Start server
    if not start_server():
        print("❌ Failed to start server")
        print("You can try starting it manually with: python api_server.py")
        return
    
    # Test system
    test_system()
    
    # Launch client
    launch_client()

if __name__ == "__main__":
    main() 