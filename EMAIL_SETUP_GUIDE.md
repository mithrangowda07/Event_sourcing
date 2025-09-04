# Email Analysis Reports Setup Guide

This guide explains how to configure email functionality for sending AI analysis reports from the Event Sourcing System.

## Overview

The email functionality allows you to send the latest AI analysis results via email with a single button click from the analysis page. The system uses SMTP to send professionally formatted HTML emails containing the analysis results.

## Features

- **One-click email sending**: Send latest analysis results with a single button click
- **Professional HTML formatting**: Emails are formatted with a modern, responsive design
- **Critical issue highlighting**: Critical issues are highlighted in red for immediate attention
- **Plain text fallback**: Includes both HTML and plain text versions for compatibility
- **Secure SMTP connection**: Uses TLS encryption for secure email transmission

## Email Configuration

### 1. Environment Variables

Add the following variables to your `.env` file:

```env
# Email Configuration for Analysis Reports
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SENDER_EMAIL=your-email@gmail.com
SENDER_PASSWORD=your-app-password
RECIPIENT_EMAIL=recipient@example.com
```

### 2. Gmail Setup (Recommended)

For Gmail accounts, you'll need to use an App Password instead of your regular password:

1. **Enable 2-Factor Authentication** on your Gmail account
2. **Generate an App Password**:
   - Go to Google Account settings
   - Security → 2-Step Verification → App passwords
   - Generate a new app password for "Mail"
   - Use this app password in the `SENDER_PASSWORD` field

### 3. Other Email Providers

For other email providers, update the SMTP settings accordingly:

#### Outlook/Hotmail
```env
SMTP_SERVER=smtp-mail.outlook.com
SMTP_PORT=587
```

#### Yahoo Mail
```env
SMTP_SERVER=smtp.mail.yahoo.com
SMTP_PORT=587
```

#### Custom SMTP Server
```env
SMTP_SERVER=your-smtp-server.com
SMTP_PORT=587  # or 465 for SSL
```

## Usage

### 1. Trigger Analysis
First, ensure you have recent analysis results by:
- Clicking the "Analyze" button to trigger immediate analysis, or
- Starting AI monitoring to get continuous analysis

### 2. Send Email
Click the "Email Analysis" button in the AI controls section. The button will show a loading state while sending.

### 3. Email Content
The email will contain:
- **Subject**: System Analysis Report with timestamp
- **Status**: Critical issues highlighted or "System Healthy"
- **Analysis Results**: Complete AI analysis with formatting
- **Professional Layout**: Modern HTML design with your system branding

## Troubleshooting

### Common Issues

#### Authentication Failed
```
Error: SMTP authentication failed. Please check your email credentials.
```
**Solution**: Verify your email and password. For Gmail, ensure you're using an App Password.

#### Connection Timeout
```
Error: SMTP error occurred: [Errno 110] Connection timed out
```
**Solution**: Check your SMTP server and port settings. Ensure firewall allows SMTP connections.

#### Email Not Configured
```
Error: Email service not configured. Please set email credentials in .env file.
```
**Solution**: Add all required email environment variables to your `.env` file.

### Testing Email Configuration

You can test your email configuration by:

1. **Using the UI**: Click the "Email Analysis" button and check for success/error messages
2. **Python Console**: 
   ```python
   from email_service import email_service
   result = email_service.test_email_configuration()
   print(result)
   ```

## Security Best Practices

1. **Use App Passwords**: Never use your main email password
2. **Environment Variables**: Keep credentials in `.env` file, not in code
3. **Secure SMTP**: Always use TLS/SSL encryption (port 587 or 465)
4. **Limited Scope**: Use dedicated email accounts for system notifications
5. **Regular Rotation**: Periodically rotate app passwords

## Email Template Customization

The email template can be customized by modifying the `_create_html_content()` method in `email_service.py`. The template includes:

- **Header**: System branding and timestamp
- **Status Badge**: Color-coded status indicator
- **Analysis Content**: Formatted analysis results
- **Footer**: System information and disclaimers

## Integration Details

### Backend Components

1. **email_service.py**: Core email functionality
2. **ai_monitor.py**: Integration with AI analysis
3. **ai_chat_server.py**: Email API endpoint
4. **ui_server.py**: Proxy endpoint for UI

### Frontend Components

1. **Email Button**: Added to AI controls section
2. **JavaScript Handler**: Manages button state and API calls
3. **User Feedback**: Success/error messages in chat

### API Endpoints

- `POST /api/ai/send-analysis-email`: Send latest analysis via email
- Response format:
  ```json
  {
    "success": true,
    "message": "Analysis report sent successfully to recipient@example.com"
  }
  ```

## Dependencies

The email functionality requires the following Python packages:
- `smtplib` (built-in)
- `ssl` (built-in)
- `email.mime` (built-in)

No additional external dependencies are required beyond the standard library.

## Support

If you encounter issues:

1. Check the console logs for detailed error messages
2. Verify all environment variables are set correctly
3. Test with a simple email provider like Gmail first
4. Ensure your network allows SMTP connections
5. Check if your email provider requires specific security settings

For Gmail specifically, you may need to:
- Enable "Less secure app access" (not recommended)
- Use OAuth2 authentication (advanced setup)
- Use App Passwords (recommended approach)
