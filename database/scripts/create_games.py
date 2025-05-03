# Cursor generated code

import requests
import csv
from datetime import datetime

GAMES_PATH = 'database/data/bundesliga_games.csv'
MATCH_ENDPOINT = 'https://api.openligadb.de/getmatchdata/bl1/2024'

def fetch_bundesliga_games():
    url = MATCH_ENDPOINT
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"Error fetching data: {response.status_code}")
        return None
    
    return response.json()

def process_games(games):
    processed_games = []
    
    for game in games:
        processed_game = {
            'match_id': game['matchID'],
            'matchday': game['group']['groupOrderID'],
            'matchDateTime': game['matchDateTime'],
            'home_team': game['team1']['teamName'],
            'away_team': game['team2']['teamName'],
            'home_goals': game['matchResults'][1]['pointsTeam1'] if len(game['matchResults']) > 1 else None,
            'away_goals': game['matchResults'][1]['pointsTeam2'] if len(game['matchResults']) > 1 else None
        }
        processed_games.append(processed_game)
    
    return processed_games

def save_to_csv(games, filename=GAMES_PATH):
    if not games:
        print("No games to save")
        return
    
    fieldnames = ['match_id', 'matchday', 'matchDateTime', 'home_team', 'away_team', 'home_goals', 'away_goals']
    
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(games)
    
    print(f"Data saved to {filename}")

if __name__ == "__main__":
    print("Fetching Bundesliga games...")
    games = fetch_bundesliga_games()
    
    if games:
        processed_games = process_games(games)
        save_to_csv(processed_games)
    else:
        print("Failed to fetch games")

