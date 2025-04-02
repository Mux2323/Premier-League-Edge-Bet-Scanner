# ⚽ EPL 1X2 Value Finder — Sports Betting with Python

Welcome to the **EPL_1x2.py** project — a sharp, data-driven script that helps you find value bets in the 1X2 market (3-way moneylines) for the English Premier League.

This tool connects to the [SportsGameOdds](https://sportsgameodds.com/?via=mux2323) API, devigs sharp lines like Pinnacle, calculates fair odds, and detects edges in the betting market — optionally sending real-time alerts to your Discord channel.

---

## 🔥 Why Use This?

Whether you're a serious bettor or a data nerd, this tool gives you:

- ✅ **Real-time odds comparison** across 75+ sportsbooks  
- 🧠 **Sharp book weighting & devigging** to reveal true market prices  
- ✂️ **Edge detection** to bet only when there's value  
- 📲 **Discord alerts** (optional) when bets beat your edge threshold  
- ⚙️ **Fully customizable** config for sport, league, market, and books  

No more betting blind. Let the data work for you.

---

## 🛠️ How It Works

1. Pulls EPL 1X2 (moneyline) odds from SportsGameOdds API  
2. Filters for specific books (e.g., Pinnacle, DraftKings, etc.)  
3. Devigs the sharpest books using weighted probabilities  
4. Compares market odds to fair odds to find +EV bets  
5. Pushes alerts to Discord if configured
6. Creates a .csv file of all edges based on your criteria 

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/Mux2323/Premier-League-EdgeBet-Finder.git
cd Premier-League-EdgeBet-Finder
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Get Your API Key

Sign up for a free or premium API key here:  
👉 [https://sportsgameodds.com/?via=mux2323](https://sportsgameodds.com/?via=mux2323)

Then paste your API key into the config section of `EPL_1x2.py`.

---

## ⚙️ Configuration

Inside `EPL_1x2.py`, adjust the top section:

```python
API_KEY = "Enter Your API Key Here"
BASE_URL = "https://api.sportsgameodds.com/events"

SPORT_ID = "SOCCER"
LEAGUE_ID = "EPL"
TARGET_STAT_ID = "points"
TARGET_PERIOD_ID = "reg"
TARGET_BETTYPE_ID = "ml3way"

INCLUDED_BOOKS = {
    "pinnacle", "betonline", "draftkings", "fanduel",
    "caesars", "betway", "ladbrokes", "888sport"
}

SHARP_BOOKS = {"pinnacle"}
SHARP_BOOK_WEIGHTS = {
    "pinnacle": 1.0,
    "tipico": 0.0,
}

MIN_EDGE = 0.03  # Only consider bets with 3%+ edge
ALERT_THRESHOLD = 0.05  # Push to Discord if edge exceeds 5%

DISCORD_ENABLED = False
DISCORD_WEBHOOK_URL = "Paste your Discord webhook here"
```

🧾 Full list of supported sportsbooks:  
👉 [https://sportsgameodds.com/docs/data-types/bookmakers](https://sportsgameodds.com/docs/data-types/bookmakers)

---

## 📣 Optional: Discord Alerts

Want bets sent directly to Discord?

1. Set `DISCORD_ENABLED = True` in `EPL_1x2.py`  
2. Paste your `DISCORD_WEBHOOK_URL`  
3. You'll get auto-alerts when edges hit your threshold

---

## 🎯 Who This Is For

- 🧠 Data-driven sports bettors  
- 📈 EV hunters & arbitrage enthusiasts  
- 🤖 Modelers who want a modular value detection base  
- 🎓 Students learning real-world data applications  

---

## 🧠 Roadmap Ideas

- Web UI for tracking and filtering value  
- Historical ROI tracker  
- Support for props, totals, and spreads  
- Custom devigging methods (e.g. Shin, Logit)

---

## 💸 Affiliate Disclosure

The link to SportsGameOdds ([https://sportsgameodds.com/?via=mux2323](https://sportsgameodds.com/?via=mux2323)) is an affiliate link.  
If you sign up through it, I may receive a small commission — at no cost to you.  
It helps support development of projects like this one 🙏

---

## 📬 Contact

Have questions, feedback, or want to collaborate?

- 📧 Email: dunk.mike@yahoo.com  
- 💼 LinkedIn: [Michael Dunk](https://www.linkedin.com/in/michael-dunk-1a8936335)  
- 🐛 Report a bug: [Open an issue](https://github.com/your-username/your-repo-name/issues)

---

> ⚠️ Disclaimer: This script is for informational/educational purposes only. Bet responsibly.
