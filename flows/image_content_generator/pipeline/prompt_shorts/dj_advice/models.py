from flows.image_content_generator.pipeline.prompt_base.models import BaseIdea, CategoryHandler
from flows.image_content_generator.pipeline.prompt_shorts.dj_advice import (
    constants as dj_constants,
)


class MindsetDJIdea(BaseIdea):
    """
    Idea model for DJ mindset transformation stories.
    """
    IDEA_PROMPT = dj_constants.IDEA_PROMPT_MINDSET
    dj_problem: str
    mindset_shift: str
    key_principle: str


class StrategyDJIdea(BaseIdea):
    """
    Idea model for practical DJ strategy videos.
    """
    IDEA_PROMPT = dj_constants.IDEA_PROMPT_ESTRATEGIA
    strategy_name: str
    common_mistake: str
    actionable_tip: str


class PerformanceDJIdea(BaseIdea):
    """Idea model for DJ performance and energy."""
    IDEA_PROMPT = dj_constants.IDEA_PROMPT_PERFORMANCE
    performance_context: str
    energy_challenge: str
    crowd_insight: str


class TechnicalDJIdea(BaseIdea):
    """Idea model for technical DJing skills."""
    IDEA_PROMPT = dj_constants.IDEA_PROMPT_TECHNICAL
    technical_concept: str
    common_bad_habit: str
    pro_correction: str


class PsychologyDJIdea(BaseIdea):
    """Idea model for crowd psychology."""
    IDEA_PROMPT = dj_constants.IDEA_PROMPT_PSYCHOLOGY
    psychological_effect: str
    crowd_behavior: str
    emotional_trigger: str


class StorytellingDJIdea(BaseIdea):
    """Idea model for musical storytelling."""
    IDEA_PROMPT = dj_constants.IDEA_PROMPT_STORYTELLING
    narrative_arc: str
    musical_transition: str
    climax_moment: str


class BrandingDJIdea(BaseIdea):
    """Idea model for DJ branding and identity."""
    IDEA_PROMPT = dj_constants.IDEA_PROMPT_BRANDING
    brand_identity: str
    differentiation_factor: str
    market_reality: str


class GearDJIdea(BaseIdea):
    """Idea model for DJ gear and tools."""
    IDEA_PROMPT = dj_constants.IDEA_PROMPT_GEAR
    gear_setup: str
    hardware_benefit: str
    workflow_tip: str


class RealityCheckDJIdea(BaseIdea):
    """Idea model for DJ industry reality checks."""
    IDEA_PROMPT = dj_constants.IDEA_PROMPT_REALITY_CHECK
    industry_myth: str
    harsh_truth: str
    growth_mindset: str


class DJAdviceHandler(CategoryHandler):
    """
    Specialized handler for DJ Advice-themed short videos.
    Encapsulates all DJ idea variants.
    """

    SCRIPT_PROMPT = dj_constants.SCRIPT_PROMPT
    idea_variants = [
        MindsetDJIdea,
        StrategyDJIdea,
        PerformanceDJIdea,
        TechnicalDJIdea,
        PsychologyDJIdea,
        StorytellingDJIdea,
        BrandingDJIdea,
        GearDJIdea,
        RealityCheckDJIdea,
    ]
