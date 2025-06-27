from ..agents import alfred, gaia_agent


def get_agent(name: str):
    """
    Get the agent by name.
    """
    agents = {
        "alfred": alfred,
        "gaia": gaia_agent,
    }

    if name in agents:
        return agents[name]
    else:
        raise ValueError(f"Agent '{name}' not found.")
