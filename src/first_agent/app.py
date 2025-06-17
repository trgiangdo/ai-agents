import datetime
import os

import pytz
import yaml
from dotenv import load_dotenv
from gradio_ui import GradioUI
from smolagents import CodeAgent, InferenceClientModel, load_tool, tool
from tools import DuckDuckGoSearchTool, FinalAnswerTool, VisitWebpageTool

load_dotenv()


# Keep the docstrings format for the description / args / args description
@tool
def my_custom_tool(arg1: str, arg2: int) -> str: # it's important to specify the return type
    """A tool that does nothing yet
    Args:
        arg1: the first argument
        arg2: the second argument
    """
    return "What magic will you build ?"

@tool
def get_current_time_in_timezone(timezone: str) -> str:
    """A tool that fetches the current local time in a specified timezone.
    Args:
        timezone: A string representing a valid timezone (e.g., 'America/New_York').
    """
    try:
        # Create timezone object
        tz = pytz.timezone(timezone)
        # Get current time in that timezone
        local_time = datetime.datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
        return f"The current local time in {timezone} is: {local_time}"
    except Exception as e:
        return f"Error fetching time for timezone '{timezone}': {str(e)}"


get_final_answer = FinalAnswerTool()
search_web = DuckDuckGoSearchTool(max_results=5)
visit_webpage = VisitWebpageTool()

# If the agent does not answer, the model is overloaded, please use another model or the following Hugging Face Endpoint that also contains qwen2.5 coder:
# model_id='https://pflgm2locj2t89co.us-east-1.aws.endpoints.huggingface.cloud'

model = InferenceClientModel(
    max_tokens=2096,
    temperature=0.5,
    model_id="Qwen/Qwen2.5-Coder-32B-Instruct",  # it is possible that this model may be overloaded
    custom_role_conversions=None,
    token=os.getenv("HF_TOKEN"),
)


# Import tool from Hub
image_generation_tool = load_tool("agents-course/text-to-image", trust_remote_code=True)

with open("prompts.yaml", "r") as stream:
    prompt_templates = yaml.safe_load(stream)

agent = CodeAgent(
    model=model,
    tools=[get_current_time_in_timezone, get_final_answer, search_web, visit_webpage],
    max_steps=6,
    verbosity_level=1,
    grammar=None,
    planning_interval=None,
    name="first_coding_agent",
    description="An agent that provides coding assistance and web search capabilities.",
    prompt_templates=prompt_templates,
)

GradioUI(agent).launch()
