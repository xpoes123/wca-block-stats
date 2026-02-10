from __future__ import annotations
from dataclasses import dataclass, field
from typing import Literal

@dataclass(kw_only=True, frozen=True)
class FieldRef:
    """Ref to a field via a dotted path. (Result.average, Result.competition.start_date)"""
    path: str

Dir = Literal["asc", "desc"]

@dataclass(kw_only=True, frozen=True)
class OrderItem:
    field: FieldRef
    direction: Dir = "asc"

FilterOp = Literal[
    "=", "!=", ">", ">=", "<", "<=", "in"
]


@dataclass(kw_only=True, frozen=True)
class FilterExpr:
    """Simple binary comparison filter"""
    op: FilterOp
    left: FieldRef
    right: object

@dataclass(kw_only=True, frozen=True)
class TopPerGroupSpec:
    """Describes a top row per group query using window functions"""
    partition_by: list[FieldRef]
    order_by: list[OrderItem]
    keep_ties:  bool = False

@dataclass(kw_only=True)
class QuerySpec:
    """Representation of a query"""
    version: int = 1
    
    base: Literal[
        "Result",
        "Person",
        "Competition",
        "Event",
        "Country",
        "RoundType",
    ] = "Result"
    
    select: list[FieldRef] = field(default_factory=list)
    
    filters: list[FilterExpr] = field(default_factory=list)
    
    group_by: list[FieldRef] = field(default_factory=list)
    
    top_per_group: TopPerGroupSpec | None = None
    
    order_by: list[OrderItem] = field(default_factory=list)
    limit: int = 200
    offset: int = 0
    