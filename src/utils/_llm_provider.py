import os
from typing import Optional

from dotenv import load_dotenv
from smolagents import ApiModel, AzureOpenAIServerModel, InferenceClientModel, OpenAIServerModel

load_dotenv()

__required_env_vars = {
    "azure_openai": [
        "AZURE_OPENAI_MODEL_ID",
        "AZURE_OPENAI_ENDPOINT",
        "AZURE_OPENAI_API_KEY",
        "AZURE_OPENAI_API_VERSION",
    ],
    "openai": ["OPENAI_API_KEY", "OPENAI_MODEL_ID"],
    "huggingface": ["HF_MODEL_ID", "HF_TOKEN"],
}

__DEFAULT_MAX_TOKENS = 4096
__DEFAULT_TEMPERATURE = 0.5


def get_llm_model(llm_provider: Optional[str] = None) -> ApiModel:
    """Get the smolagents model based on the LLM providers.

    If the LLM provider is not specified, it will be retrieved from the environment variable LLM_PROVIDER.

    Args:
        llm_provider (Optional[str]): The LLM provider to use. If not provided, it will be fetched from the environment
            variable LLM_PROVIDER. Possible values are "azure_openai", "openai", or "huggingface".

    Returns:
        ApiModel: An instance of the appropriate model based on the LLM provider.
    """
    llm_provider = llm_provider or os.getenv("LLM_PROVIDER")

    max_token = os.getenv("MAX_TOKENS", __DEFAULT_MAX_TOKENS)
    try:
        max_token = int(max_token)
    except ValueError as e:
        raise ValueError(f"Invalid MAX_TOKENS value: {max_token}. It should be an integer.") from e

    temperature = os.getenv("TEMPERATURE", __DEFAULT_TEMPERATURE)
    try:
        temperature = float(temperature)
    except ValueError as e:
        raise ValueError(f"Invalid TEMPERATURE value: {temperature}. It should be a float.") from e

    if not llm_provider:
        raise ValueError("LLM provider not specified. Please set the LLM_PROVIDER environment variable.")

    if llm_provider.lower() == "azure_openai":
        missing_vars = [var for var in __required_env_vars["azure_openai"] if not os.getenv(var)]
        if missing_vars:
            raise ValueError(f"Missing required Azure OpenAI environment variables: {', '.join(missing_vars)}")

        return AzureOpenAIServerModel(
            model_id=os.getenv("AZURE_OPENAI_MODEL_ID"),
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
            max_tokens=max_token,
            temperature=temperature,
        )

    elif llm_provider.lower() == "openai":
        missing_vars = [var for var in __required_env_vars["openai"] if not os.getenv(var)]
        if missing_vars:
            raise ValueError(f"Missing required OpenAI environment variables: {', '.join(missing_vars)}")

        return OpenAIServerModel(
            model_id=os.getenv("OPENAI_MODEL_ID"),
            api_key=os.getenv("OPENAI_API_KEY"),
            max_tokens=max_token,
            temperature=temperature,
        )

    elif llm_provider.lower() == "huggingface":
        missing_vars = [var for var in __required_env_vars["huggingface"] if not os.getenv(var)]
        if missing_vars:
            raise ValueError(f"Missing required Hugging Face environment variables: {', '.join(missing_vars)}")

        return InferenceClientModel(
            model_id=os.getenv("HF_MODEL_ID"),
            token=os.getenv("HF_TOKEN"),
            max_tokens=max_token,
            temperature=temperature,
        )

    else:
        raise ValueError("No valid model configuration found. Please set the appropriate environment variables.")
