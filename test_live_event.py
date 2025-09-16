#!/usr/bin/env python3
"""
Quick test script to verify live event detection works with existing baseline
"""

import sys
import os
sys.path.append('.')

from live_orientation_picker import LiveOrientationPicker

def test_live_event():
    print("🧪 TESTING LIVE EVENT DETECTION")
    print("=" * 50)
    
    picker = LiveOrientationPicker()
    
    # Test with ieeeras_iit account using a time window that should find existing baseline
    # We have baselines from 08:40, so let's use a 10 minute window (0.17 hours)
    username = "ieeeras_iit"
    time_window = 0.17  # ~10 minutes = 0.17 hours
    
    print(f"🎯 Testing @{username} with {time_window}h window")
    print(f"📅 This should find baseline from 08:40 (about 5-6 minutes ago)")
    
    recent_followers = picker.find_recent_followers(username, time_window)
    
    if recent_followers:
        print(f"\n✅ SUCCESS! Found {len(recent_followers)} new followers!")
        print(f"👥 Ready to pick winner from:")
        for i, follower in enumerate(recent_followers[:5], 1):
            print(f"   {i}. @{follower.get('username', 'unknown')}")
        if len(recent_followers) > 5:
            print(f"   ... and {len(recent_followers) - 5} more")
    else:
        print(f"\n❌ No new followers detected")
        print(f"💡 This could mean:")
        print(f"   • No one actually followed in the last ~10 minutes")
        print(f"   • The account still has exactly 50 followers")
        print(f"   • Need to test with an account that has recent growth")
        
        # Let's also test with a longer window to see if we can detect any growth
        print(f"\n🔄 Trying with longer window...")
        longer_window = 1.0  # 1 hour
        print(f"🎯 Testing with {longer_window}h window")
        recent_followers = picker.find_recent_followers(username, longer_window)
        
        if recent_followers:
            print(f"✅ Found {len(recent_followers)} new followers with longer window!")
        else:
            print(f"❌ Still no new followers detected")
            print(f"💡 The account likely has no growth or the API is returning the same 50 followers")

if __name__ == "__main__":
    test_live_event()