import re
from enum import Enum
from typing import Any, List

from langchain.chat_models import init_chat_model
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from config import settings


class TranslationProvider(str, Enum):
    OPENAI = "openai"
    GOOGLE = "google"
    GROQ = "groq"


BATCH_DELIMITER = "|||---|||"


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
        system_message = f"""
        You are an expert subtitle translation engine.
        Translate each numbered text line from '{{source_lang}}' to '{{target_lang}}'.
        - Maintain the original meaning and tone.
        - Return the translations in the same numbered format.
        - **Crucially, separate each translated line with the delimiter: {BATCH_DELIMITER}**
        - Do not add any extra text, introductions, or explanations.
        
        Example Input:
        1. Hello, world.
        2. How are you?
        
        Example Output:
        1. Olá, mundo.
        {BATCH_DELIMITER}
        2. Como você está?
        """
        human_message = "{text_batch}"

        return ChatPromptTemplate.from_messages(
            [("system", system_message), ("user", human_message)]
        )

    def translate_batch(
        self, texts: List[str], source_lang: str, target_lang: str
    ) -> List[str]:
        if not texts:
            return []

        formatted_batch = "\n".join(f"{i+1}. {text}" for i, text in enumerate(texts))
        response: str = self.chain.invoke(
            {
                "text_batch": formatted_batch,
                "source_lang": source_lang,
                "target_lang": target_lang,
            }
        )

        translated_texts = response.split(BATCH_DELIMITER)

        cleaned_translations = [
            re.sub(r"^\d+\.\s*", "", t.strip()).strip() for t in translated_texts
        ]

        if len(cleaned_translations) != len(texts):
            print(
                f"[bold yellow]Warning:[/bold yellow] Batch translation mismatch. Expected {len(texts)}, got {len(cleaned_translations)}. This batch will not be translated."
            )
            return texts

        return cleaned_translations
