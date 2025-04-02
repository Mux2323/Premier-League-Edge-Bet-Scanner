README - Sports Game Odds Python Project
========================================

This Python project analyzes sports betting markets using data from SportsGameOdds. It’s fully configurable and supports a wide range of sportsbooks. You’ll need to set up a configuration file and obtain an API key.

------------------------------------------------------------
CONFIGURATION SETUP
------------------------------------------------------------

Edit the `config.py` file to set your preferences:

    # === CONFIGURATION ===
    API_KEY = "Enter Your API Key Here"
    BASE_URL = "https://api.sportsgameodds.com/events"

    SPORT_ID = "SOCCER"
    LEAGUE_ID = "EPL"
    TARGET_STAT_ID = "points"
    TARGET_PERIOD_ID = "reg"
    TARGET_BETTYPE_ID = "ml3way"

    INCLUDED_BOOKS = {
        "1xbet", "888sport", "ballybet", "barstool", "betvictor", "bet365",
        "betanysports", "betclic", "betfairexchange", "betfairsportsbook",
        "betfred", "betmgm", "betonline", "betparx", "betrsportsbook",
        "betrivers", "betsafe", "betsson", "betus", "betway", "bluebet",
        "bodog", "bookmakereu", "boombet", "bovada", "boylesports", "caesars",
        "casumo", "circa", "coolbet", "coral", "draftkings", "espnbet",
        "everygame", "fanatics", "fanduel", "fliff", "fourwinds", "foxbet",
        "grosvenor", "gtbets", "hardrockbet", "hotstreak", "ladbrokes",
        "leovegas", "livescorebet", "lowvig", "marathonbet", "matchbook",
        "mrgreen", "mybookie", "neds", "nordicbet", "northstarbets",
        "paddypower", "parlayplay", "pinnacle", "playup", "pointsbet",
        "primesports", "prizepicks", "prophetexchange", "si", "skybet",
        "sleeper", "sportsbet", "sportsbetting_ag", "sporttrade", "stake",
        "superbook", "suprabets", "tab", "tabtouch", "thescorebet", "tipico",
        "topsport", "underdog", "unibet", "unknown", "virginbet", "williamhill",
        "windcreek", "wynnbet"
    }

    SHARP_BOOKS = {"pinnacle"}

    SHARP_BOOK_WEIGHTS = {
        "pinnacle": 1.0,
        "tipico": 0.0,
    }

    MIN_EDGE = 0.0
    ALERT_THRESHOLD = 0.0

    DISCORD_ENABLED = False  # Change to True to enable Discord alerts
    DISCORD_WEBHOOK_URL = "Insert a Discord webhook here to populate a channel"

For an up-to-date list of available sportsbooks, visit:
https://sportsgameodds.com/docs/data-types/bookmakers

------------------------------------------------------------
GETTING AN API KEY
------------------------------------------------------------

1. Go to: https://sportsgameodds.com/?via=mux2323
2. Sign up for an account
3. Log into your dashboard
4. Copy your API key
5. Paste it into the `API_KEY` field in `config.py`

------------------------------------------------------------
RUNNING THE PROJECT
------------------------------------------------------------

1. Clone this repository:
       git clone https://github.com/your-username/your-repo-name.git
       cd your-repo-name

2. Install the dependencies:
       pip install -r requirements.txt

3. Edit `config.py` with your API key and preferences

4. Run the script:
       python main.py

------------------------------------------------------------
AFFILIATE DISCLOSURE
------------------------------------------------------------

The link to SportsGameOdds (https://sportsgameodds.com/?via=mux2323) is an affiliate link.  
If you sign up through it, I may receive a commission at no extra cost to you.  
This helps support ongoing development and maintenance of this project. Thanks for the support!

------------------------------------------------------------
CONTACT
------------------------------------------------------------

Questions or feedback?
- Open an issue on GitHub
- Or email: dunk.mike@yahoo.com
