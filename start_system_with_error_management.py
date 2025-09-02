#!/usr/bin/env python3
"""
Temperature Monitoring System Startup Script with Error Management
Launches all servers with integrated error detection, correction code display, and server pause/resume functionality.
When errors are detected, the terminal shows only the error correction code and pauses other servers.
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
    print("=" * 80)
    print("🌡️  Temperature Monitoring System with Error Management")
    print("🛡️  AI-Powered Error Detection & Auto-Correction")
    print("=" * 80)
    print("🚀 Starting all servers with integrated error management...")
    print("=" * 80)

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
    required_packages = {
        'flask': 'flask',
        'flask_cors': 'flask_cors', 
        'requests': 'requests',
        'python_dotenv': 'dotenv',
        'google_generativeai': 'google.generativeai'
    }
    missing_packages = []
    
    for package_name, import_name in required_packages.items():
        try:
            __import__(import_name)
        except ImportError:
            missing_packages.append(package_name)
    
    if missing_packages:
        print(f"❌ Missing required packages: {', '.join(missing_packages)}")
        print("📦 Install them using: pip install -r requirements.txt")
        return False
    
    print("✅ All required packages are installed")
    return True

def check_required_files():
    """Check if all required files exist."""
    required_files = [
        "error_manager.py",
        "terminal_error_interface.py",
        "ai_monitor.py",
        "simulation/sensor_server.py",
        "UI/ui_server.py",
        "ai_chat_server.py"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        print("❌ Missing required files:")
        for file_path in missing_files:
            print(f"   - {file_path}")
        return False
    
    print("✅ All required files found")
    return True

def start_error_management_system():
    """Start the error management system."""
    try:
        print("🛡️  Starting error management system...")
        
        # Import and start the terminal error interface
        from terminal_error_interface import TerminalErrorInterface
        
        interface = TerminalErrorInterface()
        
        # Start monitoring in a separate thread
        monitor_thread = threading.Thread(target=interface.start_monitoring, daemon=True)
        monitor_thread.start()
        
        print("✅ Error management system started")
        return interface
        
    except ImportError as e:
        print(f"❌ Failed to import error management system: {e}")
        return None
    except Exception as e:
        print(f"❌ Failed to start error management system: {e}")
        return None

def start_servers_with_error_management():
    """Start all servers using the error management system."""
    try:
        print("🚀 Starting servers with error management...")
        
        # Import error manager
        from error_manager import error_manager
        
        # Start all servers through error manager
        error_manager.start_all_servers()
        
        # Start monitoring
        monitor_thread = threading.Thread(target=error_manager.start_monitoring, daemon=True)
        monitor_thread.start()
        
        print("✅ All servers started with error management")
        return error_manager
        
    except ImportError as e:
        print(f"❌ Failed to import error manager: {e}")
        return None
    except Exception as e:
        print(f"❌ Failed to start servers with error management: {e}")
        return None

def start_traditional_servers():
    """Start servers using traditional method (fallback)."""
    print("⚠️  Using traditional server startup (error management not available)")
    
    def start_simulation_server():
        try:
            print("🌡️  Starting simulation server on port 5000...")
            simulation_dir = Path("simulation")
            if simulation_dir.exists():
                subprocess.run([sys.executable, "sensor_server.py"], 
                             cwd=simulation_dir, check=True)
        except subprocess.CalledProcessError as e:
            print(f"❌ Simulation server failed to start: {e}")
        except KeyboardInterrupt:
            print("⏹️  Simulation server stopped by user")

    def start_ui_server():
        try:
            print("🖥️  Starting UI server on port 5001...")
            ui_dir = Path("UI")
            if ui_dir.exists():
                subprocess.run([sys.executable, "ui_server.py"], 
                             cwd=ui_dir, check=True)
        except subprocess.CalledProcessError as e:
            print(f"❌ UI server failed to start: {e}")
        except KeyboardInterrupt:
            print("⏹️  UI server stopped by user")

    def start_ai_chat_server():
        try:
            print("🤖 Starting AI chat server on port 5002...")
            subprocess.run([sys.executable, "ai_chat_server.py"], 
                         cwd=Path("."), check=True)
        except subprocess.CalledProcessError as e:
            print(f"❌ AI chat server failed to start: {e}")
        except KeyboardInterrupt:
            print("⏹️  AI chat server stopped by user")

    # Start servers in separate threads
    simulation_thread = threading.Thread(target=start_simulation_server, daemon=True)
    simulation_thread.start()
    
    ai_chat_thread = threading.Thread(target=start_ai_chat_server, daemon=True)
    ai_chat_thread.start()
    
    # Start UI server in main thread
    start_ui_server()

def main():
    """Main startup function with error management."""
    print_banner()
    
    # Check .env file first
    if not check_env_file():
        print("\n📋 Configuration Steps:")
        print("1. Copy .env.example to .env")
        print("2. Update .env with your actual values:")
        print("   - ThingSpeak API keys")
        print("   - Channel ID")
        print("   - Local IP address")
        print("   - Gemini API key (for AI error correction)")
        print("3. Run this script again")
        sys.exit(1)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Check required files
    if not check_required_files():
        sys.exit(1)
    
    # Try to start with error management
    error_manager = start_servers_with_error_management()
    
    if error_manager:
        print("\n🎉 System started with full error management capabilities!")
        print("📱 Simulation Dashboard: http://<raspberry_pi_ip>:5000")
        print("🖥️  UI Dashboard: http://localhost:5001")
        print("🤖 AI Chat Dashboard: http://localhost:5002")
        print("\n🛡️  Error Management Features:")
        print("   - Automatic error detection")
        print("   - AI-generated correction code display")
        print("   - Server pause/resume on errors")
        print("   - Terminal-based error interface")
        print("\n💡 Press Ctrl+C to stop all servers")
        print("=" * 80)
        
        try:
            # Keep the main thread alive
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n\n⏹️  Shutting down system...")
            error_manager.server_manager.stop_all_servers()
            print("👋 Goodbye!")
            sys.exit(0)
    else:
        # Fallback to traditional startup
        print("\n⚠️  Error management not available, using traditional startup")
        print("📱 Simulation Dashboard: http://<raspberry_pi_ip>:5000")
        print("🖥️  UI Dashboard: http://localhost:5001")
        print("🤖 AI Chat Dashboard: http://localhost:5002")
        print("\n💡 Press Ctrl+C to stop all servers")
        print("=" * 80)
        
        try:
            start_traditional_servers()
        except KeyboardInterrupt:
            print("\n\n⏹️  Shutting down system...")
            print("👋 Goodbye!")
            sys.exit(0)

if __name__ == "__main__":
    main()
