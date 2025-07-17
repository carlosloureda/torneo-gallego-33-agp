#!/usr/bin/env python3
"""
Prueba avanzada de la API de Cuescore
Usa diferentes estrategias para acceder a los datos
"""

import requests
import json
import time
from urllib.parse import urljoin

# ID del torneo
TOURNAMENT_ID = "63505243"

def test_with_session():
    """Prueba usando una sesión de navegador"""
    print("🔄 Probando con sesión de navegador...")
    
    session = requests.Session()
    
    # Configurar headers como un navegador real
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'es-ES,es;q=0.9,en;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    })
    
    try:
        # 1. Visitar la página principal primero
        print("   📡 Visitando página principal...")
        main_response = session.get('https://cuescore.com/', timeout=30)
        print(f"   Status principal: {main_response.status_code}")
        
        # 2. Visitar la página del torneo
        tournament_url = f"https://cuescore.com/tournament/{TOURNAMENT_ID}"
        print(f"   📡 Visitando torneo: {tournament_url}")
        tournament_response = session.get(tournament_url, timeout=30)
        print(f"   Status torneo: {tournament_response.status_code}")
        
        # 3. Intentar acceder a la API interna
        api_urls = [
            f"https://cuescore.com/api/tournament/?id={TOURNAMENT_ID}",
            f"https://cuescore.com/api/tournaments/?id={TOURNAMENT_ID}",
            f"https://api.cuescore.com/tournament/?id={TOURNAMENT_ID}",
            f"https://api.cuescore.com/tournaments/?id={TOURNAMENT_ID}"
        ]
        
        # Cambiar headers para API
        session.headers.update({
            'Accept': 'application/json',
            'X-Requested-With': 'XMLHttpRequest'
        })
        
        for api_url in api_urls:
            try:
                print(f"   🔗 Probando API: {api_url}")
                response = session.get(api_url, timeout=30)
                print(f"   Status: {response.status_code}")
                
                if response.status_code == 200:
                    print("   ✅ ¡Éxito!")
                    data = response.json()
                    return data
                else:
                    print(f"   ❌ Error: {response.status_code}")
                    if response.text:
                        print(f"   Respuesta: {response.text[:100]}...")
                        
            except Exception as e:
                print(f"   ❌ Error: {e}")
        
        return None
        
    except Exception as e:
        print(f"❌ Error en sesión: {e}")
        return None

def test_direct_api():
    """Prueba directa de la API con headers optimizados"""
    print("🎯 Probando API directa...")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
        'Accept': 'application/json',
        'Referer': f'https://cuescore.com/tournament/{TOURNAMENT_ID}',
        'Origin': 'https://cuescore.com',
        'Accept-Language': 'es-ES,es;q=0.9,en;q=0.8'
    }
    
    urls = [
        f"https://cuescore.com/api/tournament/{TOURNAMENT_ID}",
        f"https://cuescore.com/api/tournaments/{TOURNAMENT_ID}",
        f"https://api.cuescore.com/tournament/{TOURNAMENT_ID}",
        f"https://api.cuescore.com/tournaments/{TOURNAMENT_ID}"
    ]
    
    for url in urls:
        try:
            print(f"   🔗 Probando: {url}")
            response = requests.get(url, headers=headers, timeout=30)
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                print("   ✅ ¡Éxito!")
                return response.json()
            else:
                print(f"   ❌ Error: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    return None

def test_webpage_scraping():
    """Prueba extraer datos de la página web directamente"""
    print("🌐 Probando scraping de página web...")
    
    url = f"https://cuescore.com/tournament/{TOURNAMENT_ID}"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'es-ES,es;q=0.9,en;q=0.8'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            print("   ✅ Página accesible")
            
            # Buscar datos JSON en el HTML
            html_content = response.text
            
            # Buscar patrones comunes de datos JSON
            import re
            
            # Patrón para encontrar datos JSON en el HTML
            json_patterns = [
                r'window\.__INITIAL_STATE__\s*=\s*({.*?});',
                r'window\.tournamentData\s*=\s*({.*?});',
                r'data-tournament\s*=\s*"({.*?})"',
                r'<script[^>]*>.*?({.*?"tournament".*?}).*?</script>'
            ]
            
            for pattern in json_patterns:
                matches = re.findall(pattern, html_content, re.DOTALL)
                if matches:
                    print(f"   🎯 Datos encontrados con patrón: {pattern[:50]}...")
                    try:
                        data = json.loads(matches[0])
                        return data
                    except:
                        continue
            
            print("   ❌ No se encontraron datos JSON en la página")
            return None
        else:
            print(f"   ❌ Error: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return None

def analyze_data(data):
    """Analiza los datos recibidos"""
    if not data:
        print("❌ No hay datos para analizar")
        return
    
    print("\n📊 ANÁLISIS DE DATOS:")
    print("=" * 40)
    
    # Mostrar estructura
    print(f"📋 Estructura:")
    for key in data.keys():
        if isinstance(data[key], list):
            print(f"   📁 {key}: {len(data[key])} elementos")
        elif isinstance(data[key], dict):
            print(f"   📁 {key}: {len(data[key])} propiedades")
        else:
            print(f"   📄 {key}: {type(data[key]).__name__}")
    
    # Buscar información específica
    if 'tournament' in data:
        tournament = data['tournament']
        print(f"\n🏆 TORNEO:")
        print(f"   Nombre: {tournament.get('name', 'N/A')}")
        print(f"   ID: {tournament.get('id', 'N/A')}")
        print(f"   Estado: {tournament.get('status', 'N/A')}")
    
    if 'players' in data:
        players = data['players']
        print(f"\n👤 JUGADORES ({len(players)}):")
        for i, (player_id, player) in enumerate(list(players.items())[:3]):
            print(f"   {i+1}. {player.get('name', 'N/A')} (ID: {player_id})")
        if len(players) > 3:
            print(f"   ... y {len(players) - 3} más")
    
    if 'matches' in data:
        matches = data['matches']
        print(f"\n🎯 PARTIDAS ({len(matches)}):")
        for i, match in enumerate(matches[:3]):
            print(f"   {i+1}. {match.get('player1', 'N/A')} vs {match.get('player2', 'N/A')}")
        if len(matches) > 3:
            print(f"   ... y {len(matches) - 3} más")

def main():
    """Función principal"""
    print("=" * 60)
    print("🧪 PRUEBA AVANZADA DE API CUESCORE")
    print("=" * 60)
    print(f"ID del torneo: {TOURNAMENT_ID}")
    print()
    
    data = None
    
    # Prueba 1: Sesión de navegador
    print("1️⃣ PRUEBA CON SESIÓN DE NAVEGADOR")
    data = test_with_session()
    
    if not data:
        # Prueba 2: API directa
        print("\n2️⃣ PRUEBA API DIRECTA")
        data = test_direct_api()
    
    if not data:
        # Prueba 3: Scraping de página
        print("\n3️⃣ PRUEBA SCRAPING DE PÁGINA")
        data = test_webpage_scraping()
    
    # Análisis de resultados
    if data:
        analyze_data(data)
        
        # Guardar datos
        try:
            with open('cuescore_data_sample.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"\n💾 Datos guardados en: cuescore_data_sample.json")
        except Exception as e:
            print(f"❌ Error al guardar: {e}")
        
        print("\n🎉 ¡Datos obtenidos exitosamente!")
        print("💡 Puedes proceder con el sistema de actualización")
        
    else:
        print("\n❌ No se pudieron obtener datos de Cuescore")
        print("💡 Posibles soluciones:")
        print("   - Verificar el ID del torneo")
        print("   - Comprobar si el torneo es público")
        print("   - Considerar usar datos estáticos")
        print("   - Contactar a Cuescore para acceso oficial")

if __name__ == "__main__":
    main() 