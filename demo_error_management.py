#!/usr/bin/env python3
"""
Error Management System Demo
Demonstrates the error detection, correction code display, and server pause functionality.
"""

import os
import sys
import time
import tempfile
from pathlib import Path

def create_demo_error_file():
    """Create a Python file with intentional syntax errors for demonstration."""
    demo_code = '''#!/usr/bin/env python3
"""
Demo file with intentional syntax errors
"""

import os
import sys

def broken_function():
    # Missing colon after if statement
    if True
        print("This will cause a syntax error")
    
    # Missing closing parenthesis
    print("Another error here"
    
    # Undefined variable
    print(undefined_variable)

def another_broken_function():
    # Missing closing bracket
    my_list = [1, 2, 3, 4, 5
    print(my_list)

if __name__ == "__main__":
    broken_function()
    another_broken_function()
'''
    
    # Create temporary file
    temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False)
    temp_file.write(demo_code)
    temp_file.close()
    
    return temp_file.name

def demo_error_detection():
    """Demonstrate error detection and correction."""
    print("🎭 Error Management System Demo")
    print("=" * 50)
    
    # Create demo error file
    demo_file = create_demo_error_file()
    print(f"📝 Created demo file with errors: {demo_file}")
    
    try:
        # Import error manager
        from error_manager import error_manager
        
        # Check for syntax errors
        errors = error_manager._check_syntax_errors()
        
        if errors:
            print(f"🚨 Found {len(errors)} syntax errors!")
            
            # Process the first error
            error = errors[0]
            print(f"📋 Error details:")
            print(f"   Type: {error['type']}")
            print(f"   File: {error['file']}")
            print(f"   Message: {error['message']}")
            print(f"   Severity: {error['severity']}")
            
            # Generate correction code
            if error_manager.ai_client:
                print("\n🤖 Generating correction code with AI...")
                correction_code = error_manager.generate_correction_code(error)
                
                if correction_code:
                    print("\n🔧 AI-Generated Correction Code:")
                    print("=" * 50)
                    print(correction_code)
                    print("=" * 50)
                else:
                    print("❌ Failed to generate correction code")
            else:
                print("⚠️  AI client not available - cannot generate correction code")
                print("💡 Set GEMINI_API_KEY in .env file to enable AI correction")
        else:
            print("✅ No syntax errors found")
    
    except ImportError:
        print("❌ Error manager not available")
    except Exception as e:
        print(f"❌ Demo failed: {e}")
    
    finally:
        # Clean up demo file
        try:
            os.unlink(demo_file)
            print(f"🗑️  Cleaned up demo file: {demo_file}")
        except:
            pass

def demo_terminal_interface():
    """Demonstrate the terminal error interface."""
    print("\n🖥️  Terminal Error Interface Demo")
    print("=" * 50)
    
    try:
        from terminal_error_interface import TerminalErrorInterface
        
        interface = TerminalErrorInterface()
        
        # Create a demo error
        demo_error = {
            'type': 'syntax_error',
            'file': 'demo_file.py',
            'message': 'Demo syntax error for testing',
            'severity': 'high',
            'line': 10,
            'text': 'if True'
        }
        
        print("📋 Demo error created:")
        print(f"   Type: {demo_error['type']}")
        print(f"   Message: {demo_error['message']}")
        print(f"   Severity: {demo_error['severity']}")
        
        # Generate correction code
        if interface.ai_monitor:
            correction_code = interface.regenerate_correction_code(demo_error)
            print(f"\n🤖 Generated correction code ({len(correction_code)} characters)")
        else:
            correction_code = "# Demo correction code\n# Fix the syntax error here"
            print("\n⚠️  AI not available, using demo correction code")
        
        print("\n🖥️  Would display terminal interface with:")
        print("   - Error details")
        print("   - AI-generated correction code")
        print("   - Server pause/resume controls")
        print("   - User interaction options")
        
    except ImportError:
        print("❌ Terminal error interface not available")
    except Exception as e:
        print(f"❌ Demo failed: {e}")

def demo_server_management():
    """Demonstrate server pause/resume functionality."""
    print("\n🖥️  Server Management Demo")
    print("=" * 50)
    
    try:
        from error_manager import ServerManager
        
        server_manager = ServerManager()
        
        # Register a demo server
        server_manager.register_server(
            "demo_server",
            [sys.executable, "-c", "import time; time.sleep(60)"],
            port=9999
        )
        
        print("📝 Registered demo server")
        
        # Start server
        if server_manager.start_server("demo_server"):
            print("🚀 Started demo server")
            
            # Check status
            status = server_manager.get_server_status()
            print(f"📊 Server status: {status}")
            
            # Pause server
            if server_manager.pause_server("demo_server"):
                print("⏸️  Paused demo server")
                
                # Resume server
                if server_manager.resume_server("demo_server"):
                    print("▶️  Resumed demo server")
            
            # Stop server
            if server_manager.stop_server("demo_server"):
                print("⏹️  Stopped demo server")
        else:
            print("❌ Failed to start demo server")
    
    except ImportError:
        print("❌ Server manager not available")
    except Exception as e:
        print(f"❌ Demo failed: {e}")

def main():
    """Main demo function."""
    print("🎭 Error Management System Demonstration")
    print("=" * 60)
    print("This demo shows the error detection and correction capabilities")
    print("=" * 60)
    
    # Check if required modules are available
    try:
        import google.generativeai
        print("✅ Gemini AI SDK available")
    except ImportError:
        print("⚠️  Gemini AI SDK not available - AI features will be limited")
    
    # Run demos
    demo_error_detection()
    demo_terminal_interface()
    demo_server_management()
    
    print("\n🎉 Demo completed!")
    print("=" * 60)
    print("To use the full system:")
    print("1. Set GEMINI_API_KEY in .env file")
    print("2. Run: python start_system_with_error_management.py")
    print("3. The system will automatically detect errors and show correction code")
    print("4. Servers will be paused during error correction")
    print("=" * 60)

if __name__ == "__main__":
    main()
