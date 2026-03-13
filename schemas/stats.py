from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List

class GameStatCreate(BaseModel):
    """Esquema para crear una estadística de partida."""
    score: int = Field(..., gt=0)
    difficulty: int = Field(..., ge=0, le=3)
    time_taken: float = Field(..., gt=0)
    test_type: str = Field(..., min_length=1, max_length=50)

class GameStatResponse(BaseModel):
    """Esquema de respuesta de estadística."""
    id: int
    user_id: int
    score: int
    difficulty: int
    time_taken: float
    test_type: str
    weighted_score: float
    created_at: datetime
    
    class Config:
        from_attributes = True

class LeaderboardEntry(BaseModel):
    """Entrada en el leaderboard."""
    rank: int
    user_id: int
    username: str
    score: int
    weighted_score: float
    difficulty: Optional[int] = None
    test_type: Optional[str] = None
    last_score_date: datetime

class LeaderboardResponse(BaseModel):
    """Respuesta de leaderboard."""
    entries: List[LeaderboardEntry]
    total_entries: int
    page: int
    page_size: int

class UserStatsResponse(BaseModel):
    """Estadísticas del usuario."""
    user_id: int
    username: str
    total_games: int
    average_score: float
    best_score: int
    best_weighted_score: float
    total_time_played: float
    games_by_difficulty: dict
    games_by_test_type: dict
    recent_games: List[GameStatResponse]
