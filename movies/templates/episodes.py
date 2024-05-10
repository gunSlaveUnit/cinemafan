from fastapi import APIRouter, Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from movies.api import episodes
from root.db import session
from root.settings import templates

router = APIRouter(prefix="/episodes", tags=["Episodes"])


@router.get("/{item_id}")
async def item(
        request: Request,
        item_id: int,
        db: AsyncSession = Depends(session)
):
    response = await episodes.item(item_id, db)

    return templates.TemplateResponse(
        request=request,
        name="movies/episode.html",
        context={
            "episode": response,
        }
    )
