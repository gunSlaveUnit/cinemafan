from fastapi import APIRouter, Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from movies import api
from root.db import session
from root.templates import templates

router = APIRouter(prefix="/movies", tags=["Movies", "Templates"])


@router.get("")
async def items(
        request: Request,
        db: AsyncSession = Depends(session)
):
    content = await api.items(db)

    return templates.TemplateResponse(
        request=request,
        name="movies/movies.html",
        context={
            "movies": content["data"],
        }
    )


@router.get("/{item_id}")
async def item(
        request: Request,
        item_id: int,
        db: AsyncSession = Depends(session)
):
    content = await api.item(item_id, db)

    return templates.TemplateResponse(
        request=request,
        name="movies/movie.html",
        context={
            "movie": content,
        }
    )
