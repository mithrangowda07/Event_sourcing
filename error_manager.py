#!/usr/bin/env python3
"""
Error Management System
Handles error detection, correction code display, and server pause/resume functionality.
When errors are detected, the terminal shows only the correction code and pauses other servers.
"""

import os
import sys
import time
import json
import threading
import subprocess
import signal
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class ServerManager:
    """Manages server processes and their pause/resume states."""
    
    def __init__(self):
        self.servers = {}
        self.server_threads = {}
        self.paused_servers = set()
        self.server_processes = {}
        
    def register_server(self, name: str, command: List[str], cwd: str = None, port: int = None):
        """Register a server for management."""
        self.servers[name] = {
            'command': command,
            'cwd': cwd,
            'port': port,
            'process': None,
            'thread': None,
            'running': False
        }
        
    def start_server(self, name: str) -> bool:
        """Start a registered server."""
        if name not in self.servers:
            print(f"❌ Server '{name}' not registered")
            return False
            
        server_info = self.servers[name]
        
        try:
            # Start server process
            process = subprocess.Popen(
                server_info['command'],
                cwd=server_info['cwd'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            server_info['process'] = process
            server_info['running'] = True
            self.server_processes[name] = process
            
            print(f"🚀 Started server '{name}' (PID: {process.pid})")
            return True
            
        except Exception as e:
            print(f"❌ Failed to start server '{name}': {e}")
            return False
    
    def pause_server(self, name: str) -> bool:
        """Pause a running server."""
        if name not in self.servers or not self.servers[name]['running']:
            return False
            
        try:
            process = self.servers[name]['process']
            if process and process.poll() is None:  # Process is still running
                # Send SIGSTOP to pause the process
                process.send_signal(signal.SIGSTOP)
                self.paused_servers.add(name)
                print(f"⏸️  Paused server '{name}'")
                return True
        except Exception as e:
            print(f"❌ Failed to pause server '{name}': {e}")
            
        return False
    
    def resume_server(self, name: str) -> bool:
        """Resume a paused server."""
        if name not in self.servers or name not in self.paused_servers:
            return False
            
        try:
            process = self.servers[name]['process']
            if process and process.poll() is None:  # Process is still running
                # Send SIGCONT to resume the process
                process.send_signal(signal.SIGCONT)
                self.paused_servers.remove(name)
                print(f"▶️  Resumed server '{name}'")
                return True
        except Exception as e:
            print(f"❌ Failed to resume server '{name}': {e}")
            
        return False
    
    def pause_all_servers(self):
        """Pause all running servers."""
        for name in list(self.servers.keys()):
            if self.servers[name]['running'] and name not in self.paused_servers:
                self.pause_server(name)
    
    def resume_all_servers(self):
        """Resume all paused servers."""
        for name in list(self.paused_servers):
            self.resume_server(name)
    
    def stop_server(self, name: str) -> bool:
        """Stop a server."""
        if name not in self.servers:
            return False
            
        try:
            process = self.servers[name]['process']
            if process and process.poll() is None:
                process.terminate()
                process.wait(timeout=5)
                
            self.servers[name]['running'] = False
            self.servers[name]['process'] = None
            
            if name in self.paused_servers:
                self.paused_servers.remove(name)
                
            if name in self.server_processes:
                del self.server_processes[name]
                
            print(f"⏹️  Stopped server '{name}'")
            return True
            
        except Exception as e:
            print(f"❌ Failed to stop server '{name}': {e}")
            return False
    
    def stop_all_servers(self):
        """Stop all servers."""
        for name in list(self.servers.keys()):
            self.stop_server(name)
    
    def get_server_status(self) -> Dict:
        """Get status of all servers."""
        status = {}
        for name, info in self.servers.items():
            status[name] = {
                'running': info['running'],
                'paused': name in self.paused_servers,
                'pid': info['process'].pid if info['process'] else None
            }
        return status

class ErrorManager:
    """Main error management system."""
    
    def __init__(self):
        self.server_manager = ServerManager()
        self.error_detected = False
        self.current_error = None
        self.correction_code = None
        self.error_lock = threading.Lock()
        self.monitoring_active = False
        self.ai_client = None
        
        # Initialize AI client for error correction
        self._init_ai_client()
        
        # Register servers
        self._register_servers()
        
    def _init_ai_client(self):
        """Initialize AI client for error correction."""
        try:
            import google.generativeai as genai
            
            api_key = os.getenv("GEMINI_API_KEY")
            if api_key and api_key != "YOUR_GEMINI_API_KEY":
                genai.configure(api_key=api_key)
                self.ai_client = genai.GenerativeModel("gemini-2.0-flash")
                print("🤖 AI client initialized for error correction")
            else:
                print("⚠️  GEMINI_API_KEY not configured - AI error correction disabled")
                
        except ImportError:
            print("⚠️  Gemini SDK not installed - AI error correction disabled")
        except Exception as e:
            print(f"⚠️  AI client initialization failed: {e}")
    
    def _register_servers(self):
        """Register all system servers."""
        # Simulation server
        self.server_manager.register_server(
            "simulation",
            [sys.executable, "sensor_server.py"],
            cwd="simulation",
            port=5000
        )
        
        # UI server
        self.server_manager.register_server(
            "ui",
            [sys.executable, "ui_server.py"],
            cwd="UI",
            port=5001
        )
        
        # AI chat server
        self.server_manager.register_server(
            "ai_chat",
            [sys.executable, "ai_chat_server.py"],
            cwd=".",
            port=5002
        )
    
    def start_all_servers(self):
        """Start all registered servers."""
        print("🚀 Starting all servers...")
        for name in self.server_manager.servers.keys():
            self.server_manager.start_server(name)
            time.sleep(1)  # Small delay between server starts
    
    def detect_errors(self) -> List[Dict]:
        """Detect errors in the system."""
        errors = []
        
        # Check server processes
        for name, info in self.server_manager.servers.items():
            if info['running'] and info['process']:
                if info['process'].poll() is not None:
                    # Process has terminated
                    errors.append({
                        'type': 'server_crash',
                        'server': name,
                        'message': f"Server '{name}' has crashed",
                        'severity': 'critical'
                    })
        
        # Check log files for errors
        errors.extend(self._check_log_errors())
        
        # Check Python file syntax
        errors.extend(self._check_syntax_errors())
        
        return errors
    
    def _check_log_errors(self) -> List[Dict]:
        """Check log files for error entries."""
        errors = []
        
        # Check simulation logs
        sim_log_dir = Path("simulation/logs")
        if sim_log_dir.exists():
            for log_file in sim_log_dir.glob("*_events.log"):
                try:
                    with open(log_file, 'r', encoding='utf-8') as f:
                        lines = f.readlines()
                        # Check last 10 lines for errors
                        for line in lines[-10:]:
                            try:
                                log_entry = json.loads(line.strip())
                                if log_entry.get('type') == 'error':
                                    errors.append({
                                        'type': 'log_error',
                                        'component': log_entry.get('component', 'unknown'),
                                        'message': log_entry.get('error_message', 'Unknown error'),
                                        'severity': 'medium',
                                        'timestamp': log_entry.get('timestamp')
                                    })
                            except:
                                continue
                except Exception as e:
                    errors.append({
                        'type': 'log_read_error',
                        'component': 'error_manager',
                        'message': f"Failed to read log file {log_file}: {e}",
                        'severity': 'low'
                    })
        
        return errors
    
    def _check_syntax_errors(self) -> List[Dict]:
        """Check Python files for syntax errors."""
        errors = []
        
        python_files = [
            "simulation/sensor_server.py",
            "UI/ui_server.py",
            "ai_chat_server.py",
            "self_healing_system.py"
        ]
        
        for file_path in python_files:
            if Path(file_path).exists():
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    compile(content, file_path, 'exec')
                except SyntaxError as e:
                    errors.append({
                        'type': 'syntax_error',
                        'file': file_path,
                        'message': f"Syntax error in {file_path}:{e.lineno}: {e.msg}",
                        'severity': 'high',
                        'line': e.lineno,
                        'text': e.text
                    })
                except Exception as e:
                    errors.append({
                        'type': 'file_error',
                        'file': file_path,
                        'message': f"Error checking {file_path}: {e}",
                        'severity': 'medium'
                    })
        
        return errors
    
    def generate_correction_code(self, error: Dict) -> Optional[str]:
        """Generate correction code using AI."""
        if not self.ai_client:
            return None
            
        try:
            # Read the problematic file if it's a syntax error
            file_content = ""
            if error['type'] == 'syntax_error' and 'file' in error:
                try:
                    with open(error['file'], 'r', encoding='utf-8') as f:
                        file_content = f.read()
                except:
                    pass
            
            prompt = f"""
            You are an expert Python engineer. Fix the following error:

            Error Type: {error['type']}
            Error Message: {error['message']}
            
            {f"File: {error['file']}" if 'file' in error else ""}
            {f"Line: {error['line']}" if 'line' in error else ""}
            {f"Problematic Text: {error['text']}" if 'text' in error else ""}
            
            {f"File Content:\n{file_content}" if file_content else ""}
            
            Provide ONLY the corrected code. Do not include explanations or markdown.
            Return the complete corrected file content.
            """
            
            response = self.ai_client.generate_content(prompt)
            return response.text.strip()
            
        except Exception as e:
            print(f"❌ Failed to generate correction code: {e}")
            return None
    
    def display_error_correction(self, error: Dict, correction_code: str):
        """Display error and correction code in terminal."""
        # Clear terminal
        os.system('cls' if os.name == 'nt' else 'clear')
        
        print("=" * 80)
        print("🚨 ERROR DETECTED - SYSTEM PAUSED")
        print("=" * 80)
        print(f"Error Type: {error['type']}")
        print(f"Severity: {error['severity'].upper()}")
        print(f"Message: {error['message']}")
        if 'file' in error:
            print(f"File: {error['file']}")
        if 'line' in error:
            print(f"Line: {error['line']}")
        print("=" * 80)
        print("🔧 CORRECTION CODE:")
        print("=" * 80)
        print(correction_code)
        print("=" * 80)
        print("📋 INSTRUCTIONS:")
        print("1. Review the correction code above")
        print("2. Apply the fix to the problematic file")
        print("3. Press ENTER to resume system monitoring")
        print("4. Press 'q' to quit the system")
        print("=" * 80)
    
    def handle_error(self, error: Dict):
        """Handle detected error."""
        with self.error_lock:
            if self.error_detected:
                return  # Already handling an error
                
            self.error_detected = True
            self.current_error = error
            
            # Generate correction code
            correction_code = self.generate_correction_code(error)
            if not correction_code:
                correction_code = f"# Manual fix required for: {error['message']}\n# Error type: {error['type']}\n# Please review and fix manually"
            
            self.correction_code = correction_code
            
            # Pause all servers
            print("⏸️  Pausing all servers...")
            self.server_manager.pause_all_servers()
            
            # Display error and correction code
            self.display_error_correction(error, correction_code)
            
            # Wait for user input
            while True:
                try:
                    user_input = input("\nPress ENTER to resume or 'q' to quit: ").strip().lower()
                    if user_input == 'q':
                        print("👋 Shutting down system...")
                        self.server_manager.stop_all_servers()
                        sys.exit(0)
                    elif user_input == '':
                        break
                except KeyboardInterrupt:
                    print("\n👋 Shutting down system...")
                    self.server_manager.stop_all_servers()
                    sys.exit(0)
            
            # Resume servers
            print("▶️  Resuming all servers...")
            self.server_manager.resume_all_servers()
            
            # Reset error state
            self.error_detected = False
            self.current_error = None
            self.correction_code = None
            
            # Clear terminal
            os.system('cls' if os.name == 'nt' else 'clear')
            print("✅ System resumed - monitoring continues...")
    
    def start_monitoring(self):
        """Start continuous error monitoring."""
        self.monitoring_active = True
        print("🔍 Starting error monitoring...")
        
        while self.monitoring_active:
            try:
                errors = self.detect_errors()
                
                if errors:
                    # Handle the first critical/high severity error
                    critical_errors = [e for e in errors if e['severity'] in ['critical', 'high']]
                    if critical_errors:
                        self.handle_error(critical_errors[0])
                    else:
                        # Handle first medium severity error
                        medium_errors = [e for e in errors if e['severity'] == 'medium']
                        if medium_errors:
                            self.handle_error(medium_errors[0])
                
                time.sleep(5)  # Check every 5 seconds
                
            except KeyboardInterrupt:
                print("\n⏹️  Stopping error monitoring...")
                self.monitoring_active = False
                break
            except Exception as e:
                print(f"❌ Error in monitoring loop: {e}")
                time.sleep(10)  # Wait longer on error
    
    def stop_monitoring(self):
        """Stop error monitoring."""
        self.monitoring_active = False
    
    def get_status(self) -> Dict:
        """Get current system status."""
        return {
            'monitoring_active': self.monitoring_active,
            'error_detected': self.error_detected,
            'current_error': self.current_error,
            'servers': self.server_manager.get_server_status(),
            'ai_client_available': self.ai_client is not None
        }

# Global error manager instance
error_manager = ErrorManager()

def main():
    """Main function to run the error management system."""
    print("🛡️  Error Management System")
    print("=" * 50)
    
    # Start all servers
    error_manager.start_all_servers()
    
    # Start monitoring
    try:
        error_manager.start_monitoring()
    except KeyboardInterrupt:
        print("\n👋 Shutting down...")
    finally:
        error_manager.server_manager.stop_all_servers()

if __name__ == "__main__":
    main()
