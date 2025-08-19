#!/usr/bin/env python3
"""
AI Monitor Module
Integrates Gemini AI with local logging system for real-time error detection
"""

import os
import json
import time
import threading
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Gemini API Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "YOUR_GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash")

class AIMonitor:
    def __init__(self):
        self.logs_dir = "logs"
        self.analysis_interval = 30  # seconds
        self.last_analysis = None
        self.monitoring_active = False
        self.alert_history = []
        self.chat_history = []
        
    def start_monitoring(self):
        """Start continuous AI monitoring."""
        self.monitoring_active = True
        monitor_thread = threading.Thread(target=self._monitoring_loop, daemon=True)
        monitor_thread.start()
        print("🤖 AI monitoring started - analyzing logs every 30 seconds")
    
    def stop_monitoring(self):
        """Stop AI monitoring."""
        self.monitoring_active = False
        print("⏹️ AI monitoring stopped")
    
    def _monitoring_loop(self):
        """Continuous monitoring loop."""
        while self.monitoring_active:
            try:
                self.analyze_system_logs()
                time.sleep(self.analysis_interval)
            except Exception as e:
                print(f"❌ AI monitoring error: {e}")
                time.sleep(60)  # Wait longer on error
    
    def collect_recent_logs(self, minutes: int = 5) -> Dict[str, List]:
        """Collect recent logs from all log files."""
        logs = {
            'sensor': [],
            'error': [],
            'data': []
        }
        
        cutoff_time = datetime.now() - timedelta(minutes=minutes)
        
        for log_type in logs.keys():
            log_file = f"{self.logs_dir}/{log_type}_events.log"
            if os.path.exists(log_file):
                try:
                    with open(log_file, 'r', encoding='utf-8') as f:
                        for line in f:
                            try:
                                log_entry = json.loads(line.strip())
                                log_time = datetime.fromisoformat(log_entry['timestamp'])
                                if log_time >= cutoff_time:
                                    logs[log_type].append(log_entry)
                            except:
                                continue
                except Exception as e:
                    print(f"Error reading {log_file}: {e}")
        
        return logs
    
    def analyze_with_gemini(self, log_data: Dict, analysis_type: str) -> str:
        """Send log data to Gemini for analysis."""
        try:
            # Prepare log summary
            log_summary = self._prepare_log_summary(log_data)
            
            # Create analysis prompt
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
            
            response = model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            return f"❌ AI Analysis Error: {str(e)}"
    
    def _prepare_log_summary(self, log_data: Dict) -> str:
        """Prepare a readable summary of log data for AI analysis."""
        summary = []
        
        for log_type, entries in log_data.items():
            if entries:
                summary.append(f"\n=== {log_type.upper()} EVENTS ({len(entries)} entries) ===")
                for entry in entries[-5:]:  # Last 5 entries of each type
                    timestamp = entry.get('timestamp', 'Unknown')
                    if log_type == 'sensor':
                        event = entry.get('event_type', 'Unknown')
                        desc = entry.get('description', 'No description')
                        summary.append(f"  {timestamp}: {event} - {desc}")
                    elif log_type == 'error':
                        component = entry.get('component', 'Unknown')
                        error = entry.get('error_message', 'No error message')
                        summary.append(f"  {timestamp}: {component} - {error}")
                    elif log_type == 'data':
                        component = entry.get('component', 'Unknown')
                        event_type = entry.get('event_type', 'Unknown')
                        desc = entry.get('description', 'No description')
                        summary.append(f"  {timestamp}: {component}.{event_type} - {desc}")
        
        return "\n".join(summary) if summary else "No recent log data available"
    
    def analyze_system_logs(self):
        """Main analysis function."""
        print(f"\n🔍 AI Analysis at {datetime.now().strftime('%H:%M:%S')}")
        
        # Collect recent logs
        recent_logs = self.collect_recent_logs(minutes=5)
        
        # Check if there are any logs to analyze
        total_logs = sum(len(logs) for logs in recent_logs.values())
        if total_logs == 0:
            print("ℹ️ No recent logs to analyze")
            return
        
        print(f"📊 Analyzing {total_logs} recent log entries...")
        
        # Perform AI analysis
        analysis = self.analyze_with_gemini(recent_logs, "system health and error detection")
        
        # Process and display results
        self._process_analysis_results(analysis)
        
        self.last_analysis = datetime.now()
    
    def _process_analysis_results(self, analysis: str):
        """Process and display AI analysis results."""
        print("\n" + "="*60)
        print("🤖 GEMINI AI ANALYSIS RESULTS")
        print("="*60)
        print(analysis)
        print("="*60)
        
        # Extract critical issues
        if "Critical" in analysis or "High" in analysis:
            print("🚨 CRITICAL ISSUES DETECTED - IMMEDIATE ATTENTION REQUIRED!")
        
        # Store in alert history
        self.alert_history.append({
            'timestamp': datetime.now().isoformat(),
            'analysis': analysis
        })
        
        # Keep only last 10 alerts
        if len(self.alert_history) > 10:
            self.alert_history.pop(0)
    
    def chat_with_ai(self, user_message: str) -> str:
        """Chat with AI about system logs and status."""
        try:
            # Collect recent logs for context
            recent_logs = self.collect_recent_logs(minutes=10)
            log_context = self._prepare_log_summary(recent_logs)
            
            # Create chat prompt
            prompt = f"""
            You are an AI system monitoring assistant. Here's the recent system log data:

            {log_context}

            User Question: {user_message}

            Please provide a helpful response based on the log data and your knowledge of system monitoring.
            Be specific about any issues you detect and provide actionable advice.
            """
            
            response = model.generate_content(prompt)
            
            # Store chat history
            self.chat_history.append({
                'timestamp': datetime.now().isoformat(),
                'user_message': user_message,
                'ai_response': response.text
            })
            
            # Keep only last 20 chat entries
            if len(self.chat_history) > 20:
                self.chat_history.pop(0)
            
            return response.text
            
        except Exception as e:
            return f"❌ AI Chat Error: {str(e)}"
    
    def get_system_status(self) -> Dict:
        """Get current AI monitoring status."""
        return {
            'monitoring_active': self.monitoring_active,
            'last_analysis': self.last_analysis.isoformat() if self.last_analysis else None,
            'analysis_interval': self.analysis_interval,
            'alert_count': len(self.alert_history),
            'recent_alerts': self.alert_history[-3:] if self.alert_history else [],
            'chat_history': self.chat_history[-5:] if self.chat_history else []
        }

# Global AI monitor instance
ai_monitor = AIMonitor()
