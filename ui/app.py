#!/usr/bin/env python3
"""
Instagram Follower Picker - Clean Web UI
========================================
Simple Flask app for Instagram winner selection.
"""

import os
import sys
import random
from datetime import datetime
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'raffle-secret-key-2024')

# Import picker modules with error handling
try:
    from instagram_social_follower_picker import InstagramSocialFollowerPicker
    from live_orientation_picker import LiveOrientationPicker
    MODULES_LOADED = True
except ImportError as e:
    print(f"Warning: Could not import picker modules: {e}")
    MODULES_LOADED = False

@app.route('/')
def index():
    """Main page with both picker options"""
    return render_template('index.html')

@app.route('/api/pick', methods=['POST'])
def api_pick():
    """Unified API endpoint for both general and orientation picking"""
    if not MODULES_LOADED:
        return jsonify({'error': 'Server configuration error. Picker modules not available.'}), 500
    
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
            
        username = data.get('username', '').strip()
        pick_type = data.get('type', 'general')
        
        if not username:
            return jsonify({'error': 'Username is required'}), 400
        
        # Check API key first
        api_key = os.getenv('RAPIDAPI_KEY')
        if not api_key:
            return jsonify({'error': 'API key not configured. Please check server configuration.'}), 500
        
        if pick_type == 'orientation':
            # Orientation-based picking
            time_window = float(data.get('time_window', 1.0))
            try:
                picker = LiveOrientationPicker()
                recent_followers = picker.find_recent_followers(username, time_window)
            except ValueError as e:
                return jsonify({'error': f'Configuration error: {str(e)}'}), 500
            
            if not recent_followers:
                return jsonify({
                    'error': f'No new followers found in the last {time_window} hour(s)'
                }), 400
            
            winner = random.choice(recent_followers)
            total_count = len(recent_followers)
            extra_info = f"from {total_count} new followers in {time_window}h"
            
        else:
            # General picking
            count = int(data.get('count', 50))
            picker = InstagramSocialFollowerPicker(api_key)
            followers = picker.get_followers(username, count)
            
            if not followers:
                return jsonify({'error': 'Could not fetch followers. Check username.'}), 400
            
            winner = picker.select_random_winner(followers)
            if not winner:
                return jsonify({'error': 'No followers found'}), 400
                
            total_count = len(followers)
            extra_info = f"from {total_count} total followers"
        
        return jsonify({
            'success': True,
            'winner': {
                'username': winner.get('username', 'Unknown'),
                'full_name': winner.get('full_name', 'No name'),
                'is_private': winner.get('is_private', False),
                'is_verified': winner.get('is_verified', False),
                'profile_pic_url': winner.get('profile_pic_url', '')
            },
            'info': extra_info,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
    
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'modules_loaded': MODULES_LOADED,
        'api_key_configured': bool(os.getenv('RAPIDAPI_KEY')),
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })

if __name__ == '__main__':
    # Check configuration
    if not os.getenv('RAPIDAPI_KEY'):
        print("⚠️  Warning: RAPIDAPI_KEY not found in .env file")
    
    if not MODULES_LOADED:
        print("⚠️  Warning: Picker modules could not be loaded")
    
    # Run the app
    port = int(os.getenv('PORT', 5000))
    print(f"🚀 Instagram Follower Picker UI starting on http://localhost:{port}")
    app.run(host='0.0.0.0', port=port, debug=False)