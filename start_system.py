#!/usr/bin/env python3
"""
Temperature Monitoring System Startup Script
Launches both the simulation server and UI server with easy management.
"""

import os
import sys
import time
import subprocess
import threading
from pathlib import Path
from dotenv import load_dotenv

def print_banner():
    """Print the system banner."""
    print("=" * 70)
    print("🌡️  Raspberry Pi Temperature Monitoring System")
    print("=" * 70)
    print("🚀 Starting both simulation server and UI server...")
    print("=" * 70)

def check_env_file():
    """Check if .env file exists and has required values."""
    env_file = Path(".env")
    if not env_file.exists():
        print("❌ .env file not found!")
        print("📝 Create a .env file with your configuration values")
        print("💡 Copy .env.example to .env and update the values")
        return False
    
    # Load environment variables
    load_dotenv()
    
    # Check for required environment variables
    required_vars = [
        "USER_ID",
        "LOCAL_SENSOR_IP", 
        "THINGSPEAK_WRITE_API_KEY",
        "THINGSPEAK_READ_API_KEY",
        "THINGSPEAK_CHANNEL_ID"
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var) or os.getenv(var).startswith("YOUR_"):
            missing_vars.append(var)
    
    if missing_vars:
        print("⚠️  Some environment variables are not configured:")
        for var in missing_vars:
            print(f"   - {var}")
        print("📝 Update your .env file with actual values")
        return False
    
    print("✅ .env file configured properly")
    return True

def check_dependencies():
    """Check if required Python packages are installed."""
    required_packages = ['flask', 'flask_cors', 'requests', 'python_dotenv']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ Missing required packages: {', '.join(missing_packages)}")
        print("📦 Install them using: pip install -r requirements.txt")
        return False
    
    print("✅ All required packages are installed")
    return True

def start_simulation_server():
    """Start the simulation server in a separate thread."""
    try:
        print("🌡️  Starting simulation server on port 5000...")
        # Change to simulation directory and run server
        simulation_dir = Path("simulation")
        if simulation_dir.exists():
            subprocess.run([sys.executable, "sensor_server.py"], 
                         cwd=simulation_dir, check=True)
        else:
            print("❌ Simulation directory not found")
    except subprocess.CalledProcessError as e:
        print(f"❌ Simulation server failed to start: {e}")
    except KeyboardInterrupt:
        print("⏹️  Simulation server stopped by user")

def start_ui_server():
    """Start the UI server in a separate thread."""
    try:
        print("🖥️  Starting UI server on port 5001...")
        # Change to UI directory and run server
        ui_dir = Path("UI")
        if ui_dir.exists():
            subprocess.run([sys.executable, "ui_server.py"], 
                         cwd=ui_dir, check=True)
        else:
            print("❌ UI directory not found")
    except subprocess.CalledProcessError as e:
        print(f"❌ UI server failed to start: {e}")
    except KeyboardInterrupt:
        print("⏹️  UI server stopped by user")

def main():
    """Main startup function."""
    print_banner()
    
    # Check .env file first
    if not check_env_file():
        print("\n📋 Configuration Steps:")
        print("1. Copy .env.example to .env")
        print("2. Update .env with your actual values:")
        print("   - ThingSpeak API keys")
        print("   - Channel ID")
        print("   - Local IP address")
        print("3. Run this script again")
        sys.exit(1)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Check if required directories and files exist
    simulation_dir = Path("simulation")
    ui_dir = Path("UI")
    
    if not simulation_dir.exists():
        print("❌ Simulation directory not found")
        print("📁 Expected: simulation/")
        sys.exit(1)
    
    if not ui_dir.exists():
        print("❌ UI directory not found")
        print("📁 Expected: UI/")
        sys.exit(1)
    
    # Check for required files in each directory
    simulation_files = ["sensor_server.py", "requirements.txt"]
    ui_files = ["ui_server.py", "requirements.txt"]
    
    for file in simulation_files:
        if not (simulation_dir / file).exists():
            print(f"❌ Required file not found: simulation/{file}")
            sys.exit(1)
    
    for file in ui_files:
        if not (ui_dir / file).exists():
            print(f"❌ Required file not found: UI/{file}")
            sys.exit(1)
    
    print("✅ All required directories and files found")
    
    # Start both servers
    print("\n🚀 Launching servers...")
    print("📱 Simulation Dashboard: http://<raspberry_pi_ip>:5000")
    print("🖥️  UI Dashboard: http://localhost:5001")
    print("\n💡 Press Ctrl+C to stop both servers")
    print("=" * 70)
    
    try:
        # Start simulation server in background thread
        simulation_thread = threading.Thread(target=start_simulation_server, daemon=True)
        simulation_thread.start()
        
        # Start UI server in main thread
        start_ui_server()
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Shutting down temperature monitoring system...")
        print("👋 Goodbye!")
        sys.exit(0)

if __name__ == "__main__":
    main()
