import os
from typing import Optional

# Try to import Databricks LlamaIndex integration
try:
    from llama_index.llms.databricks import Databricks as DbxLLM
    from databricks.sdk import WorkspaceClient
    llamaindex_available = True
except ImportError:
    llamaindex_available = False


def llm_explain_itinerary(itinerary, user_question: Optional[str] = None, api_key: Optional[str] = None):
    """
    Use Databricks LlamaIndex LLM to explain the itinerary or answer a user question about it.
    """
    prompt = (
        "You are a helpful wellness travel assistant. "
        + (f"Given the following itinerary, answer the user's question.\nItinerary: {itinerary}\nUser question: {user_question}" if user_question else f"Explain the following wellness itinerary in a friendly, concise way.\nItinerary: {itinerary}")
    )
    # Try Databricks LlamaIndex first
    if llamaindex_available:
        try:
            # Try to get Databricks host/token from env or WorkspaceClient
            db_host = os.getenv("DATABRICKS_HOST")
            db_token = os.getenv("DATABRICKS_TOKEN")
            if not (db_host and db_token):
                w = WorkspaceClient()
                db_host = db_host or w.config.host
                db_token = db_token or w.tokens.create(comment="for model serving", lifetime_seconds=1200).token_value
            llm = DbxLLM(
                model="databricks-llama-4-maverick",
                api_key=db_token,
                api_base=f"{db_host}/serving-endpoints/"
            )
            response = llm.complete(prompt)
            return response.text if hasattr(response, 'text') else str(response)
        except Exception as e:
            return f"[ERROR] Databricks LLM call failed: {e}"
    return "[ERROR] Databricks LlamaIndex LLM is not available. Please install llama-index-llms-databricks and ensure Databricks credentials are set." 