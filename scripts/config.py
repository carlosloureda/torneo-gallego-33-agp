"""
Configuración para el sistema de actualización del torneo
"""
INDIVIDUAL_TERCERA_TORNEO_ID = "63505243"
# ID del torneo en Cuescore
# Este es el ID que aparece en la URL del torneo
TOURNAMENT_ID = INDIVIDUAL_TERCERA_TORNEO_ID

# URL base de la API de Cuescore
CUESCORE_API_URL = "https://api.cuescore.com/tournament"

# Archivos de datos
TOURNAMENT_FILE = "tournament-viewer/data/tournament_extended.json"
BACKUP_FILE = "tournament-viewer/data/tournament_backup.json"

# Configuración de actualización
UPDATE_INTERVAL_MINUTES = 10  # Cada cuántos minutos se actualiza automáticamente
CHECK_INTERVAL_SECONDS = 30   # Cada cuántos segundos verifica el frontend

# Headers para las peticiones HTTP
REQUEST_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (compatible; TournamentUpdater/1.0)',
    'Accept': 'application/json',
    'Accept-Language': 'es-ES,es;q=0.9,en;q=0.8'
}

# Configuración de notificaciones
NOTIFICATION_DURATION_SUCCESS = 3000  # 3 segundos
NOTIFICATION_DURATION_ERROR = 5000    # 5 segundos

# Configuración de rate limiting
MIN_UPDATE_INTERVAL_SECONDS = 30  # Mínimo entre actualizaciones manuales
API_RATE_LIMIT_DELAY = 2  # Segundos de espera entre peticiones a la API
MAX_RETRIES = 3  # Máximo de reintentos si falla la API

# Configuración del torneo
# Las fechas del torneo se obtienen automáticamente de la API de Cuescore 