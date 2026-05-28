# main.py
from agent_crew import start_crew
from db_logger import create_db_tables
from dotenv import load_dotenv
import os # Import os for the key check

if __name__ == "__main__":
    # --- 1. Setup ---
    load_dotenv()
    
    # Check if the key is available before starting the database
    if not os.getenv("GEMINI_API_KEY"):
        print("\nERROR: GEMINI_API_KEY not found in .env file.")
        print("Please add your free Gemini API key to the .env file.")
        exit()

    create_db_tables()
    
    # --- 2. Define the User Requirement ---
    USER_GOAL = """
    Create a simple Python Flask API in a file named 'api_app.py'. 
    This API must have one endpoint: '/health'. 
    When a user visits '/health', the API should return a JSON response: 
    {'status': 'ok'}. 
    
    Ensure you also create a 'requirements.txt' file listing only the 'Flask' library.
    """

    # --- 3. Start the Crew ---
    print("\n==============================================")
    print("   AI AGENT DEVELOPMENT ASSISTANT IS STARTING")
    print("==============================================")
    
    try:
        final_result = start_crew(USER_GOAL)
        
        print("\n==============================================")
        print("         JOB COMPLETE - FINAL RESULT")
        print("==============================================")
        print(final_result)
        
    except Exception as e:
        print(f"\nFATAL ERROR DURING EXECUTION: {e}")
        print("Please review the logs and ensure your Gemini API key is valid and has sufficient quota.")