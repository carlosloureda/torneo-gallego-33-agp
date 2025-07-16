# Tournament Viewer - Vista Modular

## 📁 Estructura del Proyecto

```
tournament-viewer/
├── index.html              # Archivo HTML principal
├── css/
│   ├── main.css           # Estilos generales y layout
│   ├── components.css     # Estilos de componentes específicos
│   └── mobile.css         # Estilos responsivos para móviles
├── js/
│   ├── utils.js           # Funciones utilitarias
│   ├── components.js      # Componentes de renderizado
│   ├── filters.js         # Lógica de filtrado
│   └── app.js             # Aplicación principal
├── data/
│   └── tournament_extended.json  # Datos del torneo
└── README.md              # Este archivo
```

## 🚀 Cómo usar

1. **Servidor local**: Ejecuta un servidor HTTP en la carpeta raíz:

   ```bash
   cd tournament-viewer
   python -m http.server 8000
   ```

2. **Abrir en navegador**: Ve a `http://localhost:8000`

## 🎯 Características

### ✅ Implementadas

- **Estructura modular**: Código separado en archivos específicos
- **Responsive design**: Optimizado para móviles y desktop
- **Sistema de rangos**: Élite, Experto, Avanzado, Intermedio, Principiante
- **Filtros avanzados**: Por liga, estado, rango y búsqueda
- **Tooltips y modales**: Información detallada de jugadores
- **Estadísticas**: Vista general y por liga

### 📱 Responsive

- Diseño adaptativo para móviles
- Grid layouts que se ajustan automáticamente
- Tamaños de fuente optimizados
- Navegación táctil mejorada

## 🔧 Mantenimiento

### Agregar nuevos componentes

1. Crea el componente en `js/components.js`
2. Agrega estilos en `css/components.css`
3. Importa en `app.js` si es necesario

### Modificar filtros

1. Edita la lógica en `js/filters.js`
2. Actualiza las opciones en `js/app.js`

### Cambiar estilos

- **Generales**: `css/main.css`
- **Componentes**: `css/components.css`
- **Móvil**: `css/mobile.css`

## 📊 Datos

El archivo `data/tournament_extended.json` contiene:

- Información de jugadores con rankings
- Datos de partidas del torneo
- Estadísticas por liga
- Información de clasificación

## 🎨 Sistema de Rangos

- **👑 Élite**: 120+ puntos, posición 1-3
- **🥇 Experto**: 100+ puntos, posición 1-8
- **🥈 Avanzado**: 80+ puntos, posición 1-15
- **🥉 Intermedio**: 60+ puntos, posición 1-25
- **⭐ Principiante**: Resto de jugadores

## 🔄 Próximas mejoras

- [ ] Exportar datos a CSV/Excel
- [ ] Gráficos estadísticos
- [ ] Modo oscuro
- [ ] Búsqueda avanzada
- [ ] Comparador de jugadores
