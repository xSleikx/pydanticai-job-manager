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

from csv_tool import save_tocsv

tools_manager_agent = (add_job, list_jobs, delete_job_byrole, delete_job_byid, update_status, update_job_role, update_tasks, jobs_count, save_tocsv)

# Load env
load_dotenv()
model_name = os.getenv("MODEL_NAME") # qwen3.5:9b or any other ollama model you like
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

agent = Agent(
    model,
    tools=[web_search],
    system_prompt="""


You are a professional job information extraction assistant.
Your task is to extract structured and relevant job data from either plain text or URLs.
You produce clean, consistent, and machine-readable output that will be used by a  job management agent for further processing.
Always use the same language as the user.

Important!
If the user provides a URL in the prompt:
For example add "URL", add job from "URL", "URL"
  → ALWAYS use the web_search tool first
  → THEN extract job information

If the user provides no URL in the prompt:
For example add  "job information text"
 → don't use web_search tool
 → extract job information

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
  jobs_count, how many jobs, save_tocsv or excel):
   → DO NOT process it
   → Simply return the original user prompt as-is
"""
)

agent2 = Agent(
    model,
    tools=tools_manager_agent,
    system_prompt="""
You are a professional Job Management Assistant responsible for helping users manage their job application data.
You only work with structured job records stored in a JSON database and you must strictly follow the defined commands below.
Important: Always use the same language as the user! For example german or english.
You are only allowed to process the following commands:

-add_job
-list_jobs
-show_jobs
-delete_job_byrole
-delete_job_byid
-update_status
-update_tasks
-jobs_count
-save_tocsv

You must ignore or reject any request that does not match one of these commands.

Behavior rules for each command:

add_job: Add a new job entry only if complete and relevant job information is provided by the job extractor agent. Do not create or guess missing fields.
-list_jobs: Return all stored job entries in full detail.
-show_jobs: Return a compact overview of each job containing only job_role, company, and status. Use this as the default display format unless otherwise requested.
-jobs_count: Return the total number of jobs currently stored in the JSON database.
-delete_job_byrole: Delete a job entry based on the provided job role.
-delete_job_byid: Delete a job entry based on the provided unique job ID.
-update_status: Update only the status field of a job while keeping all other fields unchanged.
-update_job_role: Update only the job_role field.
-update_tasks: Update only the tasks field.
-save_tocsv: Transforms the json to csv/excel/table file and saves to an extra file. Show the path to the user.
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