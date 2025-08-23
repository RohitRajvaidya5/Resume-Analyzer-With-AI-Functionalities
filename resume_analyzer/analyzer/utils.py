import logging
import os
from dotenv import load_dotenv
from portia import (
    Config,
    DefaultToolRegistry,
    Portia,
    StorageClass,
    open_source_tool_registry,
    LLMProvider,
)
from portia.cli import CLIExecutionHooks
import json


def analyze_resume(model_name, resume_text, job_description):
    # Silence logs
    logging.disable(logging.CRITICAL)

    # Load .env file
    load_dotenv()

    # Fetch key from environment
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    if not GOOGLE_API_KEY:
        raise ValueError("GOOGLE_API_KEY is not set. Please check your .env file.")

    # Configure Portia with Google Gemini
    google_config = Config.from_default(
        llm_provider=LLMProvider.GOOGLE,
        default_model=f"google/{model_name}",
        google_api_key=GOOGLE_API_KEY
    )

    portia = Portia(
        config=google_config,
        tools=DefaultToolRegistry(google_config),
        execution_hooks=CLIExecutionHooks(),
    )

    # Prompt for Resume-to-Job Match Analyzer
    prompt = f"""
 You are an AI Resume-to-Job Match Analyzer. Compare the following RESUME and JOB DESCRIPTION. Return ONLY a valid JSON object with these fields: - match_score: float from 1 to 10 - strengths: list of top 3 strengths - missing_keywords: list of missing important skills - improvement_tips: list of resume improvement tips RESUME: {resume_text} JOB DESCRIPTION: {job_description} and send rajvaidyarohit25@outlook.com a report in plain text not json about it.
"""

    try:
        plan = portia.plan(prompt)

        if not plan:
            print("⚠️ Plan creation failed. Check model name, quota, or missing API keys.")
            return False

        print(plan.pretty_print())
        plan_run = portia.run_plan(plan, end_user="its me, mario")

        if plan_run and plan_run.outputs:
            print(plan_run.outputs)
            return True
        else:
            print("⚠️ No outputs returned from Portia.")
            return False

    except Exception as e:
        print("Error:", e)
        return False

# Example resume and job description
resume = """
Software Engineer with 2+ years of experience in Python, Django, SQL, and automation.
Worked on RPA (Automation Anywhere), Selenium, and Playwright for process optimization.
Built internal tools to reduce manual effort by 40%.
"""

jd = """
We are looking for a Backend Developer with experience in Python, Django, REST APIs,
cloud platforms (AWS/GCP), and system design. Knowledge of containerization (Docker, Kubernetes) and database optimization is a plus.
"""


def analyze_resume_with_fallback(resume, jd):
    models = [
        "gemini-2.0-flash",
        "gemini-1.5-flash",
        "gemini-1.5-pro",
        "gemini-2.5-flash"
    ]

    for model in models:
        print(f"🔄 Attempting with {model} ...")
        try:
            result = analyze_resume(model, resume, jd)
            if result:  # Only succeed if non-empty / valid result
                print(f"✅ Resume analysis completed successfully with {model}")
        except Exception as e:
            print(f"⚠️ {model} failed with error: {e}")
            continue  # Try the next model

    print("❌ All models failed. Please check API keys, quota, or network issues.")
    return None

# analyze_resume_with_fallback(resume, jd)
