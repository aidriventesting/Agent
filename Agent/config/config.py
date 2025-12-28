import os
from dotenv import load_dotenv
from .model_config import ModelConfig

load_dotenv()

_model_config = ModelConfig()


class Config:
    """
    Configuration for Robot Framework Agent.
    Loads settings from environment variables (.env file).
    """

    # LLM Provider Settings
    DEFAULT_LLM_CLIENT = os.getenv("DEFAULT_LLM_CLIENT", "openai")

    # API Keys
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY", "")

    # OmniParser (Hugging Face space)
    OMNIPARSER_SPACE = os.getenv("OMNIPARSER_SPACE", "AI-DrivenTesting/OmniParser-v2")
    OMNIPARSER_API_NAME = os.getenv("OMNIPARSER_API_NAME", "/process")
    OMNIPARSER_USE_PADDLE_OCR = os.getenv("OMNIPARSER_USE_PADDLE_OCR", "true").lower() == "true"
    OMNIPARSER_DEFAULT_BOX_THRESHOLD = float(os.getenv("OMNIPARSER_BOX_THRESHOLD", "0.25"))
    OMNIPARSER_DEFAULT_IOU_THRESHOLD = float(os.getenv("OMNIPARSER_IOU_THRESHOLD", "0.1"))
    OMNIPARSER_DEFAULT_IMAGE_SIZE = int(os.getenv("OMNIPARSER_IMAGE_SIZE", "640"))

    # Default Models
    DEFAULT_OPENAI_MODEL = os.getenv("DEFAULT_OPENAI_MODEL") or _model_config.get_provider_default_model("openai")
    DEFAULT_ANTHROPIC_MODEL = os.getenv("DEFAULT_ANTHROPIC_MODEL") or _model_config.get_provider_default_model("anthropic")
    DEFAULT_GEMINI_MODEL = os.getenv("DEFAULT_GEMINI_MODEL") or _model_config.get_provider_default_model("gemini")

    # Image Upload
    IMGBB_API_KEY = os.getenv("IMGBB_API_KEY", "")
    FREEIMAGEHOST_API_KEY = os.getenv("FREEIMAGEHOST_API_KEY", "")

    @classmethod
    def get_huggingface_token(cls) -> str:
        return cls.HUGGINGFACE_API_KEY

    @classmethod
    def get_omniparser_params(
        cls,
        box_threshold: float | None = None,
        iou_threshold: float | None = None,
        use_paddleocr: bool | None = None,
        imgsz: int | None = None,
    ) -> dict[str, float | bool | int]:
        return {
            "box_threshold": box_threshold if box_threshold is not None else cls.OMNIPARSER_DEFAULT_BOX_THRESHOLD,
            "iou_threshold": iou_threshold if iou_threshold is not None else cls.OMNIPARSER_DEFAULT_IOU_THRESHOLD,
            "use_paddleocr": use_paddleocr if use_paddleocr is not None else cls.OMNIPARSER_USE_PADDLE_OCR,
            "imgsz": imgsz if imgsz is not None else cls.OMNIPARSER_DEFAULT_IMAGE_SIZE,
        }