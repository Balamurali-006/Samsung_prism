from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List

# ✅ Import token counter
from latest_ai_development.tools.token_counter import count_tokens


@CrewBase
class PRAutomationCrew():
    """PR Automation & Competitor Monitoring Crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    # -------------------- AGENTS --------------------

    @agent
    def competitor_researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['competitor_researcher'],
            verbose=True
        )

    @agent
    def event_classifier(self) -> Agent:
        return Agent(
            config=self.agents_config['event_classifier'],
            verbose=True
        )

    @agent
    def email_notifier(self) -> Agent:
        return Agent(
            config=self.agents_config['email_notifier'],
            verbose=True
        )

    # -------------------- TASKS --------------------

    @task
    def competitor_research_task(self) -> Task:
        task = Task(
            config=self.tasks_config['competitor_research_task']
        )

        # ✅ Token logging
        def callback(output):
            tokens = count_tokens(str(output))
            print(f"\n🔢 Tokens used in competitor_research_task: {tokens}\n")

        task.callback = callback
        return task

    @task
    def event_classification_task(self) -> Task:
        task = Task(
            config=self.tasks_config['event_classification_task']
        )

        # ✅ Token logging
        def callback(output):
            tokens = count_tokens(str(output))
            print(f"\n🔢 Tokens used in event_classification_task: {tokens}\n")

        task.callback = callback
        return task

    @task
    def email_notification_task(self) -> Task:
        task = Task(
            config=self.tasks_config['email_notification_task'],
            output_file='pr_alert_email.md'
        )

        # ✅ Token logging
        def callback(output):
            tokens = count_tokens(str(output))
            print(f"\n🔢 Tokens used in email_notification_task: {tokens}\n")

        task.callback = callback
        return task

    # -------------------- CREW --------------------

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
            tracing=True  # tracing for CrewAI UI
        )
