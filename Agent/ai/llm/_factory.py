from typing import Optional, Callable, Dict
from Agent.ai.llm._baseclient import BaseLLMClient
from Agent.ai.llm._openaiclient import OpenAIClient
from Agent.config.model_config import ModelConfig
from Agent.config.config import Config


class LLMClientFactory:
    """Factory to create LLM client instances. Supports OpenAI, Anthropic, Gemini."""

    _model_config = ModelConfig()
    DEFAULT_MODELS = {
        "openai": _model_config.get_provider_default_model("openai"),
        "anthropic": _model_config.get_provider_default_model("anthropic"),
        "gemini": _model_config.get_provider_default_model("gemini"),
    }

    _registry: Dict[str, Callable[[Optional[str], Config], BaseLLMClient]] = {}

    @staticmethod
    def _create_anthropic_client(model: Optional[str], cfg: Config):
        try:
            from Agent.ai.llm._anthropic import AnthropicClient
        except ImportError as e:
            raise ImportError(
                "anthropic package not installed. "
                "Install with: pip install 'robotframework-agent[anthropic]'"
            ) from e
        return AnthropicClient(
            model=model or LLMClientFactory.DEFAULT_MODELS.get("anthropic"),
            api_key=cfg.ANTHROPIC_API_KEY
        )
    
    @staticmethod
    def _create_gemini_client(model: Optional[str], cfg: Config):
        try:
            from Agent.ai.llm._gemini import GeminiClient
        except ImportError as e:
            raise ImportError(
                "google-generativeai package not installed. "
                "Install with: pip install 'robotframework-agent[gemini]'"
            ) from e
        return GeminiClient(model=model or LLMClientFactory.DEFAULT_MODELS.get("gemini"))

    @staticmethod
    def register_client(name: str, factory: Callable[[Optional[str], Config], BaseLLMClient]) -> None:
        """
        Register custom provider: factory(model, config) -> BaseLLMClient
        Example: factory.register_client("custom", lambda m, c: CustomClient(m))
        """
        LLMClientFactory._registry[name.lower()] = factory

    @staticmethod
    def list_providers() -> Dict[str, str]:
        return {name: "registered" for name in LLMClientFactory._registry.keys()}

    @staticmethod
    def create_client(client_name: str = "openai", model: Optional[str] = None) -> BaseLLMClient:
        client_name_lower = client_name.lower()
        config = Config()

        factory = LLMClientFactory._registry.get(client_name_lower)
        if not factory:
            supported = ", ".join(sorted(LLMClientFactory._registry.keys()))
            raise ValueError(
                f"Unsupported LLM client: {client_name}. Registered providers: {supported}"
            )
        return factory(model, config)


LLMClientFactory._registry.update({
    "openai": lambda model, cfg: OpenAIClient(
        model=model or LLMClientFactory.DEFAULT_MODELS.get("openai"),
        api_key=cfg.OPENAI_API_KEY
    ),
    "anthropic": lambda model, cfg: LLMClientFactory._create_anthropic_client(model, cfg),
    "claude": lambda model, cfg: LLMClientFactory._create_anthropic_client(model, cfg),
    "gemini": lambda model, cfg: LLMClientFactory._create_gemini_client(model, cfg),
    "google": lambda model, cfg: LLMClientFactory._create_gemini_client(model, cfg),
})
