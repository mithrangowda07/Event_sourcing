#!/usr/bin/env python3
"""
Email Service Module
Handles sending analysis results via SMTP
"""

import os
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from typing import Optional, Dict
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class EmailService:
    def __init__(self):
        # Email configuration from environment variables
        self.smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        self.sender_email = os.getenv("SENDER_EMAIL", "")
        self.sender_password = os.getenv("SENDER_PASSWORD", "")
        self.recipient_email = os.getenv("RECIPIENT_EMAIL", "")
        
        # Validate configuration
        self.is_configured = all([
            self.sender_email,
            self.sender_password,
            self.recipient_email
        ])
        
        if not self.is_configured:
            print("⚠️  Email service not fully configured. Please set SENDER_EMAIL, SENDER_PASSWORD, and RECIPIENT_EMAIL in .env file")
    
    def send_analysis_email(self, analysis_data: Dict) -> Dict:
        """
        Send analysis results via email.
        
        Args:
            analysis_data: Dictionary containing analysis results
            
        Returns:
            Dictionary with success status and message
        """
        if not self.is_configured:
            return {
                'success': False,
                'error': 'Email service not configured. Please set email credentials in .env file.'
            }
        
        try:
            # Create message
            message = MIMEMultipart("alternative")
            message["Subject"] = f"System Analysis Report - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            message["From"] = self.sender_email
            message["To"] = self.recipient_email
            
            # Create email content
            html_content = self._create_html_content(analysis_data)
            text_content = self._create_text_content(analysis_data)
            
            # Create MIMEText objects
            text_part = MIMEText(text_content, "plain")
            html_part = MIMEText(html_content, "html")
            
            # Add parts to message
            message.attach(text_part)
            message.attach(html_part)
            
            # Create secure connection and send email
            context = ssl.create_default_context()
            
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls(context=context)
                server.login(self.sender_email, self.sender_password)
                server.sendmail(self.sender_email, self.recipient_email, message.as_string())
            
            return {
                'success': True,
                'message': f'Analysis report sent successfully to {self.recipient_email}'
            }
            
        except smtplib.SMTPAuthenticationError:
            return {
                'success': False,
                'error': 'SMTP authentication failed. Please check your email credentials.'
            }
        except smtplib.SMTPException as e:
            return {
                'success': False,
                'error': f'SMTP error occurred: {str(e)}'
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'Failed to send email: {str(e)}'
            }
    
    def _create_html_content(self, analysis_data: Dict) -> str:
        """Create HTML email content."""
        timestamp = analysis_data.get('timestamp', datetime.now().isoformat())
        analysis = analysis_data.get('analysis', 'No analysis available')
        critical = analysis_data.get('critical', False)
        
        # Format timestamp
        try:
            dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            formatted_timestamp = dt.strftime('%Y-%m-%d %H:%M:%S')
        except:
            formatted_timestamp = timestamp
        
        # Determine status color
        status_color = "#dc3545" if critical else "#28a745"  # Red for critical, green for normal
        status_text = "CRITICAL ISSUES DETECTED" if critical else "SYSTEM HEALTHY"
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>System Analysis Report</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    max-width: 800px;
                    margin: 0 auto;
                    padding: 20px;
                }}
                .header {{
                    background: linear-gradient(135deg, #6366f1, #8b5cf6);
                    color: white;
                    padding: 20px;
                    border-radius: 8px;
                    text-align: center;
                    margin-bottom: 20px;
                }}
                .status {{
                    background-color: {status_color};
                    color: white;
                    padding: 10px;
                    border-radius: 5px;
                    text-align: center;
                    font-weight: bold;
                    margin-bottom: 20px;
                }}
                .analysis-content {{
                    background-color: #f8f9fa;
                    padding: 20px;
                    border-radius: 8px;
                    border-left: 4px solid #6366f1;
                    white-space: pre-line;
                }}
                .footer {{
                    margin-top: 20px;
                    padding: 15px;
                    background-color: #e9ecef;
                    border-radius: 5px;
                    font-size: 12px;
                    color: #6c757d;
                }}
                .timestamp {{
                    color: #6c757d;
                    font-size: 14px;
                }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>🤖 System Analysis Report</h1>
                <p class="timestamp">Generated on {formatted_timestamp}</p>
            </div>
            
            <div class="status">
                {status_text}
            </div>
            
            <div class="analysis-content">
                {analysis}
            </div>
            
            <div class="footer">
                <p><strong>Event Sourcing System Monitor</strong></p>
                <p>This is an automated report generated by the AI monitoring system.</p>
                <p>If you have any questions, please contact your system administrator.</p>
            </div>
        </body>
        </html>
        """
        
        return html
    
    def _create_text_content(self, analysis_data: Dict) -> str:
        """Create plain text email content."""
        timestamp = analysis_data.get('timestamp', datetime.now().isoformat())
        analysis = analysis_data.get('analysis', 'No analysis available')
        critical = analysis_data.get('critical', False)
        
        # Format timestamp
        try:
            dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            formatted_timestamp = dt.strftime('%Y-%m-%d %H:%M:%S')
        except:
            formatted_timestamp = timestamp
        
        status_text = "CRITICAL ISSUES DETECTED" if critical else "SYSTEM HEALTHY"
        
        text = f"""
SYSTEM ANALYSIS REPORT
======================

Generated on: {formatted_timestamp}
Status: {status_text}

ANALYSIS RESULTS:
{analysis}

---
Event Sourcing System Monitor
This is an automated report generated by the AI monitoring system.
If you have any questions, please contact your system administrator.
        """
        
        return text.strip()
    
    def test_email_configuration(self) -> Dict:
        """Test email configuration by sending a test email."""
        if not self.is_configured:
            return {
                'success': False,
                'error': 'Email service not configured'
            }
        
        test_data = {
            'timestamp': datetime.now().isoformat(),
            'analysis': 'This is a test email to verify email configuration is working correctly.',
            'critical': False
        }
        
        return self.send_analysis_email(test_data)

# Global email service instance
email_service = EmailService()
