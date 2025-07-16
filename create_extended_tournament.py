#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
from datetime import datetime

def load_ranking_data():
    """
    Carga los datos de análisis de participantes con información de rankings
    """
    try:
        with open('analisis_participantes_gallego.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Error cargando datos de rankings: {e}")
        return []

def load_tournament_data():
    """
    Carga los datos del torneo de Cuescore
    """
    try:
        with open('individual-match-data.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Error cargando datos del torneo: {e}")
        return {}

def create_player_lookup(ranking_data):
    """
    Crea un diccionario de búsqueda de jugadores por playerId
    """
    lookup = {}
    for player in ranking_data:
        if player.get('player_id'):
            lookup[player['player_id']] = player
    return lookup

def enrich_match_data(match, player_lookup):
    """
    Enriquece los datos de una partida con información de rankings
    """
    enriched_match = match.copy()
    
    # Enriquecer playerA
    if match['playerA']['playerId'] in player_lookup:
        player_data = player_lookup[match['playerA']['playerId']]
        enriched_match['playerA']['ranking_info'] = {
            'liga': player_data.get('liga'),
            'posicion_liga': player_data.get('posicion'),
            'puntos_totales': player_data.get('puntos_totales'),
            'puntos_base': player_data.get('puntos_base'),
            'partidas_favor': player_data.get('partidas_favor'),
            'partidas_contra': player_data.get('partidas_contra'),
            'diferencia_partidas': player_data.get('diferencia_partidas'),
            'clasificado': player_data.get('clasificado'),
            'agp': player_data.get('agp'),
            'pruebas_jugadas': player_data.get('pruebas_jugadas')
        }
    else:
        enriched_match['playerA']['ranking_info'] = None
    
    # Enriquecer playerB
    if match['playerB']['playerId'] in player_lookup:
        player_data = player_lookup[match['playerB']['playerId']]
        enriched_match['playerB']['ranking_info'] = {
            'liga': player_data.get('liga'),
            'posicion_liga': player_data.get('posicion'),
            'puntos_totales': player_data.get('puntos_totales'),
            'puntos_base': player_data.get('puntos_base'),
            'partidas_favor': player_data.get('partidas_favor'),
            'partidas_contra': player_data.get('partidas_contra'),
            'diferencia_partidas': player_data.get('diferencia_partidas'),
            'clasificado': player_data.get('clasificado'),
            'agp': player_data.get('agp'),
            'pruebas_jugadas': player_data.get('pruebas_jugadas')
        }
    else:
        enriched_match['playerB']['ranking_info'] = None
    
    return enriched_match

def create_tournament_summary(tournament_data, ranking_data):
    """
    Crea un resumen del torneo con estadísticas
    """
    total_matches = len(tournament_data.get('matches', []))
    total_players = len(ranking_data)
    players_with_ranking = sum(1 for p in ranking_data if p.get('liga'))
    
    # Estadísticas por liga
    ligas_stats = {}
    for player in ranking_data:
        if player.get('liga'):
            liga = player['liga']
            if liga not in ligas_stats:
                ligas_stats[liga] = {
                    'total_players': 0,
                    'clasificados': 0,
                    'puntos_promedio': 0,
                    'mejor_posicion': float('inf')
                }
            
            ligas_stats[liga]['total_players'] += 1
            if player.get('clasificado'):
                ligas_stats[liga]['clasificados'] += 1
            
            if player.get('puntos_totales'):
                ligas_stats[liga]['puntos_promedio'] += player['puntos_totales']
            
            if player.get('posicion'):
                ligas_stats[liga]['mejor_posicion'] = min(ligas_stats[liga]['mejor_posicion'], player['posicion'])
    
    # Calcular promedios
    for liga in ligas_stats:
        if ligas_stats[liga]['total_players'] > 0:
            ligas_stats[liga]['puntos_promedio'] = round(
                ligas_stats[liga]['puntos_promedio'] / ligas_stats[liga]['total_players'], 2
            )
        if ligas_stats[liga]['mejor_posicion'] == float('inf'):
            ligas_stats[liga]['mejor_posicion'] = None
    
    return {
        'total_matches': total_matches,
        'total_players': total_players,
        'players_with_ranking': players_with_ranking,
        'players_without_ranking': total_players - players_with_ranking,
        'coverage_percentage': round((players_with_ranking / total_players) * 100, 1) if total_players > 0 else 0,
        'ligas_stats': ligas_stats
    }

def create_extended_tournament():
    """
    Crea el JSON extendido del torneo con toda la información combinada
    """
    print("🔄 Cargando datos...")
    
    # Cargar datos
    ranking_data = load_ranking_data()
    tournament_data = load_tournament_data()
    
    if not ranking_data or not tournament_data:
        print("❌ No se pudieron cargar los datos necesarios")
        return
    
    print(f"✅ Cargados {len(ranking_data)} jugadores con ranking")
    print(f"✅ Cargadas {len(tournament_data.get('matches', []))} partidas del torneo")
    
    # Crear lookup de jugadores
    player_lookup = create_player_lookup(ranking_data)
    print(f"✅ Creado lookup con {len(player_lookup)} jugadores")
    
    # Crear resumen del torneo
    tournament_summary = create_tournament_summary(tournament_data, ranking_data)
    
    # Enriquecer partidas
    print("🔄 Enriqueciendo datos de partidas...")
    enriched_matches = []
    for match in tournament_data.get('matches', []):
        enriched_match = enrich_match_data(match, player_lookup)
        enriched_matches.append(enriched_match)
    
    # Crear JSON extendido
    extended_tournament = {
        'tournament_info': {
            'id': tournament_data.get('tournamentId'),
            'name': tournament_data.get('name'),
            'url': tournament_data.get('url'),
            'display_date': tournament_data.get('displayDate'),
            'starttime': tournament_data.get('starttime'),
            'stoptime': tournament_data.get('stoptime'),
            'status': tournament_data.get('status'),
            'discipline': tournament_data.get('discipline'),
            'venue': tournament_data.get('venues', [{}])[0] if tournament_data.get('venues') else None,
            'owner': tournament_data.get('owner')
        },
        'summary': tournament_summary,
        'players': ranking_data,
        'matches': enriched_matches,
        'generated_at': datetime.now().isoformat(),
        'version': '1.0'
    }
    
    # Guardar JSON extendido
    output_file = 'tournament_extended.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(extended_tournament, f, ensure_ascii=False, indent=2)
    
    print(f"✅ JSON extendido guardado en: {output_file}")
    
    # Mostrar resumen
    print("\n📊 RESUMEN DEL TORNEO EXTENDIDO:")
    print("=" * 50)
    print(f"Total partidas: {tournament_summary['total_matches']}")
    print(f"Total jugadores: {tournament_summary['total_players']}")
    print(f"Jugadores con ranking: {tournament_summary['players_with_ranking']}")
    print(f"Jugadores sin ranking: {tournament_summary['players_without_ranking']}")
    print(f"Cobertura: {tournament_summary['coverage_percentage']}%")
    
    print(f"\n🏆 Estadísticas por ligas:")
    for liga, stats in sorted(tournament_summary['ligas_stats'].items(), 
                             key=lambda x: x[1]['total_players'], reverse=True):
        print(f"   {liga}: {stats['total_players']} jugadores, "
              f"{stats['clasificados']} clasificados, "
              f"promedio {stats['puntos_promedio']} puntos")
    
    return extended_tournament

if __name__ == "__main__":
    create_extended_tournament() 