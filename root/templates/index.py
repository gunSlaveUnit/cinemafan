import random

from fastapi import APIRouter, Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.db import get_db
from infrastructure.settings import templates
from movies.api import movies

router = APIRouter(tags=["Root"])


@router.get("/")
async def index(request: Request,
                db: AsyncSession = Depends(get_db),
                ):
    response = await movies.items(db)
    data = response["data"]
    movie = random.choice(data)
    return templates.TemplateResponse(
        request=request,
        name="root/index.html",
        context={"movie_id": movie.id},
    )
