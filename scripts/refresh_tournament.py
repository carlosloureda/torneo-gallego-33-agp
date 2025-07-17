#!/usr/bin/env python3
"""
Script para actualizar datos del torneo desde Cuescore
Mantiene los datos de AGP y actualiza solo partidas y resultados
"""

import json
import requests
import os
from datetime import datetime
from typing import Dict, Any, List

# Importar configuración
import sys
import os
sys.path.append(os.path.dirname(__file__))
from config import *

def load_existing_data() -> Dict[str, Any]:
    """Carga los datos existentes del torneo"""
    try:
        with open(TOURNAMENT_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo {TOURNAMENT_FILE}")
        return {}

def backup_current_data():
    """Crea una copia de seguridad de los datos actuales"""
    if os.path.exists(TOURNAMENT_FILE):
        import shutil
        shutil.copy2(TOURNAMENT_FILE, BACKUP_FILE)
        print(f"Backup creado: {BACKUP_FILE}")

def fetch_cuescore_data() -> Dict[str, Any]:
    """Descarga datos actualizados de Cuescore"""
    try:
        # URL del torneo específico
        url = f"{CUESCORE_API_URL}/?id={TOURNAMENT_ID}"
        
        headers = REQUEST_HEADERS
        
        print(f"Descargando datos de: {url}")
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        print(f"Datos descargados exitosamente")
        return data
        
    except requests.exceptions.RequestException as e:
        print(f"Error al descargar datos de Cuescore: {e}")
        return {}

def merge_tournament_data(cuescore_data: Dict[str, Any], existing_data: Dict[str, Any]) -> Dict[str, Any]:
    """Fusiona datos de Cuescore con datos AGP existentes"""
    
    if not cuescore_data:
        print("No hay datos de Cuescore para fusionar")
        return existing_data
    
    if not existing_data:
        print("No hay datos existentes para fusionar")
        return cuescore_data
    
    # Crear nueva estructura fusionada
    merged_data = {
        "tournament": cuescore_data.get("tournament", {}),
        "players": existing_data.get("players", {}),  # Mantener datos AGP
        "matches": cuescore_data.get("matches", []),  # Actualizar partidas
        "last_updated": datetime.now().isoformat(),
        "source": "cuescore_agp_merged"
    }
    
    # Actualizar información de jugadores con datos de Cuescore si están disponibles
    if "players" in cuescore_data:
        for player_id, cuescore_player in cuescore_data["players"].items():
            if player_id in merged_data["players"]:
                # Mantener datos AGP pero actualizar información básica
                agp_player = merged_data["players"][player_id]
                merged_data["players"][player_id] = {
                    **agp_player,  # Datos AGP (rankings, etc.)
                    "name": cuescore_player.get("name", agp_player.get("name")),
                    "country": cuescore_player.get("country", agp_player.get("country")),
                    "cuescore_id": cuescore_player.get("id", agp_player.get("cuescore_id"))
                }
            else:
                # Nuevo jugador de Cuescore
                merged_data["players"][player_id] = {
                    **cuescore_player,
                    "ranking": "unknown",
                    "liga": "unknown",
                    "rank_level": "beginner"
                }
    
    print(f"Datos fusionados exitosamente")
    return merged_data

def save_merged_data(data: Dict[str, Any]):
    """Guarda los datos fusionados"""
    try:
        # Crear directorio si no existe
        os.makedirs(os.path.dirname(TOURNAMENT_FILE), exist_ok=True)
        
        with open(TOURNAMENT_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"Datos guardados en: {TOURNAMENT_FILE}")
        
    except Exception as e:
        print(f"Error al guardar datos: {e}")

def main():
    """Función principal"""
    print(f"Iniciando actualización del torneo: {datetime.now()}")
    
    # Crear backup
    backup_current_data()
    
    # Cargar datos existentes
    existing_data = load_existing_data()
    if not existing_data:
        print("No se pudieron cargar los datos existentes")
        return
    
    # Descargar datos de Cuescore
    cuescore_data = fetch_cuescore_data()
    if not cuescore_data:
        print("No se pudieron descargar datos de Cuescore")
        return
    
    # Fusionar datos
    merged_data = merge_tournament_data(cuescore_data, existing_data)
    
    # Guardar datos fusionados
    save_merged_data(merged_data)
    
    print(f"Actualización completada: {datetime.now()}")

if __name__ == "__main__":
    main() 