import os
from typing import Optional, List, Dict, Any

# Try to import Databricks LlamaIndex integration
try:
    from llama_index.llms.databricks import Databricks as DbxLLM
    from databricks.sdk import WorkspaceClient
    llamaindex_available = True
except ImportError:
    llamaindex_available = False


def _get_llm(api_key: Optional[str] = None) -> Optional[Any]:
    """
    Helper to instantiate and return the Databricks LlamaIndex LLM client.
    Returns None if not available.
    """
    if not llamaindex_available:
        return None
    try:
        db_host = os.getenv("DATABRICKS_HOST")
        db_token = api_key or os.getenv("DATABRICKS_TOKEN")
        if not (db_host and db_token):
            w = WorkspaceClient()
            db_host = db_host or w.config.host
            db_token = db_token or w.tokens.create(comment="for model serving", lifetime_seconds=1200).token_value
        llm = DbxLLM(
            model="databricks-llama-4-maverick",
            api_key=db_token,
            api_base=f"{db_host}/serving-endpoints/"
        )
        return llm
    except Exception as e:
        # Optionally log error here
        return None


def _build_prompt(base: str, context: Dict, user_question: Optional[str] = None) -> str:
    """
    Helper to build a prompt for the LLM given a base instruction, context, and optional user question.
    """
    prompt = base + "\n" + "\n".join(f"{k}: {v}" for k, v in context.items())
    if user_question:
        prompt += f"\nUser question: {user_question}"
    return prompt


def llm_explain_itinerary(
    itinerary: Dict,
    user_question: Optional[str] = None,
    api_key: Optional[str] = None
) -> str:
    """
    Use Databricks LlamaIndex LLM to explain the itinerary or answer a user question about it.
    Args:
        itinerary (Dict): The itinerary dictionary.
        user_question (Optional[str]): Optional custom question for the LLM.
        api_key (Optional[str]): Optional API key override.
    Returns:
        str: LLM's response with explanation or answer.
    """
    base = "You are a helpful wellness travel assistant."
    context = {"Itinerary": itinerary}
    prompt = _build_prompt(base, context, user_question)
    llm = _get_llm(api_key)
    if llm:
        try:
            response = llm.complete(prompt)
            return response.text if hasattr(response, 'text') else str(response)
        except Exception as e:
            return f"[ERROR] Databricks LLM call failed: {e}"
    return "[ERROR] Databricks LlamaIndex LLM is not available. Please install llama-index-llms-databricks and ensure Databricks credentials are set."


def llm_analyze_venues(
    venues: List[Dict],
    user_profile: Dict,
    user_question: Optional[str] = None,
    api_key: Optional[str] = None
) -> str:
    """
    Use Databricks LlamaIndex LLM to analyze a list of venues and recommend the best ones for the user.
    Args:
        venues (List[Dict]): List of venue dictionaries.
        user_profile (Dict): The user's profile dictionary.
        user_question (Optional[str]): Optional custom question for the LLM.
        api_key (Optional[str]): Optional API key override.
    Returns:
        str: LLM's response with recommendations and reasoning.
    """
    base = (
        "You are a wellness travel assistant. "
        "Given the following user profile and a list of possible venues, "
        "analyze which venues are the best fit for the user and explain your reasoning. "
        "Be concise and specific."
    )
    context = {"User profile": user_profile, "Venues": venues}
    prompt = _build_prompt(base, context, user_question)
    llm = _get_llm(api_key)
    if llm:
        try:
            response = llm.complete(prompt)
            return response.text if hasattr(response, 'text') else str(response)
        except Exception as e:
            return f"[ERROR] Databricks LLM call failed: {e}"
    return "[ERROR] Databricks LlamaIndex LLM is not available. Please install llama-index-llms-databricks and ensure Databricks credentials are set." 