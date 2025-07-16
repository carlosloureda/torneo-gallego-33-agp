#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
import re
from difflib import SequenceMatcher
import unicodedata

def normalize_name(name):
    """
    Normaliza un nombre para comparación:
    - Convierte a minúsculas
    - Elimina acentos
    - Elimina espacios extra
    - Elimina caracteres especiales
    """
    # Convertir a minúsculas
    name = name.lower()
    
    # Eliminar acentos
    name = unicodedata.normalize('NFD', name)
    name = ''.join(c for c in name if not unicodedata.combining(c))
    
    # Eliminar caracteres especiales y espacios extra
    name = re.sub(r'[^\w\s]', '', name)
    name = re.sub(r'\s+', ' ', name).strip()
    
    return name

def similarity_score(name1, name2):
    """
    Calcula la similitud entre dos nombres normalizados
    """
    norm1 = normalize_name(name1)
    norm2 = normalize_name(name2)
    
    # Si son exactamente iguales después de normalizar
    if norm1 == norm2:
        return 1.0
    
    # Usar SequenceMatcher para calcular similitud
    return SequenceMatcher(None, norm1, norm2).ratio()

def find_player_in_rankings(player_name, rankings_data):
    """
    Busca un jugador en todos los rankings disponibles
    """
    best_match = None
    best_score = 0
    best_ranking = None
    
    for ranking_name, ranking_data in rankings_data.items():
        for player in ranking_data['jugadores']:
            score = similarity_score(player_name, player['nombre'])
            
            if score > best_score and score > 0.7:  # Umbral de similitud
                best_score = score
                best_match = player
                best_ranking = ranking_name
    
    return best_match, best_ranking, best_score

def load_all_rankings():
    """
    Carga todos los rankings de la carpeta jsons-agp
    """
    rankings = {}
    jsons_dir = "jsons-agp"
    
    if not os.path.exists(jsons_dir):
        print(f"Error: No se encuentra la carpeta {jsons_dir}")
        return rankings
    
    for filename in os.listdir(jsons_dir):
        if filename.endswith('.json'):
            ranking_name = filename.replace('_ranking.json', '').replace('-ranking.json', '')
            filepath = os.path.join(jsons_dir, filename)
            
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    rankings[ranking_name] = json.load(f)
                print(f"✅ Cargado: {ranking_name} ({len(rankings[ranking_name]['jugadores'])} jugadores)")
            except Exception as e:
                print(f"❌ Error cargando {filename}: {e}")
    
    return rankings

def load_participants_with_fix():
    """
    Carga los participantes del gallego manejando el problema del JSON y normaliza 'country' y 'represents'.
    Si hay error, imprime el fragmento que intenta cargar.
    """
    try:
        with open('individual-lista-participantes.json', 'r', encoding='utf-8') as f:
            content = f.read()
        # Reemplazar todas las apariciones de '"country": []' y '"represents": []' por objetos vacíos
        content = content.replace('"country": []', '"country": {}')
        content = content.replace('"represents": []', '"represents": {}')
        # Buscar el final del JSON válido (antes de cualquier basura)
        json_end = content.find(']')
        if json_end != -1:
            json_content = content[:json_end+1]
            try:
                participantes = json.loads(json_content)
            except Exception as e:
                print('--- FRAGMENTO JSON ---')
                print(json_content[:500])
                print('--- FIN FRAGMENTO ---')
                print(f"❌ Error cargando participantes (fragmento): {e}")
                return None
            print(f"📋 Cargados {len(participantes)} participantes del gallego (normalizados)")
            return participantes
        else:
            print("❌ No se pudo encontrar el final del JSON válido")
            return None
    except Exception as e:
        print(f"❌ Error cargando participantes: {e}")
        return None

def analyze_gallego_participants():
    """
    Analiza los participantes del gallego y busca información en los rankings
    """
    # Cargar participantes del gallego
    participantes = load_participants_with_fix()
    if not participantes:
        return
    
    # Cargar todos los rankings
    rankings = load_all_rankings()
    if not rankings:
        print("❌ No se pudieron cargar los rankings")
        return
    
    # Analizar cada participante
    resultados = []
    encontrados = 0
    no_encontrados = 0
    
    print(f"\n🔍 Analizando participantes...")
    print("=" * 80)
    
    for participante in participantes:
        nombre = participante['name']
        player_id = participante['playerId']
        
        # Buscar en rankings
        jugador_ranking, ranking_name, score = find_player_in_rankings(nombre, rankings)
        
        if jugador_ranking:
            encontrados += 1
            resultado = {
                'player_id': player_id,
                'nombre_gallego': nombre,
                'nombre_ranking': jugador_ranking['nombre'],
                'similitud': round(score, 3),
                'liga': ranking_name,
                'posicion': jugador_ranking['posicion'],
                'agp': jugador_ranking['agp'],
                'puntos_totales': jugador_ranking['puntos']['pt'],
                'puntos_base': jugador_ranking['puntos']['p'],
                'puntos_extra': jugador_ranking['puntos']['v'],
                'penalizaciones': jugador_ranking['puntos']['penalizaciones'],
                'partidas_favor': jugador_ranking['partidas']['pf'],
                'partidas_contra': jugador_ranking['partidas']['pc'],
                'diferencia_partidas': jugador_ranking['partidas']['dp'],
                'pruebas_jugadas': sum(1 for p in jugador_ranking['pruebas'].values() if p > 0),
                'clasificado': jugador_ranking['posicion'] <= 5  # Asumimos top 5 clasificados
            }
            
            print(f"✅ {nombre}")
            print(f"   📍 Liga: {ranking_name} | Posición: {jugador_ranking['posicion']}")
            print(f"   🏆 Puntos: {jugador_ranking['puntos']['pt']} | Partidas: {jugador_ranking['partidas']['pf']}-{jugador_ranking['partidas']['pc']}")
            print(f"   🎯 Similitud: {score:.3f}")
            print()
            
        else:
            no_encontrados += 1
            resultado = {
                'player_id': player_id,
                'nombre_gallego': nombre,
                'nombre_ranking': None,
                'similitud': 0,
                'liga': None,
                'posicion': None,
                'agp': None,
                'puntos_totales': None,
                'puntos_base': None,
                'puntos_extra': None,
                'penalizaciones': None,
                'partidas_favor': None,
                'partidas_contra': None,
                'diferencia_partidas': None,
                'pruebas_jugadas': None,
                'clasificado': False
            }
            
            print(f"❌ {nombre} - No encontrado en rankings")
            print()
        
        resultados.append(resultado)
    
    # Guardar resultados
    with open('analisis_participantes_gallego.json', 'w', encoding='utf-8') as f:
        json.dump(resultados, f, ensure_ascii=False, indent=2)
    
    # Generar resumen
    print("=" * 80)
    print("📊 RESUMEN DEL ANÁLISIS")
    print("=" * 80)
    print(f"Total participantes: {len(participantes)}")
    print(f"Encontrados en rankings: {encontrados}")
    print(f"No encontrados: {no_encontrados}")
    print(f"Porcentaje de éxito: {(encontrados/len(participantes)*100):.1f}%")
    
    # Estadísticas por liga
    ligas_count = {}
    clasificados_count = 0
    
    for resultado in resultados:
        if resultado['liga']:
            liga = resultado['liga']
            ligas_count[liga] = ligas_count.get(liga, 0) + 1
            if resultado['clasificado']:
                clasificados_count += 1
    
    print(f"\n🏆 Clasificados por liga: {clasificados_count}")
    print("\n📈 Distribución por ligas:")
    for liga, count in sorted(ligas_count.items(), key=lambda x: x[1], reverse=True):
        print(f"   {liga}: {count} jugadores")
    
    print(f"\n💾 Resultados guardados en: analisis_participantes_gallego.json")

if __name__ == "__main__":
    analyze_gallego_participants() 