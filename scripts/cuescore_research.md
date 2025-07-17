# 🔍 Investigación de la API de Cuescore

## 📋 Información Importante

**Cuescore NO tiene una API pública tradicional**. Los datos se obtienen de diferentes maneras:

### 1. **Endpoints Internos de la Web**

Cuescore usa endpoints internos en su sitio web que devuelven JSON:

```
https://cuescore.com/api/tournament/{ID}
https://cuescore.com/api/tournaments/{ID}
```

### 2. **Estructura de URLs**

- **Torneo individual**: `https://cuescore.com/tournament/{ID}`
- **API interna**: `https://cuescore.com/api/tournament/{ID}`

### 3. **Headers Necesarios**

```javascript
{
  'User-Agent': 'Mozilla/5.0 (compatible; TournamentUpdater/1.0)',
  'Accept': 'application/json',
  'Referer': 'https://cuescore.com/',
  'Origin': 'https://cuescore.com'
}
```

### 4. **Posibles Problemas**

- **CORS**: La API puede bloquear peticiones desde otros dominios
- **Rate Limiting**: Límites de peticiones por IP
- **Autenticación**: Algunos endpoints pueden requerir cookies de sesión
- **Cloudflare**: Protección anti-bot

## 🧪 Estrategias de Prueba

### Opción 1: Simular Navegador

```python
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
    'Accept': 'application/json',
    'Referer': 'https://cuescore.com/',
    'Accept-Language': 'es-ES,es;q=0.9,en;q=0.8'
}
```

### Opción 2: Usar Sesión

```python
import requests

session = requests.Session()
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
})

# Primero visitar la página principal
session.get('https://cuescore.com/')

# Luego hacer la petición a la API
response = session.get(f'https://cuescore.com/api/tournament/{ID}')
```

### Opción 3: Scraping de la Página

Si la API no funciona, podemos extraer datos directamente de la página HTML.

## 🔧 Próximos Pasos

1. **Probar endpoints internos** con headers de navegador
2. **Verificar si necesitamos cookies** de sesión
3. **Comprobar si hay rate limiting**
4. **Considerar scraping** como alternativa

## 📊 URLs a Probar

```
https://cuescore.com/api/tournament/63505243
https://cuescore.com/api/tournaments/63505243
https://api.cuescore.com/tournament/63505243
https://api.cuescore.com/tournaments/63505243
```

## ⚠️ Consideraciones Legales

- Verificar términos de servicio de Cuescore
- Respetar rate limits
- No sobrecargar sus servidores
- Considerar contactarles para acceso oficial
