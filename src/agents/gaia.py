import yaml
from smolagents import CodeAgent, DuckDuckGoSearchTool, FinalAnswerTool, VisitWebpageTool

from ..utils._llm_provider import get_llm_model

get_final_answer = FinalAnswerTool()
search_web = DuckDuckGoSearchTool(max_results=10)
visit_webpage = VisitWebpageTool()

model = get_llm_model()

with open("src/prompts/gaia.prompts.yaml", "r") as stream:
    prompt_templates = yaml.safe_load(stream)

gaia_agent = CodeAgent(
    model=model,
    tools=[
        get_final_answer,
        search_web,
        visit_webpage,
    ],
    verbosity_level=1,
    grammar=None,
    planning_interval=None,
    name="gaia_agent",
    description="An AI agent that has coding ability and web search capabilities to help answering questions",
    prompt_templates=prompt_templates,
    additional_authorized_imports=["datetime"],
)
