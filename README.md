
# 🧠 Job Manager Agent System  
A two-agent system for **extracting**, **managing**, and **tracking** job applications using **PydanticAI**, custom tools, and local ollama models.

---

## ✅ Features

### 🧩 Dual Agent Architecture
- **Agent 1 – Job Extractor**
  - Extracts structured job data (role, company, tasks, job type, location, source, link)
  - Detects URLs and **always performs web search first**  via `web_search`
  - Returns a clean structured job object

- **Agent 2 – Job Manager**
  - Manages job entries using CRUD‑style tools
  - Supports:
    - `add_job`
    - `list_jobs`
    - `delete_job_byrole`
    - `delete_job_byid`
    - `update_status`
    - `update_job_role`
    - `update_tasks`
    - `jobs_count`

---

## 🔧 Technologies Used

This experiment uses several Python libraries beyond PydanticAI:

### ✅ PydanticAI Imports
```python
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider
```

### ✅ Search & Parsing Tools
```python
import requests
from bs4 import BeautifulSoup  # HTML parser
```

These support:
- Web scraping
- Local job storage
- JSON management
- Unique IDs
- Strong typing
- Task extraction logic

---

## 🌍 Environment Configuration
Your `.env` file should contain:

```
MODEL_NAME=qwen3.5:9b
BASE_URL=http://localhost:11434/v1
API_KEY=ollama
```

✅ This allows full compatibility with **Ollama** using the Qwen 3.5 9B model.

---

## 📦 Project Structure
```
.
├── main.py               # Entry point with both agents
├── tools.py              # Job manager tool functions
├── README.md             # Documentation
└── .env                  # Model config
```

---

## ▶️ Running the Program
```bash
python main.py
```

You will see:
```
Welcome to the Job Manager Agent!
Type your question or paste job details or link to extract the details.
Commands: 'quit' to exit
```

---

## ✅ Example Usage
### Add job from a URL
```
add this job https://example.com/job123
```

### List jobs
```
list jobs
```

### Update job status
```
update status for job ID 3 to Interviewing
```

---

## 🧰 Tools Summary
All job management operations are executed through the following tools:
- **add_job** – Add structured job entry
- **list_jobs** – Output all stored jobs
- **delete_job_byrole** – Remove job by role name
- **delete_job_byid** – Remove job by internal ID
- **update_status** – Modify job process state
- **update_job_role** – Change job title
- **update_tasks** – Replace job task description
- **jobs_count** – Return total number of stored jobs

---

## ✅ Summary
This system demonstrates:
- A practical multi-agent pattern using **PydanticAI**
- Automatic job extraction from text & URLs
- Web search via BeautifulSoup parsing
- Robust job management with tool-based LLM interaction
- Seamless integration with **Ollama** running Qwen 3.5:9b

Ideal for experiments involving LLM tooling, agent chaining, and structured data extraction.

---