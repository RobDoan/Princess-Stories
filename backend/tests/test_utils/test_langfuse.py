import os
from unittest.mock import patch, MagicMock
from backend.utils.langfuse import get_langfuse_client, get_langfuse_callback

def test_get_langfuse_client_no_keys():
    with patch.dict(os.environ, {}, clear=True):
        # Reset singleton for test
        import backend.utils.langfuse
        backend.utils.langfuse._langfuse_client = None
        
        client = get_langfuse_client()
        assert client is None

@patch("backend.utils.langfuse.Langfuse")
def test_get_langfuse_client_with_keys(mock_langfuse):
    with patch.dict(os.environ, {
        "LANGFUSE_PUBLIC_KEY": "pk-123",
        "LANGFUSE_SECRET_KEY": "sk-123"
    }):
        import backend.utils.langfuse
        backend.utils.langfuse._langfuse_client = None
        
        client = get_langfuse_client()
        assert client is not None
        mock_langfuse.assert_called_once_with(
            public_key="pk-123",
            secret_key="sk-123",
            host="http://langfuse.langfuse.svc.cluster.local"
        )

def test_get_langfuse_callback_no_keys():
    with patch.dict(os.environ, {}, clear=True):
        callback = get_langfuse_callback()
        assert callback is None

@patch("backend.utils.langfuse.CallbackHandler")
def test_get_langfuse_callback_basic(mock_handler):
    with patch.dict(os.environ, {
        "LANGFUSE_PUBLIC_KEY": "pk-123",
        "LANGFUSE_SECRET_KEY": "sk-123"
    }):
        callback = get_langfuse_callback()
        assert callback is not None
        mock_handler.assert_called_once_with(
            public_key="pk-123",
            secret_key="sk-123",
            host="http://langfuse.langfuse.svc.cluster.local"
        )
