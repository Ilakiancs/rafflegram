# Instagram Follower Winner Picker

A Python script for selecting random winners from **ACTUAL Instagram followers** using the Instagram Social API.

## 🎯 What This Does

- ✅ Selects from **REAL followers** (not post likers)
- 📡 Uses Instagram Social API (RapidAPI)
- 🎯 Perfect for Instagram giveaways and contests
- 🎲 Truly random winner selection
- 👥 Fetches actual follower data with usernames and profiles

## 🚀 Quick Start

**Main Script:**
```bash
python instagram_social_follower_picker.py
```

**Menu System:**
```bash
python instagram_winner_picker.py
```

The script will prompt you for:
1. Instagram username (without @)
2. Number of followers to fetch (default: 50)

Example output:
```
👥 Instagram Social API Follower Picker
=============================================
🎯 This tool selects winners from ACTUAL followers

Enter Instagram username (without @): ieeeras_iit
Number of followers to fetch: 30

🔍 Fetching followers for @ieeeras_iit...
✅ Successfully fetched 30 followers!

============================================================
🎉 WINNER SELECTED FROM ACTUAL FOLLOWERS! 🎉
============================================================
🏆 Winner: @daniru0_senarathne
📝 Full Name: Daniru Senarathne
🔐 Account: 🔒 Private
============================================================

🎊 Congratulations to @daniru0_senarathne! 🎊
```

## Prerequisites

- Python 3.7 or higher
- RapidAPI account with access to [Instagram Social API](https://rapidapi.com/DataFanatic/api/instagram-social-api)

## Installation

1. Clone or download this repository:
   ```bash
   cd instagram-scraper
   ```

2. Create a virtual environment (recommended):
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up your API key:
   ```bash
   cp .env.example .env
   ```
   Edit the `.env` file and add your RapidAPI key:
   ```
   RAPIDAPI_KEY=your_actual_rapidapi_key_here
   ```

## API Information

This script uses the Instagram Social API from RapidAPI:
- **Host**: `instagram-social-api.p.rapidapi.com`
- **Main Endpoint**: `/v1/followers`
- **Required Headers**:
  - `x-rapidapi-host: instagram-social-api.p.rapidapi.com`
  - `x-rapidapi-key: your_api_key`

## How It Works

1. **Enter Instagram username** (without @ symbol)
2. **Specify follower count** to fetch (recommended: 50+ for good randomness)
3. **Script fetches actual followers** using the Instagram Social API
4. **Random winner selected** from the follower list
5. **Winner details displayed** with username, full name, and profile info

## Error Handling

The script includes comprehensive error handling for:
- Invalid API responses
- Network connection issues
- Missing or invalid usernames
- Empty follower lists
- API rate limits

## Security Notes

- Never commit your `.env` file to version control
- Keep your RapidAPI key secure and private
- The `.gitignore` file is configured to exclude sensitive files

## License

This project is open source and available under the MIT License.

## Troubleshooting

### Common Issues

1. **Import Error for requests**: Make sure you've activated your virtual environment and installed requirements
2. **API Key Error**: Verify your RapidAPI key is correct and you have access to the Instagram Social API
3. **No followers found**: The username might be private or the API might be rate-limited

### Support

If you encounter issues, please check:
1. Your RapidAPI subscription status for Instagram Social API
2. The Instagram account is public
3. Your internet connection is stable# rafflegram
