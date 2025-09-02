# Error Management System Guide

## Overview

The Error Management System provides automatic error detection, AI-generated correction code display, and server pause/resume functionality. When errors are detected, the terminal shows only the error correction code and pauses other servers until the error is corrected.

## Features

- 🚨 **Automatic Error Detection**: Monitors system logs, syntax errors, and server crashes
- 🤖 **AI-Generated Correction Code**: Uses Gemini AI to generate fix suggestions
- ⏸️ **Server Pause/Resume**: Automatically pauses all servers during error correction
- 🖥️ **Terminal Interface**: Clean terminal display showing only correction code
- 🔄 **Real-time Monitoring**: Continuous monitoring with 5-second intervals
- 🛡️ **Integrated with AI Monitor**: Works with existing AI monitoring system

## System Components

### 1. Error Manager (`error_manager.py`)
- Main error detection and management system
- Handles server pause/resume functionality
- Generates AI correction code
- Manages error state and recovery

### 2. Terminal Error Interface (`terminal_error_interface.py`)
- Clean terminal interface for error display
- Syntax highlighting for correction code
- User interaction controls
- System status display

### 3. Enhanced AI Monitor (`ai_monitor.py`)
- Integrated with error management system
- Triggers error handling on critical issues
- Generates correction code for specific errors

### 4. Startup Script (`start_system_with_error_management.py`)
- Launches system with full error management
- Fallback to traditional startup if error management unavailable
- Comprehensive system checks

## Installation and Setup

### Prerequisites

1. **Python Dependencies**:
   ```bash
   pip install flask flask-cors requests python-dotenv google-generativeai
   ```

2. **Environment Variables** (`.env` file):
   ```env
   # Required for AI error correction
   GEMINI_API_KEY=your_gemini_api_key_here
   
   # Existing system variables
   USER_ID=your_user_id
   LOCAL_SENSOR_IP=your_ip
   THINGSPEAK_WRITE_API_KEY=your_write_key
   THINGSPEAK_READ_API_KEY=your_read_key
   THINGSPEAK_CHANNEL_ID=your_channel_id
   ```

### Getting Gemini API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Add it to your `.env` file as `GEMINI_API_KEY`

## Usage

### Starting the System

```bash
# Start with full error management
python start_system_with_error_management.py
```

### Demo Mode

```bash
# Run demonstration of error management features
python demo_error_management.py
```

### Manual Error Management

```bash
# Start only the error management system
python error_manager.py

# Start only the terminal interface
python terminal_error_interface.py
```

## How It Works

### Error Detection Process

1. **Continuous Monitoring**: System checks every 5 seconds for:
   - Server process crashes
   - Syntax errors in Python files
   - Error entries in log files
   - Critical issues from AI analysis

2. **Error Classification**: Errors are classified by severity:
   - **Critical**: Server crashes, system failures
   - **High**: Syntax errors, major functionality issues
   - **Medium**: Log errors, minor issues
   - **Low**: Warnings, informational messages

3. **Priority Handling**: System handles errors in priority order:
   - Critical errors are handled immediately
   - High severity errors are handled next
   - Medium severity errors are handled last

### Error Correction Process

1. **Server Pause**: All running servers are paused using SIGSTOP
2. **Terminal Display**: Clean terminal interface shows:
   - Error details and severity
   - AI-generated correction code with syntax highlighting
   - User interaction options
3. **User Interaction**: User can:
   - Review correction code
   - Apply fixes manually
   - Regenerate correction code
   - View system status
   - Resume or quit system
4. **Server Resume**: All servers are resumed using SIGCONT

### AI Correction Code Generation

The system uses Gemini AI to generate correction code by:
1. Analyzing the error context (type, message, file, line)
2. Reading the problematic file content
3. Generating a complete corrected version
4. Providing clean, executable code

## Terminal Interface

### Error Display Screen

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

## Server Management

### Supported Servers

- **Simulation Server** (Port 5000): Temperature sensor simulation
- **UI Server** (Port 5001): Web dashboard interface
- **AI Chat Server** (Port 5002): AI monitoring interface

### Server States

- **Running**: Server is active and processing requests
- **Paused**: Server is suspended (SIGSTOP) but process remains
- **Stopped**: Server process has been terminated

### Pause/Resume Mechanism

- Uses Unix signals (SIGSTOP/SIGCONT) for pause/resume
- Maintains server state and connections
- Allows for quick recovery after error correction

## Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GEMINI_API_KEY` | Gemini AI API key for error correction | Yes |
| `AI_VERBOSE` | Enable verbose AI monitoring output | No |
| `AI_MODEL` | Gemini model to use (default: gemini-2.0-flash) | No |

### Monitoring Intervals

- **Error Detection**: 5 seconds
- **AI Analysis**: 30 seconds
- **Log Collection**: 1 minute

## Troubleshooting

### Common Issues

1. **AI Client Not Available**
   - Check GEMINI_API_KEY in .env file
   - Verify internet connection
   - Install google-generativeai package

2. **Servers Not Starting**
   - Check port availability
   - Verify file permissions
   - Review error logs

3. **Error Management Not Working**
   - Ensure all required files are present
   - Check Python dependencies
   - Review system logs

### Debug Mode

Enable verbose output by setting in `.env`:
```env
AI_VERBOSE=1
```

### Log Files

Error management logs are stored in:
- `logs/error_events.log`: Error events
- `logs/sensor_events.log`: Sensor events
- `logs/data_events.log`: Data events

## Integration with Existing System

The error management system integrates seamlessly with:
- **AI Monitor**: Triggers error handling on critical issues
- **Event Logger**: Monitors log files for errors
- **Self-Healing System**: Can work alongside existing self-healing
- **Web Dashboards**: All web interfaces remain functional

## Best Practices

1. **Regular Monitoring**: Keep the system running for continuous monitoring
2. **API Key Security**: Store Gemini API key securely in .env file
3. **Error Review**: Always review AI-generated correction code before applying
4. **Backup Strategy**: System creates backups before applying fixes
5. **Testing**: Test error scenarios in development environment first

## Advanced Usage

### Custom Error Handlers

You can extend the error management system by:
1. Adding custom error detection methods
2. Implementing specific correction strategies
3. Integrating with external monitoring tools

### API Integration

The system provides APIs for:
- Error status monitoring
- Manual error triggering
- Server management
- AI analysis results

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review log files for detailed error information
3. Run the demo script to test functionality
4. Verify all dependencies and configuration

## License

This error management system is part of the Temperature Monitoring System and follows the same licensing terms.
