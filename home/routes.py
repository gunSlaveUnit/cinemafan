from fastapi import APIRouter, Depends, Request
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_db
from movies.models import Movie
import psycopg
from settings import templates
from shared.utils import fill_base_context

router = APIRouter()


@router.get("/")
async def home(
        request: Request,
        base_context: dict = Depends(fill_base_context),
        db: AsyncSession = Depends(get_db),
):
    async with await psycopg.AsyncConnection.connect("postgresql://postgres:postgres@localhost:5432/cinemafan") as conn:
        async with conn.cursor() as cur:
            await cur.execute("SELECT id, original_title, translated_title FROM movies ORDER BY created_at DESC LIMIT 5")

            new = await cur.fetchall()

            extended_context = {"new": new}
            context = base_context
            context.update(extended_context)

            return templates.TemplateResponse(
                request=request,
                name="home/home.html",
                context=context,
            )
