#!/usr/bin/env python3
"""
Temperature Monitoring User Interface Server
Part B: Flask application that displays temperature data from either
local Flask API or ThingSpeak cloud, depending on availability.
"""

import os
import json
import time
import socket
import requests
from datetime import datetime
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configuration - Load from environment variables
USER_ID = os.getenv("USER_ID", "RASPBERRY_PI_SENSOR_2024")
LOCAL_SENSOR_IP = os.getenv("LOCAL_SENSOR_IP", "0.0.0.0")
LOCAL_SENSOR_PORT = int(os.getenv("LOCAL_SENSOR_PORT", "5000"))
THINGSPEAK_READ_KEY = os.getenv("THINGSPEAK_READ_API_KEY", "YOUR_THINGSPEAK_READ_API_KEY")
THINGSPEAK_CHANNEL_ID = os.getenv("THINGSPEAK_CHANNEL_ID", "YOUR_CHANNEL_ID")
THINGSPEAK_FIELD = os.getenv("THINGSPEAK_FIELD", "field1")
UI_PORT = int(os.getenv("UI_PORT", "5001"))

# Flask app initialization
app = Flask(__name__)
CORS(app)

def get_local_ip():
    """Get the local IP address of this machine."""
    try:
        # Connect to a remote address to determine local IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception:
        return "127.0.0.1"

def is_same_network(local_ip, sensor_ip):
    """Check if two IPs are on the same network (same subnet)."""
    try:
        local_parts = local_ip.split('.')
        sensor_parts = sensor_ip.split('.')
        
        # Check if they're both private IPs and in same subnet (first 3 octets)
        if (len(local_parts) == 4 and len(sensor_parts) == 4 and
            local_parts[0] == sensor_parts[0] and
            local_parts[1] == sensor_parts[1] and
            local_parts[2] == sensor_parts[2]):
            return True
        return False
    except Exception:
        return False

def verify_local_identity():
    """Verify identity with the local sensor server."""
    try:
        url = f"http://{LOCAL_SENSOR_IP}:{LOCAL_SENSOR_PORT}/api/verify"
        data = {"user_id": USER_ID}
        
        response = requests.post(url, json=data, timeout=5)
        
        if response.status_code == 200:
            result = response.json()
            return result.get('verified', False)
        return False
        
    except Exception as e:
        print(f"Local identity verification failed: {str(e)}")
        return False

def fetch_local_temperature():
    """Fetch temperature data from local sensor server."""
    try:
        url = f"http://{LOCAL_SENSOR_IP}:{LOCAL_SENSOR_PORT}/data"
        
        response = requests.get(url, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            return {
                'temperature': data.get('temperature'),
                'timestamp': data.get('timestamp'),
                'source': 'local',
                'sensor_name': data.get('sensor_name', 'Local Sensor'),
                'success': True
            }
        else:
            return {'success': False, 'error': f'HTTP {response.status_code}'}
            
    except requests.exceptions.Timeout:
        return {'success': False, 'error': 'Local server timeout'}
    except requests.exceptions.ConnectionError:
        return {'success': False, 'error': 'Local server unreachable'}
    except Exception as e:
        return {'success': False, 'error': str(e)}

def fetch_cloud_temperature():
    """Fetch temperature data from ThingSpeak cloud service."""
    try:
        url = f"https://api.thingspeak.com/channels/{THINGSPEAK_CHANNEL_ID}/feeds.json"
        params = {
            'api_key': THINGSPEAK_READ_KEY,
            'results': 1  # Get only the latest reading
        }
        
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            feeds = data.get('feeds', [])
            
            if feeds:
                latest_feed = feeds[0]
                temperature = latest_feed.get(THINGSPEAK_FIELD)
                timestamp = latest_feed.get('created_at')
                
                if temperature is not None:
                    return {
                        'temperature': float(temperature),
                        'timestamp': timestamp,
                        'source': 'cloud',
                        'sensor_name': 'ThingSpeak Cloud',
                        'success': True
                    }
            
            return {'success': False, 'error': 'No temperature data in channel'}
        else:
            return {'success': False, 'error': f'HTTP {response.status_code}'}
            
    except requests.exceptions.Timeout:
        return {'success': False, 'error': 'Cloud server timeout'}
    except requests.exceptions.ConnectionError:
        return {'success': False, 'error': 'Cloud server unreachable'}
    except Exception as e:
        return {'success': False, 'error': str(e)}

def get_temperature_data():
    """Get temperature data with local-first logic."""
    local_ip = get_local_ip()
    
    # Check if we're on the same network as the sensor
    if is_same_network(local_ip, LOCAL_SENSOR_IP):
        print(f"🌐 Same network detected: {local_ip} and {LOCAL_SENSOR_IP}")
        
        # Try to verify identity and fetch local data
        if verify_local_identity():
            print("✅ Identity verified, attempting local fetch")
            local_data = fetch_local_temperature()
            
            if local_data.get('success'):
                print("📡 Local data fetch successful")
                return local_data
            else:
                print(f"⚠️ Local fetch failed: {local_data.get('error')}")
        else:
            print("❌ Identity verification failed")
    else:
        print(f"🌐 Different network: {local_ip} vs {LOCAL_SENSOR_IP}")
    
    # Fall back to cloud data
    print("☁️ Falling back to cloud data")
    cloud_data = fetch_cloud_temperature()
    
    if cloud_data.get('success'):
        print("☁️ Cloud data fetch successful")
    else:
        print(f"❌ Cloud fetch failed: {cloud_data.get('error')}")
    
    return cloud_data

# Flask Routes

@app.route('/')
def dashboard():
    """Main dashboard page."""
    return render_template('ui_dashboard.html')

@app.route('/fetch')
def fetch_data():
    """AJAX endpoint to get temperature data."""
    data = get_temperature_data()
    
    if data.get('success'):
        # Format timestamp for display
        if data.get('timestamp'):
            try:
                if isinstance(data['timestamp'], str):
                    # Parse ISO format timestamp
                    dt = datetime.fromisoformat(data['timestamp'].replace('Z', '+00:00'))
                    data['formatted_timestamp'] = dt.strftime('%Y-%m-%d %H:%M:%S')
                else:
                    data['formatted_timestamp'] = str(data['timestamp'])
            except Exception:
                data['formatted_timestamp'] = str(data['timestamp'])
        else:
            data['formatted_timestamp'] = 'Unknown'
        
        return jsonify(data)
    else:
        return jsonify({
            'success': False,
            'error': data.get('error', 'Unknown error'),
            'source': 'none',
            'temperature': None,
            'timestamp': None,
            'formatted_timestamp': 'Error'
        })

@app.route('/api/status')
def get_status():
    """Get system status and configuration."""
    local_ip = get_local_ip()
    same_network = is_same_network(local_ip, LOCAL_SENSOR_IP)
    
    return jsonify({
        'local_ip': local_ip,
        'sensor_ip': LOCAL_SENSOR_IP,
        'same_network': same_network,
        'user_id': USER_ID,
        'cloud_channel': THINGSPEAK_CHANNEL_ID
    })

if __name__ == '__main__':
    print("🖥️  Temperature Monitoring User Interface Server")
    print("=" * 60)
    print(f"🔑 User ID: {USER_ID}")
    print(f"📡 Local Sensor IP: {LOCAL_SENSOR_IP}:{LOCAL_SENSOR_PORT}")
    print(f"☁️ ThingSpeak Channel ID: {THINGSPEAK_CHANNEL_ID}")
    print(f"🌐 Local IP: {get_local_ip()}")
    print(f"🌐 Server Port: {UI_PORT}")
    print("=" * 60)
    
    # Check if API keys are still placeholders
    if THINGSPEAK_READ_KEY == "YOUR_THINGSPEAK_READ_API_KEY":
        print("⚠️  WARNING: THINGSPEAK_READ_API_KEY not set in .env file!")
        print("   Update the .env file with your actual ThingSpeak read API key")
    else:
        print("✅ ThingSpeak read API key configured")
    
    if THINGSPEAK_CHANNEL_ID == "YOUR_CHANNEL_ID":
        print("⚠️  WARNING: THINGSPEAK_CHANNEL_ID not set in .env file!")
        print("   Update the .env file with your actual ThingSpeak channel ID")
    else:
        print("✅ ThingSpeak channel ID configured")
    
    print("=" * 60)
    
    # Start Flask app
    app.run(host='0.0.0.0', port=UI_PORT, debug=False)
