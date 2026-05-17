from fastapi import Depends, Query

def get_pagination(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=100, description="Number of items per page")
):
    return {"page": page, "page_size": page_size}