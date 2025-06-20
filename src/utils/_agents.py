from ..agents import alfred


def get_agent(name: str):
    """
    Get the agent by name.
    """
    agents = {
        "alfred": alfred,
    }

    if name in agents:
        return agents[name]
    else:
        raise ValueError(f"Agent '{name}' not found.")
