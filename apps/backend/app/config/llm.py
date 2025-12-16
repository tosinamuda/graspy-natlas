from __future__ import annotations

import dspy
import logging
import litellm
from typing import Optional

from ..settings import Settings

logger = logging.getLogger("dspy")

def configure_llm(settings: Settings) -> None:
    litellm.drop_params = True
    
    # Prefer N-Atlas as default if available
    if settings.n_atlas_api_base:
        logger.info("Configuring N-Atlas as default LM")
        lm = dspy.LM(
            model=settings.n_atlas_model_id if hasattr(settings, 'n_atlas_model_id') else "openai/n-atlas",
            api_base=settings.n_atlas_api_base,
            api_key="EMPTY",
            max_tokens=4096,
            temperature=0.7,
        )
    else:
        logger.info("Configuring Bedrock as default LM")
        model_id = settings.strands_model_id
        full_model_id = f"bedrock/{model_id}" if not model_id.startswith("bedrock/") else model_id

        lm = dspy.LM(
            model=full_model_id,
            max_tokens=settings.strands_max_tokens,
            temperature=settings.strands_default_temperature,
        )
    
    dspy.settings.configure(lm=lm)

def get_n_atlas_lm() -> Optional[dspy.LM]:
    from ..settings import get_settings
    settings = get_settings()
    
    if not settings.n_atlas_api_base:
        return None
        
    try:
        lm = dspy.LM(
            model=settings.n_atlas_model_id,
            api_base=settings.n_atlas_api_base,
            api_key="EMPTY",
            max_tokens=4096,
            temperature=0.7,
        )
        return lm
    except Exception as e:
        logger.error(f"Failed to instantiate N-Atlas LM: {e}")
        return None

def get_openrouter_judge_lm() -> Optional[dspy.LM]:
    import os
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        logger.warning("OPENROUTER_API_KEY not found in environment.")
        return None
        
    return dspy.LM(
        model="openrouter/openai/gpt-oss-20b:free",
        api_base="https://openrouter.ai/api/v1",
        api_key=api_key,
        max_tokens=4096,
        temperature=0.1,
    )

def get_lm_for_locale(language: str) -> Optional[dspy.LM]:
    target_languages = ["english", "yoruba", "hausa", "igbo", "pidgin", "broken english"]

    if language.lower() in target_languages:
        return get_n_atlas_lm()
    return None
