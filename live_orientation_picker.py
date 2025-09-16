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
    
    def get_followers_count(self, username):
        """Just get follower count without full data"""
        print(f"🔍 Checking follower count for @{username}...")
        
        url = f"{self.base_url}/v1/followers"
        params = {
            'username_or_id_or_url': username,
            'amount': '1'  # Just get count, minimal data
        }
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            
            if response.status_code == 200:
                data = response.json()
                if 'data' in data and 'count' in data['data']:
                    count = data['data']['count']
                    print(f"✅ Current followers: {count}")
                    return count
                elif 'data' in data and 'items' in data['data']:
                    # Fallback if count not available
                    followers = data['data']['items']
                    return len(followers)
            
            print(f"❌ API Error: {response.status_code}")
            return None
                
        except Exception as e:
            print(f"❌ Network Error: {e}")
            return None

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
    
    def get_baseline_snapshot(self, username, time_window_hours):
        """Get baseline snapshot from X hours ago"""
        now = datetime.now()
        target_time = now - timedelta(hours=time_window_hours)
        
        print(f"🕐 Looking for baseline from: {target_time.strftime('%H:%M:%S')} ({time_window_hours}h ago)")
        
        # Look for existing snapshots within ±30 minutes of target time
        snapshot_dir = 'live_snapshots'
        if os.path.exists(snapshot_dir):
            files = [f for f in os.listdir(snapshot_dir) if f.startswith(f"{username}_") and f.endswith('.json')]
            
            best_snapshot = None
            best_time_diff = float('inf')
            
            for filename in sorted(files, reverse=True):
                filepath = os.path.join(snapshot_dir, filename)
                if os.path.exists(filepath):
                    try:
                        with open(filepath, 'r', encoding='utf-8') as f:
                            snapshot = json.load(f)
                        
                        snapshot_time = datetime.fromisoformat(snapshot['datetime'])
                        
                        # We want baselines that are:
                        # 1. Older than current time (obviously)
                        # 2. Can be newer than target time (we use the closest available baseline)
                        # This is more flexible for real-world usage
                        
                        if snapshot_time <= now:  # Baseline is from the past
                            time_from_target = abs((snapshot_time - target_time).total_seconds())
                            if time_from_target < best_time_diff or best_time_diff == float('inf'):
                                best_snapshot = snapshot
                                best_time_diff = time_from_target
                    except:
                        continue
            
            if best_snapshot:
                snapshot_time = datetime.fromisoformat(best_snapshot['datetime'])
                actual_hours = (now - snapshot_time).total_seconds() / 3600
                print(f"✅ Found baseline from {actual_hours:.1f}h ago: {os.path.basename(files[0])}")
                return best_snapshot
        
        # No suitable baseline found - this is expected for the first run
        print(f"⚠️ No baseline snapshot found from {time_window_hours}h ago")
        print(f"💡 This means:")
        print(f"   • First time running the picker for this time window")
        print(f"   • Need to wait {time_window_hours}h and run again")
        print(f"   • Or use a shorter time window (0.5h or 1h)")
        
        # Create a snapshot for future use, but don't use it now
        print(f"📄 Creating baseline for future use...")
        current_count = self.get_followers_count(username)
        if current_count:
            timestamp = now.strftime("%Y%m%d_%H%M%S")
            filename = f"live_snapshots/{username}_baseline_{timestamp}.json"
            
            snapshot = {
                'username': username,
                'datetime': now.isoformat(),
                'unix_timestamp': now.timestamp(),
                'follower_count': current_count,
                'metadata_only': True  # Lightweight baseline
            }
            
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(snapshot, f, indent=2, ensure_ascii=False)
                print(f"💾 Baseline saved: {filename}")
                print(f"📊 Follower count: {current_count}")
                print(f"⏰ Timestamp: {now.strftime('%H:%M:%S')}")
            except Exception as e:
                print(f"⚠️ Could not save baseline: {e}")
        
        return None
    
    def find_recent_followers(self, username, time_window_hours):
        """Main function: find followers from the selected time window"""
        print(f"\n🎯 FINDING RECENT FOLLOWERS")
        print("=" * 50)
        
        # Get baseline (followers from X hours ago)
        baseline = self.get_baseline_snapshot(username, time_window_hours)
        if not baseline:
            print("\n❌ CANNOT ANALYZE WITHOUT BASELINE")
            print(f"� Creating baseline snapshot...")
            
            # Just get count for quick baseline creation
            current_count = self.get_followers_count(username)
            if current_count:
                now = datetime.now()
                timestamp = now.strftime("%Y%m%d_%H%M%S")
                filename = f"live_snapshots/{username}_baseline_{timestamp}.json"
                
                # Create lightweight baseline with just metadata
                snapshot = {
                    'username': username,
                    'datetime': now.isoformat(),
                    'unix_timestamp': now.timestamp(),
                    'follower_count': current_count,
                    'metadata_only': True  # Mark as lightweight
                }
                
                try:
                    with open(filename, 'w', encoding='utf-8') as f:
                        json.dump(snapshot, f, indent=2, ensure_ascii=False)
                    print(f"💾 Baseline created: {filename}")
                    print(f"📊 Follower count: {current_count}")
                    print(f"⏰ Timestamp: {now.strftime('%H:%M:%S')}")
                except Exception as e:
                    print(f"⚠️ Could not save baseline: {e}")
            
            print(f"\n💡 SOLUTION:")
            print(f"   1. Baseline created with {current_count} followers")
            print(f"   2. Wait {time_window_hours} hour(s)")
            print(f"   3. Run again to find new followers")
            print(f"\n   OR try a shorter time window (0.5h or 1h)")
            return []
        
        # Get current followers
        current_followers = self.get_followers(username)
        if not current_followers:
            print("❌ Could not fetch current followers")
            return []
        
        # Check if we have a metadata-only baseline
        if baseline.get('metadata_only', False):
            # For metadata-only baselines, we can only detect growth by count
            baseline_count = baseline.get('follower_count', 0)
            current_count = len(current_followers)
            
            print(f"\n📊 METADATA-ONLY ANALYSIS:")
            print(f"   ⏰ Time window: Last {time_window_hours} hour(s)")
            baseline_time = datetime.fromisoformat(baseline['datetime'])
            print(f"   📅 Baseline: {baseline_time.strftime('%H:%M:%S')}")
            print(f"   📅 Current: {datetime.now().strftime('%H:%M:%S')}")
            print(f"   👥 Baseline followers: {baseline_count}")
            print(f"   👥 Current followers: {current_count}")
            
            growth = current_count - baseline_count
            print(f"   📈 Growth: +{growth}")
            
            if growth <= 0:
                print(f"   ❌ No growth detected in {time_window_hours}h window")
                return []
            
            # For metadata-only, we assume the most recent followers are the new ones
            # This is not 100% accurate but the best we can do without full baseline
            print(f"   🎯 Assuming last {growth} followers are new")
            print(f"   💡 Note: This picks from the most recent followers")
            
            # Return the most recent followers (assuming API returns in recent order)
            new_followers = current_followers[:growth]
            print(f"   🆕 New followers to pick from: {len(new_followers)}")
            return new_followers
        
        # Full baseline with actual follower list
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
        print(f"\n📊 FULL ANALYSIS RESULTS:")
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