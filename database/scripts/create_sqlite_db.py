# Cursor generated code
import sqlite3
import pandas as pd
from pathlib import Path

DATABASE_DIR = 'database/data'
DATABASE_FILE = 'database/data/bundesliga.db'
GAMES_FILE = 'database/data/bundesliga_games.csv'
GOALS_FILE = 'database/data/bundesliga_goals.csv'
STANDINGS_FILE = 'database/data/bundesliga_standings.csv'

if __name__ == "__main__":
    """Create SQLite database and import data from CSV files."""
    # Create database directory if it doesn't exist
    db_dir = Path(DATABASE_DIR)
    db_dir.mkdir(exist_ok=True)
    
    # Connect to SQLite database
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    
    # Create matches table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS matches (
        match_id INTEGER PRIMARY KEY,
        matchday INTEGER,
        matchDate DATE,
        matchDateTime DATETIME,
        home_team TEXT,
        away_team TEXT,
        home_goals INTEGER,
        away_goals INTEGER
                   
    )
    ''')
    
    # Create goals table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS goals (
        goal_id INTEGER PRIMARY KEY AUTOINCREMENT,
        match_id INTEGER,
        goalID INTEGER,
        score_home INTEGER,
        score_away INTEGER,
        matchMinute INTEGER,
        goalGetterID INTEGER,
        team TEXT,
        goalGetterName TEXT,
        FOREIGN KEY (match_id) REFERENCES matches(match_id)
    )
    ''')
    
    # Create standings table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS standings (
        matchday INTEGER,
        position INTEGER,
        team TEXT,
        matches INTEGER,
        wins INTEGER,
        draws INTEGER,
        losses INTEGER,
        goals_scored INTEGER,
        goals_conceded INTEGER,
        goal_difference INTEGER,
        points INTEGER,
        PRIMARY KEY (matchday, team)
    )
    ''')
    
    # Create indexes
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_goals_match_id ON goals(match_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_goals_goalgetter ON goals(goalGetterName)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_matches_date ON matches(matchDateTime)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_standings_matchday ON standings(matchday)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_standings_team ON standings(team)')
    
    # Import matches data
    print("Importing matches data...")
    matches_df = pd.read_csv(GAMES_FILE)

    # Convert matchDate to DATE format (eg. 2025-04-26T18:30:00)
    matches_df['matchDate'] = pd.to_datetime(matches_df['matchDateTime']).dt.strftime('%Y-%m-%d')
    matches_df.to_sql('matches', conn, if_exists='replace', index=False)
    
    # Import goals data
    print("Importing goals data...")
    goals_df = pd.read_csv(GOALS_FILE)
    goals_df.to_sql('goals', conn, if_exists='replace', index=False)
    
    # Import standings data
    print("Importing standings data...")
    standings_df = pd.read_csv(STANDINGS_FILE)
    standings_df.to_sql('standings', conn, if_exists='replace', index=False)
    
    # Add foreign key constraint
    cursor.execute('''
    PRAGMA foreign_keys = ON;
    ''')
    
    # Commit changes and close connection
    conn.commit()
    conn.close()
    
    print("Database created successfully!")