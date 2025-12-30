from crewai import Agent

def get_discovery_agent(llm):
    return Agent(
        role="Competitor Discovery Agent",
        goal="Identify relevant direct and indirect competitors for a given company or product",
        backstory=(
            "You are a market research assistant specialized in identifying competitors "
            "using search results, product descriptions, and industry signals."
        ),
        llm=llm,
        verbose=False,
        allow_delegation=False
    )
