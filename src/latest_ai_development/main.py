#!/usr/bin/env python
import sys
import warnings
from datetime import datetime

from latest_ai_development.crew import PRAutomationCrew

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

def run():
    """
    Run PR automation crew.
    """
    inputs = {
        "topic": "AI companies and startups",
        "current_year": str(datetime.now().year)
    }

    try:
        PRAutomationCrew().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"PR Automation failed: {e}")

def run_with_trigger():
    """
    Run the crew with webhook / cron trigger.
    """
    import json

    if len(sys.argv) < 2:
        raise Exception("Trigger payload missing")

    trigger_payload = json.loads(sys.argv[1])

    inputs = {
        "topic": trigger_payload.get("topic", "AI companies"),
        "current_year": str(datetime.now().year)
    }

    return PRAutomationCrew().crew().kickoff(inputs=inputs)
