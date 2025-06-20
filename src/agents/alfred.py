import yaml
from smolagents import CodeAgent, load_tool

from ..tools import DuckDuckGoSearchTool, FinalAnswerTool, VisitWebpageTool, get_current_time_in_timezone
from ..utils._llm_provider import get_llm_model

get_final_answer = FinalAnswerTool()
search_web = DuckDuckGoSearchTool(max_results=5)
visit_webpage = VisitWebpageTool()

model = get_llm_model()

# Import the image generation tool from Hub
image_generation_tool = load_tool("agents-course/text-to-image", trust_remote_code=True)

with open("src/prompts/prompts.yaml", "r") as stream:
    prompt_templates = yaml.safe_load(stream)

alfred = CodeAgent(
    model=model,
    tools=[get_current_time_in_timezone, get_final_answer, search_web, visit_webpage, image_generation_tool],
    max_steps=6,
    verbosity_level=1,
    grammar=None,
    planning_interval=None,
    name="first_coding_agent",
    description="An agent that provides coding assistance and web search capabilities.",
    prompt_templates=prompt_templates,
)
