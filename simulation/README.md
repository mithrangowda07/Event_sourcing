# Temperature Sensor Simulation Server (Part A)

This is the Raspberry Pi temperature sensor simulation server that generates realistic temperature readings and sends data to ThingSpeak cloud service.

## 🌟 Features

- Simulates realistic temperature sensor readings (20°C - 40°C)
- On/Off toggle control via web interface
- Real-time temperature display
- Automatic cloud data transfer to ThingSpeak every 15 seconds
- Local API endpoint for direct data access
- Background thread processing for responsive web interface
- Identity verification system for secure local access

## 🚀 Quick Start

### Prerequisites
- Python 3.7 or higher
- Raspberry Pi (recommended) or any computer
- ThingSpeak account and API keys

### Installation

1. **Navigate to the simulation directory**
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure the application:**
   - Update API keys and configuration in `sensor_server.py`

## ⚙️ Configuration

Update these variables at the top of `sensor_server.py`:

```python
THINGSPEAK_API_KEY = "YOUR_THINGSPEAK_WRITE_API_KEY"  # Your ThingSpeak write API key
THINGSPEAK_CHANNEL_ID = "YOUR_CHANNEL_ID"              # Your ThingSpeak channel ID
USER_ID = "RASPBERRY_PI_SENSOR_2024"                   # Identity key (keep default or customize)
SENSOR_NAME = "Raspberry Pi Temperature Sensor"         # Display name for the sensor
TEMP_MIN = 20.0                                         # Minimum temperature in Celsius
TEMP_MAX = 40.0                                         # Maximum temperature in Celsius
UPDATE_INTERVAL = 15                                    # Seconds between cloud updates
```

## 🏃‍♂️ Running the Server

1. **Navigate to the simulation directory**
2. **Run the sensor server:**
   ```bash
   python sensor_server.py
   ```

The sensor server will:
- Start on port 5000
- Display configuration information
- Show real-time status updates
- Be accessible at `http://<raspberry_pi_ip>:5000`

## 🌐 Web Interface

### Sensor Dashboard
- **URL:** `http://<raspberry_pi_ip>:5000`
- **Features:** Start/Stop sensor, real-time temperature, cloud status

## 🔧 How It Works

### Temperature Generation
- Generates realistic temperature readings with small variations
- Maintains temperature within configured bounds
- Updates every 15 seconds when active

### Cloud Integration
- Automatically sends temperature data to ThingSpeak
- Includes timestamp with each reading
- Handles connection errors gracefully

### Local API
- Provides `/data` endpoint for local clients
- Includes `/api/verify` for identity verification
- Supports CORS for local network access

## 📊 ThingSpeak Integration

### Channel Configuration
- **Field 1:** Temperature (Celsius)
- **Field 2:** Timestamp
- **Update interval:** 15 seconds (when sensor active)

## 🔄 Customization

### Temperature Range
```python
TEMP_MIN = 20.0  # Minimum temperature
TEMP_MAX = 40.0  # Maximum temperature
```

### Update Intervals
```python
UPDATE_INTERVAL = 15  # Seconds between cloud updates
```

## 🔒 Security Features

- **Identity Verification:** USER_ID must match between servers
- **Network Isolation:** Local access only on same network
- **CORS Support:** Secure cross-origin requests
- **Timeout Protection:** Prevents hanging connections

## 🐛 Troubleshooting

### Common Issues

1. **"Failed to send to ThingSpeak"**
   - Verify ThingSpeak API key
   - Check internet connectivity
   - Ensure channel ID is correct

2. **Port conflicts**
   - Change port in configuration if needed
   - Ensure no other services use port 5000

### Debug Mode

To enable debug mode, change the last line in `sensor_server.py`:

```python
# Change from:
app.run(host='0.0.0.0', port=5000, debug=False)

# To:
app.run(host='0.0.0.0', port=5000, debug=True)
```

## 📁 File Structure

```
simulation/
├── sensor_server.py          # Main sensor simulation server
├── requirements.txt          # Python dependencies
├── README.md                # This file
└── templates/               # HTML templates
    └── sensor_dashboard.html # Sensor control interface
```

---

**Part of the complete Temperature Monitoring System** 🌡️📊
