#!/usr/bin/env python3
"""
Instagram Follower Picker - Web UI
==================================
Flask web application for Instagram winner selection.
Provides clean UI for both general and orientation-based picking.
"""

import os
import sys
import json
import random
from datetime import datetime, timedelta
from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
from dotenv import load_dotenv

# Add parent directory to path to import our picker modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from instagram_social_follower_picker import InstagramSocialFollowerPicker
    from live_orientation_picker import LiveOrientationPicker
except ImportError as e:
    print(f"Error importing picker modules: {e}")
    print("Make sure you're running from the correct directory")
    sys.exit(1)

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'your-secret-key-change-this')

load_dotenv()

@app.route('/')
def index():
    """Main page with picker options"""
    return render_template('index.html')

@app.route('/general')
def general_picker():
    """General follower picker page"""
    return render_template('general.html')

@app.route('/orientation')
def orientation_picker():
    """Orientation event picker page"""
    return render_template('orientation.html')

@app.route('/api/general-pick', methods=['POST'])
def api_general_pick():
    """API endpoint for general follower picking"""
    try:
        data = request.get_json()
        username = data.get('username', '').strip()
        count = int(data.get('count', 50))
        
        if not username:
            return jsonify({'error': 'Username is required'}), 400
        
        # Initialize picker
        picker = InstagramSocialFollowerPicker()
        
        # Get followers
        followers = picker.get_followers(username, count)
        if not followers:
            return jsonify({'error': 'Could not fetch followers. Check username and API access.'}), 400
        
        # Select winner
        winner = picker.select_random_winner(followers)
        if not winner:
            return jsonify({'error': 'No followers found'}), 400
        
        return jsonify({
            'success': True,
            'winner': {
                'username': winner.get('username', 'Unknown'),
                'full_name': winner.get('full_name', 'No name'),
                'is_private': winner.get('is_private', False),
                'is_verified': winner.get('is_verified', False),
                'profile_pic_url': winner.get('profile_pic_url', '')
            },
            'total_followers': len(followers),
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@app.route('/api/orientation-pick', methods=['POST'])
def api_orientation_pick():
    """API endpoint for orientation event picking"""
    try:
        data = request.get_json()
        username = data.get('username', '').strip()
        time_window = float(data.get('time_window', 1.0))
        
        if not username:
            return jsonify({'error': 'Username is required'}), 400
        
        # Initialize orientation picker
        picker = LiveOrientationPicker()
        
        # Find recent followers
        recent_followers = picker.find_recent_followers(username, time_window)
        
        if not recent_followers:
            return jsonify({
                'error': f'No new followers found in the last {time_window} hour(s). Make sure the orientation is active and people are following.'
            }), 400
        
        # Select winner
        winner = random.choice(recent_followers)
        
        return jsonify({
            'success': True,
            'winner': {
                'username': winner.get('username', 'Unknown'),
                'full_name': winner.get('full_name', 'No name'),
                'is_private': winner.get('is_private', False),
                'is_verified': winner.get('is_verified', False),
                'profile_pic_url': winner.get('profile_pic_url', '')
            },
            'recent_followers_count': len(recent_followers),
            'time_window': time_window,
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'api_key_configured': bool(os.getenv('RAPIDAPI_KEY'))
    })

@app.errorhandler(404)
def not_found(error):
    return render_template('error.html', error="Page not found"), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('error.html', error="Server error"), 500

if __name__ == '__main__':
    # Check if API key is configured
    if not os.getenv('RAPIDAPI_KEY'):
        print("Warning: RAPIDAPI_KEY not found in environment variables")
        print("Make sure to configure your .env file")
    
    # Run the app
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_ENV') == 'development'
    
    print(f"Starting Instagram Follower Picker UI on http://localhost:{port}")
    app.run(host='0.0.0.0', port=port, debug=debug)