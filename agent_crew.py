# agent_crew.py
import os
from crewai import Agent, Task, Crew, Process, LLM
from dotenv import load_dotenv
from tools import file_writer_tool, file_reader_tool
from db_logger import log_agent_action

# --- 1. Load Environment Variables ---
# This loads the GEMINI_API_KEY from the .env file
load_dotenv() 

# --- 2. LLM Configuration (Final Working Setup) ---
GEMINI_KEY = os.getenv("GEMINI_API_KEY") 

if not GEMINI_KEY:
    # Fail cleanly if the key is missing
    raise ValueError("GEMINI_API_KEY not loaded. Please check your .env file.")

# 🌟 FINAL FIX: Use the direct LiteLLM provider/model format 🌟
# This is the format the internal router requires for proper authentication.
GEMINI_LLM = LLM(
    # Use the 'gemini/' prefix to satisfy LiteLLM's provider check
    model='gemini/gemini-2.5-flash',
    temperature=0.3,
    # Pass the key explicitly to ensure it overrides default credentials
    google_api_key=GEMINI_KEY 
)

# --- 3. Define the Agents (Roles) ---

# The Planner Agent (The Architect) - Decides WHAT to do
planner_agent = Agent(
    role="Project Planner and Task Architect",
    goal="""Create a comprehensive, step-by-step development plan to build a small, functional Python application 
            that meets the user's requirement. Break the task into discrete, ordered steps, including file creation 
            and code logic before delegating to the Coder Agent.""",
    backstory="""You are a veteran Senior Solutions Architect known for designing efficient, logical, 
               and high-quality software solutions. Your specialty is breaking down complex requests 
               into simple, executable tasks for the Coder Agent.""",
    tools=[], 
    llm=GEMINI_LLM, 
    allow_delegation=True, 
    verbose=True 
)

# The Coder Agent (The Builder) - Executes the plan and uses tools
coder_agent = Agent(
    role="Expert Python Code Generator",
    goal="""Execute the steps defined by the Planner, using the provided tools to read and write files 
            to construct the application code accurately and efficiently. Always log actions and results 
            to the database before and after using a tool.""",
    backstory="""You are an expert Python developer with a focus on clean, secure, and idiomatic code. 
               You strictly follow the plan and use the available tools (File Reader/Writer) to interact 
               with the project file system.""",
    tools=[file_writer_tool, file_reader_tool],
    llm=GEMINI_LLM, 
    allow_delegation=False,
    verbose=True
)

# --- 4. Define the Tasks ---

def get_development_task(user_requirement: str):
    """Defines the main task structure: Planning followed by Coding."""
    
    planning_task = Task(
        description=f"""
        Analyze the user's requirement: '{user_requirement}'
        1.  **Determine the necessary files** (e.g., api_app.py, requirements.txt).
        2.  **Generate the complete code/content** for the *requirements.txt* file.
        3.  **Create a step-by-step plan** for the Coder to implement the application.
        4.  The final output must be a clean, numbered list of actions for the Coder to execute.
        """,
        expected_output="A clean, ordered list of steps starting with creating the necessary files. The final step must be the full Python code for the main application file.",
        agent=planner_agent
    )

    coding_task = Task(
        description="""
        Execute the step-by-step plan provided in the context. 
        For every step that involves file I/O, you MUST use the 'Code/File Writer Tool' or 'File Reader Tool'.
        """,
        expected_output="A confirmation message that the entire Python Flask application has been successfully written to the project files, including 'api_app.py' and 'requirements.txt'.",
        agent=coder_agent,
        context=[planning_task]
    )
    
    return [planning_task, coding_task]


# --- 5. Define the Crew (The Team Orchestration) ---

def start_crew(user_requirement: str):
    """Sets up and runs the sequential Crew."""
    tasks = get_development_task(user_requirement)
    
    project_crew = Crew(
        agents=[planner_agent, coder_agent],
        tasks=tasks,
        process=Process.sequential, 
        verbose=True
    )
    
    log_agent_action("System", "Start", f"Starting job for requirement: {user_requirement[:60]}...")
    result = project_crew.kickoff()
    log_agent_action("System", "Finish", "Crew finished execution.")
    
    return result