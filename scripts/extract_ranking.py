#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import sys
import re
from bs4 import BeautifulSoup

def extract_ranking_data(html_file):
    """
    Extrae los datos del ranking de billar del archivo HTML
    """
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Parsear el HTML
    soup = BeautifulSoup(content, 'html.parser')
    
    # Encontrar todas las filas de datos (excluyendo las filas de encabezado)
    rows = soup.find_all('tr')
    
    players = []
    
    for row in rows:
        cells = row.find_all('td')
        
        # Verificar que es una fila de datos (debe tener al menos 20 celdas)
        if len(cells) >= 20:
            # Extraer el contenido de las celdas
            cell_contents = []
            for cell in cells:
                div = cell.find('div')
                if div:
                    cell_contents.append(div.get_text(strip=True))
                else:
                    cell_contents.append(cell.get_text(strip=True))
            
            # Verificar que la primera celda contiene un número (posición)
            if cell_contents and cell_contents[0].isdigit():
                try:
                    player_data = {
                        "posicion": int(cell_contents[0]),
                        "agp": cell_contents[1],
                        "nombre": cell_contents[2],
                        "pruebas": {
                            "p1": int(cell_contents[3]) if cell_contents[3].isdigit() else 0,
                            "p2": int(cell_contents[4]) if cell_contents[4].isdigit() else 0,
                            "p3": int(cell_contents[5]) if cell_contents[5].isdigit() else 0,
                            "p4": int(cell_contents[6]) if cell_contents[6].isdigit() else 0,
                            "p5": int(cell_contents[7]) if cell_contents[7].isdigit() else 0,
                            "p6": int(cell_contents[8]) if cell_contents[8].isdigit() else 0,
                            "p7": int(cell_contents[9]) if cell_contents[9].isdigit() else 0,
                            "p8": int(cell_contents[10]) if cell_contents[10].isdigit() else 0,
                            "p9": int(cell_contents[11]) if cell_contents[11].isdigit() else 0
                        },
                        "partidas": {
                            "pf": int(cell_contents[12]) if cell_contents[12].isdigit() else 0,  # Partidas a favor
                            "pc": int(cell_contents[13]) if cell_contents[13].isdigit() else 0,  # Partidas en contra
                            "dp": int(cell_contents[14]) if cell_contents[14].isdigit() or (cell_contents[14].startswith('-') and cell_contents[14][1:].isdigit()) else 0  # Diferencia de partidas
                        },
                        "puntos": {
                            "p": int(cell_contents[15]) if cell_contents[15].isdigit() else 0,  # Puntos
                            "v": int(cell_contents[16]) if cell_contents[16].isdigit() else 0,  # Puntos extra por participar
                            "t": int(cell_contents[17]) if cell_contents[17].isdigit() else 0,  # Total (P+V)
                            "penalizaciones": int(cell_contents[18]) if cell_contents[18].isdigit() else 0,  # Penalizaciones
                            "pt": int(cell_contents[19]) if cell_contents[19].isdigit() else 0  # Puntos totales (T-P)
                        }
                    }
                    players.append(player_data)
                except (ValueError, IndexError) as e:
                    print(f"Error procesando fila: {e}")
                    continue
    
    return players

def get_tournament_name(html_file):
    """
    Extrae el nombre del torneo del archivo HTML
    """
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    soup = BeautifulSoup(content, 'html.parser')
    
    # Buscar el título del torneo
    title_div = soup.find('div', style=lambda x: x and 'font-size: 18pt' in x)
    if title_div:
        return title_div.get_text(strip=True)
    
    # Si no encuentra el título, usar el nombre del archivo
    return html_file.replace('-individual.html', '').replace('_', ' ').title()

def main():
    # Verificar si se proporciona un archivo como argumento
    if len(sys.argv) > 1:
        html_file = sys.argv[1]
    else:
        print("Uso: python extract_ranking.py <archivo_html>")
        print("Ejemplos:")
        print("  python extract_ranking.py corunha-individual.html")
        print("  python extract_ranking.py santiago-individual.html")
        return
    
    # Extraer datos del ranking
    players = extract_ranking_data(html_file)
    
    # Obtener nombre del torneo
    tournament_name = get_tournament_name(html_file)
    
    # Crear el JSON final
    ranking_data = {
        "torneo": tournament_name,
        "descripcion": {
            "cabeza_serie": "Cabeza de serie XXXIII Campeonato Gallego 3ª Categoría",
            "clasificado": "Clasificado XXXIII Campeonato Gallego 3ª Categoría",
            "nota_clasificados": "Los jugadores clasificados para el XXXIII Campeonato Gallego (Lalín del 18 al 20 de Julio) deberán confirmar su participación antes del día 9 de Junio a las 12:00 horas",
            "nota_repesca": "Los jugadores no clasificados que hayan disputado un mínimo de 5 pruebas podrán optar a más plazas en una repesca provincial el día 14 de Junio, para la que deberán confirmar su participación antes del día 9 de Junio a las 12:00 horas"
        },
        "jugadores": players
    }
    
    # Generar nombre del archivo JSON basado en el archivo HTML
    json_filename = html_file.replace('-individual.html', '_ranking.json')
    
    # Guardar el JSON
    with open(json_filename, 'w', encoding='utf-8') as f:
        json.dump(ranking_data, f, ensure_ascii=False, indent=2)
    
    print(f"Se han extraído {len(players)} jugadores del ranking")
    print(f"Archivo JSON generado: {json_filename}")

if __name__ == "__main__":
    main() 