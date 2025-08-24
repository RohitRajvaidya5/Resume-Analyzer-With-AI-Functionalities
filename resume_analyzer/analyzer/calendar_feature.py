"""
Example showing how Portia OAuth works with Google Gemini.
"""

import os
from dotenv import load_dotenv
from portia import (
    Config,
    DefaultToolRegistry,
    Portia,
    StorageClass,
    LLMProvider,
)
from portia.cli import CLIExecutionHooks

# Load environment variables
load_dotenv()

# Fetch key from environment
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY is not set. Please check your .env file.")

# Define tasks

task = """

"""

# Configure Portia with Google Gemini
google_config = Config.from_default(
    llm_provider=LLMProvider.GOOGLE,
    default_model="google/gemini-2.0-flash",   # ✅ Correct model
    google_api_key=GOOGLE_API_KEY,
)

# Tool registry (cloud-based storage for tasks)
tool_config = Config.from_default(storage_class=StorageClass.CLOUD)

# Instantiate Portia runner
portia = Portia(
    config=google_config,
    tools=DefaultToolRegistry(tool_config),
    execution_hooks=CLIExecutionHooks(),
)

# Run the task (change task0 -> task1 if needed)
plan_run = portia.run(task1)
print(plan_run.outputs)
