#!/usr/bin/env python3
"""
Test script for local logging functionality
Demonstrates how logs are stored locally
"""

import time
from event_logger import log_sensor_event, log_error_event, log_data_event, get_log_status, force_upload_logs

def test_local_logging():
    """Test the local logging functionality."""
    print("🧪 Testing Local Logging Functionality")
    print("=" * 50)
    
    # Check initial status
    status = get_log_status()
    print(f"Initial Status: {status}")
    
    # Generate some test logs
    print("\n📝 Generating test logs...")
    
    # Sensor events
    log_sensor_event('test_start', 'Local logging test started')
    log_sensor_event('sensor_on', 'Test sensor activated')
    
    # Data events
    log_data_event('test', 'data_generated', 'Test temperature data: 25.5°C')
    log_data_event('test', 'local_storage', 'Test data stored locally')
    
    # Error events
    log_error_event('test', 'Simulated error for testing')
    log_error_event('test', 'Another test error message')
    
    # Wait a moment
    print("⏳ Waiting 2 seconds...")
    time.sleep(2)
    
    # Check status after logs
    status = get_log_status()
    print(f"\nStatus after logs: {status}")
    
    # Note about local logging
    print("\n📁 Local logging mode - logs are stored in logs/ directory")
    print("Check the logs/ folder for log files")
    
    # Final status
    status = get_log_status()
    print(f"\nFinal Status: {status}")
    
    print("\n✅ Local logging test completed!")
    print("Check the logs/ directory to see the log files.")

if __name__ == "__main__":
    test_local_logging()
