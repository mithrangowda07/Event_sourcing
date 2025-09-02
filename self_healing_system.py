#!/usr/bin/env python3
"""
Self-Healing Temperature Monitoring System
A comprehensive system that automatically detects and fixes errors without shutting down.
"""

import os
import sys
import time
import subprocess
import threading
import re
import shutil
import tempfile
from pathlib import Path
from datetime import datetime
from typing import List, Optional, Tuple, Dict
from dotenv import load_dotenv

# Global variables for system monitoring
SYSTEM_RUNNING = True
MONITORING_ACTIVE = True
BACKUP_DIR = Path(".self_healing_backups")
PROJECT_ROOT = Path(__file__).resolve().parent

class AIClient:
    """AI client for Gemini integration."""
    
    def __init__(self, model: str = "auto") -> None:
        self.model = self._choose_model(model)
    
    def _choose_model(self, requested: str) -> str:
        if requested != "auto":
            return requested
        env_model = os.environ.get("AI_MODEL")
        if env_model:
            return env_model
        return os.environ.get("GEMINI_MODEL", "gemini-1.5-flash")
    
    def generate(self, prompt: str) -> str:
        return self._generate_with_gemini(prompt)
    
    def _generate_with_gemini(self, prompt: str) -> str:
        try:
            import google.generativeai as genai
        except Exception as exc:
            raise RuntimeError(
                "Gemini SDK not installed. Install with: pip install google-generativeai"
            ) from exc
        
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise RuntimeError("GEMINI_API_KEY not set in environment")
        
        genai.configure(api_key=api_key)
        model_name = self.model or "gemini-1.5-flash"
        
        try:
            model = genai.GenerativeModel(model_name)
            response = model.generate_content(prompt)
            text = getattr(response, "text", None) or ""
            if not text and getattr(response, "candidates", None):
                parts = []
                for c in response.candidates:
                    for p in getattr(c.content, "parts", []) or []:
                        parts.append(getattr(p, "text", ""))
                text = "\n".join([p for p in parts if p])
            return text.strip()
        except Exception as exc:
            raise RuntimeError(f"Gemini generation failed: {exc}") from exc

class SelfHealingMonitor:
    """Continuous monitoring and self-healing system."""
    
    def __init__(self):
        self.ai_client = None
        self.monitored_files = set()
        self.error_history = []
        self.fix_history = []
        self.last_check = time.time()
        
        # Initialize AI client
        try:
            self.ai_client = AIClient()
            print("🤖 AI Self-Healing Monitor initialized")
        except Exception as e:
            print(f"⚠️  AI client initialization failed: {e}")
            print("💡 Self-healing will be disabled. Set GEMINI_API_KEY to enable.")
    
    def find_all_python_files(self) -> List[Path]:
        """Find all Python files in the project."""
        python_files = []
        for root, dirs, files in os.walk(PROJECT_ROOT):
            # Skip hidden directories and common non-source directories
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in {
                '__pycache__', 'node_modules', 'venv', 'env', 'self_healing_backups'
            }]
            
            for file in files:
                if file.endswith('.py'):
                    python_files.append(Path(root) / file)
        
        return python_files
    
    def check_file_syntax(self, file_path: Path) -> Tuple[bool, str]:
        """Check if a Python file has syntax errors."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Try to compile the file
            compile(content, str(file_path), 'exec')
            return True, ""
        except SyntaxError as e:
            error_msg = f"SyntaxError in {file_path.name}:{e.lineno}: {e.msg}"
            return False, error_msg
        except Exception as e:
            error_msg = f"Error checking {file_path.name}: {str(e)}"
            return False, error_msg
    
    def run_python_file(self, file_path: Path, timeout: int = 30) -> Tuple[int, str, str]:
        """Run a single Python file and capture output."""
        try:
            proc = subprocess.Popen(
                [sys.executable, str(file_path)],
                cwd=str(PROJECT_ROOT),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding='utf-8'
            )
            stdout, stderr = proc.communicate(timeout=timeout)
            return proc.returncode, stdout or "", stderr or ""
        except subprocess.TimeoutExpired:
            proc.kill()
            return 124, "", "File execution timed out"
        except Exception as e:
            return 1, "", f"Error running file: {str(e)}"
    
    def create_backup(self, file_path: Path) -> Path:
        """Create a backup of the file before modification."""
        BACKUP_DIR.mkdir(exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"{file_path.name}.backup_{timestamp}"
        backup_path = BACKUP_DIR / backup_name
        shutil.copy2(file_path, backup_path)
        return backup_path
    
    def get_user_permission(self, file_path: Path, error_text: str, proposed_fix: str) -> bool:
        """Ask user for permission before applying a fix."""
        rel_path = file_path.relative_to(PROJECT_ROOT)
        print(f"\n🔧 AI wants to fix: {rel_path}")
        print(f"📋 Error: {error_text[:200]}{'...' if len(error_text) > 200 else ''}")
        print(f"💡 Proposed fix preview: {proposed_fix[:300]}{'...' if len(proposed_fix) > 300 else ''}")
        
        while True:
            response = input("\n❓ Apply this fix? (y/n/d for details): ").lower().strip()
            if response in ['y', 'yes']:
                return True
            elif response in ['n', 'no']:
                return False
            elif response in ['d', 'details']:
                print(f"\n📄 Full proposed fix:\n{'-' * 50}")
                print(proposed_fix)
                print(f"{'-' * 50}")
            else:
                print("Please enter 'y' for yes, 'n' for no, or 'd' for details.")
    
    def fix_file_with_ai(self, file_path: Path, error_text: str) -> bool:
        """Fix a file using AI with user permission."""
        if not self.ai_client:
            print("❌ AI client not available. Cannot fix file.")
            return False
        
        try:
            # Read the file
            with open(file_path, 'r', encoding='utf-8') as f:
                source = f.read()
            
            # Build prompt for AI
            rel_path = file_path.relative_to(PROJECT_ROOT)
            prompt = (
                "You are an expert Python engineer.\n"
                "Task: Fix the provided file so it runs without errors.\n"
                "Rules:\n"
                "- Return ONLY the full corrected contents of the file.\n"
                "- Do not include explanations, comments, or markdown fences.\n"
                "- Preserve functionality; if unclear, choose the simplest working fix.\n"
                f"\n--- BEGIN ERROR OUTPUT ---\n{error_text}\n--- END ERROR OUTPUT ---\n"
                f"\n--- BEGIN {rel_path.as_posix()} ---\n{source}\n--- END {rel_path.as_posix()} ---\n"
            )
            
            # Get AI response
            ai_response = self.ai_client.generate(prompt)
            
            # Extract code from response
            code_block_re = re.compile(r"```[a-zA-Z0-9_\-]*\n([\s\S]*?)```", re.MULTILINE)
            match = code_block_re.search(ai_response)
            if match:
                fixed_code = match.group(1).strip()
            else:
                fixed_code = ai_response.strip()
            
            if not fixed_code:
                print("❌ AI returned empty fix. Aborting.")
                return False
            
            # Ask for user permission
            if not self.get_user_permission(file_path, error_text, fixed_code):
                print("❌ User declined the fix.")
                return False
            
            # Create backup
            backup_path = self.create_backup(file_path)
            print(f"💾 Created backup: {backup_path}")
            
            # Apply the fix
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(fixed_code)
            
            print(f"📝 Applied AI-corrected code to {rel_path}")
            
            # Verify the fix
            print("🔍 Verifying fix...")
            is_valid, error_msg = self.check_file_syntax(file_path)
            if is_valid:
                print("✅ Fix applied successfully!")
                self.fix_history.append({
                    'file': str(rel_path),
                    'timestamp': datetime.now(),
                    'error': error_text[:100],
                    'success': True
                })
                return True
            else:
                print(f"❌ Fix verification failed: {error_msg}")
                print("🔄 You can restore from backup if needed.")
                self.fix_history.append({
                    'file': str(rel_path),
                    'timestamp': datetime.now(),
                    'error': error_text[:100],
                    'success': False
                })
                return False
                
        except Exception as e:
            print(f"❌ Error during AI fix: {e}")
            return False
    
    def monitor_files(self):
        """Continuously monitor files for errors."""
        print("🔍 Starting continuous file monitoring...")
        
        while SYSTEM_RUNNING and MONITORING_ACTIVE:
            try:
                # Get all Python files
                python_files = self.find_all_python_files()
                
                for file_path in python_files:
                    if not SYSTEM_RUNNING:
                        break
                    
                    # Check syntax
                    is_valid, error_msg = self.check_file_syntax(file_path)
                    if not is_valid:
                        print(f"🚨 Syntax error detected in {file_path.relative_to(PROJECT_ROOT)}")
                        self.error_history.append({
                            'file': str(file_path.relative_to(PROJECT_ROOT)),
                            'timestamp': datetime.now(),
                            'error': error_msg,
                            'type': 'syntax'
                        })
                        
                        # Try to fix with AI
                        if self.ai_client:
                            self.fix_file_with_ai(file_path, error_msg)
                        else:
                            print("⚠️  AI client not available. Manual fix required.")
                        continue
                    
                    # Check runtime errors for main files
                    if file_path.name in ['sensor_server.py', 'ui_server.py', 'ai_chat_server.py']:
                        returncode, stdout, stderr = self.run_python_file(file_path, timeout=10)
                        if returncode != 0 and stderr:
                            print(f"🚨 Runtime error detected in {file_path.relative_to(PROJECT_ROOT)}")
                            self.error_history.append({
                                'file': str(file_path.relative_to(PROJECT_ROOT)),
                                'timestamp': datetime.now(),
                                'error': stderr[:200],
                                'type': 'runtime'
                            })
                            
                            # Try to fix with AI
                            if self.ai_client:
                                self.fix_file_with_ai(file_path, stderr)
                            else:
                                print("⚠️  AI client not available. Manual fix required.")
                
                # Wait before next check
                time.sleep(30)  # Check every 30 seconds
                
            except Exception as e:
                print(f"❌ Error in monitoring loop: {e}")
                time.sleep(60)  # Wait longer on error
    
    def get_system_status(self) -> Dict:
        """Get current system status."""
        return {
            'monitoring_active': MONITORING_ACTIVE,
            'ai_client_available': self.ai_client is not None,
            'total_errors_detected': len(self.error_history),
            'total_fixes_applied': len([f for f in self.fix_history if f['success']]),
            'last_check': datetime.fromtimestamp(self.last_check).isoformat(),
            'recent_errors': self.error_history[-5:] if self.error_history else [],
            'recent_fixes': self.fix_history[-5:] if self.fix_history else []
        }

def print_banner():
    """Print the system banner."""
    print("=" * 80)
    print("🌡️  Self-Healing Temperature Monitoring System")
    print("🤖 AI-Powered Error Detection & Auto-Fixing")
    print("=" * 80)
    print("🚀 Starting all servers with continuous monitoring...")
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
        'python_dotenv': 'dotenv'  # python-dotenv imports as 'dotenv'
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

def start_simulation_server():
    """Start the simulation server in a separate thread."""
    try:
        print("🌡️  Starting simulation server on port 5000...")
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

def start_ai_chat_server():
    """Start the AI chat server in a separate thread."""
    try:
        print("🤖 Starting AI chat server on port 5002...")
        subprocess.run([sys.executable, "ai_chat_server.py"], 
                     cwd=Path("."), check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ AI chat server failed to start: {e}")
    except KeyboardInterrupt:
        print("⏹️  AI chat server stopped by user")

def main():
    """Main startup function with self-healing capabilities."""
    global SYSTEM_RUNNING, MONITORING_ACTIVE
    
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
    
    # Initialize self-healing monitor
    monitor = SelfHealingMonitor()
    
    # Start monitoring thread
    monitor_thread = threading.Thread(target=monitor.monitor_files, daemon=True)
    monitor_thread.start()
    
    # Start all servers
    print("\n🚀 Launching servers with self-healing...")
    print("📱 Simulation Dashboard: http://<raspberry_pi_ip>:5000")
    print("🖥️  UI Dashboard: http://localhost:5001")
    print("🤖 AI Chat Dashboard: http://localhost:5002")
    print("\n💡 Press Ctrl+C to stop all servers")
    print("🔍 AI monitoring is active - errors will be auto-detected and fixed")
    print("=" * 80)
    
    try:
        # Start simulation server in background thread
        simulation_thread = threading.Thread(target=start_simulation_server, daemon=True)
        simulation_thread.start()
        
        # Start AI chat server in background thread
        ai_chat_thread = threading.Thread(target=start_ai_chat_server, daemon=True)
        ai_chat_thread.start()
        
        # Start UI server in main thread
        start_ui_server()
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Shutting down self-healing temperature monitoring system...")
        SYSTEM_RUNNING = False
        MONITORING_ACTIVE = False
        
        # Print system status
        status = monitor.get_system_status()
        print(f"\n📊 System Status Summary:")
        print(f"   - Total errors detected: {status['total_errors_detected']}")
        print(f"   - Total fixes applied: {status['total_fixes_applied']}")
        print(f"   - AI client was available: {status['ai_client_available']}")
        
        print("👋 Goodbye!")
        sys.exit(0)

if __name__ == "__main__":
    main()
