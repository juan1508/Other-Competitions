# 🏆 MMJ Emirates Cup — Registro de Resultados

App Streamlit para registrar resultados reales, goleadores y llevar el control completo del torneo MMJ Emirates Cup con 30 equipos.

---

## 🚀 Publicar en GitHub + Streamlit Cloud

### Paso 1 — Crear cuenta GitHub
Ve a [github.com](https://github.com) y crea una cuenta gratuita.

### Paso 2 — Nuevo repositorio
1. Click en **"New"** → Dale nombre: `mmj-emirates-cup`
2. Márcalo **Public** → **"Create repository"**

### Paso 3 — Subir archivos
1. En el repositorio click en **"uploading an existing file"**
2. Sube estos archivos:
   - `app.py`
   - `data.py`
   - `state.py`
   - `requirements.txt`
3. Crea la carpeta `.streamlit/` y sube `config.toml` dentro
4. Click **"Commit changes"**

> 💡 Para la carpeta `.streamlit`, en GitHub web puedes escribir `.streamlit/config.toml` directamente en el campo del nombre del archivo.

### Paso 4 — Deploy en Streamlit Cloud
1. Ve a [share.streamlit.io](https://share.streamlit.io)
2. Login con GitHub
3. Click **"New app"**
4. Selecciona tu repo → Main file: `app.py`
5. Click **"Deploy!"**

¡Listo! Tendrás un link como:
`https://tu-usuario-mmj-emirates-cup-app-xxxxx.streamlit.app`

---

## 📁 Estructura

```
mmj-emirates-cup/
├── app.py                  ← App principal
├── data.py                 ← Equipos, jugadores, logos
├── state.py                ← Motor del torneo + persistencia JSON
├── requirements.txt
├── tournament_state.json   ← Se crea automáticamente al registrar datos
└── .streamlit/
    └── config.toml         ← Tema oscuro dorado
```

---

## ⚽ Cómo usar la app

1. **Clasificación** — Ver los 30 equipos con sus escudos y roles
2. **Ronda 1** — Registra el resultado de Llave M y Llave N, selecciona los goleadores con minuto
3. Confirma → se desbloquea **Ronda 2**
4. Registra R2 → confirma → realiza el **Sorteo de Grupos** (manual o aleatorio)
5. **Fase de Grupos** — Registra los 6 partidos de cada grupo, la tabla se actualiza en vivo
6. Confirma → **Sorteo R4** → registra R4
7. **Cuartos → Semifinales → Final**
8. **Goleadores** — Tabla en tiempo real con podio 🥇🥈🥉 y escudos

---

## 💾 Persistencia

Los resultados se guardan en `tournament_state.json` automáticamente. Si usas Streamlit Cloud, los datos persisten mientras la app esté activa en la misma sesión. Para persistencia permanente en la nube, considera usar **Streamlit Community Cloud + GitHub** haciendo commit del JSON, o migrar a una base de datos SQLite.

---

## 🖥 Correr localmente

```bash
pip install streamlit pandas
streamlit run app.py
```
