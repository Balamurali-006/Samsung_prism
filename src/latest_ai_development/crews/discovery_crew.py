from crewai import Crew, Task
from agents.discovery_agent import get_discovery_agent
from crews.llm_factory import get_light_llm
from tools.token_counter import estimate_tokens_for_model, track_token_usage


def run_discovery_crew(company_name: str):
    llm = get_light_llm()
    agent = get_discovery_agent(llm)

    task = Task(
    description=f"""
    Identify top 5 direct and indirect competitors of {company_name}.
    Use web knowledge and return ONLY a JSON object with no additional text.
    """,
    expected_output="""
    Return ONLY valid JSON with no additional text or explanation. The JSON must have this exact structure:
    {{
      "competitors": [
        {{
          "name": "string",
          "website": "string",
          "reason": "string"
        }}
      ]
    }}
    Do not include any text before or after the JSON object.
    """,
    agent=agent
)


    crew = Crew(
        agents=[agent],
        tasks=[task],
        verbose=False
    )

    result = crew.kickoff()
    
    # Track token usage for discovery crew
    task_desc = task.description
    result_str = str(result) if result else ""
    
    input_tokens = estimate_tokens_for_model(task_desc, llm.model)
    output_tokens = estimate_tokens_for_model(result_str, llm.model)
    
    track_token_usage(f"Discovery ({llm.model})", input_tokens, output_tokens)
    
    return result

