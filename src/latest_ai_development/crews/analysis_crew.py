from crewai import Crew, Task
from agents.strategy_agent import get_strategy_agent
from crews.llm_factory import get_strong_llm
from tools.token_counter import estimate_tokens_for_model, track_token_usage


def run_analysis_crew(company: str, competitors_data: dict):
    llm = get_strong_llm()
    agent = get_strategy_agent(llm)

    task = Task(
    description=f"""
    Perform strategic competitive analysis for {company}
    using the following data:
    {competitors_data}
    """,
    expected_output="""
    JSON object:
    {
      "company": "string",
      "positioning": "string",
      "strengths": ["string"],
      "weaknesses": ["string"],
      "opportunities": ["string"],
      "threats": ["string"]
    }
    """,
    agent=agent
)


    crew = Crew(
        agents=[agent],
        tasks=[task],
        verbose=True
    )

    result = crew.kickoff()
    
    # Track token usage for analysis crew
    task_desc = task.description
    result_str = str(result) if result else ""
    
    input_tokens = estimate_tokens_for_model(task_desc, llm.model)
    output_tokens = estimate_tokens_for_model(result_str, llm.model)
    
    track_token_usage(f"Analysis ({llm.model})", input_tokens, output_tokens)
    
    return result

