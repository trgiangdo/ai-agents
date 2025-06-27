import yaml
from smolagents import CodeAgent

from ..tools import (
    DuckDuckGoSearchTool,
    FinalAnswerTool,
    VisitWebpageTool,
)
from ..utils._llm_provider import get_llm_model

get_final_answer = FinalAnswerTool()
search_web = DuckDuckGoSearchTool(max_results=5)
visit_webpage = VisitWebpageTool()

model = get_llm_model()

with open("src/prompts/prompts.yaml", "r") as stream:
    prompt_templates = yaml.safe_load(stream)

boss = CodeAgent(
    model=model,
    tools=[
        get_final_answer,
        search_web,
        visit_webpage,
    ],
    max_steps=6,
    verbosity_level=1,
    grammar=None,
    planning_interval=None,
    name="boss_agent",
    description="Boss agent that has coding ability and web search capabilities for the final project.",
    prompt_templates=prompt_templates,
    additional_authorized_imports=["datetime"],
)
