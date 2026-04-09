from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider

from dotenv import load_dotenv
import os

from tools import (
    web_search,
    add_job,
    list_jobs,
    delete_job_byrole,
    delete_job_byid,
    update_status,
    update_job_role,
    update_tasks,
    jobs_count
)

tools_manager_agent = (add_job, list_jobs, delete_job_byrole, delete_job_byid, update_status, update_job_role, update_tasks, jobs_count)

# Load env
load_dotenv()
model_name = os.getenv("MODEL_NAME") # qwen3.5:9b or any other ollama model
base_url = os.getenv("BASE_URL")
api_key = os.getenv("API_KEY")

# Model
model = OpenAIChatModel(
    model_name,
    provider=OpenAIProvider(
        base_url=base_url,
        api_key=api_key
    ),
)

model2 = OpenAIChatModel(
    model_name,
    provider=OpenAIProvider(
        base_url=base_url,
        api_key=api_key
    ),
)

agent2 = Agent(
    model,
    tools=tools_manager_agent,
    system_prompt="""
You are a professional Job Manager assistant focused on helping users manage their job applications.

Responsibilities:
- Handle only the following job management commands:
  add_job, list_jobs, delete_job_byrole, delete_job_byid, update_status, update_job_role, update_tasks
- show_jobs: display only the job_role, company and status for compact search! if no other fields are specified
- jobs_count: return the total number of jobs in the JSON
- Add new jobs (job_role) only if relevant information is provided by the job extractor agent
"""
)

agent = Agent(
    model,
    tools=[web_search],
    system_prompt="""


You are a professional Job Extractor assistant that helps users manage their job applications.

Important!
If the user provides a URL in the prompt:
For example add "URL", add job from "URL", "URL"
  → ALWAYS use the web_search tool first
  → THEN extract job information

Responsibilities:

1. Extract job information:
    - From user text or job descriptions for example:
        - job_role (e.g., "AI-Engineer (m/w/d)")
        - tasks (e.g., responsibilities like "Deine Aufgaben")
        - source (e.g., LinkedIn, StepStone, Indeed, company website)
        - company (if available)
        - link (URL)
        - location
        - job_type (e.g., Vollzeit, Teilzeit, Homeoffice möglich)
    - Return the extracted information as a structured object:
        job_role: str
        company: str
        location: str
        job_type: strvu
        tasks: str
        source: str
        link: str

2. If the user prompt is related to job management commands and not extraction!
   (add_job, list_jobs, delete_job_byrole, delete_job_byid, update_status, update_job_role, update_tasks
  jobs_count how many jobs):
   → DO NOT process it
   → Simply return the original user prompt as-is
"""
)

def chat_loop():
    """Main chat loop for user interaction."""
    print("\nWelcome to the Job Manager Agent!")
    print("Type your question or paste job details or link to extract the details.")
    print("Commands: 'quit' to exit\n")

    while True:
        user_prompt = input("\nYou: ")
        if user_prompt.lower() == "quit":
            print("Goodbye!")
            break
        if not user_prompt.strip():
            print("Please enter a valid prompt.")
            continue
        
        # Run first agent
        result = agent.run_sync(user_prompt)
        print("Research Agent Output:", result.output)  # use `.output` to get the string

        # Pass output to second agent
        result2 = agent2.run_sync(result.output)  # pass string, not list
        print("Job Manager Output:", result2.output)

def main():

    os.system('cls' if os.name == 'nt' else 'clear')
    chat_loop()


if __name__ == "__main__":
    main()