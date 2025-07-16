// ===== COMPONENTES =====

// Componente para renderizar tarjeta de jugador
function renderPlayerCard(player) {
  const rankInfo = getPlayerRank(player);
  const pruebasText = getPruebasText(player);

  return `
        <div class="player-card ${player.clasificado ? "clasificado" : ""} ${
    rankInfo.rank
  }">
            <div class="player-rank">
                <span class="rank-crown">${rankInfo.crown}</span>
                <span class="rank-badge rank-${rankInfo.rank}">${
    rankInfo.label
  }</span>
                ${pruebasText}
            </div>
            <div class="player-name">${escapeHtml(player.nombre_gallego)}</div>
            <div class="player-liga">
                ${
                  player.liga
                    ? `<span class="liga-badge">${player.liga}</span>`
                    : "Sin liga"
                }
                ${
                  player.clasificado
                    ? ' <span style="color: #28a745;">✓ Clasificado</span>'
                    : ""
                }
            </div>
            ${
              player.liga
                ? `
                <div class="player-stats">
                    <div class="stat-item">
                        <span class="stat-label">Posición:</span>
                        <span class="stat-value">${
                          player.posicion || "N/A"
                        }</span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-label">Puntos:</span>
                        <span class="stat-value">${
                          player.puntos_totales || "N/A"
                        }</span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-label">Partidas:</span>
                        <span class="stat-value">${
                          player.partidas_favor || 0
                        }-${player.partidas_contra || 0}</span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-label">Diferencia:</span>
                        <span class="stat-value">${
                          player.diferencia_partidas || 0
                        }</span>
                    </div>
                </div>
            `
                : '<div style="color: #999; font-style: italic;">Sin datos de ranking</div>'
            }
        </div>
    `;
}

// Componente para renderizar tarjeta de partida
function renderMatchCard(match) {
  const playerA = findPlayerByName(match.playerA.name);
  const playerB = findPlayerByName(match.playerB.name);
  const rankInfoA = playerA ? getPlayerRank(playerA) : null;
  const rankInfoB = playerB ? getPlayerRank(playerB) : null;

  return `
        <div class="player-card">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
                <div style="font-weight: bold; color: #1e3c72;">${escapeHtml(
                  match.roundName
                )} - Partida ${match.matchno}</div>
                <span class="match-status status-${
                  match.matchstatus
                }">${getStatusText(match.matchstatus)}</span>
            </div>
            
            <div class="match-players-row">
                <div class="match-player match-player-left">
                    <div class="player-details">
                        <div class="player-name-clickable ${
                          rankInfoA ? "has-ranking" : ""
                        }" 
                             onmouseover="if(window.innerWidth > 768) showPlayerTooltip(event, '${escapeHtml(
                               match.playerA.name
                             )}')" 
                             onmouseout="if(window.innerWidth > 768) hidePlayerTooltip()" 
                             onclick="showPlayerModal('${escapeHtml(
                               match.playerA.name
                             )}')" 
                             style="font-weight: bold;">
                            ${rankInfoA ? `${rankInfoA.crown} ` : ""}
                            ${escapeHtml(match.playerA.name)}
                        </div>
                        ${
                          match.playerA.ranking_info
                            ? `
                            <div style="font-size: 0.8em; color: #666;">
                                ${match.playerA.ranking_info.liga} - Pos. ${match.playerA.ranking_info.posicion_liga}
                            </div>
                        `
                            : ""
                        }
                    </div>
                </div>
                
                <div class="match-score">${match.scoreA} - ${match.scoreB}</div>
                
                <div class="match-player match-player-right">
                    <div class="player-details">
                        <div class="player-name-clickable ${
                          rankInfoB ? "has-ranking" : ""
                        }" 
                             onmouseover="if(window.innerWidth > 768) showPlayerTooltip(event, '${escapeHtml(
                               match.playerB.name
                             )}')" 
                             onmouseout="if(window.innerWidth > 768) hidePlayerTooltip()" 
                             onclick="showPlayerModal('${escapeHtml(
                               match.playerB.name
                             )}')" 
                             style="font-weight: bold;">
                            ${rankInfoB ? `${rankInfoB.crown} ` : ""}
                            ${escapeHtml(match.playerB.name)}
                        </div>
                        ${
                          match.playerB.ranking_info
                            ? `
                            <div style="font-size: 0.8em; color: #666;">
                                ${match.playerB.ranking_info.liga} - Pos. ${match.playerB.ranking_info.posicion_liga}
                            </div>
                        `
                            : ""
                        }
                    </div>
                </div>
            </div>
            
            <div style="font-size: 0.8em; color: #666;">
                Race to ${match.raceTo} • ${match.discipline}
            </div>
        </div>
    `;
}

// Componente para renderizar tarjeta de liga
function renderLigaCard(liga, stats) {
  return `
        <div class="player-card">
            <div class="player-name">${liga.toUpperCase()}</div>
            <div class="player-stats">
                <div class="stat-item">
                    <span class="stat-label">Jugadores:</span>
                    <span class="stat-value">${stats.total_players}</span>
                </div>
                <div class="stat-item">
                    <span class="stat-label">Clasificados:</span>
                    <span class="stat-value">${stats.clasificados}</span>
                </div>
                <div class="stat-item">
                    <span class="stat-label">Promedio puntos:</span>
                    <span class="stat-value">${stats.puntos_promedio}</span>
                </div>
                <div class="stat-item">
                    <span class="stat-label">Mejor posición:</span>
                    <span class="stat-value">${
                      stats.mejor_posicion || "N/A"
                    }</span>
                </div>
            </div>
        </div>
    `;
}

// Función para mostrar tooltip de jugador
function showPlayerTooltip(event, playerName) {
  const player = findPlayerByName(playerName);
  if (!player || !player.liga) return;

  const tooltip = document.getElementById("playerTooltip");
  const rankInfo = getPlayerRank(player);

  tooltip.innerHTML = `
        <div class="tooltip-header">${escapeHtml(player.nombre_gallego)}</div>
        <div class="tooltip-stats">
            <div class="tooltip-stat">
                <span class="label">Liga:</span>
                <span class="value">${player.liga}</span>
            </div>
            <div class="tooltip-stat">
                <span class="label">Posición:</span>
                <span class="value">${player.posicion || "N/A"}</span>
            </div>
            <div class="tooltip-stat">
                <span class="label">Puntos:</span>
                <span class="value">${player.puntos_totales || "N/A"}</span>
            </div>
            <div class="tooltip-stat">
                <span class="label">Rango:</span>
                <span class="value">${rankInfo.label}</span>
            </div>
        </div>
    `;

  tooltip.style.left = event.pageX + 10 + "px";
  tooltip.style.top = event.pageY - 10 + "px";
  tooltip.classList.add("show");
}

// Función para ocultar tooltip
function hidePlayerTooltip() {
  const tooltip = document.getElementById("playerTooltip");
  tooltip.classList.remove("show");
}

// Función para mostrar modal de jugador
function showPlayerModal(playerName) {
  const player = findPlayerByName(playerName);
  if (!player) return;

  const modal = document.getElementById("playerModal");
  const modalContent = document.getElementById("modalContent");
  const rankInfo = getPlayerRank(player);

  modalContent.innerHTML = `
        <div class="modal-header">
            <div>
                <h2 style="margin: 0; color: #1e3c72;">${escapeHtml(
                  player.nombre_gallego
                )}</h2>
                <div style="color: #666; margin-top: 15px;">
                    ${
                      player.liga
                        ? `<span class="liga-badge">${player.liga}</span>`
                        : "Sin liga"
                    }
                    ${
                      player.clasificado
                        ? ' <span style="color: #28a745;">✓ Clasificado</span>'
                        : ""
                    }
                </div>
            </div>
            <div class="modal-rank">
                <span style="font-size: 1.5em;">${rankInfo.crown}</span>
                <span class="modal-rank-badge rank-${rankInfo.rank}">${
    rankInfo.label
  }</span>
            </div>
        </div>

        ${
          player.liga
            ? `
            <div class="modal-stats">
                <div class="modal-stat-item">
                    <div class="modal-stat-value">${
                      player.posicion || "N/A"
                    }</div>
                    <div class="modal-stat-label">Posición</div>
                </div>
                <div class="modal-stat-item">
                    <div class="modal-stat-value">${
                      player.puntos_totales || "N/A"
                    }</div>
                    <div class="modal-stat-label">Puntos Totales</div>
                </div>
                <div class="modal-stat-item">
                    <div class="modal-stat-value">${
                      player.puntos_base || "N/A"
                    }</div>
                    <div class="modal-stat-label">Puntos Base</div>
                </div>
                <div class="modal-stat-item">
                    <div class="modal-stat-value">${
                      player.pruebas_jugadas || 0
                    }</div>
                    <div class="modal-stat-label">Pruebas Jugadas</div>
                </div>
            </div>

            <div style="background: #f8f9fa; padding: 15px; border-radius: 8px; margin-bottom: 15px;">
                <h4 style="margin: 0 0 10px 0; color: #1e3c72;">Estadísticas de Partidas</h4>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
                    <div>
                        <strong>Partidas a favor:</strong> ${
                          player.partidas_favor || 0
                        }
                    </div>
                    <div>
                        <strong>Partidas en contra:</strong> ${
                          player.partidas_contra || 0
                        }
                    </div>
                    <div>
                        <strong>Diferencia:</strong> ${
                          player.diferencia_partidas || 0
                        }
                    </div>
                    <div>
                        <strong>AGP:</strong> ${player.agp || "N/A"}
                    </div>
                </div>
            </div>
        `
            : `
            <div style="text-align: center; color: #999; font-style: italic; padding: 20px;">
                Sin datos de ranking disponibles
            </div>
        `
        }
    `;

  modal.classList.add("show");
}

// Función para cerrar modal
function closePlayerModal() {
  const modal = document.getElementById("playerModal");
  modal.classList.remove("show");
}
