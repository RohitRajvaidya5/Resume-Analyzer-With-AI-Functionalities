import logging
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
from portia import PlanBuilderV2
from pydantic import BaseModel
from typing import List
import json



# -------- Define structured output --------
class ResumeMatchResult(BaseModel):
    match_score: float
    strengths: List[str]
    missing_keywords: List[str]
    improvement_tips: List[str]


# -------- Build plan using PlanBuilderV2 --------
def build_resume_analysis_plan(resume_text, job_description):
    builder = PlanBuilderV2(label="Resume to Job Match Analyzer")

    # Define inputs
    resume_input = builder.input(
        name="resume_text", description=f"{resume_text}"
    )
    jd_input = builder.input(
        name="job_description", description=f"{job_description}"
    )

    # Step: LLM analyzes resume vs job description
    builder.llm_step(
        task=(
            """You are a Resume-Job Match Detective 🕵️‍♂️.

Compare the RESUME against the JOB DESCRIPTION and provide a structured evaluation.
Return ONLY a valid JSON object matching this schema:
{
  'match_score': number from 1–10 (higher means stronger match),
  'strengths': list of 3 strengths that the resume already shows off,
  'missing_keywords': list of important skills/keywords from the JD that are hiding from the resume,
  'improvement_tips': list of 3–5 actionable suggestions to level up the resume,
  'schedule_plan_to_improve': create a smart plan to learn from the improvement tips.
}

Do not include any extra text, commentary, or formatting outside of JSON."""
        ),
        inputs=[resume_input, jd_input],
        output_schema=ResumeMatchResult,
        step_name="analyze_resume",
    )

    # Final structured output
    builder.final_output(output_schema=ResumeMatchResult)

    return builder.build()


# -------- Main analyzer --------
def analyze_resume(model_name, resume_text, job_description):
    logging.disable(logging.CRITICAL)
    load_dotenv()

    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    if not GOOGLE_API_KEY:
        raise ValueError("GOOGLE_API_KEY is not set. Please check your .env file.")

    google_config = Config.from_default(
        llm_provider=LLMProvider.GOOGLE,
        default_model=f"google/{model_name}",
        google_api_key=GOOGLE_API_KEY,
        storage_class=StorageClass.MEMORY,
    )

    portia = Portia(
        config=google_config,
        tools=DefaultToolRegistry(google_config),
        execution_hooks=CLIExecutionHooks(),
    )

    plan = build_resume_analysis_plan(resume_text, job_description)

    try:
        plan_run = portia.run_plan(
            plan,
            plan_run_inputs={"resume_text": resume_text, "job_description": job_description},
            end_user="its me, mario",
        )

        if plan_run and plan_run.outputs:
            return plan_run.outputs  # ✅ Already validated JSON
        else:
            print("⚠️ No outputs returned from Portia.")
            return None

    except Exception as e:
        print("Error:", e)
        return None


# -------- Fallback across models --------
def analyze_resume_with_fallback(resume_text, job_description):
    models = [
        "gemini-2.0-flash",
        "gemini-1.5-flash",
        "gemini-1.5-pro",
        "gemini-2.5-flash",
    ]

    for model in models:
        print(f"🔄 Attempting with {model} ...")
        result = analyze_resume(model, resume_text, job_description)

        if result:
            print(f"✅ Success with {model}")

            try:
                # Convert PlanRunOutputs → dict
                result_dict = result.model_dump()

                # Extract the final JSON string safely
                raw_value = result_dict.get("final_output", {}).get("value", "{}")

                # Parse string → Python dict
                parsed = json.loads(raw_value)

                # Pretty print important fields
                print(f"\n📊 Match Score: {parsed.get('match_score', 'N/A')}")

                strengths = parsed.get("strengths", [])
                if strengths:
                    print("💪 Strengths:")
                    for s in strengths[:3]:  # show top 3
                        print(f"   - {s}")

                missing = parsed.get("missing_keywords", [])
                if missing:
                    print("❌ Missing Keywords:")
                    print("   " + ", ".join(missing))

                tips = parsed.get("improvement_tips", [])
                if tips:
                    print("📝 Improvement Tips:")
                    for t in tips:
                        print(f"   - {t}")

                schedule_plan = parsed.get("schedule_plan_to_improve", [])
                if schedule_plan:
                    print("Schedule Plan:")
                    if schedule_plan:
                        print("   " + ", ".join(schedule_plan))

                # ✅ Return parsed dict for downstream usage
                return parsed

            except (json.JSONDecodeError, KeyError) as e:
                print(f"⚠️ Failed to parse LLM output: {e}")
                return None

    print("❌ All models failed.")
    return None


# -------- Example run --------
resume_text = """
Software Engineer with 2+ years of experience in Python, Django, SQL, and automation.
Worked on RPA (Automation Anywhere), Selenium, and Playwright for process optimization.
Built internal tools to reduce manual effort by 40%.
"""

job_description = """
We are looking for a Backend Developer with experience in Python, Django, REST APIs,
cloud platforms (AWS/GCP), and system design. Knowledge of containerization (Docker, Kubernetes) and database optimization is a plus.
"""









