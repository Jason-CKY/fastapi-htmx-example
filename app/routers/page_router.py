from fastapi import APIRouter
router = APIRouter()


@router.get("/")
async def home_page():
    return "<h1>Hello World</h1>"
