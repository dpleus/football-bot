from src.agents.bundesliga_agent import ask_question
import uuid

def main():
    """Main function to run the Bundesliga agent. Multi-turn conversation."""
        
    thread_id = str(uuid.uuid4())
    
    while True:
        question = input("\nAsk a question about Bundesliga data (or 'quit' to exit): ")
        if question.lower() == 'quit':
            break
        try:
            answer = ask_question(question, thread_id)
            print("\nAnswer:", answer)
            
            # Print detailed interaction information
            #print(interaction_history)
            
        except Exception as e:
            print(f"Error: {str(e)}")

if __name__ == "__main__":
    main() 