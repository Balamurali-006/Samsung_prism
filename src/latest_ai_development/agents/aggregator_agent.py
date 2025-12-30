from crewai import Agent

def get_aggregator_agent(llm):
    return Agent(
        role="Insight Aggregation Agent",
        goal="Merge all agent outputs into a clean, structured JSON response",
        backstory=(
            "You are responsible for producing final structured insights "
            "that strictly follow a predefined JSON schema."
        ),
        llm=llm,
        verbose=False,
        allow_delegation=False
    )
