#!/usr/bin/env python3
"""
Script de prueba para verificar el sistema de actualización
"""

import json
import os
from datetime import datetime

# Configuración de prueba
TOURNAMENT_FILE = "tournament-viewer/data/tournament_extended.json"

def test_load_data():
    """Prueba cargar datos existentes"""
    try:
        with open(TOURNAMENT_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"✅ Datos cargados exitosamente")
        print(f"   - Jugadores: {len(data.get('players', {}))}")
        print(f"   - Partidas: {len(data.get('matches', []))}")
        print(f"   - Última actualización: {data.get('last_updated', 'N/A')}")
        return True
    except Exception as e:
        print(f"❌ Error al cargar datos: {e}")
        return False

def test_backup():
    """Prueba crear backup"""
    try:
        if os.path.exists(TOURNAMENT_FILE):
            import shutil
            backup_file = TOURNAMENT_FILE.replace('.json', '_backup_test.json')
            shutil.copy2(TOURNAMENT_FILE, backup_file)
            print(f"✅ Backup creado: {backup_file}")
            
            # Limpiar backup de prueba
            os.remove(backup_file)
            print(f"✅ Backup de prueba eliminado")
            return True
        else:
            print(f"❌ Archivo de torneo no encontrado: {TOURNAMENT_FILE}")
            return False
    except Exception as e:
        print(f"❌ Error en backup: {e}")
        return False

def main():
    """Función principal de prueba"""
    print(f"🧪 Iniciando pruebas del sistema de actualización: {datetime.now()}")
    print("=" * 60)
    
    # Prueba 1: Cargar datos
    print("\n1. Probando carga de datos...")
    test1 = test_load_data()
    
    # Prueba 2: Backup
    print("\n2. Probando sistema de backup...")
    test2 = test_backup()
    
    # Resumen
    print("\n" + "=" * 60)
    print("📊 RESUMEN DE PRUEBAS:")
    print(f"   Carga de datos: {'✅ PASÓ' if test1 else '❌ FALLÓ'}")
    print(f"   Sistema backup: {'✅ PASÓ' if test2 else '❌ FALLÓ'}")
    
    if test1 and test2:
        print("\n🎉 ¡Todas las pruebas pasaron! El sistema está listo.")
    else:
        print("\n⚠️  Algunas pruebas fallaron. Revisar configuración.")

if __name__ == "__main__":
    main() 