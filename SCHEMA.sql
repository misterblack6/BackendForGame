-- ============================================================================
-- ESQUEMA DE BASE DE DATOS - PRUEBA HUMANA BACKEND
-- ============================================================================
-- Base de datos: prueba_humana
-- Motor: MySQL 5.7+
-- Charset: utf8mb4
-- ============================================================================

-- Crear base de datos
CREATE DATABASE IF NOT EXISTS prueba_humana 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

USE prueba_humana;

-- ============================================================================
-- TABLA: users
-- Descripción: Almacena información de usuarios registrados
-- ============================================================================
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT 'ID único del usuario',
    username VARCHAR(50) NOT NULL UNIQUE COMMENT 'Nombre de usuario único',
    email VARCHAR(100) UNIQUE COMMENT 'Email del usuario (opcional)',
    password_hash VARCHAR(255) NOT NULL COMMENT 'Contraseña encriptada con bcrypt',
    is_active BOOLEAN DEFAULT TRUE COMMENT 'Estado del usuario (activo/inactivo)',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT 'Fecha de creación',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'Fecha de última actualización',
    last_login TIMESTAMP NULL COMMENT 'Fecha del último inicio de sesión',
    
    INDEX idx_username (username),
    INDEX idx_email (email),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci 
COMMENT='Tabla de usuarios del sistema';

-- ============================================================================
-- TABLA: game_stats
-- Descripción: Almacena estadísticas de cada partida jugada
-- ============================================================================
CREATE TABLE IF NOT EXISTS game_stats (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT 'ID único de la estadística',
    user_id INT NOT NULL COMMENT 'ID del usuario que jugó',
    score INT NOT NULL COMMENT 'Puntaje bruto obtenido',
    difficulty INT NOT NULL COMMENT 'Nivel de dificultad (0-3)',
    time_taken FLOAT NOT NULL COMMENT 'Tiempo empleado en segundos',
    test_type VARCHAR(50) NOT NULL COMMENT 'Tipo de prueba realizada',
    weighted_score FLOAT NOT NULL COMMENT 'Puntaje ponderado (score * multiplicador)',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT 'Fecha de la partida',
    
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_difficulty (difficulty),
    INDEX idx_test_type (test_type),
    INDEX idx_weighted_score (weighted_score),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci 
COMMENT='Tabla de estadísticas de partidas';

-- ============================================================================
-- TABLA: active_sessions
-- Descripción: Almacena sesiones activas para gestión de presencia
-- ============================================================================
CREATE TABLE IF NOT EXISTS active_sessions (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT 'ID único de la sesión',
    user_id INT NOT NULL COMMENT 'ID del usuario',
    token VARCHAR(500) NOT NULL UNIQUE COMMENT 'Token JWT de la sesión',
    is_online BOOLEAN DEFAULT TRUE COMMENT 'Estado de conexión (online/offline)',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT 'Fecha de creación de sesión',
    last_heartbeat TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'Último heartbeat recibido',
    
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_token (token),
    INDEX idx_is_online (is_online)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci 
COMMENT='Tabla de sesiones activas para presencia';

-- ============================================================================
-- VISTAS ÚTILES
-- ============================================================================

-- Vista: leaderboard_global
-- Muestra el ranking global de jugadores
CREATE OR REPLACE VIEW leaderboard_global AS
SELECT 
    ROW_NUMBER() OVER (ORDER BY MAX(gs.weighted_score) DESC) as rank,
    u.id as user_id,
    u.username,
    MAX(gs.weighted_score) as best_weighted_score,
    MAX(gs.score) as best_score,
    COUNT(gs.id) as total_games,
    MAX(gs.created_at) as last_game_date
FROM users u
LEFT JOIN game_stats gs ON u.id = gs.user_id
GROUP BY u.id, u.username
ORDER BY best_weighted_score DESC;

-- Vista: leaderboard_by_difficulty
-- Muestra el ranking por nivel de dificultad
CREATE OR REPLACE VIEW leaderboard_by_difficulty AS
SELECT 
    gs.difficulty,
    ROW_NUMBER() OVER (PARTITION BY gs.difficulty ORDER BY MAX(gs.weighted_score) DESC) as rank,
    u.id as user_id,
    u.username,
    MAX(gs.weighted_score) as best_weighted_score,
    MAX(gs.score) as best_score,
    COUNT(gs.id) as games_at_difficulty,
    MAX(gs.created_at) as last_game_date
FROM users u
LEFT JOIN game_stats gs ON u.id = gs.user_id
WHERE gs.difficulty IS NOT NULL
GROUP BY gs.difficulty, u.id, u.username
ORDER BY gs.difficulty, best_weighted_score DESC;

-- Vista: leaderboard_by_test_type
-- Muestra el ranking por tipo de prueba
CREATE OR REPLACE VIEW leaderboard_by_test_type AS
SELECT 
    gs.test_type,
    ROW_NUMBER() OVER (PARTITION BY gs.test_type ORDER BY MAX(gs.weighted_score) DESC) as rank,
    u.id as user_id,
    u.username,
    MAX(gs.weighted_score) as best_weighted_score,
    MAX(gs.score) as best_score,
    COUNT(gs.id) as games_of_type,
    MAX(gs.created_at) as last_game_date
FROM users u
LEFT JOIN game_stats gs ON u.id = gs.user_id
WHERE gs.test_type IS NOT NULL
GROUP BY gs.test_type, u.id, u.username
ORDER BY gs.test_type, best_weighted_score DESC;

-- Vista: user_statistics
-- Muestra estadísticas agregadas por usuario
CREATE OR REPLACE VIEW user_statistics AS
SELECT 
    u.id as user_id,
    u.username,
    COUNT(gs.id) as total_games,
    ROUND(AVG(gs.score), 2) as average_score,
    MAX(gs.score) as best_score,
    MAX(gs.weighted_score) as best_weighted_score,
    ROUND(SUM(gs.time_taken), 2) as total_time_played,
    MIN(gs.created_at) as first_game_date,
    MAX(gs.created_at) as last_game_date,
    u.last_login
FROM users u
LEFT JOIN game_stats gs ON u.id = gs.user_id
GROUP BY u.id, u.username, u.last_login;

-- ============================================================================
-- ÍNDICES ADICIONALES PARA OPTIMIZACIÓN
-- ============================================================================

-- Índice compuesto para búsquedas frecuentes
ALTER TABLE game_stats ADD INDEX idx_user_difficulty (user_id, difficulty);
ALTER TABLE game_stats ADD INDEX idx_user_test_type (user_id, test_type);
ALTER TABLE game_stats ADD INDEX idx_user_weighted (user_id, weighted_score);

-- ============================================================================
-- DATOS DE EJEMPLO (OPCIONAL)
-- ============================================================================

-- Insertar usuario de prueba
INSERT INTO users (username, email, password_hash, is_active) VALUES 
('test_player', 'test@example.com', '$2b$12$example_hash_here', TRUE);

-- Insertar algunas estadísticas de ejemplo
INSERT INTO game_stats (user_id, score, difficulty, time_taken, test_type, weighted_score) VALUES
(1, 8500, 2, 145.5, 'memory_test', 14450.0),
(1, 7200, 1, 120.0, 'reaction_test', 9360.0),
(1, 9200, 3, 200.0, 'logic_test', 20240.0);

-- ============================================================================
-- INFORMACIÓN DE MULTIPLICADORES DE DIFICULTAD
-- ============================================================================
-- Dificultad 0: Multiplicador 1.0x
-- Dificultad 1: Multiplicador 1.3x
-- Dificultad 2: Multiplicador 1.7x
-- Dificultad 3: Multiplicador 2.2x
-- ============================================================================
