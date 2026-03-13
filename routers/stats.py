from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.models.database import get_db
from app.schemas.stats import GameStatCreate, GameStatResponse
from app.services.stats_service import StatsService
from app.utils.dependencies import get_current_user

router = APIRouter(prefix="/stats", tags=["Estadísticas"])

@router.post("/register", response_model=dict)
async def register_game_stat(
    stat_data: GameStatCreate,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Registrar estadística de una partida."""
    result = StatsService.register_game_stat(db, current_user.id, stat_data)
    return {
        "success": True,
        "message": "Estadística registrada exitosamente",
        "data": result
    }

@router.get("/user", response_model=dict)
async def get_user_stats(
    user_id: int = Query(None),
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Obtener estadísticas del usuario."""
    target_user_id = user_id if user_id else current_user.id
    result = StatsService.get_user_stats(db, target_user_id)
    return {
        "success": True,
        "data": result
    }

@router.get("/leaderboard/global", response_model=dict)
async def get_global_leaderboard(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Obtener leaderboard global."""
    result = StatsService.get_global_leaderboard(db, page, page_size)
    return {
        "success": True,
        "data": result
    }

@router.get("/leaderboard/difficulty/{difficulty}", response_model=dict)
async def get_leaderboard_by_difficulty(
    difficulty: int,
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Obtener leaderboard filtrado por dificultad."""
    if difficulty not in [0, 1, 2, 3]:
        return {
            "success": False,
            "error": "Dificultad debe estar entre 0 y 3"
        }
    
    result = StatsService.get_leaderboard_by_difficulty(db, difficulty, page, page_size)
    return {
        "success": True,
        "data": result
    }

@router.get("/leaderboard/test/{test_type}", response_model=dict)
async def get_leaderboard_by_test_type(
    test_type: str,
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Obtener leaderboard filtrado por tipo de prueba."""
    result = StatsService.get_leaderboard_by_test_type(db, test_type, page, page_size)
    return {
        "success": True,
        "data": result
    }
