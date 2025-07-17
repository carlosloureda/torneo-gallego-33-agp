#!/usr/bin/env python3
"""
Prueba simple de la API de Cuescore
Ejecuta este script manualmente: python3 simple_api_test.py
"""

import requests
import json

# ID del torneo que configuraste
TOURNAMENT_ID = "63505243"

def test_cuescore_api():
    print("🧪 Probando API de Cuescore...")
    print(f"ID del torneo: {TOURNAMENT_ID}")
    
    # URL de la API
    url = f"https://api.cuescore.com/tournament/?id={TOURNAMENT_ID}"
    print(f"URL: {url}")
    
    try:
        # Headers para simular un navegador
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            'Accept': 'application/json',
            'Accept-Language': 'es-ES,es;q=0.9,en;q=0.8'
        }
        
        print("📡 Haciendo petición...")
        response = requests.get(url, headers=headers, timeout=30)
        
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ ¡Éxito! Datos recibidos")
            
            # Parsear JSON
            data = response.json()
            
            # Mostrar información básica
            print(f"\n📋 Estructura de datos:")
            for key in data.keys():
                if isinstance(data[key], list):
                    print(f"   📁 {key}: {len(data[key])} elementos")
                elif isinstance(data[key], dict):
                    print(f"   📁 {key}: {len(data[key])} propiedades")
                else:
                    print(f"   📄 {key}: {type(data[key]).__name__}")
            
            # Guardar muestra
            with open('api_test_result.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"\n💾 Muestra guardada en: api_test_result.json")
            
            return True
            
        else:
            print(f"❌ Error HTTP: {response.status_code}")
            print(f"Respuesta: {response.text[:200]}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_alternative_urls():
    """Prueba URLs alternativas"""
    print("\n🔄 Probando URLs alternativas...")
    
    urls = [
        f"https://api.cuescore.com/tournaments/?id={TOURNAMENT_ID}",
        f"https://cuescore.com/api/tournament/?id={TOURNAMENT_ID}",
        f"https://cuescore.com/api/tournaments/?id={TOURNAMENT_ID}"
    ]
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
        'Accept': 'application/json'
    }
    
    for url in urls:
        try:
            print(f"\n🔗 Probando: {url}")
            response = requests.get(url, headers=headers, timeout=10)
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                print("   ✅ ¡Funciona!")
                return True
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    return False

if __name__ == "__main__":
    print("=" * 60)
    print("🧪 PRUEBA DE API CUESCORE")
    print("=" * 60)
    
    # Prueba principal
    success = test_cuescore_api()
    
    if not success:
        print("\n⚠️  URL principal falló, probando alternativas...")
        test_alternative_urls()
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 ¡API funcionando! Puedes proceder con el sistema de actualización")
    else:
        print("❌ API no funciona. Revisa el ID del torneo o la estructura de la URL")
    print("=" * 60) 