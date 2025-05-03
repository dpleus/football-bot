# Bundesliga Chat Assistant

A conversational AI assistant that provides insights and answers questions about Bundesliga football data. The project uses LangChain and OpenAI to create an intelligent agent that can analyze and discuss Bundesliga statistics, standings, and match data.

## Features

- Interactive chat interface using Streamlit
- Natural language processing for Bundesliga-related queries
- Multi-turn conversation support
- Data-driven insights about teams, players, and matches
- Dynamic data visualization capabilities

## How the Agent Works

The Bundesliga Chat Assistant uses a multi-layered approach to answer questions:

1. **Database Query Layer**
   - Primary source of information is the SQLite database
   - Queries match information, player statistics, and team standings
   - Uses natural language to SQL conversion for complex queries
   - Maintains historical data and current season information

2. **Web Search Fallback**
   - If information is not found in the database, the agent performs web searches
   - Useful for recent news, transfers, or information not yet in the database
   - Ensures up-to-date information even when database is not current

3. **Plotting Agent**
   - Generates visualizations for statistical analysis
   - Creates charts for:
     - Team performance over time
     - Player statistics comparisons
     - League standings visualization
     - Match result distributions
   - Currently in development with basic plotting capabilities

4. **Multi-Agent Architecture**
   - Uses LangGraph for orchestrating different specialized agents
   - Each agent handles specific types of queries:
     - Data retrieval agent
     - Analysis agent
     - Visualization agent
   - Agents collaborate to provide comprehensive answers

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- SQLite
- OpenAI API key

### Installation

1. Clone the repository:
```bash
git clone [repository-url]
cd football-bot
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
# Copy the example environment file
cp env.example .env

# Edit the .env file with your actual values
# Required: OPENAI_API_KEY
# Optional: LANGSMITH_* variables for tracing
```

### Database Setup

The database setup must be performed in the following order:

1. **Create Games Table**
   - First, create the games table which contains match information
   - This is the foundation for other tables

2. **Calculate Standings**
   - After games are created, calculate the standings
   - This depends on the games data being present

3. **Create Goals Table**
   - Place the `cleaned_name_mapping.csv` file in the `database/data` directory
   - This file contains player name mappings for unifying the players names (data quality issues)
   - Create the goals table using this data

4. **Create SQLite Database**
   - The final step is to create the SQLite database
   - This will combine all the tables into a single database file

### Running the Application

1. Run the Streamlit app:
```bash
streamlit run app.py
```

2. Alternatively, run the command-line version:
```bash
python main.py
```

## Project Structure

- `src/` - Source code containing the Bundesliga agent implementation
- `database/` - Database-related files and scripts
- `images/` - Project images and assets
- `app.py` - Streamlit web application
- `main.py` - Command-line interface
- `requirements.txt` - Python dependencies

## Usage

Once the application is running, you can:
- Ask questions about Bundesliga teams, players, and matches
- Get statistical insights and analysis
- Compare teams and players
- Query historical data and current standings

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

[Add your license information here] 