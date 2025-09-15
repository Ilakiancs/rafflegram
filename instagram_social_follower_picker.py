#!/usr/bin/env python3
"""
Instagram Social API Follower Picker

This script uses the Instagram Social API from RapidAPI to fetch ACTUAL followers
of a given Instagram username and randomly selects a winner.

This API works with your current subscription!
"""

import os
import sys
import random
import requests
import json
from typing import List, Dict, Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class InstagramSocialFollowerPicker:
    """Class to handle Instagram follower fetching using Social API."""
    
    def __init__(self, api_key: str):
        """
        Initialize the Instagram Social Follower Picker.
        
        Args:
            api_key (str): RapidAPI key for authentication
        """
        self.api_key = api_key
        self.base_url = "https://instagram-social-api.p.rapidapi.com"
        self.headers = {
            "x-rapidapi-host": "instagram-social-api.p.rapidapi.com",
            "x-rapidapi-key": api_key
        }
    
    def get_followers(self, username: str, limit: int = 50) -> List[Dict]:
        """
        Fetch followers for a given Instagram username using Social API.
        
        Args:
            username (str): Instagram username to fetch followers for
            limit (int): Number of followers to fetch (default: 50)
            
        Returns:
            List[Dict]: List of follower data
            
        Raises:
            requests.RequestException: If API request fails
            ValueError: If invalid response is received
        """
        url = f"{self.base_url}/v1/followers"
        
        params = {
            "username_or_id_or_url": username
        }
        
        try:
            print(f"🔍 Fetching followers for @{username}...")
            print(f"📡 Using Instagram Social API")
            
            response = requests.get(
                url,
                headers=self.headers,
                params=params,
                timeout=60  # Longer timeout as this might take time
            )
            
            print(f"📊 Response status: {response.status_code}")
            
            response.raise_for_status()
            
            data = response.json()
            print(f"📄 Response data keys: {list(data.keys()) if isinstance(data, dict) else 'Response is a list'}")
            
            # Check if the API returned an error
            if isinstance(data, dict):
                if "message" in data:
                    if "not subscribed" in data["message"].lower():
                        raise ValueError("❌ API Subscription Required: You need to subscribe to Instagram Social API on RapidAPI")
                    elif "not found" in data["message"].lower():
                        raise ValueError(f"❌ Username '{username}' not found or account is private")
                    else:
                        raise ValueError(f"API Message: {data['message']}")
                
                if "error" in data:
                    raise ValueError(f"API Error: {data['error']}")
            
            # Extract followers from the response
            followers = []
            if isinstance(data, dict):
                if "data" in data:
                    data_section = data["data"]
                    if "items" in data_section:
                        followers = data_section["items"]
                    elif isinstance(data_section, list):
                        followers = data_section
                elif "items" in data:
                    followers = data["items"]
                elif "followers" in data:
                    followers = data["followers"]
            elif isinstance(data, list):
                followers = data
            
            if not followers:
                raise ValueError("No followers found. The account might be private or have no followers.")
            
            # Limit the results if needed
            if limit and len(followers) > limit:
                followers = followers[:limit]
            
            print(f"✅ Successfully fetched {len(followers)} followers!")
            return followers
            
        except requests.RequestException as e:
            if "403" in str(e) or "401" in str(e):
                raise ValueError("❌ API Access Error: Please check your subscription to Instagram Social API")
            elif "timeout" in str(e).lower():
                raise ValueError("❌ Request timeout: The API is taking too long to respond. Try again in a moment.")
            raise requests.RequestException(f"Failed to fetch followers: {str(e)}")
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON response from API")
    
    def select_random_winner(self, followers: List[Dict]) -> Dict:
        """
        Randomly select a winner from the list of followers.
        
        Args:
            followers (List[Dict]): List of follower data
            
        Returns:
            Dict: Selected winner's data
        """
        if not followers:
            raise ValueError("Cannot select winner from empty followers list")
        
        winner = random.choice(followers)
        return winner
    
    def display_winner(self, winner: Dict) -> None:
        """
        Display the selected winner's information.
        
        Args:
            winner (Dict): Winner's data
        """
        print("\n" + "="*60)
        print("🎉 WINNER SELECTED FROM ACTUAL FOLLOWERS! 🎉")
        print("="*60)
        
        # Extract username (handle different possible response formats)
        username = (
            winner.get("username") or 
            winner.get("user", {}).get("username") or
            winner.get("pk") or
            str(winner.get("id", "")) or
            "Unknown"
        )
        
        print(f"🏆 Winner: @{username}")
        
        # Display additional information if available
        if "full_name" in winner:
            print(f"📝 Full Name: {winner['full_name']}")
        elif winner.get("user", {}).get("full_name"):
            print(f"📝 Full Name: {winner['user']['full_name']}")
            
        if "is_verified" in winner and winner["is_verified"]:
            print(f"✅ Verified Account")
        
        if "is_private" in winner:
            privacy = "🔒 Private" if winner["is_private"] else "🌐 Public"
            print(f"🔐 Account: {privacy}")
        
        # Show profile picture if available
        if "profile_pic_url" in winner:
            print(f"🖼️  Profile Picture: Available")
        
        print("="*60)
    
    def run(self, username: str, limit: int = 50) -> str:
        """
        Main method to fetch followers and select a winner.
        
        Args:
            username (str): Instagram username to fetch followers for
            limit (int): Number of followers to fetch
            
        Returns:
            str: Winner's username
        """
        try:
            # Fetch followers
            followers = self.get_followers(username, limit)
            
            # Select random winner
            winner = self.select_random_winner(followers)
            
            # Display winner
            self.display_winner(winner)
            
            # Return winner username
            winner_username = (
                winner.get("username") or 
                winner.get("user", {}).get("username") or
                winner.get("pk") or
                str(winner.get("id", "")) or
                "Unknown"
            )
            
            return winner_username
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            sys.exit(1)


def main():
    """Main function to run the Instagram Social Follower Picker."""
    print("👥 Instagram Social API Follower Picker")
    print("="*45)
    print("🎯 This tool selects winners from ACTUAL followers")
    print("📡 Uses Instagram Social API (WORKING with your subscription!)")
    print("")
    
    # Get API key from environment variable or user input
    api_key = os.getenv("RAPIDAPI_KEY")
    
    if not api_key:
        print("⚠️  RapidAPI key not found in environment variables.")
        api_key = input("Please enter your RapidAPI key: ").strip()
        
        if not api_key:
            print("❌ API key is required to proceed.")
            sys.exit(1)
    
    # Get Instagram username from user input
    username = input("Enter Instagram username (without @): ").strip()
    
    if not username:
        print("❌ Username is required.")
        sys.exit(1)
    
    # Get number of followers to fetch
    limit_input = input("Number of followers to fetch (default 50, recommended for random selection): ").strip()
    limit = 50
    
    if limit_input:
        try:
            limit = int(limit_input)
            if limit < 1:
                limit = 50
                print("⚠️  Using minimum value: 50")
            elif limit > 200:
                limit = 200
                print("⚠️  Using maximum recommended value: 200")
        except ValueError:
            print("⚠️  Invalid number entered. Using default (50).")
    
    # Create picker instance and run
    picker = InstagramSocialFollowerPicker(api_key)
    winner_username = picker.run(username, limit)
    
    print(f"\n🎊 Congratulations to @{winner_username}! 🎊")
    print("👥 This winner was randomly selected from ACTUAL followers!")


if __name__ == "__main__":
    main()