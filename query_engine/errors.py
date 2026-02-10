from __future__ import annotations
from dataclasses import dataclass

@dataclass(kw_only=True)
class QueryErrorDetail:
    message: str
    block_id: str | None = None
    field: str | None = None
    hint: str | None = None

class QuerySpecError(Exception):
    def __init__(self, detail: QueryErrorDetail):
        super().__init__(detail.message)
        self.detail = detail
        
    def to_dict(self) -> dict:
        return {
            "message": self.detail.message,
            "block_id": self.detail.block_id,
            "field": self.detail.field,
            "hint": self.detail.hint,
        }

class ValidationError(QuerySpecError):
    """User made an invalid query"""
    raise NotImplementedError

class InvariantError(QuerySpecError):
    """Bug in our system, internal assumptions violated"""
    raise NotImplementedError