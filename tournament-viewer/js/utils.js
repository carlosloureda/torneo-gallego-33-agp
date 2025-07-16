// ===== UTILIDADES =====

// Función para obtener el rango de un jugador
function getPlayerRank(player) {
  if (!player.liga || !player.puntos_totales) {
    return { rank: "beginner", crown: "", label: "Sin datos" };
  }

  const puntos = player.puntos_totales;
  const posicion = player.posicion || 999;

  // Sistema de rangos basado en puntos y posición
  if (puntos >= 120 && posicion <= 3) {
    return { rank: "elite", crown: "👑", label: "Élite" };
  } else if (puntos >= 100 && posicion <= 8) {
    return { rank: "expert", crown: "🥇", label: "Experto" };
  } else if (puntos >= 80 && posicion <= 15) {
    return { rank: "advanced", crown: "🥈", label: "Avanzado" };
  } else if (puntos >= 60 && posicion <= 25) {
    return { rank: "intermediate", crown: "🥉", label: "Intermedio" };
  } else {
    return { rank: "beginner", crown: "⭐", label: "Principiante" };
  }
}

// Función para obtener el texto de pruebas
function getPruebasText(player) {
  const pruebas = player.pruebas_jugadas || 0;
  if (pruebas === 0) return "";

  const icon = pruebas >= 10 ? "🏆" : pruebas >= 5 ? "🎯" : "📊";
  return `<span class="pruebas-badge">${icon} ${pruebas} pruebas</span>`;
}

// Función para obtener el texto del estado de partida
function getStatusText(status) {
  const statusMap = {
    finished: "Finalizada",
    waiting: "En espera",
    playing: "En juego",
  };
  return statusMap[status] || status;
}

// Función para encontrar un jugador por nombre
function findPlayerByName(name) {
  return tournamentData.players.find(
    (player) => player.nombre_gallego === name || player.nombre === name
  );
}

// Función para formatear números
function formatNumber(num) {
  return num ? num.toLocaleString() : "N/A";
}

// Función para capitalizar texto
function capitalize(text) {
  return text.charAt(0).toUpperCase() + text.slice(1).toLowerCase();
}

// Función para escapar HTML
function escapeHtml(text) {
  const div = document.createElement("div");
  div.textContent = text;
  return div.innerHTML;
}
