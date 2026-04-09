from pydantic import BaseModel, Field
from typing import Optional, Literal


class KeyFigure(BaseModel):
    name: str
    role: str
    portrait_url: Optional[str] = None


class HistoricalEvent(BaseModel):
    id: str
    title: str
    year: int  # negative = BCE
    region: str
    description: str
    category: str  # collapse, revolution, cultural_peak, war, discovery, migration
    confidence: Literal["high", "medium", "speculative"] = "high"
    figures: list[KeyFigure] = Field(default_factory=list)
    resonances: list[str] = Field(default_factory=list)
    resonance_reasons: dict[str, str] = Field(default_factory=dict)
    resonance_reasons_zh: dict[str, str] = Field(default_factory=dict)
    lat: Optional[float] = None
    lng: Optional[float] = None
    title_local: Optional[str] = None
    description_local: Optional[str] = None
    wiki_title: Optional[str] = None
    image_url: Optional[str] = None
    title_zh: Optional[str] = None
    description_zh: Optional[str] = None
