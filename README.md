# 🌡️ Temperature Monitoring System with AI-Powered Error Management & Email Notifications

A comprehensive IoT temperature monitoring system with advanced AI-powered error detection, correction, self-healing capabilities, and automated email reporting. The system automatically detects errors, pauses servers, displays correction code in the terminal, provides intelligent fixes using Gemini AI, and sends analysis reports via email.

## 📋 Table of Contents

- [Overview](#overview)
- [System Architecture](#system-architecture)
- [Core Features](#core-features)
- [Email Notification System](#email-notification-system)
- [Event Generation & Logging](#event-generation--logging)
- [AI Error Detection & Scanning](#ai-error-detection--scanning)
- [Error Management System](#error-management-system)
- [Server Management](#server-management)
- [Installation & Setup](#installation--setup)
- [Usage Guide](#usage-guide)
- [API Documentation](#api-documentation)
- [Configuration](#configuration)
- [System Properties](#system-properties)
- [Troubleshooting](#troubleshooting)
- [Advanced Features](#advanced-features)
- [Contributing](#contributing)
- [License](#license)

## 🎯 Overview

This system provides a complete IoT temperature monitoring solution with the following key capabilities:

- **Real-time Temperature Monitoring**: Simulates Raspberry Pi temperature sensors with cloud integration
- **AI-Powered Error Detection**: Automatically scans code and logs for errors using Gemini AI
- **Intelligent Error Correction**: Generates and displays correction code in terminal
- **Email Notification System**: Automated email reports of AI analysis results with professional formatting
- **Server Pause/Resume**: Automatically pauses all servers during error correction
- **Self-Healing Capabilities**: Can automatically fix detected errors
- **Web Dashboards**: Multiple web interfaces for monitoring and control
- **Event Logging**: Comprehensive logging system for all system events

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    Temperature Monitoring System                │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐            │
│  │ Simulation  │  │ UI Server   │  │ AI Chat     │            │
│  │ Server      │  │ (Port 5001) │  │ Server      │            │
│  │ (Port 5000) │  │             │  │ (Port 5002) │            │
│  └─────────────┘  └─────────────┘  └─────────────┘            │
│         │                 │                 │                  │
│         └─────────────────┼─────────────────┘                  │
│                           │                                    │
│  ┌─────────────────────────────────────────────────────────────┤
│  │              Event Logger & AI Monitor                     │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │  │ Sensor      │  │ Error       │  │ Data        │        │
│  │  │ Events      │  │ Events      │  │ Events      │        │
│  │  │ Log         │  │ Log         │  │ Log         │        │
│  │  └─────────────┘  └─────────────┘  └─────────────┘        │
│  └─────────────────────────────────────────────────────────────┤
│                           │                                    │
│  ┌─────────────────────────────────────────────────────────────┤
│  │              Error Management System                       │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │  │ Error       │  │ Terminal    │  │ Server      │        │
│  │  │ Detection   │  │ Interface   │  │ Manager     │        │
│  │  └─────────────┘  └─────────────┘  └─────────────┘        │
│  └─────────────────────────────────────────────────────────────┤
│                           │                                    │
│  ┌─────────────────────────────────────────────────────────────┤
│  │              AI Integration (Gemini)                       │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │  │ Code        │  │ Error       │  │ System      │        │
│  │  │ Analysis    │  │ Correction  │  │ Monitoring  │        │
│  │  └─────────────┘  └─────────────┘  └─────────────┘        │
│  └─────────────────────────────────────────────────────────────┤
│                           │                                    │
│  ┌─────────────────────────────────────────────────────────────┤
│  │              Email Notification System                     │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │  │ SMTP        │  │ HTML        │  │ Analysis    │        │
│  │  │ Service     │  │ Templates   │  │ Reports     │        │
│  │  └─────────────┘  └─────────────┘  └─────────────┘        │
│  └─────────────────────────────────────────────────────────────┘
└─────────────────────────────────────────────────────────────────┘
```

## ✨ Core Features

### 🌡️ Temperature Monitoring
- **Real-time Sensor Simulation**: Generates realistic temperature readings
- **Cloud Integration**: Automatic upload to ThingSpeak IoT platform
- **Local Data Storage**: Maintains local temperature history
- **Web Dashboard**: Real-time temperature visualization
- **API Endpoints**: RESTful APIs for data access

### 🤖 AI-Powered Error Management
- **Automatic Error Detection**: Scans code, logs, and system processes
- **AI Code Analysis**: Uses Gemini AI for intelligent error analysis
- **Correction Code Generation**: AI generates fix suggestions
- **Terminal Error Display**: Clean interface showing only correction code
- **Server Pause/Resume**: Automatically manages server states during errors

### 🛡️ Self-Healing System
- **Automatic Fixes**: Can apply AI-generated corrections
- **Backup Management**: Creates backups before applying fixes
- **User Approval**: Requires user confirmation for critical changes
- **Rollback Capability**: Can restore from backups if needed

### 📊 Event Logging & Monitoring
- **Comprehensive Logging**: Tracks all system events
- **Real-time Monitoring**: Continuous system health monitoring
- **Log Analysis**: AI analyzes logs for patterns and issues
- **Alert System**: Notifies of critical issues

### 📧 Email Notification System
- **Automated Reports**: Send AI analysis results via email with one-click
- **Professional Formatting**: HTML emails with modern responsive design
- **Critical Issue Highlighting**: Color-coded status indicators for urgent issues
- **SMTP Integration**: Secure email delivery using TLS encryption
- **Multiple Provider Support**: Works with Gmail, Outlook, Yahoo, and custom SMTP servers
- **Plain Text Fallback**: Ensures compatibility across all email clients

## 📧 Email Notification System

### Overview
The email notification system allows administrators to receive AI analysis reports directly via email. This feature provides instant access to system health information and critical issue alerts, even when not actively monitoring the dashboard.

### Key Features

#### 1. One-Click Email Sending
- **Email Analysis Button**: Located in the AI controls section of the events page
- **Real-time Feedback**: Button shows loading state and provides success/error messages
- **Latest Analysis**: Always sends the most recent AI analysis results

#### 2. Professional Email Templates
- **HTML Formatting**: Modern, responsive email design with system branding
- **Status Indicators**: Color-coded headers (red for critical, green for healthy)
- **Structured Layout**: Clear sections for analysis results, timestamps, and system info
- **Mobile Responsive**: Optimized for viewing on all devices

#### 3. SMTP Configuration
- **Secure Connections**: Uses TLS encryption for email transmission
- **Multiple Providers**: Pre-configured for Gmail, Outlook, Yahoo Mail
- **Custom SMTP**: Supports any SMTP server configuration
- **App Password Support**: Secure authentication using app-specific passwords

#### 4. Email Content Structure
```
Subject: System Analysis Report - [Timestamp]

Header: System branding with timestamp
Status Badge: CRITICAL ISSUES DETECTED / SYSTEM HEALTHY
Analysis Content: Complete AI analysis with formatting
Footer: System information and contact details
```

### Configuration

Add these variables to your `.env` file:
```env
# Email Configuration
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SENDER_EMAIL=your-email@gmail.com
SENDER_PASSWORD=your-app-password
RECIPIENT_EMAIL=recipient@example.com
```

### Usage Workflow

1. **Trigger Analysis**: Click "Analyze" or start AI monitoring
2. **Send Email**: Click "Email Analysis" button in the UI
3. **Receive Report**: Professional email with analysis results
4. **Take Action**: Review critical issues and recommendations

### Security Features

- **Environment Variables**: Credentials stored securely in `.env` file
- **TLS Encryption**: All email transmissions are encrypted
- **App Passwords**: Supports secure app-specific authentication
- **No Hardcoded Secrets**: All sensitive data externalized

For detailed setup instructions, see [EMAIL_SETUP_GUIDE.md](EMAIL_SETUP_GUIDE.md).

## 📝 Event Generation & Logging

### Event Types

The system generates and logs three main types of events:

#### 1. Sensor Events (`sensor_events.log`)
```json
{
  "timestamp": "2024-01-15T14:30:25.123456",
  "type": "sensor",
  "event_type": "sensor_on",
  "description": "Temperature sensor simulation started"
}
```

**Generated when:**
- Sensor is activated/deactivated
- Temperature readings are generated
- Sensor status changes
- Configuration updates

#### 2. Error Events (`error_events.log`)
```json
{
  "timestamp": "2024-01-15T14:30:25.123456",
  "type": "error",
  "component": "sensor",
  "error_message": "ThingSpeak upload failed with status 401"
}
```

**Generated when:**
- API calls fail
- Network errors occur
- File system errors
- Configuration errors
- Server crashes

#### 3. Data Events (`data_events.log`)
```json
{
  "timestamp": "2024-01-15T14:30:25.123456",
  "type": "data",
  "component": "sensor",
  "event_type": "cloud_upload",
  "description": "Temperature 25.3°C sent to ThingSpeak"
}
```

**Generated when:**
- Data is uploaded to cloud
- Local API requests are made
- Data processing occurs
- Identity verification

### Event Generation Process

1. **Event Trigger**: System action occurs (sensor reading, error, data transfer)
2. **Event Creation**: Event object is created with timestamp and metadata
3. **Logging**: Event is written to appropriate log file
4. **Console Output**: Event is displayed in console with emoji indicators
5. **AI Analysis**: Events are analyzed by AI monitoring system

### Log File Structure

```
logs/
├── sensor_events.log    # Sensor-related events
├── error_events.log     # Error and exception events
└── data_events.log      # Data transfer and processing events
```

Each log file contains JSON-formatted entries, one per line, making it easy to parse and analyze.

## 🔍 AI Error Detection & Scanning

### AI Monitoring System

The AI monitoring system continuously analyzes the system for errors and issues:

#### 1. Code Syntax Scanning
```python
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
    
    return errors
```

#### 2. Log Analysis
```python
def _check_log_errors(self) -> List[Dict]:
    """Check log files for error entries."""
    errors = []
    
    for log_file in sim_log_dir.glob("*_events.log"):
        with open(log_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            for line in lines[-10:]:  # Check last 10 lines
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
    
    return errors
```

#### 3. Server Process Monitoring
```python
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
    
    return errors
```

### AI Analysis Process

1. **Data Collection**: Gathers recent logs, checks file syntax, monitors processes
2. **AI Processing**: Sends data to Gemini AI for analysis
3. **Issue Detection**: AI identifies problems, errors, and anomalies
4. **Severity Assessment**: Classifies issues by severity (Critical/High/Medium/Low)
5. **Recommendation Generation**: AI provides specific fix suggestions
6. **Action Triggering**: Triggers error management system for critical issues

### AI Prompt Engineering

The system uses carefully crafted prompts for different analysis types:

```python
prompt = f"""
Analyze this system log data for {analysis_type}:

{log_summary}

Please provide:
1. **Issues Detected**: List any problems, errors, or anomalies
2. **Severity Levels**: Rate each issue (Low/Medium/High/Critical)
3. **Root Causes**: Identify possible causes for each issue
4. **Recommendations**: Suggest specific actions to resolve issues
5. **System Health**: Overall system status (Good/Fair/Poor/Critical)
6. **Predictive Insights**: Any potential future issues to watch for

Format your response clearly with sections and bullet points.
"""
```

## 🛡️ Error Management System

### Error Detection Workflow

1. **System Starts**: All servers launch with error monitoring
2. **Continuous Monitoring**: System checks for errors every 5 seconds
3. **Error Detection**: When error is found:
   - All servers are paused
   - Terminal shows error details and correction code
   - User can review and apply fixes
4. **Recovery**: After fix is applied, servers resume automatically

### Error Classification

| Severity | Description | Action |
|----------|-------------|---------|
| **Critical** | Server crashes, system failures | Immediate pause, display correction |
| **High** | Syntax errors, major functionality issues | Pause, display correction |
| **Medium** | Log errors, minor issues | Log, monitor |
| **Low** | Warnings, informational messages | Log only |

### Terminal Error Interface

When an error is detected, the terminal displays:

```
================================================================================
🚨 CRITICAL ERROR DETECTED
================================================================================
⏰ Time: 2024-01-15 14:30:25
🔍 Error Type: syntax_error
⚠️  Severity: HIGH
📝 Message: Syntax error in sensor_server.py:45: invalid syntax
📁 File: simulation/sensor_server.py
📍 Line: 45
🔧 Component: sensor
================================================================================
🔧 AI-GENERATED CORRECTION CODE:
================================================================================
  1 | #!/usr/bin/env python3
  2 | """
  3 | Raspberry Pi Temperature Sensor Simulation Server
  4 | """
  5 | 
  6 | import os
  7 | import time
  8 | # ... corrected code continues ...
================================================================================
📋 INSTRUCTIONS:
================================================================================
1. 📖 Review the correction code above
2. ✏️  Apply the fix to the problematic file
3. ✅ Press ENTER to resume system monitoring
4. ❌ Press 'q' to quit the system
5. 🔄 Press 'r' to regenerate correction code
6. 📊 Press 's' to show system status
================================================================================
⏸️  All servers are currently PAUSED
================================================================================
```

### User Commands

- **ENTER**: Resume system monitoring
- **q**: Quit the system
- **r**: Regenerate correction code
- **s**: Show system status

## 🚀 Installation & Setup

### Prerequisites

- Python 3.8 or higher
- Internet connection (for AI features and cloud upload)
- ThingSpeak account (for cloud data storage)
- Gemini API key (for AI error correction)

### Step 1: Clone Repository

```bash
git clone <repository-url>
cd Event_sourcing
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

**Required packages:**
- `flask` - Web framework
- `flask-cors` - Cross-origin resource sharing
- `requests` - HTTP library
- `python-dotenv` - Environment variable management
- `google-generativeai` - Gemini AI integration

### Step 3: Environment Configuration

Create a `.env` file in the root directory:

```env
# ThingSpeak Configuration
THINGSPEAK_WRITE_API_KEY=your_write_api_key_here
THINGSPEAK_READ_API_KEY=your_read_api_key_here
THINGSPEAK_CHANNEL_ID=your_channel_id_here

# System Configuration
USER_ID=your_user_id_here
LOCAL_SENSOR_IP=your_local_ip_here

# AI Configuration
GEMINI_API_KEY=your_gemini_api_key_here
AI_VERBOSE=1
AI_MODEL=gemini-2.0-flash

# Server Ports
SIMULATION_PORT=5000
UI_PORT=5001
AI_CHAT_PORT=5002
```

### Step 4: Get API Keys

#### ThingSpeak Setup
1. Go to [ThingSpeak](https://thingspeak.com/)
2. Create a new channel
3. Get your Write API Key, Read API Key, and Channel ID
4. Add them to your `.env` file

#### Gemini AI Setup
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Add it to your `.env` file as `GEMINI_API_KEY`

### Step 5: Verify Installation

```bash
python demo_error_management.py
```

This will test all system components and verify everything is working correctly.

## 📖 Usage Guide

### Starting the System

#### Option 1: Full System with Error Management
```bash
python start_system_with_error_management.py
```

#### Option 2: Traditional Startup (Fallback)
```bash
python start_system.py
```

#### Option 3: Individual Components
```bash
# Start only simulation server
cd simulation && python sensor_server.py

# Start only UI server
cd UI && python ui_server.py

# Start only AI chat server
python ai_chat_server.py
```

### Accessing Web Interfaces

- **Simulation Dashboard**: http://localhost:5000
- **UI Dashboard**: http://localhost:5001
- **AI Chat Dashboard**: http://localhost:5002

### Error Management Workflow

1. **System Starts**: All servers launch with error monitoring
2. **Continuous Monitoring**: System checks for errors every 5 seconds
3. **Error Detection**: When error is found:
   - All servers are paused
   - Terminal shows error details and correction code
   - User can review and apply fixes
4. **Recovery**: After fix is applied, servers resume automatically

## 🔌 API Documentation

### Simulation Server API (Port 5000)

#### GET `/api/status`
Get current sensor status and latest temperature.

**Response:**
```json
{
  "active": true,
  "temperature": 25.3,
  "timestamp": "2024-01-15T14:30:25.123456",
  "sensor_name": "Raspberry Pi Temperature Sensor",
  "user_id": "RASPBERRY_PI_SENSOR_2024",
  "logging": {
    "logging_enabled": true,
    "storage_mode": "local",
    "logs_directory": "logs",
    "log_files": ["sensor_events.log", "error_events.log", "data_events.log"]
  }
}
```

#### POST `/api/start`
Start the temperature sensor simulation.

#### POST `/api/stop`
Stop the temperature sensor simulation.

#### GET `/data`
Get current temperature data for local UI clients.

#### POST `/api/verify`
Verify client identity for local access.

### AI Chat Server API (Port 5002)

#### POST `/api/chat`
Chat with AI about system status.

**Request:**
```json
{
  "message": "What errors are currently detected?"
}
```

**Response:**
```json
{
  "success": true,
  "user_message": "What errors are currently detected?",
  "ai_response": "Currently no critical errors detected...",
  "timestamp": "2024-01-15T14:30:25.123456"
}
```

#### GET `/api/status`
Get AI monitoring status.

#### POST `/api/analyze`
Trigger immediate AI analysis.

#### POST `/api/start-monitoring`
Start AI monitoring.

#### POST `/api/stop-monitoring`
Stop AI monitoring.

#### POST `/api/send-analysis-email`
Send latest AI analysis results via email.

**Response:**
```json
{
  "success": true,
  "message": "Analysis report sent successfully to recipient@example.com"
}
```

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `THINGSPEAK_WRITE_API_KEY` | ThingSpeak write API key | Yes | - |
| `THINGSPEAK_READ_API_KEY` | ThingSpeak read API key | Yes | - |
| `THINGSPEAK_CHANNEL_ID` | ThingSpeak channel ID | Yes | - |
| `USER_ID` | System user identifier | Yes | - |
| `LOCAL_SENSOR_IP` | Local sensor IP address | Yes | - |
| `GEMINI_API_KEY` | Gemini AI API key | Yes | - |
| `AI_VERBOSE` | Enable verbose AI output | No | 0 |
| `AI_MODEL` | Gemini model to use | No | gemini-2.0-flash |
| `SIMULATION_PORT` | Simulation server port | No | 5000 |
| `UI_PORT` | UI server port | No | 5001 |
| `AI_CHAT_PORT` | AI chat server port | No | 5002 |
| `TEMP_MIN` | Minimum temperature (°C) | No | 20.0 |
| `TEMP_MAX` | Maximum temperature (°C) | No | 40.0 |
| `UPDATE_INTERVAL` | Update interval (seconds) | No | 15 |
| `SMTP_SERVER` | SMTP server for email | No | smtp.gmail.com |
| `SMTP_PORT` | SMTP port for email | No | 587 |
| `SENDER_EMAIL` | Email sender address | No | - |
| `SENDER_PASSWORD` | Email sender password/app password | No | - |
| `RECIPIENT_EMAIL` | Email recipient address | No | - |

### Monitoring Intervals

- **Error Detection**: 5 seconds
- **AI Analysis**: 30 seconds
- **Log Collection**: 1 minute
- **Temperature Updates**: 15 seconds (configurable)

### Log Configuration

Log files are stored in the `logs/` directory:
- `sensor_events.log`: Sensor-related events
- `error_events.log`: Error and exception events
- `data_events.log`: Data transfer and processing events

## 🏗️ System Properties

### Core Components

#### 1. Simulation Server (`simulation/sensor_server.py`)
**Purpose**: Simulates Raspberry Pi temperature sensor with cloud integration
**Port**: 5000 (configurable via `SIMULATION_PORT`)
**Key Features**:
- Temperature reading generation (20-40°C range)
- ThingSpeak cloud upload integration
- Local API endpoints for data access
- Identity verification system
- Comprehensive event logging

**Dependencies**:
- Flask web framework
- Requests for HTTP calls
- Python-dotenv for configuration
- JSON for data serialization

#### 2. UI Server (`UI/ui_server.py`)
**Purpose**: Main web interface for system monitoring and control
**Port**: 5001 (configurable via `UI_PORT`)
**Key Features**:
- Temperature dashboard with real-time updates
- Events page with filtering and search
- AI chat interface integration
- Proxy endpoints for AI services
- Email functionality integration

**Templates**:
- `ui_dashboard.html`: Main temperature monitoring dashboard
- `events.html`: Comprehensive events viewer with AI chat

#### 3. AI Chat Server (`ai_chat_server.py`)
**Purpose**: AI-powered system monitoring and chat interface
**Port**: 5002 (configurable via `AI_CHAT_PORT`)
**Key Features**:
- Gemini AI integration for system analysis
- Real-time chat interface
- Analysis triggering and monitoring
- Email report generation
- System status reporting

#### 4. AI Monitor (`ai_monitor.py`)
**Purpose**: Core AI monitoring and analysis engine
**Key Features**:
- Continuous log analysis (30-second intervals)
- Error detection and classification
- AI-powered system health assessment
- Analysis result storage and retrieval
- Email integration for report sending

#### 5. Email Service (`email_service.py`)
**Purpose**: Professional email reporting system
**Key Features**:
- SMTP integration with TLS security
- HTML email templates with responsive design
- Critical issue highlighting
- Multiple email provider support
- Configuration validation and testing

#### 6. Error Management System (`error_manager.py`)
**Purpose**: Comprehensive error detection and handling
**Key Features**:
- Multi-level error classification
- Server pause/resume functionality
- Terminal interface for error display
- AI-powered error correction
- Backup and recovery management

#### 7. Self-Healing System (`self_healing_system.py`)
**Purpose**: Automated error correction and system recovery
**Key Features**:
- Automatic error detection
- AI-generated correction code
- User approval workflow
- Backup creation before fixes
- System state management

### System Architecture Layers

#### 1. Presentation Layer
- **Web Dashboards**: Real-time monitoring interfaces
- **Terminal Interface**: Error management and correction display
- **Email Reports**: Professional analysis notifications

#### 2. Application Layer
- **Flask Servers**: Web application framework
- **API Endpoints**: RESTful service interfaces
- **Event Handlers**: User interaction processing

#### 3. Business Logic Layer
- **AI Monitor**: System analysis and health assessment
- **Error Manager**: Error detection and classification
- **Email Service**: Report generation and delivery

#### 4. Data Layer
- **Event Logging**: JSON-formatted log files
- **Configuration**: Environment variable management
- **Backup Storage**: System state preservation

### Data Flow Architecture

```
Temperature Sensor → Event Logger → AI Monitor → Analysis Results
                                        ↓
Email Service ← Analysis Storage ← Error Manager ← Terminal Interface
     ↓
SMTP Server → Email Client (Administrator)
```

### Inter-Component Communication

#### 1. HTTP APIs
- **Internal**: Server-to-server communication via REST APIs
- **External**: ThingSpeak cloud integration
- **Client**: Web browser to server communication

#### 2. File System
- **Log Files**: JSON-formatted event storage
- **Configuration**: Environment variables via `.env`
- **Backups**: Automated file preservation

#### 3. Process Management
- **Threading**: Concurrent monitoring and analysis
- **Server Control**: Start/stop/pause functionality
- **Error Handling**: Graceful degradation and recovery

### Security Properties

#### 1. Authentication
- **API Keys**: Secure service authentication
- **Identity Verification**: Local network access control
- **App Passwords**: Email service security

#### 2. Data Protection
- **Environment Variables**: Secure credential storage
- **TLS Encryption**: Secure email transmission
- **Input Validation**: SQL injection and XSS prevention

#### 3. Access Control
- **Network Isolation**: Local vs cloud service separation
- **File Permissions**: Secure log and backup access
- **API Rate Limiting**: Service abuse prevention

### Performance Characteristics

#### 1. Monitoring Intervals
- **Error Detection**: 5 seconds
- **AI Analysis**: 30 seconds
- **Temperature Updates**: 15 seconds
- **Log Collection**: Real-time

#### 2. Resource Usage
- **Memory**: ~50MB per server process
- **CPU**: Low usage except during AI analysis
- **Disk**: Minimal (log files grow over time)
- **Network**: Periodic cloud uploads and email sending

#### 3. Scalability
- **Horizontal**: Multiple sensor support possible
- **Vertical**: Configurable analysis intervals
- **Cloud**: ThingSpeak handles data scaling

### Configuration Management

#### 1. Environment Variables
- **Centralized**: Single `.env` file configuration
- **Typed**: Automatic type conversion and validation
- **Defaulted**: Sensible defaults for optional settings

#### 2. Runtime Configuration
- **Dynamic**: Some settings changeable without restart
- **Persistent**: Configuration changes saved automatically
- **Validated**: Input validation and error reporting

### Error Handling Strategy

#### 1. Error Classification
- **Critical**: System failures requiring immediate attention
- **High**: Major functionality issues
- **Medium**: Minor issues with workarounds
- **Low**: Informational messages and warnings

#### 2. Recovery Mechanisms
- **Automatic**: Self-healing for common issues
- **Semi-automatic**: User approval for critical changes
- **Manual**: Terminal interface for complex problems

#### 3. Notification Channels
- **Terminal**: Real-time error display
- **Email**: Automated analysis reports
- **Logs**: Persistent error recording
- **Web UI**: Dashboard status indicators

## 🔧 Troubleshooting

### Common Issues

#### 1. AI Client Not Available
**Symptoms**: AI error correction not working
**Solutions**:
- Check `GEMINI_API_KEY` in `.env` file
- Verify internet connection
- Install `google-generativeai` package
- Check API key validity

#### 2. Servers Not Starting
**Symptoms**: Port already in use errors
**Solutions**:
- Check if ports 5000, 5001, 5002 are available
- Kill existing processes using those ports
- Change port numbers in `.env` file
- Check file permissions

#### 3. ThingSpeak Upload Failures
**Symptoms**: Cloud upload errors in logs
**Solutions**:
- Verify ThingSpeak API keys
- Check internet connectivity
- Verify channel ID is correct
- Check API key permissions

#### 4. Error Management Not Working
**Symptoms**: Errors not being detected or handled
**Solutions**:
- Ensure all required files are present
- Check Python dependencies
- Verify `.env` configuration
- Review system logs

### Debug Mode

Enable verbose output by setting in `.env`:
```env
AI_VERBOSE=1
```

### Log Analysis

Check log files for detailed error information:
```bash
# View recent sensor events
tail -f logs/sensor_events.log

# View recent errors
tail -f logs/error_events.log

# View recent data events
tail -f logs/data_events.log
```

### System Health Check

Run the demo script to test all components:
```bash
python demo_error_management.py
```

## 🚀 Advanced Features

### Custom Error Handlers

You can extend the error management system by adding custom error detection methods:

```python
def custom_error_detector(self) -> List[Dict]:
    """Custom error detection logic."""
    errors = []
    
    # Add your custom error detection logic here
    # Return list of error dictionaries
    
    return errors
```

### API Integration

The system provides APIs for external integration:

```python
# Get system status
response = requests.get('http://localhost:5002/api/status')
status = response.json()

# Trigger AI analysis
response = requests.post('http://localhost:5002/api/analyze')
result = response.json()

# Chat with AI
response = requests.post('http://localhost:5002/api/chat', 
                        json={'message': 'Check system health'})
ai_response = response.json()
```

### Backup and Recovery

The system automatically creates backups before applying fixes:

```python
def create_backup(self, file_path: Path) -> Path:
    """Create a backup of the file before modification."""
    BACKUP_DIR.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"{file_path.name}.backup_{timestamp}"
    backup_path = BACKUP_DIR / backup_name
    shutil.copy2(file_path, backup_path)
    return backup_path
```

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

### Development Setup

```bash
# Clone your fork
git clone <your-fork-url>
cd Event_sourcing

# Install development dependencies
pip install -r requirements.txt
pip install pytest black flake8

# Run tests
python -m pytest tests/

# Format code
black .

# Lint code
flake8 .
```

### Code Style

- Follow PEP 8 guidelines
- Use type hints where appropriate
- Add docstrings to all functions and classes
- Include error handling and logging

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Support

For support and questions:

1. Check the troubleshooting section
2. Review log files for detailed error information
3. Run the demo script to test functionality
4. Verify all dependencies and configuration
5. Create an issue on GitHub

## 🎉 Acknowledgments

- **Google Gemini AI** for intelligent error analysis and correction
- **ThingSpeak** for IoT cloud platform
- **Flask** for web framework
- **Python Community** for excellent libraries and tools

---

**Made with ❤️ for IoT and AI enthusiasts**

*This system demonstrates the power of combining IoT monitoring with AI-powered error management for robust, self-healing applications.*
