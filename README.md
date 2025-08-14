# Raspberry Pi Temperature Sensor System

A complete Flask-based temperature monitoring system with local and cloud data transfer capabilities. The system consists of two main components organized in separate directories:

1. **Simulation** (Part A): Temperature sensor simulation server with cloud integration
2. **UI** (Part B): User interface server with intelligent local/cloud data fetching

## 🌟 System Overview

### Simulation Server (Part A)
- Simulates realistic temperature sensor readings (20°C - 40°C)
- On/Off toggle control via web interface
- Real-time temperature display
- Automatic cloud data transfer to ThingSpeak every 15 seconds
- Local API endpoint for direct data access
- Background thread processing for responsive web interface
- Identity verification system for secure local access

### User Interface Server (Part B)
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
- Raspberry Pi (for simulation server) or any computer
- ThingSpeak account and API keys
- Both devices on the same Wi-Fi network (for local access)

### Installation

1. **Clone or download the project files**
2. **Install dependencies for each component:**

   **For Simulation Server:**
   ```bash
   cd simulation
   pip install -r requirements.txt
   ```

   **For UI Server:**
   ```bash
   cd UI
   pip install -r requirements.txt
   ```

3. **Configure the system using .env file:**
   ```bash
   # Copy the example configuration
   cp .env.example .env
   
   # Edit .env file with your actual values
   # Update API keys, channel ID, and IP addresses
   ```

## ⚙️ Configuration

### Environment Variables (.env file)

The system now uses a `.env` file for all configuration. Create this file by copying `.env.example`:

```bash
cp .env.example .env
```

Then edit `.env` with your actual values:

```env
# Identity and Security
USER_ID=RASPBERRY_PI_SENSOR_2024

# Network Configuration
LOCAL_SENSOR_IP=192.168.1.107
LOCAL_SENSOR_PORT=5000

# ThingSpeak Configuration
THINGSPEAK_WRITE_API_KEY=YOUR_ACTUAL_THINGSPEAK_WRITE_API_KEY
THINGSPEAK_READ_API_KEY=YOUR_ACTUAL_THINGSPEAK_READ_API_KEY
THINGSPEAK_CHANNEL_ID=YOUR_ACTUAL_CHANNEL_ID
THINGSPEAK_FIELD=field1

# Sensor Configuration
SENSOR_NAME=Raspberry Pi Temperature Sensor
TEMP_MIN=20.0
TEMP_MAX=40.0
UPDATE_INTERVAL=15

# Server Ports
SIMULATION_PORT=5000
UI_PORT=5001
```

### Required Configuration Values

**Essential (must be set):**
- `THINGSPEAK_WRITE_API_KEY` - Your ThingSpeak write API key
- `THINGSPEAK_READ_API_KEY` - Your ThingSpeak read API key  
- `THINGSPEAK_CHANNEL_ID` - Your ThingSpeak channel ID
- `LOCAL_SENSOR_IP` - Your local IP address (e.g., 192.168.1.107)

**Optional (have sensible defaults):**
- `USER_ID` - Identity key (default: RASPBERRY_PI_SENSOR_2024)
- `SENSOR_NAME` - Display name for the sensor
- `TEMP_MIN/MAX` - Temperature range (default: 20°C - 40°C)
- `UPDATE_INTERVAL` - Cloud update frequency (default: 15 seconds)
- `SIMULATION_PORT/UI_PORT` - Server ports (default: 5000/5001)

## 🏃‍♂️ Running the System

### Option 1: Use Startup Script (Recommended)

1. **Configure your .env file first**
2. **Run the startup script:**
   ```bash
   python start_system.py
   ```

The startup script will:
- ✅ Check if .env file exists and is configured
- ✅ Verify all dependencies are installed
- ✅ Launch both servers simultaneously
- ✅ Provide clear error messages if configuration is missing

### Option 2: Run Separately

1. **Start the Simulation Server (Raspberry Pi):**
   ```bash
   cd simulation
   python sensor_server.py
   ```

2. **Start the UI Server (Any Computer):**
   ```bash
   cd UI
   python ui_server.py
   ```

## 🌐 Accessing the Interfaces

### Simulation Dashboard
- **URL:** `http://<raspberry_pi_ip>:5000`
- **Features:** Start/Stop sensor, real-time temperature, cloud status

### User Interface Dashboard
- **URL:** `http://localhost:5001`
- **Features:** Temperature display, data source indicator, network status

## 🔧 How It Works

### Local vs Cloud Logic

1. **Network Detection:** UI server checks if it's on the same network as the simulation server
2. **Identity Verification:** If same network, verifies USER_ID match
3. **Local Fetch:** Attempts to get data from local simulation API
4. **Cloud Fallback:** If local fails, automatically fetches from ThingSpeak
5. **Real-time Updates:** UI refreshes every 10 seconds with latest data

### Data Flow

```
Simulation Server (Raspberry Pi)
├── Generates temperature readings every 15 seconds
├── Sends data to ThingSpeak cloud
└── Provides local API endpoint (/data)

UI Server (Any Computer)
├── Checks network and identity
├── Fetches from local simulation if available
├── Falls back to ThingSpeak if local unavailable
└── Displays data with source indication
```

## 📱 Web Interface Features

### Simulation Dashboard
- Large temperature display
- Start/Stop controls
- Real-time status updates
- Cloud integration status
- System information

### UI Dashboard
- Temperature display with source indicator
- Network status monitoring
- Auto-refresh controls
- Error handling and notifications
- Responsive design for mobile/desktop

## 🔒 Security Features

- **Identity Verification:** USER_ID must match between servers
- **Network Isolation:** Local access only on same network
- **CORS Support:** Secure cross-origin requests
- **Timeout Protection:** Prevents hanging connections
- **Environment Variables:** Sensitive data stored in .env file (not in code)

## 🐛 Troubleshooting

### Common Issues

1. **"❌ .env file not found!"**
   - Copy `.env.example` to `.env`
   - Update `.env` with your actual values

2. **"⚠️ Some environment variables are not configured"**
   - Check that all required variables in `.env` are set
   - Ensure API keys and channel ID are not placeholder values

3. **"Local server unreachable"**
   - Check if simulation server is running
   - Verify `LOCAL_SENSOR_IP` in `.env` is correct
   - Ensure both devices are on same network

4. **"Identity verification failed"**
   - Verify `USER_ID` matches in both servers
   - Check network connectivity
   - Restart both servers

5. **"Cloud fetch failed"**
   - Verify ThingSpeak API keys in `.env`
   - Check internet connectivity
   - Ensure channel ID is correct

### Debug Mode

To enable debug mode, modify the last line in both Python files:

```python
# Change from:
app.run(host='0.0.0.0', port=5000, debug=False)

# To:
app.run(host='0.0.0.0', port=5000, debug=True)
```

## 📊 ThingSpeak Integration

### Setting Up ThingSpeak

1. **Create a ThingSpeak account** at [thingspeak.com](https://thingspeak.com)
2. **Create a new channel** for temperature data
3. **Get your API keys:**
   - Write API key (for simulation server)
   - Read API key (for UI server)
4. **Note your channel ID**

### Channel Configuration

- **Field 1:** Temperature (Celsius)
- **Field 2:** Timestamp
- **Update interval:** 15 seconds (when sensor active)

## 🔄 Customization

### Temperature Range
Modify these values in `.env`:
```env
TEMP_MIN=20.0  # Minimum temperature
TEMP_MAX=40.0  # Maximum temperature
```

### Update Intervals
```env
UPDATE_INTERVAL=15      # Simulation to cloud (seconds)
# In UI dashboard: 10 seconds auto-refresh
```

### Network Detection
The system automatically detects if devices are on the same network by comparing IP subnets (e.g., 192.168.x.x).

## 📁 Project Structure

```
temperature-sensor-system/
├── .env                    # Configuration file (create from .env.example)
├── .env.example           # Example configuration template
├── simulation/                    # Part A: Temperature sensor simulation
│   ├── sensor_server.py          # Main simulation server
│   ├── requirements.txt          # Python dependencies
│   ├── README.md                # Simulation-specific documentation
│   └── templates/               # HTML templates
│       └── sensor_dashboard.html # Sensor control interface
├── UI/                          # Part B: User interface server
│   ├── ui_server.py             # Main UI server
│   ├── requirements.txt          # Python dependencies
│   ├── README.md                # UI-specific documentation
│   └── templates/               # HTML templates
│       └── ui_dashboard.html    # Temperature display interface
├── requirements.txt              # Main dependencies file
├── README.md                    # This main documentation
└── start_system.py              # Startup script with .env validation
```

## 🚀 Alternative Startup

You can also use the startup script to launch both servers:

```bash
python start_system.py
```

This will start both the simulation server and UI server simultaneously with proper configuration validation.

## 🤝 Contributing

Feel free to submit issues, feature requests, or pull requests to improve the system.

## 📄 License

This project is open source and available under the MIT License.

## 🆘 Support

If you encounter issues:

1. Check the troubleshooting section above
2. Verify your `.env` file is properly configured
3. Ensure network connectivity between devices
4. Check console output for error messages
5. Verify ThingSpeak API keys and channel configuration
6. Check the individual README files in each directory for specific guidance

---

**Happy Monitoring! 🌡️📊**
