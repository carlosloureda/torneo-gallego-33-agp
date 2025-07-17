#!/usr/bin/env python3
"""
Script para probar la API de Cuescore
"""

import requests
import json
from datetime import datetime

# Configuración
TOURNAMENT_ID = "63505243"  # ID que configuraste
CUESCORE_API_URL = "https://api.cuescore.com/tournament"

def test_api_connection():
    """Prueba la conexión básica a la API"""
    try:
        url = f"{CUESCORE_API_URL}/{TOURNAMENT_ID}"
        print(f"🔗 Probando conexión a: {url}")
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (compatible; TournamentUpdater/1.0)',
            'Accept': 'application/json'
        }
        
        response = requests.get(url, headers=headers, timeout=30)
        
        print(f"📊 Status Code: {response.status_code}")
        print(f"📋 Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            print("✅ Conexión exitosa!")
            return response.json()
        else:
            print(f"❌ Error HTTP: {response.status_code}")
            print(f"📄 Respuesta: {response.text[:500]}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Error de conexión: {e}")
        return None

def analyze_tournament_data(data):
    """Analiza los datos del torneo recibidos"""
    if not data:
        print("❌ No hay datos para analizar")
        return
    
    print("\n📊 ANÁLISIS DE DATOS DEL TORNEO:")
    print("=" * 50)
    
    # Información básica del torneo
    if 'tournament' in data:
        tournament = data['tournament']
        print(f"🏆 Nombre: {tournament.get('name', 'N/A')}")
        print(f"📅 Fecha: {tournament.get('date', 'N/A')}")
        print(f"📍 Ubicación: {tournament.get('location', 'N/A')}")
        print(f"👥 Jugadores: {tournament.get('playerCount', 'N/A')}")
    
    # Jugadores
    if 'players' in data:
        players = data['players']
        print(f"\n👤 JUGADORES ({len(players)}):")
        for i, (player_id, player) in enumerate(list(players.items())[:5]):
            print(f"   {i+1}. {player.get('name', 'N/A')} (ID: {player_id})")
        if len(players) > 5:
            print(f"   ... y {len(players) - 5} más")
    
    # Partidas
    if 'matches' in data:
        matches = data['matches']
        print(f"\n🎯 PARTIDAS ({len(matches)}):")
        for i, match in enumerate(matches[:5]):
            print(f"   {i+1}. {match.get('player1', 'N/A')} vs {match.get('player2', 'N/A')}")
            print(f"      Estado: {match.get('status', 'N/A')}")
            print(f"      Resultado: {match.get('score1', 'N/A')} - {match.get('score2', 'N/A')}")
        if len(matches) > 5:
            print(f"   ... y {len(matches) - 5} más")
    
    # Estructura de datos
    print(f"\n📋 ESTRUCTURA DE DATOS:")
    for key in data.keys():
        if isinstance(data[key], list):
            print(f"   📁 {key}: Lista con {len(data[key])} elementos")
        elif isinstance(data[key], dict):
            print(f"   📁 {key}: Objeto con {len(data[key])} propiedades")
        else:
            print(f"   📄 {key}: {type(data[key]).__name__}")

def test_alternative_urls():
    """Prueba URLs alternativas de la API"""
    print("\n🔄 PROBANDO URLs ALTERNATIVAS:")
    print("=" * 40)
    
    # Diferentes formatos de URL
    urls_to_test = [
        f"https://api.cuescore.com/tournament/{TOURNAMENT_ID}",
        f"https://api.cuescore.com/tournaments/{TOURNAMENT_ID}",
        f"https://cuescore.com/api/tournament/{TOURNAMENT_ID}",
        f"https://cuescore.com/api/tournaments/{TOURNAMENT_ID}"
    ]
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (compatible; TournamentUpdater/1.0)',
        'Accept': 'application/json'
    }
    
    for url in urls_to_test:
        try:
            print(f"\n🔗 Probando: {url}")
            response = requests.get(url, headers=headers, timeout=10)
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                print("   ✅ ¡Funciona!")
                return response.json()
            else:
                print(f"   ❌ Error: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    return None

def main():
    """Función principal"""
    print(f"🧪 PRUEBA DE API CUESCORE - {datetime.now()}")
    print("=" * 60)
    
    # Prueba 1: Conexión básica
    print("\n1️⃣ PRUEBA DE CONEXIÓN BÁSICA")
    data = test_api_connection()
    
    if not data:
        print("\n⚠️  La URL principal no funcionó, probando alternativas...")
        data = test_alternative_urls()
    
    if data:
        # Prueba 2: Análisis de datos
        print("\n2️⃣ ANÁLISIS DE DATOS")
        analyze_tournament_data(data)
        
        # Prueba 3: Guardar muestra
        print("\n3️⃣ GUARDANDO MUESTRA DE DATOS")
        try:
            with open('scripts/api_test_sample.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print("✅ Muestra guardada en: scripts/api_test_sample.json")
        except Exception as e:
            print(f"❌ Error al guardar: {e}")
        
        print("\n🎉 ¡API funcionando correctamente!")
        print("💡 Puedes proceder con el sistema de actualización")
        
    else:
        print("\n❌ No se pudo conectar a la API de Cuescore")
        print("💡 Posibles soluciones:")
        print("   - Verificar el ID del torneo")
        print("   - Comprobar si la API requiere autenticación")
        print("   - Revisar si hay rate limiting")
        print("   - Verificar la estructura de la URL")

if __name__ == "__main__":
    main() 