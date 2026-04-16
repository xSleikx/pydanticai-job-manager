from pydantic_ai import RunContext
from ddgs import DDGS
import json
import uuid
from pathlib import Path
from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import datetime
from typing import Set, Callable, Any
from requests.exceptions import RequestException, SSLError, Timeout

import requests
from bs4 import BeautifulSoup

# -------------------
# Data Model
# -------------------
class Job(BaseModel):
    id: Optional[str] = None
    job_role: str
    company: str
    location: str
    job_type: str
    status: Optional[str] = None
    tasks: str
    source: str
    link: str


# -------------------
# Storage
# -------------------

JOB_FILE = Path(__file__).parent / "jobs.json"

if not JOB_FILE.exists():
    JOB_FILE.write_text("[]")


def read_jobs() -> List[Dict]:
    # return json.loads(JOB_FILE.read_text())
    return json.loads(JOB_FILE.read_text(encoding="utf-8"))

def write_jobs(jobs: List[Dict]):
    JOB_FILE.write_text(
        json.dumps(jobs, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

# -------------------
# Tools
# -------------------

# fetch text from the provided URL, Agent summarizes the content, and prepare data for storage in jobs.json
def web_search(ctx, url: str) -> dict:
    print("\nweb_search tool used\n")

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        res = requests.get(url, headers=headers, timeout=10)
        res.raise_for_status()  # raises HTTPError for bad status codes

    except SSLError as e:
        return {
            "error": "SSL error",
            "message": str(e),
            "url": url
        }

    except Timeout:
        return {
            "error": "Timeout error",
            "message": "Request took too long",
            "url": url
        }

    except RequestException as e:
        return {
            "error": "Request error",
            "message": str(e),
            "url": url
        }

    try:
        soup = BeautifulSoup(res.text, "html.parser")
        text = soup.get_text(separator="\n", strip=True)

        if not text:
            return {
                "error": "Empty content",
                "url": url
            }

        return {
            "url": url,
            "text": text
        }

    except Exception as e:
        return {
            "error": "Parsing error",
            "message": str(e),
            "url": url
        }

async def add_job(ctx: RunContext, job: Job) -> dict:
    applied_date = datetime.utcnow().strftime("%d.%m.%Y")  # DD.MM.YYYY format
    job_id = str(uuid.uuid4())
    job_item = {
        "id": job_id,
        "job_role": job.job_role,
        "company": job.company,
        "job_type": job.job_type,
        "location": job.location,
        "status": f"applied ({applied_date})",
        "tasks": job.tasks,
        "source": job.source,
        "link": job.link
    }
    # Load existing jobs
    jobs = read_jobs()
    jobs.append(job_item)
    print("job has been added by agent")

    # Save back
    write_jobs(jobs)
    return job_item


async def list_jobs(ctx: RunContext) -> List[Dict]:
    """Return all saved jobs."""
    return read_jobs()

async def delete_job_byrole(ctx: RunContext, job_role: str)-> dict:
    jobs = read_jobs()
    for job in jobs:
        if job.get("job_role") == job_role:
            jobs.remove(job)
            write_jobs(jobs)
            return {"message": f"Job '{job_role}' deleted successfully."}
    return {"error": f"Job with id '{job_role}' not found."}

async def delete_job_byid(ctx: RunContext, job_id: str)-> dict:
    jobs = read_jobs()
    for job in jobs:
        if job.get("id") == job_id:
            jobs.remove(job)
            write_jobs(jobs)
            return {"message": f"Job '{job_id}' deleted successfully."}
    return {"error": f"Job with id '{job_id}' not found."}

async def update_status(ctx: RunContext, job_id: str, status: str) -> dict:
    jobs = read_jobs()
    for job in jobs:
        if job["id"] == job_id:
            job["status"] = status
            write_jobs(jobs)
            return job
    return {"error": "Job not found", "id": job_id}

async def update_job_role(ctx: RunContext, job_id: str, job_role: str) -> dict:
    jobs = read_jobs()
    for job in jobs:
        if job["id"] == job_id:
            job["job_role"] = job_role
            write_jobs(jobs)
            return job
    return {"error": "Job not found", "id": job_id}

async def update_tasks(ctx: RunContext, job_id: str, tasks: str) -> dict:
    jobs = read_jobs()
    for job in jobs:
        if job["id"] == job_id:
            job["tasks"] = tasks
            write_jobs(jobs)
            return job
    return {"error": "Job not found", "id": job_id}

async def jobs_count(ctx: RunContext) -> int:
    jobs = read_jobs()
    return len(jobs)
