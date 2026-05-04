import os
from typing import Any, Callable, Optional

from dotenv import load_dotenv
from openai import OpenAI
from pydantic import PrivateAttr
from tenacity import retry, stop_after_attempt, wait_exponential

from tools.common.base_model import BaseModelTool
from tools.common.messenger import Messenger

load_dotenv()


class OpenAIBase(BaseModelTool):
    _client: OpenAI = PrivateAttr()
    _provider_name: str = PrivateAttr(default="OpenAI")

    @property
    def client(self) -> OpenAI:
        return self._client

    def __init__(self, provider_name: str = "OpenAI", api_key: Optional[str] = None, base_url: Optional[str] = None, **kwargs: Any):
        super().__init__(**kwargs)
        self._provider_name = provider_name
        
        actual_key = api_key or os.getenv("OPENAI_API_KEY")
        if not actual_key:
            raise RuntimeError(f"❌ {self._provider_name} API Key is not defined")
            
        self._client = OpenAI(api_key=actual_key, base_url=base_url)

    @retry(
        wait=wait_exponential(multiplier=1, min=4, max=60),
        stop=stop_after_attempt(5),
        before_sleep=lambda retry_state: Messenger.info(
            f"Error en {retry_state.args[0]._provider_name}. Reintentando en {retry_state.next_action.sleep}s... "
            f"(Intento {retry_state.attempt_number})"
        ),
        reraise=True,
    )
    def _execute_with_retry(self, func: Callable[..., Any], *args: Any, **kwargs: Any) -> Any:
        """
        Executes an OpenAI API call with exponential backoff retry.
        """
        return func(*args, **kwargs)
