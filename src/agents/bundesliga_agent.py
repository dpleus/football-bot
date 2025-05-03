from typing import List, Dict
from src.agents.config import EXAMPLE_QUERIES, SYSTEM_PROMPT
from langchain_openai import ChatOpenAI
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langgraph.prebuilt import create_react_agent
from datetime import datetime
from dotenv import load_dotenv
import os
from pathlib import Path
from langchain_community.utilities import SQLDatabase
from typing import Any
from langchain.tools import Tool
from openai import OpenAI
from langgraph.checkpoint.memory import InMemorySaver
import matplotlib.pyplot as plt
import seaborn as sns
import uuid

# Define variables
IMAGE_PATH = "images"
MODEL_NAME = "gpt-4o"
SEARCH_MODEL = "gpt-4o-search-preview"
DATABASE_PATH = Path('database') / 'data' / 'bundesliga.db'

# Initialize components
load_dotenv()

# Initialize OpenAI client for web search
openai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Initialize database
db = SQLDatabase.from_uri(f"sqlite:///{DATABASE_PATH}") 

# Initialize LLM
llm = ChatOpenAI(
        model=MODEL_NAME,
        temperature=0,
        api_key=os.getenv("OPENAI_API_KEY")
)

# Create tools
def web_search(query: str) -> str:
    """Useful for searching the web for current information."""
    response = openai.chat.completions.create(
        model=SEARCH_MODEL,
        messages=[{"role": "user", "content": query}],
    )
    return response.choices[0].message.content

def plot_barplot(data_x: str, data_y: str) -> str:
    """Useful for plotting a graph of the data. Use this when you need to visualize the data.
    data_x: str - The data to plot on the x-axis. As a comma-separated string of values.
    data_y: str - The data to plot on the y-axis. As a comma-separated string of values.
    Returns:
        str: The filename of the graph.
    """
    # Convert comma-separated strings to lists
    try:
        x_values = [x.strip() for x in data_x.split(',')]
        y_values = [int(y.strip()) for y in data_y.split(',')]
        
        if len(x_values) != len(y_values):
            raise ValueError("X and Y data must have the same length")
            
    except Exception as e:
        return f"Error processing data: {str(e)}"
    
    unique_filename = str(uuid.uuid4())
    
    # Set figure size and style
    plt.figure(figsize=(12, 6))
    try:
        plt.style.use('seaborn')
    except:
        plt.style.use('ggplot')  # Fallback to ggplot style if seaborn is not available
    
    # Create the bar plot
    bars = plt.bar(x_values, y_values, color='skyblue', edgecolor='black')
    
    # Add value labels on top of each bar
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{height}',
                ha='center', va='bottom')
    
    # Customize the plot
    plt.title('Top Bundesliga Scorers', pad=20, fontsize=14)
    plt.xlabel('Players', labelpad=10)
    plt.ylabel('Goals', labelpad=10)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    
    # Add grid
    plt.grid(True, axis='y', linestyle='--', alpha=0.7)

    # Save the plot
    plt.savefig(f"{IMAGE_PATH}/{unique_filename}.png", dpi=300, bbox_inches='tight')
    plt.close()  # Close the figure to free memory
    
    print(f"Graph saved to images/{unique_filename}.png")
    return unique_filename


# Initialize toolkit
toolkit = SQLDatabaseToolkit(db=db, llm=llm)
toolkit = toolkit.get_tools()+[web_search]+[plot_barplot]

# Initialize checkpointer
checkpointer = InMemorySaver()

# Initialize agent  
agent = create_react_agent(
        model=llm,
        tools=toolkit,
        prompt=SYSTEM_PROMPT,
        checkpointer=checkpointer
        ) 

# Track all messages
message_history: List[Dict[str, str]] = []

# Track all interactions
interaction_history: List[Dict[str, Any]] = []


def ask_question(question: str, thread_id: str) -> str:
    """Ask a question about Bundesliga data and get a response.
    
    Args:
        question (str): The question to ask about Bundesliga data
        
    Returns:
        str: The response from the AI agent containing the analysis
    """
    # Add user message to history
    message_history.append({"role": "user", "content": question})
    
    # Add example queries to the context if the question is about standings
    context = {
            "messages": [{"role": "user", "content": question}],
            "example_queries": EXAMPLE_QUERIES
        }

    config = {"configurable": {"thread_id": thread_id}}

    response = agent.invoke(context, config=config)
    answer = response["messages"][-1].content

    return answer

