---
title: Final Agent Assignment
emoji: 🕵🏻‍♂️
colorFrom: indigo
colorTo: indigo
sdk: gradio
sdk_version: 5.34.2
app_file: app.py
pinned: false
hf_oauth: true
# optional, default duration is 8 hours/480 minutes. Max duration is 30 days/43200 minutes.
hf_oauth_expiration_minutes: 480
---

For each agent:
- Rename the `.env_example` file to `.env`
- Update the `.env` file with the appropriate values for your environment

Review agent libraries:
- `smolagents` is minimal, suitable for prototyping with basic Python tools. The CodeAgent provided by smolagents are
    simple and very flexible, but not providing much features for controlling the agent.
- `langgraph` is more advanced, providing a framework for building agents with more complex workflows and state management. The developer needs to build a graph for the agent to follow, which can be more beneficial for complex tasks.
