from crewai import Agent

def get_web_agent(llm):
    return Agent(
        role="Web Intelligence Collection Agent",
        goal="Extract product features, pricing, and offerings from competitor websites",
        backstory=(
            "You specialize in extracting structured business information "
            "from websites and landing pages."
        ),
        llm=llm,
        verbose=False,
        allow_delegation=False
    )
