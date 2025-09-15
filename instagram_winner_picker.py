#!/usr/bin/env python3
"""
Instagram Winner Picker - Universal Solution

This script provides multiple options for selecting winners from Instagram users:
1. Premium API - Real followers (requires subscription)
2. Engagement Method - Users who liked posts (free alternative)
3. Demo Mode - For testing
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def main():
    """Main menu for Instagram Winner Picker."""
    print("🎯 Instagram Winner Picker - Universal Solution")
    print("="*50)
    print()
    print("Choose your method:")
    print()
    print("1. 👥 Premium Followers Picker")
    print("   • Selects from ACTUAL followers")
    print("   • Requires Instagram Premium API 2023 subscription")
    print("   • Most accurate for 'followers'")
    print()
    print("2. 💖 Engagement Picker (RECOMMENDED)")
    print("   • Selects from users who liked posts")
    print("   • Uses free API (no subscription needed)")
    print("   • Gets engaged users (likely followers)")
    print()
    print("3. 🎮 Demo Mode")
    print("   • Test the picker with fake data")
    print("   • No API required")
    print()
    
    while True:
        choice = input("Enter your choice (1, 2, or 3): ").strip()
        
        if choice == "1":
            print("\n🚀 Starting Premium Followers Picker...")
            print("📡 This requires Instagram Premium API 2023 subscription")
            confirm = input("Do you have the subscription? (y/N): ").strip().lower()
            
            if confirm == 'y':
                os.system(f"{sys.executable} instagram_premium_follower_picker.py")
            else:
                print("\n💡 To subscribe:")
                print("   Visit: https://rapidapi.com/sfgeek/api/instagram-premium-api-2023")
                print("   Check for free tier options!")
                print("\n🔄 Consider using option 2 (Engagement Picker) instead")
            break
            
        elif choice == "2":
            print("\n🚀 Starting Engagement Picker...")
            print("💖 This selects from users who actively engage with posts")
            os.system(f"{sys.executable} instagram_engagement_picker.py")
            break
            
        elif choice == "3":
            print("\n🚀 Starting Demo Mode...")
            print("🎮 This simulates the winner selection process")
            os.system(f"{sys.executable} demo_follower_picker.py")
            break
            
        else:
            print("❌ Invalid choice. Please enter 1, 2, or 3.")


if __name__ == "__main__":
    main()