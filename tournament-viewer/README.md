# 🏆 Visualizador del Torneo Gallego 3ª Categoría

Visualizador web moderno y responsivo para el XXXIII Campeonato Gallego 3ª Categoría con datos extendidos de rankings AGP y actualización automática en tiempo real.

## ✨ Características

- **📊 Datos Extendidos**: Combina información del torneo con rankings y estadísticas de AGP
- **🔄 Actualización Automática**: Sistema de actualización automática cada 10 minutos
- **📱 Responsive Design**: Optimizado para desktop y móvil
- **🎯 Filtros Avanzados**: Búsqueda y filtrado por liga, estado, rango, etc.
- **🏅 Sistema de Rankings**: 5 niveles con badges coloridos
- **💬 Modales Informativos**: Información detallada de jugadores
- **⚡ Tiempo Real**: Detecta cambios automáticamente y refresca la vista

## 🚀 Instalación y Uso

### Opción 1: Servidor Local (Desarrollo)

```bash
# Navegar al directorio
cd tournament-viewer

# Iniciar servidor HTTP
python -m http.server 8000

# Abrir en navegador
open http://localhost:8000
```

### Opción 2: GitHub Pages (Producción)

El proyecto está configurado para desplegarse automáticamente en GitHub Pages.

1. **Configurar GitHub Pages**:

   - Ve a Settings > Pages
   - Source: Deploy from a branch
   - Branch: `gh-pages`
   - Folder: `/ (root)`

2. **Acceder al sitio**:
   - URL: `https://[tu-usuario].github.io/[repo-name]/tournament-viewer/`

## 🔄 Sistema de Actualización Automática

### Componentes

1. **GitHub Actions** (`.github/workflows/update-tournament.yml`)

   - Actualiza datos cada 10 minutos automáticamente
   - Se ejecuta también manualmente desde GitHub
   - Fusiona datos de Cuescore con rankings AGP

2. **Script Python** (`scripts/refresh_tournament.py`)

   - Descarga datos actualizados de Cuescore
   - Mantiene datos AGP existentes
   - Crea backups automáticos

3. **Frontend JavaScript** (`js/refresh.js`)
   - Detecta cambios cada 30 segundos
   - Refresca la vista automáticamente
   - Botón manual de actualización
   - Notificaciones de estado

### Configuración

Editar `scripts/config.py` para personalizar:

```python
# ID del torneo en Cuescore
TOURNAMENT_ID = "xxxiii-campeonato-gallego-3a-categoria-lalin-2025"

# Intervalos de actualización
UPDATE_INTERVAL_MINUTES = 10  # GitHub Actions
CHECK_INTERVAL_SECONDS = 30   # Frontend
```

### Actualización Manual

#### Desde GitHub:

1. Ve a Actions > Update Tournament Data
2. Click en "Run workflow"

#### Desde Terminal:

```bash
cd scripts
python refresh_tournament.py
```

## 📁 Estructura del Proyecto

```
tournament-viewer/
├── index.html              # Página principal
├── css/
│   ├── main.css           # Estilos principales
│   ├── components.css     # Componentes y modales
│   └── mobile.css         # Responsive design
├── js/
│   ├── app.js             # Lógica principal
│   ├── components.js      # Componentes UI
│   ├── filters.js         # Sistema de filtros
│   ├── utils.js           # Utilidades
│   └── refresh.js         # Sistema de actualización
├── data/
│   └── tournament_extended.json  # Datos del torneo
└── README.md
```

## 🎨 Características de la UI

### Sistema de Rankings

- **🥇 Élite**: Oro (top players)
- **🥈 Experto**: Plata (high level)
- **🥉 Avanzado**: Bronce (advanced)
- **🟢 Intermedio**: Verde (intermediate)
- **🔵 Principiante**: Azul (beginner)

### Filtros Disponibles

- **🔍 Búsqueda**: Por nombre de jugador
- **🏆 Liga**: Filtrar por liga específica
- **📊 Estado**: Clasificado/No clasificado
- **⭐ Rango**: Por nivel de ranking
- **🎯 Ronda**: Para partidas
- **⏱️ Estado**: Finalizada/En espera/En juego

### Responsive Design

- **Desktop**: Grid layouts, tooltips, modales
- **Mobile**: Layouts optimizados, sin tooltips, modales adaptados

## 🔧 Desarrollo

### Agregar Nuevas Funcionalidades

1. **Estilos**: Editar archivos en `css/`
2. **Lógica**: Modificar archivos en `js/`
3. **Datos**: Actualizar estructura en `data/`

### Testing

```bash
# Servidor local para desarrollo
python -m http.server 8000

# Verificar actualización automática
# Los cambios se reflejan automáticamente cada 30 segundos
```

## 📊 Datos y Fuentes

- **Cuescore**: Datos del torneo y resultados en tiempo real
- **AGP**: Rankings y estadísticas de jugadores
- **Fusión**: Sistema híbrido que mantiene lo mejor de ambas fuentes

## 🤝 Contribuir

1. Fork el proyecto
2. Crear rama para feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crear Pull Request

## 📝 Licencia

Este proyecto es de uso interno para la Liga de Billar Gallega.

---

**Desarrollado para el XXXIII Campeonato Gallego 3ª Categoría - Lalín 2025** 🏆
