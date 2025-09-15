#!/usr/bin/env python3
"""
Live Orientation Winner Picker
==============================
Super simple approach:
1. Select time window (30min, 1hr, 2hr)
2. Script automatically finds recent followers
3. Picks winner from recent followers
4. Done!

Perfect for IEEE RAS IIT live orientation events!
"""

import os
import json
import requests
import random
from datetime import datetime, timedelta
from dotenv import load_dotenv

class LiveOrientationPicker:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv('RAPIDAPI_KEY')
        if not self.api_key:
            raise ValueError("RAPIDAPI_KEY not found in .env file")
        
        self.base_url = "https://instagram-social-api.p.rapidapi.com"
        self.headers = {
            'x-rapidapi-host': 'instagram-social-api.p.rapidapi.com',
            'x-rapidapi-key': self.api_key
        }
        
        # Create snapshots directory
        os.makedirs('live_snapshots', exist_ok=True)
    
    def get_followers(self, username, max_followers=400):
        """Fetch current followers"""
        print(f"🔍 Fetching followers for @{username}...")
        
        url = f"{self.base_url}/v1/followers"
        params = {
            'username_or_id_or_url': username,
            'amount': str(max_followers)
        }
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            
            if response.status_code == 200:
                data = response.json()
                if 'data' in data and 'items' in data['data']:
                    followers = data['data']['items']
                    print(f"✅ Fetched {len(followers)} followers!")
                    return followers
            
            print(f"❌ API Error: {response.status_code}")
            return []
                
        except Exception as e:
            print(f"❌ Error: {e}")
            return []
    
    def get_baseline_snapshot(self, username, hours_back):
        """Get or create baseline snapshot for comparison"""
        cutoff_time = datetime.now() - timedelta(hours=hours_back)
        
        # Look for existing snapshot within timeframe
        if os.path.exists('live_snapshots'):
            for filename in os.listdir('live_snapshots'):
                if filename.startswith(f"{username}_") and filename.endswith('.json'):
                    filepath = os.path.join('live_snapshots', filename)
                    try:
                        with open(filepath, 'r') as f:
                            snapshot = json.load(f)
                        
                        snapshot_time = datetime.fromisoformat(snapshot['datetime'])
                        if snapshot_time >= cutoff_time:
                            print(f"📊 Using existing baseline from {snapshot_time.strftime('%H:%M:%S')}")
                            return snapshot
                    except:
                        continue
        
        # No suitable baseline found, create new one
        print(f"📸 Creating new baseline snapshot...")
        current_followers = self.get_followers(username)
        
        if not current_followers:
            return None
        
        now = datetime.now()
        snapshot = {
            'username': username,
            'datetime': now.isoformat(),
            'unix_timestamp': now.timestamp(),
            'follower_count': len(current_followers),
            'followers': current_followers
        }
        
        # Save baseline
        timestamp = now.strftime("%Y%m%d_%H%M%S")
        filename = f"live_snapshots/{username}_baseline_{timestamp}.json"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(snapshot, f, indent=2, ensure_ascii=False)
            print(f"💾 Baseline saved: {filename}")
        except Exception as e:
            print(f"⚠️ Could not save baseline: {e}")
        
        return snapshot
    
    def find_recent_followers(self, username, time_window_hours):
        """Main function: find followers from the selected time window"""
        print(f"\n🎯 FINDING RECENT FOLLOWERS")
        print("=" * 50)
        
        # Get baseline (followers from X hours ago)
        baseline = self.get_baseline_snapshot(username, time_window_hours)
        if not baseline:
            print("❌ Could not establish baseline")
            return []
        
        # Get current followers
        current_followers = self.get_followers(username)
        if not current_followers:
            print("❌ Could not fetch current followers")
            return []
        
        # Find new followers
        baseline_usernames = set()
        for follower in baseline.get('followers', []):
            username_field = follower.get('username', '')
            if username_field:
                baseline_usernames.add(username_field.lower())
        
        new_followers = []
        for follower in current_followers:
            username_field = follower.get('username', '')
            if username_field and username_field.lower() not in baseline_usernames:
                new_followers.append(follower)
        
        # Show results
        baseline_time = datetime.fromisoformat(baseline['datetime'])
        print(f"\n📊 ANALYSIS RESULTS:")
        print(f"   ⏰ Time window: Last {time_window_hours} hour(s)")
        print(f"   📅 Baseline: {baseline_time.strftime('%H:%M:%S')}")
        print(f"   📅 Current: {datetime.now().strftime('%H:%M:%S')}")
        print(f"   👥 Baseline followers: {baseline['follower_count']}")
        print(f"   👥 Current followers: {len(current_followers)}")
        
        growth = len(current_followers) - baseline['follower_count']
        print(f"   📈 Growth: +{growth}")
        print(f"   🆕 New followers: {len(new_followers)}")
        
        return new_followers
    
    def select_winner(self, new_followers, time_window_hours):
        """Select and announce winner"""
        if not new_followers:
            print(f"\n❌ NO NEW FOLLOWERS IN LAST {time_window_hours} HOUR(S)")
            print(f"💡 Try:")
            print(f"   • Longer time window")
            print(f"   • Announce giveaway during orientation") 
            print(f"   • Make sure people are actually following")
            return None
        
        winner = random.choice(new_followers)
        
        print(f"\n" + "🎉" * 25)
        print(f"🏆 ORIENTATION WINNER! 🏆")
        print(f"🎉" * 25)
        print(f"\n👤 Winner: @{winner.get('username', 'Unknown')}")
        print(f"📝 Name: {winner.get('full_name', 'No name')}")
        
        is_private = winner.get('is_private', False)
        print(f"🔐 Account: {'🔒 Private' if is_private else '🔓 Public'}")
        
        if winner.get('is_verified', False):
            print(f"✅ Verified Account")
        
        print(f"\n🎊 Congratulations @{winner.get('username')}!")
        print(f"⏰ Followed in the last {time_window_hours} hour(s)")
        print(f"🎯 Selected from {len(new_followers)} recent followers")
        print(f"🎉" * 25)
        
        return winner

def main():
    print("🎯 LIVE ORIENTATION WINNER PICKER")
    print("=" * 50)
    print("⚡ Super simple: Pick time window → Get winner!")
    print("🎓 Perfect for IEEE RAS IIT orientation!")
    print()
    
    picker = LiveOrientationPicker()
    
    # Get username
    username = input("Instagram username (without @): ").strip()
    if not username:
        print("❌ Username required!")
        return
    
    # Time window selection
    print(f"\n⏰ SELECT TIME WINDOW:")
    print("1. ⚡ Last 30 minutes (quick events)")
    print("2. 🕐 Last 1 hour (normal orientation)") 
    print("3. 🕑 Last 2 hours (long events)")
    
    choice = input("\nChoice (1-3): ").strip()
    
    time_options = {
        '1': (0.5, "30 minutes"),
        '2': (1.0, "1 hour"),
        '3': (2.0, "2 hours")
    }
    
    if choice not in time_options:
        print("❌ Invalid choice")
        return
    
    hours, label = time_options[choice]
    
    print(f"\n🚀 PROCESSING...")
    print(f"⏰ Finding followers from last {label}")
    
    # Do the work automatically
    recent_followers = picker.find_recent_followers(username, hours)
    
    # Select winner automatically
    winner = picker.select_winner(recent_followers, hours)
    
    if winner:
        print(f"\n✅ MISSION COMPLETE!")
        print(f"🎁 Winner selected from orientation attendees!")
    else:
        print(f"\n⚠️ No recent followers found")
        print(f"💡 Make sure the orientation is happening and people are following!")

if __name__ == "__main__":
    main()