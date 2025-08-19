#!/usr/bin/env python3
"""
Test script to verify AI analysis results are being displayed on the web page
"""

import requests
import json
import time

def test_ai_integration():
    """Test the AI integration endpoints."""
    
    base_url = "http://localhost:5002"
    
    print("🧪 Testing AI Integration...")
    print("=" * 50)
    
    # Test 1: Check if AI chat server is running
    try:
        response = requests.get(f"{base_url}/api/status", timeout=5)
        if response.status_code == 200:
            print("✅ AI chat server is running")
            status_data = response.json()
            print(f"   Monitoring active: {status_data.get('monitoring_active', False)}")
            print(f"   Alert count: {status_data.get('alert_count', 0)}")
            print(f"   Last analysis: {status_data.get('last_analysis', 'Never')}")
        else:
            print(f"❌ AI chat server returned status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ AI chat server is not running")
        print("   Start it with: python ai_chat_server.py")
        return False
    except Exception as e:
        print(f"❌ Error connecting to AI chat server: {e}")
        return False
    
    # Test 2: Check recent analysis results
    try:
        response = requests.get(f"{base_url}/api/analysis", timeout=5)
        if response.status_code == 200:
            analysis_data = response.json()
            if analysis_data.get('success'):
                recent_alerts = analysis_data.get('recent_alerts', [])
                print(f"✅ Found {len(recent_alerts)} recent analysis results")
                
                if recent_alerts:
                    print("📊 Recent analysis results:")
                    for i, alert in enumerate(recent_alerts[-3:], 1):  # Show last 3
                        timestamp = alert.get('timestamp', 'Unknown')
                        analysis = alert.get('analysis', 'No analysis')
                        print(f"   {i}. {timestamp}")
                        print(f"      Preview: {analysis[:100]}...")
                else:
                    print("   ℹ️ No analysis results yet - trigger an analysis first")
            else:
                print("❌ Analysis endpoint returned error")
                return False
        else:
            print(f"❌ Analysis endpoint returned status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error getting analysis results: {e}")
        return False
    
    # Test 3: Trigger an analysis
    print("\n🔍 Triggering AI analysis...")
    try:
        response = requests.post(f"{base_url}/api/analyze", timeout=30)
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print("✅ Analysis triggered successfully")
                print("   Wait a moment for results to appear on the web page...")
                
                # Wait a bit and check for new results
                time.sleep(3)
                response = requests.get(f"{base_url}/api/analysis", timeout=5)
                if response.status_code == 200:
                    analysis_data = response.json()
                    recent_alerts = analysis_data.get('recent_alerts', [])
                    print(f"   Found {len(recent_alerts)} total analysis results")
            else:
                print(f"❌ Analysis failed: {result.get('error', 'Unknown error')}")
        else:
            print(f"❌ Analysis endpoint returned status {response.status_code}")
    except Exception as e:
        print(f"❌ Error triggering analysis: {e}")
    
    print("\n" + "=" * 50)
    print("🎯 To view AI analysis results on the web page:")
    print("   1. Open http://localhost:5002 in your browser")
    print("   2. Look for the 'Recent AI Analysis Results' section")
    print("   3. Click 'Analyze Now' button to trigger new analysis")
    print("   4. Results will appear in the analysis section")
    
    return True

if __name__ == "__main__":
    test_ai_integration()
