
from fastapi import APIRouter
from app.services.user_service import get_leaderboard

router = APIRouter()

@router.get("/leaderboard")
def leaderboard():
    return get_leaderboard()
