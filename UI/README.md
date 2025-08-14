# Temperature Monitoring User Interface (Part B)

This is the user interface server that displays temperature data from either local sensor or ThingSpeak cloud, with intelligent fallback logic.

## 🌟 Features

- Local-first data fetching logic
- Automatic fallback to cloud data when local unavailable
- Network detection and identity verification
- Real-time temperature display with auto-refresh
- Data source indicator (Local vs Cloud)
- Responsive Bootstrap-based interface
- Error handling and status monitoring

## 🚀 Quick Start

### Prerequisites
- Python 3.7 or higher
- Any computer (desktop, laptop, etc.)
- ThingSpeak account and read API key
- Sensor server running (for local access)

### Installation

1. **Navigate to the UI directory**
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure the application:**
   - Update API keys and configuration in `ui_server.py`

## ⚙️ Configuration

Update these variables at the top of `ui_server.py`:

```python
USER_ID = "RASPBERRY_PI_SENSOR_2024"                   # Must match sensor server USER_ID
LOCAL_SENSOR_IP = "192.168.1.100"                       # Your Raspberry Pi's local IP address
LOCAL_SENSOR_PORT = 5000                                # Sensor server port (default: 5000)
THINGSPEAK_READ_KEY = "YOUR_THINGSPEAK_READ_API_KEY"   # Your ThingSpeak read API key
THINGSPEAK_CHANNEL_ID = "YOUR_CHANNEL_ID"              # Your ThingSpeak channel ID
```

## 🏃‍♂️ Running the Server

1. **Navigate to the UI directory**
2. **Run the UI server:**
   ```bash
   python ui_server.py
   ```

The UI server will:
- Start on port 5001
- Display network configuration
- Be accessible at `http://localhost:5001`

## 🌐 Web Interface

### User Interface Dashboard
- **URL:** `http://localhost:5001`
- **Features:** Temperature display, data source indicator, network status

## 🔧 How It Works

### Local vs Cloud Logic

1. **Network Detection:** Checks if on same network as sensor
2. **Identity Verification:** Verifies USER_ID match with sensor
3. **Local Fetch:** Attempts to get data from local sensor API
4. **Cloud Fallback:** If local fails, fetches from ThingSpeak
5. **Real-time Updates:** Refreshes every 10 seconds with latest data

### Data Flow

```
UI Server (Any Computer)
├── Checks network and identity
├── Fetches from local sensor if available
├── Falls back to ThingSpeak if local unavailable
└── Displays data with source indication
```

## 📱 Interface Features

### Temperature Display
- Large temperature display with source indicator
- Real-time updates with auto-refresh
- Timestamp of last reading
- Data source indication (Local vs Cloud)

### Network Status
- Local IP address display
- Sensor IP address display
- Network connectivity status
- User ID verification status

### Controls
- Manual refresh button
- Auto-refresh toggle (every 10 seconds)
- Error and success notifications

## 🔒 Security Features

- **Identity Verification:** USER_ID must match sensor server
- **Network Isolation:** Local access only on same network
- **CORS Support:** Secure cross-origin requests
- **Timeout Protection:** Prevents hanging connections

## 🐛 Troubleshooting

### Common Issues

1. **"Local server unreachable"**
   - Check if sensor server is running
   - Verify IP address and port
   - Ensure both devices are on same network

2. **"Identity verification failed"**
   - Verify USER_ID matches in both files
   - Check network connectivity
   - Restart both servers

3. **"Cloud fetch failed"**
   - Verify ThingSpeak API keys
   - Check internet connectivity
   - Ensure channel ID is correct

### Debug Mode

To enable debug mode, change the last line in `ui_server.py`:

```python
# Change from:
app.run(host='0.0.0.0', port=5001, debug=False)

# To:
app.run(host='0.0.0.0', port=5001, debug=True)
```

## 📊 ThingSpeak Integration

### Reading Data
- Fetches latest temperature from ThingSpeak channel
- Uses read API key (not write key)
- Gets most recent feed entry
- Handles connection errors gracefully

## 🔄 Customization

### Update Intervals
```python
# In UI dashboard: 10 seconds auto-refresh
# Can be modified in the JavaScript code
```

### Network Detection
The system automatically detects if devices are on the same network by comparing IP subnets (e.g., 192.168.x.x).

## 📁 File Structure

```
UI/
├── ui_server.py              # Main user interface server
├── requirements.txt          # Python dependencies
├── README.md                # This file
└── templates/               # HTML templates
    └── ui_dashboard.html    # Temperature display interface
```

---

**Part of the complete Temperature Monitoring System** 🌡️📊
