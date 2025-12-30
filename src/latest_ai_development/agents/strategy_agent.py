from crewai import Agent

def get_strategy_agent(llm):
    return Agent(
        role="Strategic Analysis Agent",
        goal="Produce high-level competitive insights, SWOT analysis, and strategic gaps",
        backstory=(
            "You are a senior competitive intelligence analyst who synthesizes "
            "market data into actionable business strategy."
        ),
        llm=llm,
        verbose=True,
        allow_delegation=False
    )
