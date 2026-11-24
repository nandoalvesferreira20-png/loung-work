"""Propostas de contrato. Os schemas passam a integrar o OpenAPI quando as rotas forem ativadas."""

from datetime import datetime
from typing import Annotated, Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, HttpUrl, StringConstraints

ShortText = Annotated[
    str, StringConstraints(strip_whitespace=True, min_length=1, max_length=120)
]
Modality = Literal["remote", "hybrid", "onsite"]
Seniority = Literal["intern", "junior", "mid", "senior", "lead"]


class ProfilePatch(BaseModel):
    model_config = ConfigDict(extra="forbid")

    display_name: ShortText | None = None
    headline: ShortText | None = None
    location: ShortText | None = None


class Profile(ProfilePatch):
    id: UUID
    updated_at: datetime


class JobFilters(BaseModel):
    q: ShortText | None = None
    location: ShortText | None = None
    modality: Modality | None = None
    seniority: Seniority | None = None
    limit: int = Field(default=20, ge=1, le=100)
    cursor: str | None = Field(default=None, max_length=512)


class JobSummary(BaseModel):
    id: UUID
    title: ShortText
    company: ShortText
    location: ShortText | None
    modality: Modality | None
    seniority: Seniority | None
    source: ShortText
    published_at: datetime | None


class JobDetail(JobSummary):
    description: str
    apply_url: HttpUrl


class JobPage(BaseModel):
    items: list[JobSummary]
    next_cursor: str | None
