/**
 * Sistema de actualización automática del torneo
 * Detecta cambios en el archivo JSON y refresca la vista
 */

class TournamentRefresher {
  constructor() {
    this.lastModified = null;
    this.isUpdating = false;
    this.updateInterval = null;
    this.checkInterval = 30000; // 30 segundos
    this.lastManualUpdate = 0; // Timestamp de última actualización manual
    this.minUpdateInterval = 30000; // 30 segundos mínimo entre actualizaciones manuales
    this.tournamentStartDate = null; // Se cargará desde el JSON
    this.tournamentEndDate = null; // Se cargará desde el JSON
    this.init();
  }

  init() {
    this.createRefreshUI();
    this.startAutoCheck();
    this.bindEvents();
  }

  createRefreshUI() {
    // Crear indicador de estado en el header
    const header = document.querySelector(".header");
    if (header) {
      const refreshStatus = document.createElement("div");
      refreshStatus.className = "refresh-status";
      refreshStatus.innerHTML = `
        <div class="refresh-info">
          <span class="last-update">Última actualización: <time id="lastUpdate">--</time></span>
          <button id="refreshBtn" class="refresh-btn" title="Actualizar datos del torneo">
            <span class="refresh-icon">🔄</span>
            Actualizar
          </button>
        </div>
        <div class="refresh-indicator" id="refreshIndicator"></div>
        <div class="refresh-counter" id="refreshCounter" style="display: none;"></div>
        <div class="tournament-status" id="tournamentStatus"></div>
      `;

      header.appendChild(refreshStatus);

      // Verificar estado del torneo
      this.checkTournamentStatus();
    }
  }

  bindEvents() {
    const refreshBtn = document.getElementById("refreshBtn");
    if (refreshBtn) {
      refreshBtn.addEventListener("click", () => this.manualRefresh());
    }
  }

  startAutoCheck() {
    // Verificar cambios cada 30 segundos
    this.updateInterval = setInterval(() => {
      this.checkForUpdates();
    }, this.checkInterval);

    // Verificación inicial y carga del timestamp
    this.initializeTimestamp();
    this.checkForUpdates();
  }

  async checkForUpdates() {
    if (this.isUpdating) return;

    try {
      const response = await fetch("data/tournament_extended.json", {
        method: "HEAD",
        cache: "no-cache",
      });

      if (!response.ok) return;

      const lastModified = response.headers.get("last-modified");

      if (lastModified && lastModified !== this.lastModified) {
        console.log("Cambios detectados en el torneo, actualizando...");
        await this.refreshData();
        this.lastModified = lastModified;
      }
    } catch (error) {
      console.log("Error al verificar actualizaciones:", error);
    }
  }

  async manualRefresh() {
    if (this.isUpdating) return;

    // Protección contra spam de clics
    const now = Date.now();
    const timeSinceLastUpdate = now - this.lastManualUpdate;

    if (timeSinceLastUpdate < this.minUpdateInterval) {
      const remainingTime = Math.ceil(
        (this.minUpdateInterval - timeSinceLastUpdate) / 1000
      );
      this.showError(
        `Espera ${remainingTime} segundos antes de actualizar de nuevo`
      );
      return;
    }

    this.lastManualUpdate = now;
    this.showLoadingState();
    await this.refreshData();
    this.hideLoadingState();
  }

  async refreshData() {
    if (this.isUpdating) return;

    this.isUpdating = true;
    this.showLoadingState();

    try {
      const response = await fetch("data/tournament_extended.json", {
        cache: "no-cache",
      });

      if (!response.ok) {
        throw new Error("Error al cargar datos");
      }

      const newData = await response.json();

      // Actualizar datos globales
      if (window.tournamentData) {
        window.tournamentData = newData;
      }

      // Refrescar la vista actual
      this.refreshCurrentView(newData);

      // Actualizar timestamp
      this.updateLastRefresh(newData.last_updated);

      // Mostrar notificación
      this.showNotification("Datos del torneo actualizados");
    } catch (error) {
      console.error("Error al actualizar datos:", error);
      this.showError("Error al actualizar datos del torneo");
    } finally {
      this.isUpdating = false;
      this.hideLoadingState();
    }
  }

  refreshCurrentView(data) {
    const activeTab = document.querySelector(".tab.active");
    if (!activeTab) return;

    const tabName = activeTab.dataset.tab;

    switch (tabName) {
      case "players":
        this.refreshPlayersView(data);
        break;
      case "matches":
        this.refreshMatchesView(data);
        break;
      case "summary":
        this.refreshSummaryView(data);
        break;
    }
  }

  refreshPlayersView(data) {
    if (window.renderPlayers) {
      window.renderPlayers(data.players || {});
    }
  }

  refreshMatchesView(data) {
    if (window.renderMatches) {
      window.renderMatches(data.matches || []);
    }
  }

  refreshSummaryView(data) {
    if (window.renderSummary) {
      window.renderSummary(data);
    }
  }

  showLoadingState() {
    const refreshBtn = document.getElementById("refreshBtn");
    const indicator = document.getElementById("refreshIndicator");

    if (refreshBtn) {
      refreshBtn.disabled = true;
      refreshBtn.innerHTML =
        '<span class="refresh-icon spinning">🔄</span> Actualizando...';
    }

    if (indicator) {
      indicator.className = "refresh-indicator loading";
      indicator.textContent = "Actualizando...";
    }
  }

  hideLoadingState() {
    const refreshBtn = document.getElementById("refreshBtn");
    const indicator = document.getElementById("refreshIndicator");

    if (refreshBtn) {
      refreshBtn.disabled = false;
      refreshBtn.innerHTML = '<span class="refresh-icon">🔄</span> Actualizar';
    }

    if (indicator) {
      indicator.className = "refresh-indicator";
      indicator.textContent = "";
    }
  }

  async initializeTimestamp() {
    try {
      const response = await fetch("data/tournament_extended.json", {
        cache: "no-cache",
      });

      if (response.ok) {
        const data = await response.json();
        this.updateLastRefresh(data.last_updated);
      }
    } catch (error) {
      console.log("Error al cargar timestamp inicial:", error);
    }
  }

  updateLastRefresh(timestamp) {
    const lastUpdate = document.getElementById("lastUpdate");
    if (lastUpdate && timestamp) {
      const date = new Date(timestamp);
      // Formato español: DD/MM/YYYY, HH:MM:SS
      const options = {
        year: "numeric",
        month: "2-digit",
        day: "2-digit",
        hour: "2-digit",
        minute: "2-digit",
        second: "2-digit",
        timeZone: "Europe/Madrid",
      };
      lastUpdate.textContent = date.toLocaleString("es-ES", options);
    } else if (lastUpdate) {
      lastUpdate.textContent = "Nunca";
    }
  }

  showNotification(message) {
    // Crear notificación temporal
    const notification = document.createElement("div");
    notification.className = "notification success";
    notification.textContent = message;

    document.body.appendChild(notification);

    // Remover después de 3 segundos
    setTimeout(() => {
      if (notification.parentNode) {
        notification.parentNode.removeChild(notification);
      }
    }, 3000);
  }

  showError(message) {
    const notification = document.createElement("div");
    notification.className = "notification error";
    notification.textContent = message;

    document.body.appendChild(notification);

    setTimeout(() => {
      if (notification.parentNode) {
        notification.parentNode.removeChild(notification);
      }
    }, 5000);
  }

  async checkTournamentStatus() {
    const tournamentStatus = document.getElementById("tournamentStatus");
    const refreshBtn = document.getElementById("refreshBtn");

    if (!tournamentStatus) return;

    // Cargar fechas del torneo desde el JSON
    if (!this.tournamentStartDate || !this.tournamentEndDate) {
      try {
        const response = await fetch("data/tournament_extended.json", {
          cache: "no-cache",
        });
        if (response.ok) {
          const data = await response.json();
          // Usar fechas del torneo desde la API de Cuescore
          if (data.tournament_start_date) {
            this.tournamentStartDate = new Date(data.tournament_start_date);
            console.log(
              "Fecha de inicio del torneo:",
              data.tournament_start_date
            );
          }
          if (data.tournament_end_date) {
            this.tournamentEndDate = new Date(data.tournament_end_date);
            console.log(
              "Fecha de finalización del torneo:",
              data.tournament_end_date
            );
          }

          if (!this.tournamentStartDate || !this.tournamentEndDate) {
            console.log("No hay fechas disponibles en los datos");
            return;
          }
        }
      } catch (error) {
        console.log("Error al cargar configuración del torneo:", error);
        return;
      }
    }

    if (!this.tournamentStartDate || !this.tournamentEndDate) return;

    const now = new Date();
    const timeUntilStart = this.tournamentStartDate - now;
    const timeUntilEnd = this.tournamentEndDate - now;

    if (timeUntilEnd <= 0) {
      // Torneo finalizado
      tournamentStatus.innerHTML = `
        <div class="tournament-finished">
          🏁 <strong>Torneo Finalizado</strong> - Los datos se mantienen para consulta
        </div>
      `;
      tournamentStatus.className = "tournament-status finished";

      // Deshabilitar botón de actualización
      if (refreshBtn) {
        refreshBtn.disabled = true;
        refreshBtn.title =
          "El torneo ha finalizado. No se pueden actualizar más datos.";
        refreshBtn.innerHTML =
          '<span class="refresh-icon">🏁</span> Finalizado';
      }

      // Detener verificaciones automáticas
      if (this.updateInterval) {
        clearInterval(this.updateInterval);
      }
    } else if (timeUntilStart > 0) {
      // Torneo aún no ha empezado
      const daysUntilStart = Math.floor(timeUntilStart / (1000 * 60 * 60 * 24));
      const hoursUntilStart = Math.floor(
        (timeUntilStart % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60)
      );

      if (daysUntilStart > 0) {
        tournamentStatus.innerHTML = `
          <div class="tournament-upcoming">
            📅 <strong>Torneo Próximo</strong> - Empieza en ${daysUntilStart} día${
          daysUntilStart > 1 ? "s" : ""
        }
          </div>
        `;
      } else {
        tournamentStatus.innerHTML = `
          <div class="tournament-upcoming">
            📅 <strong>Torneo Próximo</strong> - Empieza en ${hoursUntilStart} hora${
          hoursUntilStart > 1 ? "s" : ""
        }
          </div>
        `;
      }
      tournamentStatus.className = "tournament-status upcoming";
    } else {
      // Torneo en curso
      const daysLeft = Math.floor(timeUntilEnd / (1000 * 60 * 60 * 24));
      const hoursLeft = Math.floor(
        (timeUntilEnd % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60)
      );

      if (daysLeft > 0) {
        tournamentStatus.innerHTML = `
          <div class="tournament-active">
            🏆 <strong>Torneo en Curso</strong> - ${daysLeft} día${
          daysLeft > 1 ? "s" : ""
        } restante${daysLeft > 1 ? "s" : ""}
          </div>
        `;
      } else {
        tournamentStatus.innerHTML = `
          <div class="tournament-active">
            🏆 <strong>Torneo en Curso</strong> - ${hoursLeft} hora${
          hoursLeft > 1 ? "s" : ""
        } restante${hoursLeft > 1 ? "s" : ""}
          </div>
        `;
      }
      tournamentStatus.className = "tournament-status active";
    }
  }

  destroy() {
    if (this.updateInterval) {
      clearInterval(this.updateInterval);
    }
  }
}

// Inicializar cuando el DOM esté listo
document.addEventListener("DOMContentLoaded", () => {
  window.tournamentRefresher = new TournamentRefresher();
});
