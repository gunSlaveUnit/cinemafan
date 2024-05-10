from fastapi import APIRouter, Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from movies.endpoints import movies
from root.db import session
from root.settings import templates

router = APIRouter(prefix="/movies", tags=["Movies", "Templates"])


@router.get("")
async def items(
        request: Request,
        db: AsyncSession = Depends(session)
):
    response = await movies.items(db)

    return templates.TemplateResponse(
        request=request,
        name="movies/movies.html",
        context={
            "movies": response["data"],
        }
    )


@router.get("/{item_id}")
async def item(
        request: Request,
        item_id: int,
        db: AsyncSession = Depends(session)
):
    response = await movies.item(item_id, db)

    return templates.TemplateResponse(
        request=request,
        name="movies/movie.html",
        context={
            "movie": response,
        }
    )
