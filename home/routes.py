from collections import namedtuple

from fastapi import APIRouter, Depends, Request
import psycopg

from db import get_cursor
from settings import templates
from shared.utils import fill_base_context

router = APIRouter()


@router.get("/")
async def home(
        request: Request,
        base_context: dict = Depends(fill_base_context),
        cursor = Depends(get_cursor),
):
    await cursor.execute("""
        SELECT
            id,
            poster,
            translated_title
        FROM
            movies
        ORDER BY
            created_at
        DESC
        LIMIT
            7
        """
    )

    new = await cursor.fetchall()

    extended_context = {"new": new}
    context = base_context
    context.update(extended_context)

    return templates.TemplateResponse(
        request=request,
        name="home/home.html",
        context=context,
    )
