from enum import Enum
from typing import Any

from langchain.chat_models import init_chat_model
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from src.config import settings


class TranslationProvider(str, Enum):
    OPENAI = "openai"
    GOOGLE = "google"
    GROQ = "groq"


class TranslatorService:
    def __init__(
        self,
        provider: TranslationProvider,
    ):
        self.provider = provider
        self.model = self._get_model()
        self.prompt_template = self._get_prompt_template()
        self.chain = self.prompt_template | self.model | StrOutputParser()

    def _get_model(self) -> Any:
        match self.provider:
            case TranslationProvider.OPENAI:
                if not settings.OPENAI_API_KEY:
                    raise ValueError("OpenAI API key not configured in the .env file")
                return init_chat_model(
                    "gpt-4.1-mini", model_provider="openai", temperature=0
                )
            case TranslationProvider.GOOGLE:
                if not settings.GOOGLE_API_KEY:
                    raise ValueError(
                        "Google Gemini API key not configured in the .env file"
                    )
                return init_chat_model(
                    "gemini-2.5-flash-lite-preview-06-17",
                    model_provider="google_genai",
                    temperature=0,
                )
            case TranslationProvider.GROQ:
                if not settings.GROQ_API_KEY:
                    raise ValueError("Groq API key not configured in the .env file")
                return init_chat_model(
                    "llama-3.3-70b-versatile", model_provider="groq", temperature=0
                )

    def _get_prompt_template(self) -> ChatPromptTemplate:
        system_message = (
            "You are a professional subtitle translator."
            "Translate the following text from {source_lang} to {target_lang}."
            "Do not add any extra text, explanations, or apologies."
            "Only provide the direct translation of the text."
            "Preserve the original meaning, tone, and formatting (like line breaks) as much as possible."
        )
        human_message = "{text}"

        return ChatPromptTemplate.from_messages(
            [("system", system_message), ("user", human_message)]
        )

    def translate(self, text: str, source_lang: str, target_lang: str) -> str:
        if not text.strip():
            return ""

        response = self.chain.invoke(
            {"text": text, "source_lang": source_lang, "target_lang": target_lang}
        )

        return response.strip()
