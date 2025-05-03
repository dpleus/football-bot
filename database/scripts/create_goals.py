# Cursor generated code

import requests
import pandas as pd
from typing import List, Dict
import json

MAPPING_PATH = 'database/data/cleaned_name_mapping.csv'
OUTPUT_PATH = 'database/data/bundesliga_goals.csv'
GOALGETTERS_ENDPOINT = 'https://api.openligadb.de/getgoalgetters/bl1/2024'
MATCH_ENDPOINT = 'https://api.openligadb.de/getmatchdata/bl1/2024'

def fetch_match_data() -> List[Dict]:
    """Fetch match data from OpenLigaDB API."""
    url = MATCH_ENDPOINT
    response = requests.get(url)
    return response.json()

def fetch_goalgetters() -> Dict:
    """Fetch goalgetter data from OpenLigaDB API."""
    url = GOALGETTERS_ENDPOINT
    response = requests.get(url)
    return {g['goalGetterId']: g['goalGetterName'] for g in response.json()}

def load_name_mapping() -> Dict[str, str]:
    """Load and create name mapping dictionary."""
    df = pd.read_csv(MAPPING_PATH)
    return dict(zip(df['Original'], df['Unified Name']))

def clean_goalgetter_name(name: str, name_mapping: Dict[str, str]) -> str:
    """Clean goalgetter name using the mapping."""
    return name_mapping.get(name, name)

def process_goals(match_data: List[Dict], goalgetters: Dict, name_mapping: Dict[str, str]) -> List[Dict]:
    """Process match data to extract individual goals."""
    goals_list = []
    
    for match in match_data:
        try:
            match_id = match['matchID']
            home_team = match['team1']['teamName']
            away_team = match['team2']['teamName']
            
            # Get goals and handle None values in matchMinute
            goals = match.get('goals', [])
            # Sort goals by matchMinute, treating None as 0
            goals = sorted(goals, key=lambda x: x['matchMinute'] if x['matchMinute'] is not None else 0)
            
            prev_home_score = 0
            prev_away_score = 0
            
            for goal in goals:
                try:
                    goal_data = {
                        'match_id': match_id,
                        'goalID': goal['goalID'],
                        'score_home': goal['scoreTeam1'],
                        'score_away': goal['scoreTeam2'],
                        'matchMinute': goal['matchMinute'] if goal['matchMinute'] is not None else 0,
                        'goalGetterID': goal['goalGetterID']
                    }
                    
                    # Determine which team scored
                    if goal['scoreTeam1'] > prev_home_score:
                        goal_data['team'] = home_team
                    else:
                        goal_data['team'] = away_team
                        
                    # Update previous scores
                    prev_home_score = goal['scoreTeam1']
                    prev_away_score = goal['scoreTeam2']
                    
                    goals_list.append(goal_data)
                except KeyError as e:
                    print(f"Error processing goal in match {match_id}: {e}")
                    continue
        except KeyError as e:
            print(f"Error processing match: {e}")
            continue
    
    return goals_list

if __name__ == "__main__":
    # Load name mapping
    print("Loading name mapping...")
    name_mapping = load_name_mapping()
    
    # Fetch data
    print("Fetching match data...")
    match_data = fetch_match_data()
    print("Fetching goalgetter data...")
    goalgetters = fetch_goalgetters()
    
    # Process goals
    print("Processing goals...")
    goals_list = process_goals(match_data, goalgetters, name_mapping)
    
    # Convert to DataFrame
    df = pd.DataFrame(goals_list)
    
    # Add goalgetter names and clean them
    df['goalGetterName'] = df['goalGetterID'].map(goalgetters)
    df['goalGetterName'] = df['goalGetterName'].apply(lambda x: clean_goalgetter_name(x, name_mapping))
    
    # Save to CSV
    output_path = OUTPUT_PATH
    df.to_csv(output_path, index=False)
    print(f"Created CSV with {len(df)} goals at {output_path}")
    
    # Print some statistics about name cleaning
    original_names = set(df['goalGetterName'].unique())
    cleaned_names = set(clean_goalgetter_name(name, name_mapping) for name in original_names)
    print(f"Number of unique original names: {len(original_names)}")
    print(f"Number of unique cleaned names: {len(cleaned_names)}")
    print(f"Number of names that were cleaned: {len(original_names - cleaned_names)}")
    
