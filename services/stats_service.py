from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from models.database import GameStat, User
from schemas.stats import GameStatCreate, LeaderboardEntry
from fastapi import HTTPException, status

# Multiplicadores de dificultad
DIFFICULTY_MULTIPLIERS = {
    0: 1.0,
    1: 1.3,
    2: 1.7,
    3: 2.2
}

class StatsService:
    """Servicio de estadísticas y leaderboards."""
    
    @staticmethod
    def calculate_weighted_score(score: int, difficulty: int) -> float:
        """Calcular puntaje ponderado."""
        multiplier = DIFFICULTY_MULTIPLIERS.get(difficulty, 1.0)
        return float(score) * multiplier
    
    @staticmethod
    def register_game_stat(db: Session, user_id: int, stat_data: GameStatCreate) -> dict:
        """Registrar estadística de partida."""
        # Verificar que el usuario existe
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado"
            )
        
        # Calcular puntaje ponderado
        weighted_score = StatsService.calculate_weighted_score(
            stat_data.score,
            stat_data.difficulty
        )
        
        # Crear estadística
        game_stat = GameStat(
            user_id=user_id,
            score=stat_data.score,
            difficulty=stat_data.difficulty,
            time_taken=stat_data.time_taken,
            test_type=stat_data.test_type,
            weighted_score=weighted_score
        )
        
        db.add(game_stat)
        db.commit()
        db.refresh(game_stat)
        
        return {
            "id": game_stat.id,
            "score": game_stat.score,
            "weighted_score": game_stat.weighted_score,
            "difficulty": game_stat.difficulty,
            "time_taken": game_stat.time_taken,
            "test_type": game_stat.test_type,
            "created_at": game_stat.created_at
        }
    
    @staticmethod
    def get_global_leaderboard(db: Session, page: int = 1, page_size: int = 10) -> dict:
        """Obtener leaderboard global."""
        skip = (page - 1) * page_size
        
        # Obtener puntajes máximos por usuario
        subquery = db.query(
            GameStat.user_id,
            func.max(GameStat.weighted_score).label("max_weighted_score")
        ).group_by(GameStat.user_id).subquery()
        
        # Obtener leaderboard
        query = db.query(
            User.id,
            User.username,
            subquery.c.max_weighted_score,
            GameStat.score,
            GameStat.created_at
        ).join(
            subquery, User.id == subquery.c.user_id
        ).join(
            GameStat, (GameStat.user_id == User.id) & 
                      (GameStat.weighted_score == subquery.c.max_weighted_score)
        ).order_by(
            desc(subquery.c.max_weighted_score)
        )
        
        total = query.count()
        entries = query.offset(skip).limit(page_size).all()
        
        leaderboard_entries = [
            LeaderboardEntry(
                rank=skip + i + 1,
                user_id=entry[0],
                username=entry[1],
                score=entry[3],
                weighted_score=float(entry[2]),
                last_score_date=entry[4]
            )
            for i, entry in enumerate(entries)
        ]
        
        return {
            "entries": leaderboard_entries,
            "total_entries": total,
            "page": page,
            "page_size": page_size
        }
    
    @staticmethod
    def get_leaderboard_by_difficulty(db: Session, difficulty: int, page: int = 1, page_size: int = 10) -> dict:
        """Obtener leaderboard filtrado por dificultad."""
        skip = (page - 1) * page_size
        
        # Obtener mejores puntajes por usuario para la dificultad especificada
        subquery = db.query(
            GameStat.user_id,
            func.max(GameStat.weighted_score).label("max_weighted_score")
        ).filter(
            GameStat.difficulty == difficulty
        ).group_by(GameStat.user_id).subquery()
        
        query = db.query(
            User.id,
            User.username,
            subquery.c.max_weighted_score,
            GameStat.score,
            GameStat.created_at
        ).join(
            subquery, User.id == subquery.c.user_id
        ).join(
            GameStat, (GameStat.user_id == User.id) & 
                      (GameStat.weighted_score == subquery.c.max_weighted_score) &
                      (GameStat.difficulty == difficulty)
        ).order_by(
            desc(subquery.c.max_weighted_score)
        )
        
        total = query.count()
        entries = query.offset(skip).limit(page_size).all()
        
        leaderboard_entries = [
            LeaderboardEntry(
                rank=skip + i + 1,
                user_id=entry[0],
                username=entry[1],
                score=entry[3],
                weighted_score=float(entry[2]),
                difficulty=difficulty,
                last_score_date=entry[4]
            )
            for i, entry in enumerate(entries)
        ]
        
        return {
            "entries": leaderboard_entries,
            "total_entries": total,
            "page": page,
            "page_size": page_size
        }
    
    @staticmethod
    def get_leaderboard_by_test_type(db: Session, test_type: str, page: int = 1, page_size: int = 10) -> dict:
        """Obtener leaderboard filtrado por tipo de prueba."""
        skip = (page - 1) * page_size
        
        subquery = db.query(
            GameStat.user_id,
            func.max(GameStat.weighted_score).label("max_weighted_score")
        ).filter(
            GameStat.test_type == test_type
        ).group_by(GameStat.user_id).subquery()
        
        query = db.query(
            User.id,
            User.username,
            subquery.c.max_weighted_score,
            GameStat.score,
            GameStat.created_at
        ).join(
            subquery, User.id == subquery.c.user_id
        ).join(
            GameStat, (GameStat.user_id == User.id) & 
                      (GameStat.weighted_score == subquery.c.max_weighted_score) &
                      (GameStat.test_type == test_type)
        ).order_by(
            desc(subquery.c.max_weighted_score)
        )
        
        total = query.count()
        entries = query.offset(skip).limit(page_size).all()
        
        leaderboard_entries = [
            LeaderboardEntry(
                rank=skip + i + 1,
                user_id=entry[0],
                username=entry[1],
                score=entry[3],
                weighted_score=float(entry[2]),
                test_type=test_type,
                last_score_date=entry[4]
            )
            for i, entry in enumerate(entries)
        ]
        
        return {
            "entries": leaderboard_entries,
            "total_entries": total,
            "page": page,
            "page_size": page_size
        }
    
    @staticmethod
    def get_user_stats(db: Session, user_id: int) -> dict:
        """Obtener estadísticas del usuario."""
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado"
            )
        
        stats = db.query(GameStat).filter(GameStat.user_id == user_id).all()
        
        if not stats:
            return {
                "user_id": user_id,
                "username": user.username,
                "total_games": 0,
                "average_score": 0,
                "best_score": 0,
                "best_weighted_score": 0,
                "total_time_played": 0,
                "games_by_difficulty": {},
                "games_by_test_type": {},
                "recent_games": []
            }
        
        # Calcular estadísticas
        total_games = len(stats)
        average_score = sum(s.score for s in stats) / total_games
        best_score = max(s.score for s in stats)
        best_weighted_score = max(s.weighted_score for s in stats)
        total_time_played = sum(s.time_taken for s in stats)
        
        # Agrupar por dificultad
        games_by_difficulty = {}
        for stat in stats:
            if stat.difficulty not in games_by_difficulty:
                games_by_difficulty[stat.difficulty] = 0
            games_by_difficulty[stat.difficulty] += 1
        
        # Agrupar por tipo de prueba
        games_by_test_type = {}
        for stat in stats:
            if stat.test_type not in games_by_test_type:
                games_by_test_type[stat.test_type] = 0
            games_by_test_type[stat.test_type] += 1
        
        # Últimas 5 partidas
        recent_games = sorted(stats, key=lambda x: x.created_at, reverse=True)[:5]
        
        return {
            "user_id": user_id,
            "username": user.username,
            "total_games": total_games,
            "average_score": round(average_score, 2),
            "best_score": best_score,
            "best_weighted_score": round(best_weighted_score, 2),
            "total_time_played": round(total_time_played, 2),
            "games_by_difficulty": games_by_difficulty,
            "games_by_test_type": games_by_test_type,
            "recent_games": [
                {
                    "id": g.id,
                    "score": g.score,
                    "weighted_score": g.weighted_score,
                    "difficulty": g.difficulty,
                    "time_taken": g.time_taken,
                    "test_type": g.test_type,
                    "created_at": g.created_at
                }
                for g in recent_games
            ]
        }
