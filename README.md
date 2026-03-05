# 🏆 MMJ Emirates Cup — Streamlit App

Aplicación interactiva del torneo **MMJ Emirates Cup** con 30 equipos, sorteos, fase de grupos y tabla de goleadores.

---

## 🚀 Cómo publicar en GitHub + Streamlit Cloud (paso a paso)

### Paso 1 — Crear cuenta en GitHub
1. Ve a [github.com](https://github.com) y crea una cuenta gratuita.

### Paso 2 — Crear un nuevo repositorio
1. Click en el botón verde **"New"** (o **"+"** → New repository).
2. Dale un nombre, por ejemplo: `mmj-emirates-cup`
3. Márcalo como **Public**.
4. Click en **"Create repository"**.

### Paso 3 — Subir los archivos
Tienes dos opciones:

**Opción A — Desde la web (más fácil):**
1. En tu repositorio, click en **"uploading an existing file"**.
2. Arrastra y suelta estos 4 archivos/carpetas:
   - `app.py`
   - `data.py`
   - `engine.py`
   - `requirements.txt`
   - Carpeta `.streamlit/` con `config.toml`
3. Click **"Commit changes"**.

**Opción B — Con Git (terminal):**
```bash
git clone https://github.com/TU_USUARIO/mmj-emirates-cup.git
# Copia los archivos dentro de esa carpeta
cd mmj-emirates-cup
git add .
git commit -m "MMJ Emirates Cup - Initial commit"
git push origin main
```

### Paso 4 — Publicar en Streamlit Cloud
1. Ve a [share.streamlit.io](https://share.streamlit.io) e inicia sesión con tu cuenta de GitHub.
2. Click en **"New app"**.
3. Selecciona tu repositorio `mmj-emirates-cup`.
4. En **"Main file path"** escribe: `app.py`
5. Click en **"Deploy!"**

¡Listo! En 1-2 minutos tendrás un link público como:
`https://TU_USUARIO-mmj-emirates-cup-app-XXXXX.streamlit.app`

---

## 📁 Estructura del proyecto

```
mmj-emirates-cup/
├── app.py              ← App principal de Streamlit
├── data.py             ← Datos de equipos y jugadores
├── engine.py           ← Motor del torneo y simulación
├── requirements.txt    ← Dependencias Python
├── .streamlit/
│   └── config.toml     ← Tema oscuro dorado
└── README.md           ← Este archivo
```

---

## 🏟 Formato del Torneo

| Ronda | Descripción |
|-------|-------------|
| **Ronda 1** | Llaves M (Pos28 vs Pos29) y N (Pos27 vs Pos30) |
| **Ronda 2** | Llaves E–L: Pos13–20 (local) vs Pos21–26 + ganadores R1 |
| **Fase de Grupos** | 4 grupos (A–D) con sorteo, todos contra todos, top 2 clasifican |
| **Ronda 4** | Sorteo 1º vs 2º de grupos, Llaves A–D |
| **Cuartos** | Pos1–4 entran como locales vs ganadores R4 |
| **Semifinales** | W-A vs W-C · W-B vs W-D |
| **Final** | 🏆 |

---

## ⚽ Funcionalidades

- ✅ Simulación aleatoria de todos los partidos
- ✅ Sorteos interactivos (Fase de Grupos y Ronda 4)
- ✅ Goleadores por partido con minuto de gol
- ✅ Tabla de artilleros completa con podio
- ✅ Estadísticas de goles por equipo (gráfico)
- ✅ Tabla de clasificación de grupos
- ✅ Estado del torneo en sidebar
- ✅ Tema oscuro dorado

---

## 🖥 Correr localmente

```bash
pip install streamlit pandas
streamlit run app.py
```
