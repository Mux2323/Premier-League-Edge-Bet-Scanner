import requests
import pandas as pd
import random
from collections import defaultdict
from datetime import datetime
from zoneinfo import ZoneInfo  # Python 3.9+ for timezone conversion

# === CONFIGURATION ===
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
MIN_EDGE = 0.0
ALERT_THRESHOLD = 0.0

DISCORD_ENABLED = False
DISCORD_WEBHOOK_URL = "Insert a discord webhook here to populate a channel"

def odds_to_prob(odds_str):
    odds = int(odds_str.replace("+", "")) if "+" in odds_str else int(odds_str)
    return 100 / (odds + 100) if odds > 0 else abs(odds) / (abs(odds) + 100)

def prob_to_odds(prob):
    if prob <= 0:
        return float("inf")
    elif prob >= 1:
        return float("-inf")
    if prob > 0.5:
        return round(-100 * prob / (1 - prob))
    else:
        return round(100 * (1 - prob) / prob)

def three_way_devig(home_odds, draw_odds, away_odds):
    probs = [odds_to_prob(home_odds), odds_to_prob(draw_odds), odds_to_prob(away_odds)]
    total = sum(probs)
    return [p / total for p in probs]

def fetch_soccer_odds():
    print("\U0001F504 Fetching EPL 1X2 odds...")
    params = {
        "sportID": SPORT_ID,
        "leagueID": LEAGUE_ID,
        "oddsAvailable": "true",
        "started": "false",
        "limit": 100,
        "apiKey": API_KEY
    }
    response = requests.get(BASE_URL, params=params)
    if response.status_code != 200:
        print(f"❌ Failed to fetch odds: {response.status_code} {response.reason}")
        return []
    data = response.json()
    if not data.get("success"):
        print("❌ API error:", data.get("error"))
        return []
    return data.get("data", [])

def send_discord_alert(content):
    if not DISCORD_ENABLED or not DISCORD_WEBHOOK_URL:
        return
    try:
        requests.post(DISCORD_WEBHOOK_URL, json={"content": content})
    except Exception as e:
        print(f"❌ Error sending Discord alert: {e}")

def parse_and_find_edges(events):
    edges = []
    available_books = set()
    alerts_sent = False

    print(f"\U0001F4E6 Events fetched: {len(events)}")

    for event in events:
        odds_data = event.get("odds", {})
        league = event.get("leagueID", LEAGUE_ID)
        teams = event.get("teams", {})
        home_team = teams.get('home', {}).get('names', {}).get('long', '')
        away_team = teams.get('away', {}).get('names', {}).get('long', '')
        event_name = f"{away_team} @ {home_team}"

        # Convert event start time to EDT
        formatted_date = ""
        try:
            start_time = event.get("status", {}).get("startsAt")
            if start_time:
                try:
                    dt = datetime.fromisoformat(start_time.rstrip("Z"))
                except ValueError:
                    dt = datetime.strptime(start_time, "%Y-%m-%dT%H:%M:%S.%fZ")
                dt = dt.replace(tzinfo=ZoneInfo("UTC"))
                local_dt = dt.astimezone(ZoneInfo("America/New_York"))   #Insert your appropriate timezone here
                formatted_date = local_dt.strftime("%Y-%m-%d %I:%M %p EDT")
        except Exception:
            formatted_date = ""

        market_lines = defaultdict(dict)

        for market_key, prop in odds_data.items():
            if prop.get("statID") != TARGET_STAT_ID or prop.get("periodID") != TARGET_PERIOD_ID:
                continue
            if prop.get("betTypeID") != TARGET_BETTYPE_ID:
                continue

            side_id = prop.get("sideID")

            for book, info in prop.get("byBookmaker", {}).items():
                if not info.get("available") or not info.get("odds"):
                    continue
                market_lines[book][side_id] = info["odds"]

        for book in INCLUDED_BOOKS:
            if book not in market_lines:
                continue
            lines = market_lines[book]
            if not all(outcome in lines for outcome in ["home", "draw", "away"]):
                continue

            if "pinnacle" not in market_lines or not all(outcome in market_lines["pinnacle"] for outcome in ["home", "draw", "away"]):
                continue

            valid_books = [book for book in SHARP_BOOKS if book in market_lines and all(outcome in market_lines[book] for outcome in ["home", "draw", "away"])]
            weights = {book: SHARP_BOOK_WEIGHTS.get(book, 1.0) for book in valid_books}
            total_weight = sum(weights.values())
            if total_weight == 0:
                continue

            fair_probs = {"home": 0, "draw": 0, "away": 0}
            for book in valid_books:
                home, draw, away = three_way_devig(market_lines[book]["home"], market_lines[book]["draw"], market_lines[book]["away"])
                fair_probs["home"] += weights[book] * home
                fair_probs["draw"] += weights[book] * draw
                fair_probs["away"] += weights[book] * away
            for key in fair_probs:
                fair_probs[key] /= total_weight

            for outcome in ["home", "draw", "away"]:
                fair_prob = fair_probs[outcome]
                fair_odd = prob_to_odds(fair_prob)
                book_prob = odds_to_prob(market_lines[book][outcome])
                edge = round((fair_prob - book_prob) * 100, 5)
                if edge < MIN_EDGE * 100:
                    continue

                row = {
                    "League": league,
                    "Event Date": formatted_date,
                    "Book": book,
                    "Game": event_name,
                    "Market": "1X2",
                    "Side": outcome.capitalize(),
                    "Book Odds": market_lines[book][outcome],
                    "Fair Odds": str(fair_odd),
                    "Edge %": edge,
                }

                edges.append(row)
                available_books.add(book)

                if edge >= ALERT_THRESHOLD * 100:
                    alert = (
                        f"\U0001F525 **Premier League - {event_name}**\n"
                        f"Book: `{book}` | Bet: `{outcome}` | Odds: `{market_lines[book][outcome]}` | Fair: `{fair_odd}`\n"
                        f"Edge: `{edge}%`"
                    )
                    send_discord_alert(alert)
                    alerts_sent = True

    if not alerts_sent:
        send_discord_alert("No EPL 1X2 edges this run.")

    return sorted(edges, key=lambda x: x["Edge %"], reverse=True), sorted(available_books)

def main():
    events = fetch_soccer_odds()
    if not events:
        return
    edges, books = parse_and_find_edges(events)
    print(f"\n\U0001F4DA Books with qualifying lines: {books}")
    print(f"\U0001F3AF Found {len(edges)} edges for 1X2 market.\n")
    if edges:
        df = pd.DataFrame(edges)
        print(df.to_string(index=False))
        df.to_csv("EPL_1x2_edges.csv", index=False)
        print("\n💾 Output saved to EPL_1x2_edges.csv")
    else:
        print("⚠️ No edges found.")

if __name__ == "__main__":
    main()
