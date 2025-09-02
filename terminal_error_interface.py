#!/usr/bin/env python3
"""
Terminal Error Interface
Provides a clean terminal interface that shows only error correction code when errors are detected.
Integrates with the existing AI monitoring system.
"""

import os
import sys
import time
import json
import threading
from datetime import datetime
from typing import Dict, List, Optional
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class TerminalErrorInterface:
    """Terminal interface for error display and management."""
    
    def __init__(self):
        self.ai_monitor = None
        self.error_manager = None
        self.display_active = False
        self.current_error = None
        self.correction_code = None
        self.servers_paused = False
        
        # Initialize AI monitor
        self._init_ai_monitor()
        
        # Initialize error manager
        self._init_error_manager()
    
    def _init_ai_monitor(self):
        """Initialize AI monitoring system."""
        try:
            from ai_monitor import ai_monitor
            self.ai_monitor = ai_monitor
            print("🤖 AI monitoring system connected")
        except ImportError:
            print("⚠️  AI monitoring system not available")
        except Exception as e:
            print(f"⚠️  AI monitoring initialization failed: {e}")
    
    def _init_error_manager(self):
        """Initialize error management system."""
        try:
            from error_manager import error_manager
            self.error_manager = error_manager
            print("🛡️  Error management system connected")
        except ImportError:
            print("⚠️  Error management system not available")
        except Exception as e:
            print(f"⚠️  Error management initialization failed: {e}")
    
    def clear_terminal(self):
        """Clear the terminal screen."""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def display_error_screen(self, error: Dict, correction_code: str):
        """Display the error correction screen."""
        self.clear_terminal()
        
        # Error header
        print("=" * 80)
        print("🚨 CRITICAL ERROR DETECTED")
        print("=" * 80)
        print(f"⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"🔍 Error Type: {error.get('type', 'Unknown')}")
        print(f"⚠️  Severity: {error.get('severity', 'Unknown').upper()}")
        print(f"📝 Message: {error.get('message', 'No message')}")
        
        if 'file' in error:
            print(f"📁 File: {error['file']}")
        if 'line' in error:
            print(f"📍 Line: {error['line']}")
        if 'component' in error:
            print(f"🔧 Component: {error['component']}")
        
        print("=" * 80)
        print("🔧 AI-GENERATED CORRECTION CODE:")
        print("=" * 80)
        
        # Display correction code with syntax highlighting
        self._display_code_with_highlighting(correction_code)
        
        print("=" * 80)
        print("📋 INSTRUCTIONS:")
        print("=" * 80)
        print("1. 📖 Review the correction code above")
        print("2. ✏️  Apply the fix to the problematic file")
        print("3. ✅ Press ENTER to resume system monitoring")
        print("4. ❌ Press 'q' to quit the system")
        print("5. 🔄 Press 'r' to regenerate correction code")
        print("6. 📊 Press 's' to show system status")
        print("=" * 80)
        
        # Show server status
        if self.servers_paused:
            print("⏸️  All servers are currently PAUSED")
        else:
            print("▶️  All servers are currently RUNNING")
        print("=" * 80)
    
    def _display_code_with_highlighting(self, code: str):
        """Display code with basic syntax highlighting."""
        lines = code.split('\n')
        for i, line in enumerate(lines, 1):
            # Basic syntax highlighting
            if line.strip().startswith('#'):
                # Comments in green
                print(f"{i:3d} | \033[92m{line}\033[0m")
            elif line.strip().startswith(('def ', 'class ', 'import ', 'from ')):
                # Keywords in blue
                print(f"{i:3d} | \033[94m{line}\033[0m")
            elif line.strip().startswith(('if ', 'for ', 'while ', 'try:', 'except:', 'finally:')):
                # Control structures in yellow
                print(f"{i:3d} | \033[93m{line}\033[0m")
            else:
                # Regular code
                print(f"{i:3d} | {line}")
    
    def display_system_status(self):
        """Display current system status."""
        self.clear_terminal()
        
        print("=" * 80)
        print("📊 SYSTEM STATUS")
        print("=" * 80)
        print(f"⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # AI Monitor status
        if self.ai_monitor:
            ai_status = self.ai_monitor.get_system_status()
            print(f"🤖 AI Monitoring: {'Active' if ai_status.get('monitoring_active') else 'Inactive'}")
            print(f"📈 Alert Count: {ai_status.get('alert_count', 0)}")
            if ai_status.get('last_analysis'):
                print(f"🔍 Last Analysis: {ai_status['last_analysis']}")
        else:
            print("🤖 AI Monitoring: Not Available")
        
        # Error Manager status
        if self.error_manager:
            error_status = self.error_manager.get_status()
            print(f"🛡️  Error Management: {'Active' if error_status.get('monitoring_active') else 'Inactive'}")
            print(f"🚨 Error Detected: {'Yes' if error_status.get('error_detected') else 'No'}")
            
            # Server status
            servers = error_status.get('servers', {})
            print("\n🖥️  SERVER STATUS:")
            for name, status in servers.items():
                state = "Running"
                if status.get('paused'):
                    state = "Paused"
                elif not status.get('running'):
                    state = "Stopped"
                print(f"   {name}: {state} (PID: {status.get('pid', 'N/A')})")
        else:
            print("🛡️  Error Management: Not Available")
        
        print("=" * 80)
        print("Press ENTER to return to error display or 'q' to quit")
        print("=" * 80)
    
    def pause_servers(self):
        """Pause all servers."""
        if self.error_manager:
            self.error_manager.server_manager.pause_all_servers()
            self.servers_paused = True
            print("⏸️  All servers paused")
    
    def resume_servers(self):
        """Resume all servers."""
        if self.error_manager:
            self.error_manager.server_manager.resume_all_servers()
            self.servers_paused = False
            print("▶️  All servers resumed")
    
    def regenerate_correction_code(self, error: Dict) -> str:
        """Regenerate correction code using AI."""
        if not self.ai_monitor:
            return "AI monitoring not available for code regeneration"
        
        try:
            # Use AI monitor to generate correction
            prompt = f"""
            Generate correction code for this error:
            
            Error Type: {error.get('type', 'Unknown')}
            Error Message: {error.get('message', 'No message')}
            File: {error.get('file', 'Unknown')}
            Line: {error.get('line', 'Unknown')}
            
            Provide ONLY the corrected code. Do not include explanations or markdown.
            Return the complete corrected file content.
            """
            
            response = self.ai_monitor.chat_with_ai(prompt)
            return response
            
        except Exception as e:
            return f"Failed to regenerate correction code: {e}"
    
    def handle_user_input(self, error: Dict) -> str:
        """Handle user input during error display."""
        while True:
            try:
                user_input = input("\nEnter command (ENTER=resume, q=quit, r=regenerate, s=status): ").strip().lower()
                
                if user_input == '' or user_input == 'resume':
                    return 'resume'
                elif user_input == 'q' or user_input == 'quit':
                    return 'quit'
                elif user_input == 'r' or user_input == 'regenerate':
                    return 'regenerate'
                elif user_input == 's' or user_input == 'status':
                    return 'status'
                else:
                    print("Invalid command. Use: ENTER (resume), q (quit), r (regenerate), s (status)")
                    
            except KeyboardInterrupt:
                return 'quit'
    
    def process_error(self, error: Dict):
        """Process a detected error."""
        self.current_error = error
        
        # Generate initial correction code
        if self.ai_monitor:
            correction_code = self.regenerate_correction_code(error)
        else:
            correction_code = f"# Manual fix required for: {error.get('message', 'Unknown error')}\n# Error type: {error.get('type', 'Unknown')}\n# Please review and fix manually"
        
        self.correction_code = correction_code
        
        # Pause servers
        self.pause_servers()
        
        # Main error handling loop
        while True:
            # Display error screen
            self.display_error_screen(error, self.correction_code)
            
            # Get user input
            action = self.handle_user_input(error)
            
            if action == 'resume':
                break
            elif action == 'quit':
                print("👋 Shutting down system...")
                if self.error_manager:
                    self.error_manager.server_manager.stop_all_servers()
                sys.exit(0)
            elif action == 'regenerate':
                print("🔄 Regenerating correction code...")
                self.correction_code = self.regenerate_correction_code(error)
            elif action == 'status':
                self.display_system_status()
                input("Press ENTER to continue...")
        
        # Resume servers
        self.resume_servers()
        
        # Clear terminal and show resume message
        self.clear_terminal()
        print("✅ System resumed - monitoring continues...")
        time.sleep(2)
    
    def start_monitoring(self):
        """Start monitoring for errors."""
        print("🔍 Starting terminal error monitoring...")
        
        while True:
            try:
                # Check for errors from AI monitor
                if self.ai_monitor:
                    # Get recent logs
                    recent_logs = self.ai_monitor.collect_recent_logs(minutes=1)
                    
                    # Check for critical errors
                    error_logs = recent_logs.get('error', [])
                    if error_logs:
                        # Process the most recent error
                        latest_error = error_logs[-1]
                        error_dict = {
                            'type': 'log_error',
                            'component': latest_error.get('component', 'unknown'),
                            'message': latest_error.get('error_message', 'Unknown error'),
                            'severity': 'high',
                            'timestamp': latest_error.get('timestamp')
                        }
                        
                        self.process_error(error_dict)
                
                # Check for syntax errors
                syntax_errors = self._check_syntax_errors()
                if syntax_errors:
                    self.process_error(syntax_errors[0])
                
                time.sleep(5)  # Check every 5 seconds
                
            except KeyboardInterrupt:
                print("\n⏹️  Stopping terminal error monitoring...")
                break
            except Exception as e:
                print(f"❌ Error in monitoring loop: {e}")
                time.sleep(10)
    
    def _check_syntax_errors(self) -> List[Dict]:
        """Check for syntax errors in Python files."""
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

def main():
    """Main function to run the terminal error interface."""
    print("🖥️  Terminal Error Interface")
    print("=" * 50)
    
    interface = TerminalErrorInterface()
    
    try:
        interface.start_monitoring()
    except KeyboardInterrupt:
        print("\n👋 Shutting down...")
    finally:
        if interface.error_manager:
            interface.error_manager.server_manager.stop_all_servers()

if __name__ == "__main__":
    main()
