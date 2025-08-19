#!/usr/bin/env python3
"""
Test script for AI integration with local logging
Demonstrates how Gemini AI analyzes system logs
"""

import time
from event_logger import log_sensor_event, log_error_event, log_data_event
from ai_monitor import ai_monitor

def test_ai_integration():
    """Test the AI integration with local logging."""
    print("🧪 Testing AI Integration with Local Logs")
    print("=" * 60)
    
    # Check AI monitor status
    status = ai_monitor.get_system_status()
    print(f"AI Monitor Status: {status}")
    
    # Generate some test logs to analyze
    print("\n📝 Generating test logs for AI analysis...")
    
    # Simulate normal operation
    log_sensor_event('test_start', 'AI integration test started')
    log_data_event('test', 'data_generated', 'Test temperature data: 25.5°C')
    log_data_event('test', 'api_request', 'Test API request processed')
    
    # Simulate some errors
    log_error_event('test', 'Simulated connection timeout')
    log_error_event('test', 'API response delay detected')
    
    # Simulate sensor events
    log_sensor_event('sensor_on', 'Test sensor activated')
    log_data_event('sensor', 'reading_generated', 'Temperature reading: 26.2°C')
    
    # Wait for logs to be written
    print("⏳ Waiting 3 seconds for logs to be processed...")
    time.sleep(3)
    
    # Trigger AI analysis
    print("\n🔍 Triggering AI analysis...")
    ai_monitor.analyze_system_logs()
    
    # Test AI chat
    print("\n💬 Testing AI chat functionality...")
    chat_response = ai_monitor.chat_with_ai("What issues do you detect in the recent logs?")
    print(f"AI Response: {chat_response}")
    
    # Test another chat query
    print("\n💬 Testing another chat query...")
    chat_response2 = ai_monitor.chat_with_ai("How is the overall system health?")
    print(f"AI Response: {chat_response2}")
    
    print("\n✅ AI integration test completed!")
    print("Check the AI dashboard at http://localhost:5002 for the full interface")

if __name__ == "__main__":
    test_ai_integration()
