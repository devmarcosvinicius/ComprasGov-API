from typing import Literal, Optional
from sqlalchemy.orm import Query
from sqlalchemy import asc, desc

def apply_pagination(query, page: int = 1, size: int = 20):
    page = max(page, 1)
    size = min(max(size, 1), 100)
    total = query.count()
    items = query.offset((page - 1) * size).limit(size).all()
    return total, items

def apply_ordering(query, model, order_by: Optional[str], direction: Literal["asc","desc"]="asc"):
    if not order_by:
        return query
    col = getattr(model, order_by, None)
    if col is None:
        return query
    return query.order_by(asc(col) if direction == "asc" else desc(col))