// ===== APLICACIÓN PRINCIPAL =====

// Variable global para los datos del torneo
let tournamentData = null;

// Función de inicialización
async function initApp() {
  try {
    // Cargar datos del torneo
    const response = await fetch("./data/tournament_extended.json");
    tournamentData = await response.json();

    // Inicializar la aplicación
    populateFilterOptions();
    renderStatsGrid();
    renderPlayersTab();
    renderMatchesTab();
    renderSummaryTab();

    // Configurar event listeners
    setupEventListeners();

    console.log("Aplicación inicializada correctamente");
  } catch (error) {
    console.error("Error al inicializar la aplicación:", error);
    document.body.innerHTML = `
            <div style="text-align: center; padding: 50px; color: white;">
                <h2>Error al cargar los datos</h2>
                <p>No se pudo cargar el archivo tournament_extended.json</p>
                <p>Asegúrate de que el archivo existe en la carpeta raíz del proyecto.</p>
            </div>
        `;
  }
}

// Función para configurar event listeners
function setupEventListeners() {
  // Event listeners para tabs
  document.querySelectorAll(".tab").forEach((tab) => {
    tab.addEventListener("click", () => {
      const tabName = tab.dataset.tab;
      switchTab(tabName);
    });
  });

  // Event listeners para filtros de jugadores
  document
    .getElementById("playerSearch")
    .addEventListener("input", updatePlayerFilters);
  document
    .getElementById("ligaFilter")
    .addEventListener("change", updatePlayerFilters);
  document
    .getElementById("statusFilter")
    .addEventListener("change", updatePlayerFilters);
  document
    .getElementById("rankFilter")
    .addEventListener("change", updatePlayerFilters);

  // Event listeners para filtros de partidas
  document
    .getElementById("matchSearch")
    .addEventListener("input", updateMatchFilters);
  document
    .getElementById("roundFilter")
    .addEventListener("change", updateMatchFilters);
  document
    .getElementById("matchStatusFilter")
    .addEventListener("change", updateMatchFilters);

  // Event listener para cerrar modal
  document
    .getElementById("modalClose")
    .addEventListener("click", closePlayerModal);
  document.getElementById("playerModal").addEventListener("click", (e) => {
    if (e.target === e.currentTarget) {
      closePlayerModal();
    }
  });

  // Event listener para ocultar tooltip al hacer scroll
  document.addEventListener("scroll", hidePlayerTooltip);
}

// Función para cambiar de tab
function switchTab(tabName) {
  // Remover clase active de todos los tabs
  document.querySelectorAll(".tab").forEach((tab) => {
    tab.classList.remove("active");
  });
  document.querySelectorAll(".tab-content").forEach((content) => {
    content.classList.remove("active");
  });

  // Activar el tab seleccionado
  document.querySelector(`[data-tab="${tabName}"]`).classList.add("active");
  document.getElementById(`${tabName}Tab`).classList.add("active");
}

// Función para renderizar estadísticas generales
function renderStatsGrid() {
  const statsGrid = document.getElementById("statsGrid");

  const totalPlayers = tournamentData.players.length;
  const clasificados = tournamentData.players.filter(
    (p) => p.clasificado
  ).length;
  const totalMatches = tournamentData.matches.length;
  const finishedMatches = tournamentData.matches.filter(
    (m) => m.matchstatus === "finished"
  ).length;
  const ligas = [
    ...new Set(tournamentData.players.filter((p) => p.liga).map((p) => p.liga)),
  ].length;

  statsGrid.innerHTML = `
        <div class="stat-card">
            <div class="stat-number">${totalPlayers}</div>
            <div class="stat-label">Total Jugadores</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">${clasificados}</div>
            <div class="stat-label">Clasificados</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">${totalMatches}</div>
            <div class="stat-label">Total Partidas</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">${finishedMatches}</div>
            <div class="stat-label">Partidas Finalizadas</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">${ligas}</div>
            <div class="stat-label">Ligas Representadas</div>
        </div>
    `;
}

// Función para renderizar tab de jugadores
function renderPlayersTab() {
  const playersGrid = document.getElementById("playersGrid");
  const filteredPlayers = filterPlayers(tournamentData.players);

  if (filteredPlayers.length === 0) {
    playersGrid.innerHTML = `
            <div style="text-align: center; padding: 50px; color: #666;">
                <h3>No se encontraron jugadores</h3>
                <p>Intenta ajustar los filtros de búsqueda</p>
            </div>
        `;
    return;
  }

  playersGrid.innerHTML = filteredPlayers
    .map((player) => renderPlayerCard(player))
    .join("");
}

// Función para renderizar tab de partidas
function renderMatchesTab() {
  const matchesContainer = document.getElementById("matchesContainer");
  const filteredMatches = filterMatches(tournamentData.matches);

  if (filteredMatches.length === 0) {
    matchesContainer.innerHTML = `
            <div style="text-align: center; padding: 50px; color: #666;">
                <h3>No se encontraron partidas</h3>
                <p>Intenta ajustar los filtros de búsqueda</p>
            </div>
        `;
    return;
  }

  // Agrupar partidas por ronda
  const matchesByRound = {};
  filteredMatches.forEach((match) => {
    if (!matchesByRound[match.roundName]) {
      matchesByRound[match.roundName] = [];
    }
    matchesByRound[match.roundName].push(match);
  });

  matchesContainer.innerHTML = Object.entries(matchesByRound)
    .map(
      ([roundName, matches]) => `
            <div style="margin-bottom: 30px;">
                <h3 style="color: #1e3c72; margin-bottom: 15px; padding-bottom: 5px; border-bottom: 2px solid #eee;">
                    ${escapeHtml(roundName)} (${matches.length} partidas)
                </h3>
                <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(400px, 1fr)); gap: 15px;">
                    ${matches.map((match) => renderMatchCard(match)).join("")}
                </div>
            </div>
        `
    )
    .join("");
}

// Función para renderizar tab de resumen
function renderSummaryTab() {
  const summaryContainer = document.getElementById("summaryContainer");

  // Estadísticas por liga
  const ligaStats = {};
  tournamentData.players.forEach((player) => {
    if (player.liga) {
      if (!ligaStats[player.liga]) {
        ligaStats[player.liga] = {
          total_players: 0,
          clasificados: 0,
          puntos_totales: 0,
          mejor_posicion: null,
        };
      }
      ligaStats[player.liga].total_players++;
      if (player.clasificado) ligaStats[player.liga].clasificados++;
      if (player.puntos_totales)
        ligaStats[player.liga].puntos_totales += player.puntos_totales;
      if (
        player.posicion &&
        (!ligaStats[player.liga].mejor_posicion ||
          player.posicion < ligaStats[player.liga].mejor_posicion)
      ) {
        ligaStats[player.liga].mejor_posicion = player.posicion;
      }
    }
  });

  // Calcular promedios
  Object.keys(ligaStats).forEach((liga) => {
    ligaStats[liga].puntos_promedio = Math.round(
      ligaStats[liga].puntos_totales / ligaStats[liga].total_players
    );
  });

  // Estadísticas por rango
  const rankStats = {};
  ["elite", "expert", "advanced", "intermediate", "beginner"].forEach(
    (rank) => {
      rankStats[rank] = tournamentData.players.filter((p) => {
        const rankInfo = getPlayerRank(p);
        return rankInfo.rank === rank;
      }).length;
    }
  );

  summaryContainer.innerHTML = `
        <div style="margin-bottom: 30px;">
            <h3 style="color: #1e3c72; margin-bottom: 20px;">Estadísticas por Liga</h3>
            <div class="players-grid">
                ${Object.entries(ligaStats)
                  .sort(([, a], [, b]) => b.total_players - a.total_players)
                  .map(([liga, stats]) => renderLigaCard(liga, stats))
                  .join("")}
            </div>
        </div>

        <div style="margin-bottom: 30px;">
            <h3 style="color: #1e3c72; margin-bottom: 20px;">Distribución por Rango</h3>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px;">
                ${Object.entries(rankStats)
                  .map(([rank, count]) => {
                    const rankInfo = getPlayerRank({ rank });
                    return `
                        <div class="stat-card">
                            <div class="stat-number">${count}</div>
                            <div class="stat-label">${rankInfo.label}</div>
                        </div>
                    `;
                  })
                  .join("")}
            </div>
        </div>

        <div>
            <h3 style="color: #1e3c72; margin-bottom: 20px;">Top 10 Jugadores por Puntos</h3>
            <div class="players-grid">
                ${tournamentData.players
                  .filter((p) => p.puntos_totales)
                  .sort((a, b) => b.puntos_totales - a.puntos_totales)
                  .slice(0, 10)
                  .map((player) => renderPlayerCard(player))
                  .join("")}
            </div>
        </div>
    `;
}

// Inicializar la aplicación cuando el DOM esté listo
document.addEventListener("DOMContentLoaded", initApp);
