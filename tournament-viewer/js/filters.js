// ===== FILTROS =====

// Variables globales para filtros
let currentPlayerFilters = {
  search: "",
  liga: "",
  status: "",
  rank: "",
};

let currentMatchFilters = {
  search: "",
  round: "",
  status: "",
};

// Función para filtrar jugadores
function filterPlayers(players) {
  return players.filter((player) => {
    // Filtro de búsqueda
    if (currentPlayerFilters.search) {
      const searchTerm = currentPlayerFilters.search.toLowerCase();
      const playerName = player.nombre_gallego.toLowerCase();
      const playerLiga = (player.liga || "").toLowerCase();

      if (
        !playerName.includes(searchTerm) &&
        !playerLiga.includes(searchTerm)
      ) {
        return false;
      }
    }

    // Filtro de liga
    if (
      currentPlayerFilters.liga &&
      player.liga !== currentPlayerFilters.liga
    ) {
      return false;
    }

    // Filtro de estado (clasificado/no clasificado)
    if (currentPlayerFilters.status) {
      if (
        currentPlayerFilters.status === "clasificado" &&
        !player.clasificado
      ) {
        return false;
      }
      if (
        currentPlayerFilters.status === "no-clasificado" &&
        player.clasificado
      ) {
        return false;
      }
    }

    // Filtro de rango
    if (currentPlayerFilters.rank) {
      const rankInfo = getPlayerRank(player);
      if (rankInfo.rank !== currentPlayerFilters.rank) {
        return false;
      }
    }

    return true;
  });
}

// Función para filtrar partidas
function filterMatches(matches) {
  return matches.filter((match) => {
    // Filtro de búsqueda
    if (currentMatchFilters.search) {
      const searchTerm = currentMatchFilters.search.toLowerCase();
      const playerAName = match.playerA.name.toLowerCase();
      const playerBName = match.playerB.name.toLowerCase();
      const roundName = match.roundName.toLowerCase();

      if (
        !playerAName.includes(searchTerm) &&
        !playerBName.includes(searchTerm) &&
        !roundName.includes(searchTerm)
      ) {
        return false;
      }
    }

    // Filtro de ronda
    if (
      currentMatchFilters.round &&
      match.roundName !== currentMatchFilters.round
    ) {
      return false;
    }

    // Filtro de estado
    if (
      currentMatchFilters.status &&
      match.matchstatus !== currentMatchFilters.status
    ) {
      return false;
    }

    return true;
  });
}

// Función para actualizar filtros de jugadores
function updatePlayerFilters() {
  currentPlayerFilters.search = document.getElementById("playerSearch").value;
  currentPlayerFilters.liga = document.getElementById("ligaFilter").value;
  currentPlayerFilters.status = document.getElementById("statusFilter").value;
  currentPlayerFilters.rank = document.getElementById("rankFilter").value;

  renderPlayersTab();
}

// Función para actualizar filtros de partidas
function updateMatchFilters() {
  currentMatchFilters.search = document.getElementById("matchSearch").value;
  currentMatchFilters.round = document.getElementById("roundFilter").value;
  currentMatchFilters.status =
    document.getElementById("matchStatusFilter").value;

  renderMatchesTab();
}

// Función para poblar opciones de filtros
function populateFilterOptions() {
  // Poblar filtro de ligas
  const ligaFilter = document.getElementById("ligaFilter");
  const ligas = [
    ...new Set(
      tournamentData.players
        .filter((p) => p.liga)
        .map((p) => p.liga)
        .sort()
    ),
  ];

  ligas.forEach((liga) => {
    const option = document.createElement("option");
    option.value = liga;
    option.textContent = liga;
    ligaFilter.appendChild(option);
  });

  // Poblar filtro de rondas
  const roundFilter = document.getElementById("roundFilter");
  const rounds = [
    ...new Set(tournamentData.matches.map((m) => m.roundName).sort()),
  ];

  rounds.forEach((round) => {
    const option = document.createElement("option");
    option.value = round;
    option.textContent = round;
    roundFilter.appendChild(option);
  });
}

// Función para limpiar filtros de jugadores
function clearPlayerFilters() {
  document.getElementById("playerSearch").value = "";
  document.getElementById("ligaFilter").value = "";
  document.getElementById("statusFilter").value = "";
  document.getElementById("rankFilter").value = "";

  currentPlayerFilters = {
    search: "",
    liga: "",
    status: "",
    rank: "",
  };

  renderPlayersTab();
}

// Función para limpiar filtros de partidas
function clearMatchFilters() {
  document.getElementById("matchSearch").value = "";
  document.getElementById("roundFilter").value = "";
  document.getElementById("matchStatusFilter").value = "";

  currentMatchFilters = {
    search: "",
    round: "",
    status: "",
  };

  renderMatchesTab();
}

// Función para obtener estadísticas de filtros
function getFilterStats(filteredPlayers, totalPlayers) {
  const stats = {
    total: totalPlayers,
    filtered: filteredPlayers.length,
    clasificados: filteredPlayers.filter((p) => p.clasificado).length,
    noClasificados: filteredPlayers.filter((p) => !p.clasificado).length,
    conRanking: filteredPlayers.filter((p) => p.liga).length,
    sinRanking: filteredPlayers.filter((p) => !p.liga).length,
  };

  // Estadísticas por rango
  const rankStats = {};
  ["elite", "expert", "advanced", "intermediate", "beginner"].forEach(
    (rank) => {
      rankStats[rank] = filteredPlayers.filter((p) => {
        const rankInfo = getPlayerRank(p);
        return rankInfo.rank === rank;
      }).length;
    }
  );

  return { ...stats, rankStats };
}
