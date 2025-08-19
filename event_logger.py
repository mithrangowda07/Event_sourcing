#!/usr/bin/env python3
"""
Event Logger Module
Provides logging functionality for sensor events, errors, and data events.
Local logging with AI monitoring capabilities.
"""

import os
import json
from datetime import datetime
from typing import Optional

# Create logs directory if it doesn't exist
LOGS_DIR = "logs"
if not os.path.exists(LOGS_DIR):
    os.makedirs(LOGS_DIR)

def _write_log_entry(log_type: str, data: dict):
    """Write a log entry to the appropriate log file."""
    timestamp = datetime.now().isoformat()
    log_entry = {
        "timestamp": timestamp,
        "type": log_type,
        **data
    }
    
    # Create filename based on log type
    filename = f"{LOGS_DIR}/{log_type}_events.log"
    
    try:
        # Write to local file
        with open(filename, 'a', encoding='utf-8') as f:
            f.write(json.dumps(log_entry) + '\n')
    except Exception as e:
        print(f"Error writing to log file {filename}: {e}")

def log_sensor_event(event_type: str, description: str, additional_data: Optional[dict] = None):
    """
    Log sensor events (on/off, status changes, etc.)
    
    Args:
        event_type: Type of sensor event (e.g., 'sensor_on', 'sensor_off')
        description: Human-readable description of the event
        additional_data: Optional additional data to include
    """
    data = {
        "event_type": event_type,
        "description": description
    }
    
    if additional_data:
        data.update(additional_data)
    
    _write_log_entry("sensor", data)
    print(f"[SENSOR] {event_type}: {description}")

def log_error_event(component: str, error_message: str, additional_data: Optional[dict] = None):
    """
    Log error events from any component.
    
    Args:
        component: Component that generated the error (e.g., 'sensor', 'ui')
        error_message: Description of the error
        additional_data: Optional additional error data
    """
    data = {
        "component": component,
        "error_message": error_message
    }
    
    if additional_data:
        data.update(additional_data)
    
    _write_log_entry("error", data)
    print(f"[ERROR] {component}: {error_message}")

def log_data_event(component: str, event_type: str, description: str, additional_data: Optional[dict] = None):
    """
    Log data-related events (uploads, requests, etc.)
    
    Args:
        component: Component that generated the event (e.g., 'sensor', 'ui')
        event_type: Type of data event (e.g., 'cloud_upload', 'local_api_request')
        description: Human-readable description of the event
        additional_data: Optional additional data to include
    """
    data = {
        "component": component,
        "event_type": event_type,
        "description": description
    }
    
    if additional_data:
        data.update(additional_data)
    
    _write_log_entry("data", data)
    print(f"[DATA] {component}.{event_type}: {description}")

def force_upload_logs():
    """Local logging function (no cloud upload)."""
    print("ℹ️  Local logging enabled - logs stored in logs/ directory")

def get_log_status():
    """Get current logging status and configuration."""
    return {
        "logging_enabled": True,
        "storage_mode": "local",
        "logs_directory": LOGS_DIR,
        "log_files": ["sensor_events.log", "error_events.log", "data_events.log"]
    }
