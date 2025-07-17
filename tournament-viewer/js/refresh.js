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
      `;

      header.appendChild(refreshStatus);
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

    // Verificación inicial
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

  updateLastRefresh(timestamp) {
    const lastUpdate = document.getElementById("lastUpdate");
    if (lastUpdate && timestamp) {
      const date = new Date(timestamp);
      lastUpdate.textContent = date.toLocaleString("es-ES");
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
