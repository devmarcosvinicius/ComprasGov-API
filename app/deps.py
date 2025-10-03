from fastapi import Query

def pagination_params(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
):
    return {"page": page, "size": size}