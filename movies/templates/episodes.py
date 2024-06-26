from fastapi import APIRouter, Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from movies.api import episodes
from movies.models import Record, Quality
from infrastructure.db import get_db
from infrastructure.settings import templates

router = APIRouter(prefix="/episodes", tags=["Episodes"])


@router.get("/{item_id}")
async def item(
        request: Request,
        item_id: int,
        db: AsyncSession = Depends(get_db)
):
    response = await episodes.item(item_id, db)
    records = [_ async for _ in Record.by_episode_id(item_id, db)]
    qualities = [await Quality.by_id(record.quality_id, db) for record in records]

    return templates.TemplateResponse(
        request=request,
        name="movies/episode.html",
        context={
            "episode": response,
            "records": records,
            "qualities": qualities
        }
    )
