from fastapi import APIRouter

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/sign-up")
async def sign_up() -> None:
    pass


@router.post("/sign-in")
async def sign_in() -> None:
    pass


@router.post("/sign-out")
async def sign_out() -> None:
    pass
