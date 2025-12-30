from crewai import Crew, Task
from agents.aggregator_agent import get_aggregator_agent
from crews.llm_factory import get_light_llm
from tools.token_counter import estimate_tokens_for_model, track_token_usage


def run_aggregation_crew(all_data: dict):
    llm = get_light_llm()
    agent = get_aggregator_agent(llm)

    # Safely serialize provided data snippets for the prompt
    import json as _json
    company_snip = _json.dumps(all_data.get('company', 'Unknown'))
    competitors_snip = _json.dumps(all_data.get('competitors', []))
    details_snip = _json.dumps(all_data.get('competitor_details', []))
    strategy_snip = _json.dumps(all_data.get('strategy', {}))

    task = Task(
        description=f"""
Merge all provided competitive intelligence data into final structured JSON insights.

Data to merge:
- Company: {company_snip}
- Competitors: {competitors_snip}
- Competitor Details: {details_snip}
- Strategy Analysis: {strategy_snip}

Return ONLY a valid JSON object with no additional text containing:
- company: the target company name
- competitors: list of competitor info
- competitor_details: list with collected details
- strategic_insights: the strategy analysis
""",
        expected_output="""
Return ONLY valid JSON with no additional text or explanation. Example structure:
{
  "company": "Samsung",
  "competitors": [...],
  "competitor_details": [...],
  "strategic_insights": {...}
}
""",
        agent=agent,
    )

    crew = Crew(
        agents=[agent],
        tasks=[task],
        verbose=False,
    )

    result = crew.kickoff()
    
    # Track token usage for aggregation crew
    task_desc = task.description
    result_str = str(result) if result else ""
    
    input_tokens = estimate_tokens_for_model(task_desc, llm.model)
    output_tokens = estimate_tokens_for_model(result_str, llm.model)
    
    track_token_usage(f"Aggregation ({llm.model})", input_tokens, output_tokens)

    return result

    return crew.kickoff()

