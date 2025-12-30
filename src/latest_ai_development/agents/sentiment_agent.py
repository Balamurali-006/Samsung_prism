from crewai import Agent

def get_sentiment_agent(llm):
    return Agent(
        role="Sentiment & Review Analysis Agent",
        goal="Analyze customer sentiment from reviews, forums, and social platforms",
        backstory=(
            "You classify user opinions into positive, negative, and neutral signals "
            "and extract recurring complaints and praise."
        ),
        llm=llm,
        verbose=False,
        allow_delegation=False
    )
