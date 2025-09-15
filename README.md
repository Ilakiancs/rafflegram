# Instagram Follower Winner Picker

A Python script for selecting random winners from Instagram followers using the Instagram Social API.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Ilakiancs/rafflegram.git
   cd rafflegram
   ```

2. Create virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure API key:
   ```bash
   cp .env.example .env
   ```
   Edit `.env` and add your RapidAPI key:
   ```
   RAPIDAPI_KEY=your_rapidapi_key_here
   ```

## Usage

### For Orientation Events (Time-based Selection)
```bash
python live_orientation_picker.py
```

### For General Giveaways (All Followers)
```bash
python instagram_social_follower_picker.py
```

### Menu Interface
```bash
python instagram_winner_picker.py
```

## Requirements

- Python 3.7+
- RapidAPI account with Instagram Social API access
- Valid Instagram account (public)

## API

Uses Instagram Social API from RapidAPI:
- Host: `instagram-social-api.p.rapidapi.com`
- Endpoint: `/v1/followers`