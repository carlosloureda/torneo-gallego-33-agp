#!/usr/bin/env python3
"""
Script para agregar el campo last_updated al archivo JSON existente
"""

import json
from datetime import datetime, timezone, timedelta

# Archivo a modificar
TOURNAMENT_FILE = "tournament-viewer/data/tournament_extended.json"

def add_timestamp():
    """Agrega el campo last_updated al archivo JSON"""
    try:
        # Cargar datos existentes
        with open(TOURNAMENT_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Agregar timestamp si no existe
        if 'last_updated' not in data:
            data['last_updated'] = datetime.now(timezone(timedelta(hours=1))).isoformat()
            print(f"✅ Timestamp agregado: {data['last_updated']}")
        else:
            print(f"ℹ️  Timestamp ya existe: {data['last_updated']}")
        
        # Guardar archivo actualizado
        with open(TOURNAMENT_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"✅ Archivo actualizado: {TOURNAMENT_FILE}")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("🕐 Agregando timestamp al archivo JSON...")
    add_timestamp()
    print("✅ Completado!") 