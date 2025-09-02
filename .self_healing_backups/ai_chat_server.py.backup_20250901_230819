#!/usr/bin/env python3
"""
AI Chat Server
Flask application for AI-powered system monitoring and chat interface
"""

import os
import json
from datetime import datetime
from flask import Flask, render_template, jsonify, request, redirect
from flask_cors import CORS
from dotenv import load_dotenv
from ai_monitor import ai_monitor

# Load environment variables
load_dotenv()

# Configuration
AI_CHAT_PORT = int(os.getenv("AI_CHAT_PORT", "5002"))
UI_PORT = int(os.getenv("UI_PORT", "5001"))

# Flask app initialization
app = Flask(__name__)
CORS(app)

@app.route('/')
def ai_dashboard():
    """Redirect to unified Events page in UI server."""
    return redirect(f"http://127.0.0.1:{UI_PORT}/events", code=302)

@app.route('/api/chat', methods=['POST'])
def chat_with_ai():
    """Chat endpoint for AI interaction."""
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({'error': 'Message is required'}), 400
        
        # Get AI response
        ai_response = ai_monitor.chat_with_ai(user_message)
        
        return jsonify({
            'success': True,
            'user_message': user_message,
            'ai_response': ai_response,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/status')
def get_ai_status():
    """Get AI monitoring status."""
    return jsonify(ai_monitor.get_system_status())

@app.route('/api/analyze', methods=['POST'])
def trigger_analysis():
    """Trigger immediate AI analysis."""
    try:
        ai_monitor.analyze_system_logs()
        return jsonify({
            'success': True,
            'message': 'Analysis triggered successfully',
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/start-monitoring', methods=['POST'])
def start_monitoring():
    """Start AI monitoring."""
    try:
        ai_monitor.start_monitoring()
        return jsonify({
            'success': True,
            'message': 'AI monitoring started',
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/stop-monitoring', methods=['POST'])
def stop_monitoring():
    """Stop AI monitoring."""
    try:
        ai_monitor.stop_monitoring()
        return jsonify({
            'success': True,
            'message': 'AI monitoring stopped',
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/logs')
def get_recent_logs():
    """Get recent logs for display."""
    try:
        recent_logs = ai_monitor.collect_recent_logs(minutes=10)
        return jsonify({
            'success': True,
            'logs': recent_logs,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/analysis')
def get_recent_analysis():
    """Get recent AI analysis results."""
    try:
        status = ai_monitor.get_system_status()
        return jsonify({
            'success': True,
            'recent_alerts': status.get('recent_alerts', []),
            'alert_count': status.get('alert_count', 0),
            'last_analysis': status.get('last_analysis'),
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("🤖 AI Chat Server")
    print("=" * 50)
    print(f"🌐 Server Port: {AI_CHAT_PORT}")
    print("=" * 50)
    
    # Check Gemini API key
    gemini_key = os.getenv("GEMINI_API_KEY", "YOUR_GEMINI_API_KEY")
    if gemini_key == "YOUR_GEMINI_API_KEY":
        print("⚠️  WARNING: GEMINI_API_KEY not set in .env file!")
        print("   Update the .env file with your actual Gemini API key")
    else:
        print("✅ Gemini API key configured")
    
    print("=" * 50)
    
    # Start Flask app
    app.run(host='0.0.0.0', port=AI_CHAT_PORT, debug=False)
