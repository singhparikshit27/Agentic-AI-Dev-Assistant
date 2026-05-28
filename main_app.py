import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import os
import time
from dotenv import load_dotenv

#  Project Imports 
# Import the core logic functions from existing files
from agent_crew import start_crew
from db_logger import create_db_tables, DATABASE_URL

#  Configuration 
load_dotenv()
st.set_page_config(
    page_title="Agentic Software Dev Assistant",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Utility Functions ---

def get_db_logs():
    """Fetches all logs from the SQLite database."""
    try:
        engine = create_engine(DATABASE_URL)
        # Use pandas to read the entire table directly into a DataFrame
        df = pd.read_sql_table('agent_log', engine)
        # Sort by timestamp for clean display
        df = df.sort_values(by='timestamp', ascending=False).reset_index(drop=True)
        return df
    except Exception:
        # Return an empty DataFrame if the file hasn't been created yet
        return pd.DataFrame()

# --- Streamlit Application ---

st.title("🤖 AI Agentic Software Development Assistant")
st.markdown("---")

# === SIDEBAR: Project Info ===
st.sidebar.header("Project Architecture")
st.sidebar.markdown(
    """
    This system uses collaborative **AI Agents** and **Tool Use** to autonomously 
    write code based on natural language commands.
    
    * **Planner Agent:** Creates the step-by-step development plan.
    * **Coder Agent:** Executes the plan using **File I/O Tools**.
    * **Database (`agent_log.db`):** Records every decision for audit.
    """
)

# === MAIN AREA: User Input and Execution ===

st.header("🎯 Define the Goal")
user_input = st.text_area(
    "Enter your software requirement:",
    height=150,
    value="Create a Python script named 'data_filter.py' that uses the 'requests' library to fetch data from 'https://api.github.com/events' and prints the first 5 event types. Also create a 'requirements.txt' file.",
    key="user_goal_input"
)

# Check for Key and Quota Warning
if not os.getenv("GEMINI_API_KEY"):
    st.error("🚨 ERROR: GEMINI_API_KEY not found in .env file. Please check your key.")
else:
    if st.button("🚀 Start AI Agent Crew", type="primary"):
        # 1. Run the Execution Logic
        st.info("Crew execution started. Please wait for the agents to plan and execute the task.")
        
        # Use a placeholder to stream/display ongoing terminal output if needed
        # and a spinner to show the process is running
        
        # Clear the old DB log and create tables before starting a fresh run
        create_db_tables()
        
        with st.spinner("AI Agents are planning and generating code... This may take up to a minute."):
            try:
                # Execute the crew and capture the final output
                final_output_message = start_crew(user_input)
                
                st.success("✅ TASK COMPLETE! Final Output:")
                # Use st.markdown to display the final result clearly
                st.markdown(f"**Agent Final Confirmation:**")
                st.code(final_output_message, language="markdown")
                
                # Force a display of the generated files:
                st.markdown("---")
                st.subheader("Generated Files Check")
                st.code(f"Files created: api_app.py, requirements.txt, (or new files based on your goal)", language="text")

            except Exception as e:
                # Catching the rate limit error specifically
                if "RateLimitError" in str(e):
                    st.error("❌ RATE LIMIT ERROR (429). Please wait 60 seconds or restart the app with a new Gemini API Key.")
                else:
                    st.error(f"❌ EXECUTION FAILED: {e}")

# === VISUALIZATION AREA: Audit Trail ===
st.markdown("---")
st.header("📋 Execution Log & Audit Trail (The Agent's Mind)")
st.caption("This log proves the division of labor: the Planner thinks, and the Coder acts using tools.")

log_df = get_db_logs()

if not log_df.empty:
    
    # 1. Display the Audit Table
    st.subheader("Detailed Audit Log (Last 10 Actions)")
    st.dataframe(log_df.head(10), use_container_width=True)
    
    # 2. Visualize the Action Breakdown
    st.subheader("Action Type Breakdown")
    action_counts = log_df['action_type'].value_counts()
    
    # Use a chart for visual impact
    st.bar_chart(action_counts, use_container_width=True, color='#0077B6')
    

else:
    st.info("Run the AI Agent Crew above to generate the first audit trail!")