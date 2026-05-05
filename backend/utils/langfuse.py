import os
import logging
from langfuse import Langfuse
from langfuse.langchain import CallbackHandler

logger = logging.getLogger(__name__)

_langfuse_client = None

def get_langfuse_client():
    global _langfuse_client
    if _langfuse_client is None:
        public_key = os.environ.get("LANGFUSE_PUBLIC_KEY")
        secret_key = os.environ.get("LANGFUSE_SECRET_KEY")
        host = os.environ.get("LANGFUSE_HOST", "http://langfuse.langfuse.svc.cluster.local")
        
        if public_key and secret_key:
            try:
                _langfuse_client = Langfuse(public_key=public_key, secret_key=secret_key, host=host)
            except Exception as e:
                logger.error(f"Failed to initialize Langfuse client: {e}")
                return None
        else:
            logger.info("Langfuse credentials missing. Tracing disabled.")
    return _langfuse_client

def get_langfuse_callback():
    """Factory for LangChain callback handler. 
    Attributes like user_id and session_id should be passed in the 
    LangChain config metadata with 'langfuse_' prefix.
    """
    try:
        public_key = os.environ.get("LANGFUSE_PUBLIC_KEY")
        secret_key = os.environ.get("LANGFUSE_SECRET_KEY")
        host = os.environ.get("LANGFUSE_HOST", "http://langfuse.langfuse.svc.cluster.local")
        
        if not public_key or not secret_key:
            return None
            
        handler = CallbackHandler(
            public_key=public_key,
            secret_key=secret_key,
            host=host
        )
        return handler
    except Exception as e:
        logger.error(f"Failed to initialize Langfuse callback: {e}")
        return None
