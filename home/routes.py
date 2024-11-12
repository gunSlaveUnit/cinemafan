import uuid
import datetime

from fastapi import APIRouter, Cookie, Depends, Request
import jwt
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_db
from settings import templates
from shared.utils import fill_base_context

router = APIRouter()


@router.get("/")
async def home(
        request: Request,
        base_context: dict = Depends(fill_base_context),
):
    return templates.TemplateResponse(
        request=request,
        name="root/home.html",
        context=base_context,
    )
