from crewai import Crew, Task
from agents.web_agent import get_web_agent
from crews.llm_factory import get_light_llm
from tools.token_counter import estimate_tokens_for_model, track_token_usage


def run_collection_crew(competitor_name: str, website: str):
    llm = get_light_llm()
    agent = get_web_agent(llm)

    task = Task(
    description=f"""
    Extract product features, pricing, and offerings from:
    {website}
    """,
    expected_output="""
    JSON object:
    {
      "competitor": "string",
      "features": ["string"],
      "pricing": "string",
      "offerings": ["string"]
    }
    """,
    agent=agent
)


    crew = Crew(
        agents=[agent],
        tasks=[task],
        verbose=False
    )

    result = crew.kickoff()
    
    # Track token usage for collection crew
    task_desc = task.description
    result_str = str(result) if result else ""
    
    input_tokens = estimate_tokens_for_model(task_desc, llm.model)
    output_tokens = estimate_tokens_for_model(result_str, llm.model)
    
    track_token_usage(f"Collection ({llm.model})", input_tokens, output_tokens)
    
    return result

