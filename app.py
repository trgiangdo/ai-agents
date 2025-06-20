from src.gradio_ui import GradioUI
from src.utils._agents import get_agent

if __name__ == "__main__":
    agent = get_agent("alfred")

    GradioUI(agent).launch()
