import os

import yaml
from dotenv import load_dotenv
from gradio_ui import GradioUI
from smolagents import AzureOpenAIServerModel, CodeAgent, InferenceClientModel, OpenAIServerModel, load_tool
from tools import DuckDuckGoSearchTool, FinalAnswerTool, VisitWebpageTool, get_current_time_in_timezone

load_dotenv()


def get_model():
    """Function to get the model based on environment variables."""
    if os.getenv("USE_AZURE_OPENAI"):
        return AzureOpenAIServerModel(
            model_id=os.getenv("AZURE_OPENAI_MODEL_ID"),
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
            max_tokens=4096,
            temperature=0.5,
        )

    elif os.getenv("OPENAI_API_KEY"):
        return OpenAIServerModel(
            model_id=os.getenv("OPENAI_MODEL_ID"),
            api_key=os.getenv("OPENAI_API_KEY"),
            max_tokens=4096,
            temperature=0.5,
        )

    elif os.getenv("HF_TOKEN"):
        return InferenceClientModel(
            max_tokens=2096,
            temperature=0.5,
            model_id=os.getenv("HF_MODEL_ID"),
            custom_role_conversions=None,
            token=os.getenv("HF_TOKEN"),
        )

    else:
        raise ValueError("No valid model configuration found. Please set the appropriate environment variables.")


if __name__ == "__main__":
    get_final_answer = FinalAnswerTool()
    search_web = DuckDuckGoSearchTool(max_results=5)
    visit_webpage = VisitWebpageTool()

    model = get_model()

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
