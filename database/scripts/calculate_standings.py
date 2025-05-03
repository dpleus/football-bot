# Cursor generated code

import pandas as pd
from pathlib import Path
from typing import List, Dict
import numpy as np

STANDINGS_PATH = 'database/data/bundesliga_standings.csv'
MATCHES_PATH = 'database/data/bundesliga_games.csv'
def calculate_standings(matches_df: pd.DataFrame) -> pd.DataFrame:
    """Calculate standings for each matchday."""
    # Initialize empty list to store standings for each matchday
    all_standings = []
    
    # Get unique matchdays
    matchdays = sorted(matches_df['matchday'].unique())
    
    for matchday in matchdays:
        # Get all matches up to current matchday
        current_matches = matches_df[matches_df['matchday'] <= matchday]
        
        # Initialize standings dictionary
        standings: Dict[str, Dict[str, int]] = {}
        
        # Process each match
        for _, match in current_matches.iterrows():
            home_team = match['home_team']
            away_team = match['away_team']
            home_goals = match['home_goals']
            away_goals = match['away_goals']
            
            # Initialize teams if not in standings
            if home_team not in standings:
                standings[home_team] = {
                    'matches': 0,
                    'wins': 0,
                    'draws': 0,
                    'losses': 0,
                    'goals_scored': 0,
                    'goals_conceded': 0,
                    'points': 0
                }
            if away_team not in standings:
                standings[away_team] = {
                    'matches': 0,
                    'wins': 0,
                    'draws': 0,
                    'losses': 0,
                    'goals_scored': 0,
                    'goals_conceded': 0,
                    'points': 0
                }
            
            # Update home team stats
            standings[home_team]['matches'] += 1
            standings[home_team]['goals_scored'] += home_goals
            standings[home_team]['goals_conceded'] += away_goals
            
            # Update away team stats
            standings[away_team]['matches'] += 1
            standings[away_team]['goals_scored'] += away_goals
            standings[away_team]['goals_conceded'] += home_goals
            
            # Update points and results
            if home_goals > away_goals:
                standings[home_team]['wins'] += 1
                standings[home_team]['points'] += 3
                standings[away_team]['losses'] += 1
            elif home_goals < away_goals:
                standings[away_team]['wins'] += 1
                standings[away_team]['points'] += 3
                standings[home_team]['losses'] += 1
            else:
                standings[home_team]['draws'] += 1
                standings[away_team]['draws'] += 1
                standings[home_team]['points'] += 1
                standings[away_team]['points'] += 1
        
        # Convert standings to DataFrame
        standings_df = pd.DataFrame.from_dict(standings, orient='index')
        standings_df['team'] = standings_df.index
        standings_df['matchday'] = matchday
        
        # Calculate goal difference
        standings_df['goal_difference'] = standings_df['goals_scored'] - standings_df['goals_conceded']
        
        # Sort by points, goal difference, goals scored
        standings_df = standings_df.sort_values(
            ['points', 'goal_difference', 'goals_scored'],
            ascending=[False, False, False]
        )
        
        # Add position
        standings_df['position'] = range(1, len(standings_df) + 1)
        
        all_standings.append(standings_df)
    
    # Combine all matchday standings
    final_standings = pd.concat(all_standings)
    
    # Reorder columns
    columns = [
        'matchday', 'position', 'team', 'matches', 'wins', 'draws', 'losses',
        'goals_scored', 'goals_conceded', 'goal_difference', 'points'
    ]
    final_standings = final_standings[columns]
    
    return final_standings

if __name__ == "__main__":
    # Read matches data
    matches_df = pd.read_csv(MATCHES_PATH)
    
    # Calculate standings
    standings_df = calculate_standings(matches_df)
    
    # Save to CSV
    output_path = STANDINGS_PATH
    standings_df.to_csv(output_path, index=False)
    print(f"Standings saved to {output_path}")
