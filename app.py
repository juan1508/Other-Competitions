# app.py — MMJ Emirates Cup — Diseño oficial con logo y colores de la copa
import streamlit as st
import pandas as pd
import random
import base64, os
from data import TEAMS, TEAM_ORDER, get_by_pos, get_team
from state import (
    load, save, reset, enrich,
    build_r2, build_groups, build_r4, build_qf, build_sf, build_final,
    recalc_group_standing, get_group_ranking, collect_all_scorers,
    GROUP_SEEDS
)

# ──────────────── CONFIG ────────────────────────────────────────────
st.set_page_config(page_title="MMJ Emirates Cup", page_icon="🏆", layout="wide",
                   initial_sidebar_state="expanded")

# ── Logo base64 ──
def get_logo_b64():
    path = os.path.join(os.path.dirname(__file__), "COPA.png")
    if os.path.exists(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return ""

LOGO_B64 = get_logo_b64()
LOGO_HTML = f'<img src="data:image/png;base64,{LOGO_B64}" style="width:{{w}}px;object-fit:contain;display:block;margin:0 auto">' if LOGO_B64 else "🏆"

def logo(w=120):
    if LOGO_B64:
        return f'<img src="data:image/png;base64,{LOGO_B64}" style="width:{w}px;object-fit:contain;display:block;margin:0 auto">'
    return f'<div style="font-size:{w//20}rem;text-align:center">🏆</div>'

# ──────────────── CSS — Purple / Silver / Black ──────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Barlow+Condensed:ital,wght@0,400;0,600;0,700;1,400&family=Barlow:wght@300;400;500&display=swap');

/* ── Base ── */
html,[class*="css"]{font-family:'Barlow',sans-serif;}
.main .block-container{padding-top:24px;}

/* ── Sidebar ── */
section[data-testid="stSidebar"]{
    background: linear-gradient(180deg,#0e0818 0%,#110d1e 60%,#0a0612 100%) !important;
    border-right: 1px solid rgba(123,63,196,0.45) !important;
}
section[data-testid="stSidebar"] .stRadio label{
    font-family:'Barlow Condensed',sans-serif;font-weight:600;letter-spacing:1px;font-size:.88rem;
}

/* ── Purple palette ── */
/* --mmj-purple:  #7B3FC4  (primary)       */
/* --mmj-violet:  #9B5EE0  (lighter)       */
/* --mmj-silver:  #C0C8D8  (silver)        */
/* --mmj-dark:    #08060f  (bg)            */
/* --mmj-card:    #110d1e  (card bg)       */
/* --mmj-border:  #2a1f44  (border)        */
/* --mmj-red:     #cc2233  (logo red gem)  */
/* --mmj-green:   #1a9944  (logo green gem)*/

/* ── Section title ── */
.sec-title{
    font-family:'Bebas Neue',sans-serif;
    font-size:1.6rem;letter-spacing:5px;
    background:linear-gradient(90deg,#9B5EE0,#C0C8D8);
    -webkit-background-clip:text;-webkit-text-fill-color:transparent;
    background-clip:text;margin-bottom:2px;
}
.badge{
    display:inline-block;
    background:rgba(123,63,196,.18);
    border:1px solid rgba(123,63,196,.5);
    border-radius:4px;padding:2px 12px;
    font-family:'Barlow Condensed',sans-serif;
    font-size:.75rem;letter-spacing:2px;
    color:#9B5EE0;text-transform:uppercase;margin-bottom:14px;
}

/* ── Divider ── */
.purple-line{
    height:2px;
    background:linear-gradient(to right,transparent,#7B3FC4,#C0C8D8,#7B3FC4,transparent);
    margin:10px 0 20px 0;
}
.silver-line{
    height:1px;
    background:linear-gradient(to right,transparent,#C0C8D8,transparent);
    margin:8px 0 16px 0;
}

/* ── Cup title (sidebar) ── */
.cup-title-main{
    font-family:'Bebas Neue',sans-serif;
    font-size:1.15rem;letter-spacing:5px;
    background:linear-gradient(135deg,#9B5EE0,#C0C8D8,#7B3FC4);
    -webkit-background-clip:text;-webkit-text-fill-color:transparent;
    background-clip:text;text-align:center;margin-top:6px;
}

/* ── Match box ── */
.match-box{
    background:linear-gradient(135deg,#110d1e,#0e0a1a);
    border:1px solid #2a1f44;border-radius:12px;
    padding:14px 16px;margin-bottom:10px;
    transition:border-color .2s,box-shadow .2s;
}
.match-box:hover{
    border-color:rgba(123,63,196,.7);
    box-shadow:0 4px 20px rgba(123,63,196,.15);
}
.match-box-played{
    border-left:3px solid #7B3FC4;
}
.mlabel{
    font-family:'Bebas Neue',sans-serif;letter-spacing:3px;
    color:#9B5EE0;font-size:.82rem;margin-bottom:8px;
    text-transform:uppercase;
}
.mteam{
    display:flex;align-items:center;gap:10px;
    font-family:'Barlow Condensed',sans-serif;font-weight:700;
    font-size:1rem;padding:5px 0;
}
.mscore{
    font-family:'Bebas Neue',sans-serif;font-size:1.7rem;
    min-width:30px;text-align:center;color:#C0C8D8;
}
.win-score{
    color:#7B3FC4 !important;
    text-shadow:0 0 10px rgba(123,63,196,.5);
}
.win-name{color:#9B5EE0;}
.pending-score{color:#2a1f44;}

/* ── Scorer chips ── */
.scorer-chip{
    display:inline-block;
    background:rgba(123,63,196,.12);
    border:1px solid rgba(123,63,196,.3);
    border-radius:5px;padding:2px 8px;
    font-size:.72rem;margin:2px;color:#a090c8;
}

/* ── Info box ── */
.info-box{
    background:rgba(123,63,196,.08);
    border:1px solid rgba(123,63,196,.3);
    border-radius:8px;padding:10px 14px;
    font-size:.82rem;color:#b090e0;
    margin-bottom:14px;line-height:1.6;
}

/* ── Champion banner ── */
.champ-box{
    background:linear-gradient(135deg,rgba(123,63,196,.2),rgba(123,63,196,.05));
    border:2px solid #7B3FC4;border-radius:16px;
    padding:32px;text-align:center;
    margin:20px auto;max-width:380px;
    box-shadow:0 0 40px rgba(123,63,196,.3);
}
.champ-title{
    font-family:'Bebas Neue',sans-serif;font-size:1.3rem;
    letter-spacing:5px;
    background:linear-gradient(90deg,#9B5EE0,#C0C8D8);
    -webkit-background-clip:text;-webkit-text-fill-color:transparent;
    background-clip:text;margin-bottom:10px;
}
.champ-name{
    font-family:'Bebas Neue',sans-serif;font-size:2.2rem;
    letter-spacing:3px;color:#e8e8f0;margin-top:8px;
}

/* ── Group headers ── */
.group-a-hdr{color:#cc2233;font-family:'Bebas Neue',sans-serif;letter-spacing:3px;font-size:1.15rem;}
.group-b-hdr{color:#9B5EE0;font-family:'Bebas Neue',sans-serif;letter-spacing:3px;font-size:1.15rem;}
.group-c-hdr{color:#C0C8D8;font-family:'Bebas Neue',sans-serif;letter-spacing:3px;font-size:1.15rem;}
.group-d-hdr{color:#1a9944;font-family:'Bebas Neue',sans-serif;letter-spacing:3px;font-size:1.15rem;}

/* ── Buttons ── */
div.stButton>button[kind="primary"]{
    background:linear-gradient(135deg,#7B3FC4,#5c2a99);
    border:1px solid #9B5EE0;color:#fff;
    font-family:'Barlow Condensed',sans-serif;font-weight:700;letter-spacing:2px;
    transition:all .2s;
}
div.stButton>button[kind="primary"]:hover{
    background:linear-gradient(135deg,#9B5EE0,#7B3FC4);
    box-shadow:0 4px 20px rgba(123,63,196,.5);transform:translateY(-1px);
}

/* ── Number inputs ── */
div[data-testid="stNumberInput"] input{
    font-family:'Bebas Neue',sans-serif;font-size:1.3rem;text-align:center;
}

/* ── Sidebar progress ── */
.prog-done{color:#7B3FC4;}
.prog-wait{color:#3a2a55;}

/* ── Scorers podium ── */
.pod-card{
    background:linear-gradient(135deg,#110d1e,#0e0a1a);
    border:1px solid #2a1f44;border-radius:12px;
    padding:16px;text-align:center;
    transition:border-color .2s;
}
.pod-card:hover{border-color:rgba(123,63,196,.6);}
.pod-goals{
    font-family:'Bebas Neue',sans-serif;font-size:2.5rem;
    background:linear-gradient(135deg,#9B5EE0,#C0C8D8);
    -webkit-background-clip:text;-webkit-text-fill-color:transparent;
    background-clip:text;
}

/* ── Tab styling ── */
.stTabs [data-baseweb="tab"]{
    font-family:'Barlow Condensed',sans-serif;font-weight:700;letter-spacing:2px;
}
.stTabs [aria-selected="true"]{
    color:#9B5EE0 !important;border-bottom-color:#7B3FC4 !important;
}

/* ── Dataframe header ── */
.stDataFrame thead tr th{
    background:#1a1030 !important;color:#9B5EE0 !important;
    font-family:'Barlow Condensed',sans-serif;letter-spacing:1px;
}
</style>""", unsafe_allow_html=True)

# ──────────────── SESSION STATE ──────────────────────────────────────
if "ts" not in st.session_state:
    st.session_state.ts = load()
ts = st.session_state.ts

def persist():
    save(ts)

# ──────────────── SIDEBAR ────────────────────────────────────────────
with st.sidebar:
    # LOGO
    st.markdown(logo(160), unsafe_allow_html=True)
    st.markdown('<div class="cup-title-main">MMJ Emirates Cup</div>', unsafe_allow_html=True)
    st.markdown('<div class="purple-line"></div>', unsafe_allow_html=True)

    page = st.radio("", [
        "🏟 Clasificación",
        "⚡ Ronda 1",
        "🔥 Ronda 2",
        "🔵 Fase de Grupos",
        "🏅 Ronda 4",
        "⚡ Cuartos de Final",
        "🌟 Semifinales",
        "🏆 Final",
        "⚽ Goleadores",
        "🛡 Equipos",
    ], label_visibility="collapsed")

    st.markdown('<div class="purple-line"></div>', unsafe_allow_html=True)
    st.markdown("**Progreso**")
    checks = [
        ("R1", ts["r1"]["done"]),
        ("R2", ts["r2"]["done"]),
        ("Sorteo Grupos", ts["groups"]["drawn"]),
        ("Grupos", ts["groups"]["done"]),
        ("Sorteo R4", ts["r4"]["drawn"]),
        ("R4", ts["r4"]["done"]),
        ("Cuartos", ts["qf"]["done"]),
        ("Semis", ts["sf"]["done"]),
        ("Final", ts["final"]["done"]),
    ]
    for lbl, done in checks:
        color = "#7B3FC4" if done else "#2a1f44"
        icon = "●" if done else "○"
        st.markdown(f"<span style='color:{color};font-size:.85rem'>{icon} {lbl}</span>", unsafe_allow_html=True)

    if ts["champion_code"]:
        st.markdown('<div class="purple-line"></div>', unsafe_allow_html=True)
        champ = TEAMS[ts["champion_code"]]
        st.image(champ["logo"], width=48)
        st.markdown(f"<span style='color:#9B5EE0;font-family:Bebas Neue,sans-serif;letter-spacing:2px;font-size:.95rem'>🏆 {champ['name']}</span>", unsafe_allow_html=True)

    st.markdown('<div class="purple-line"></div>', unsafe_allow_html=True)
    if st.button("🔄 Reiniciar Torneo", type="secondary"):
        st.session_state.ts = reset()
        st.rerun()

# ──────────────── HELPERS ────────────────────────────────────────────
def sec(title, badge=""):
    # Page header with logo watermark
    hc1, hc2 = st.columns([6, 1])
    with hc1:
        st.markdown(f'<div class="sec-title">{title}</div>', unsafe_allow_html=True)
        if badge:
            st.markdown(f'<div class="badge">{badge}</div>', unsafe_allow_html=True)
    with hc2:
        if LOGO_B64:
            st.markdown(logo(70), unsafe_allow_html=True)
    st.markdown('<div class="purple-line"></div>', unsafe_allow_html=True)

def info(txt):
    st.markdown(f'<div class="info-box">ℹ️ &nbsp;{txt}</div>', unsafe_allow_html=True)

def show_match_result(m):
    me = enrich(m)
    hs = m["home_score"]
    as_ = m["away_score"]
    played = m["played"]
    hw = played and hs > as_
    aw = played and as_ > hs

    h_sc = "win-score" if hw else ("pending-score" if not played else "")
    a_sc = "win-score" if aw else ("pending-score" if not played else "")
    h_n  = "win-name"  if hw else ""
    a_n  = "win-name"  if aw else ""
    h_st = str(hs) if played else "—"
    a_st = str(as_) if played else "—"

    scorers_html = ""
    if played and m.get("scorers"):
        chips = "".join(
            f"<span class='scorer-chip'>⚽ {s['minute']}' {s['player']}</span>"
            for s in sorted(m["scorers"], key=lambda x: x["minute"])
        )
        scorers_html = f"<div style='margin-top:8px;line-height:2'>{chips}</div>"

    played_cls = "match-box-played" if played else ""
    st.markdown(f"""
    <div class="match-box {played_cls}">
      <div class="mlabel">{m['label']}</div>
      <div style="display:flex;align-items:center;gap:10px;padding:4px 0">
        <img src="{me['home']['logo']}" width="34" style="object-fit:contain;flex-shrink:0">
        <span class="mteam {h_n}" style="flex:1">{me['home']['name']}</span>
        <span class="mscore {h_sc}">{h_st}</span>
      </div>
      <div style="height:1px;background:#2a1f44;margin:2px 0"></div>
      <div style="display:flex;align-items:center;gap:10px;padding:4px 0">
        <img src="{me['away']['logo']}" width="34" style="object-fit:contain;flex-shrink:0">
        <span class="mteam {a_n}" style="flex:1">{me['away']['name']}</span>
        <span class="mscore {a_sc}">{a_st}</span>
      </div>
      {scorers_html}
    </div>""", unsafe_allow_html=True)

def match_entry_form(match, match_key, allow_draw=False):
    me = enrich(match)
    home = me["home"]
    away = me["away"]
    played = match["played"]
    icon = "✅" if played else "📋"

    with st.expander(f"{icon}  {match['label']}  ·  {home['name']} vs {away['name']}", expanded=not played):
        # Header with logos
        lc, mc, rc = st.columns([3, 1, 3])
        with lc:
            st.image(home["logo"], width=60)
            st.markdown(f"<div style='font-family:Barlow Condensed,sans-serif;font-weight:700;font-size:.95rem'>{home['name']}</div>", unsafe_allow_html=True)
            st.markdown(f"<div style='font-size:.72rem;color:#6b5a8a'>LOCAL</div>", unsafe_allow_html=True)
        with mc:
            st.markdown("<div style='text-align:center;font-family:Bebas Neue,sans-serif;font-size:1.4rem;color:#3a2a55;padding-top:14px'>VS</div>", unsafe_allow_html=True)
        with rc:
            st.image(away["logo"], width=60)
            st.markdown(f"<div style='font-family:Barlow Condensed,sans-serif;font-weight:700;font-size:.95rem'>{away['name']}</div>", unsafe_allow_html=True)
            st.markdown(f"<div style='font-size:.72rem;color:#6b5a8a'>VISITANTE</div>", unsafe_allow_html=True)

        st.markdown('<div class="silver-line"></div>', unsafe_allow_html=True)

        # Score
        sc1, sc2, sc3 = st.columns([5, 2, 5])
        with sc1:
            hs = st.number_input("⚽ Local", min_value=0, max_value=20,
                                 value=match["home_score"] if match["home_score"] is not None else 0,
                                 key=f"{match_key}_hs", label_visibility="visible")
        with sc2:
            st.markdown("<div style='text-align:center;padding-top:26px;font-family:Bebas Neue,sans-serif;font-size:1.6rem;color:#7B3FC4'>—</div>", unsafe_allow_html=True)
        with sc3:
            as_ = st.number_input("⚽ Visitante", min_value=0, max_value=20,
                                  value=match["away_score"] if match["away_score"] is not None else 0,
                                  key=f"{match_key}_as", label_visibility="visible")

        if not allow_draw and hs == as_:
            st.markdown("<div style='color:#cc2233;font-size:.8rem;padding:4px 0'>⚠️ Partido eliminatorio — no puede terminar en empate.</div>", unsafe_allow_html=True)

        # Scorers
        st.markdown('<div class="silver-line"></div>', unsafe_allow_html=True)
        st.markdown("**⚽ Goleadores**")
        total = hs + as_
        all_players = [(home["code"], p) for p in home["players"]] + \
                      [(away["code"], p) for p in away["players"]]
        player_opts = [f"{TEAMS[c]['name']} — {p}" for c, p in all_players]
        player_map = {f"{TEAMS[c]['name']} — {p}": (c, p) for c, p in all_players}
        existing = match.get("scorers", [])
        scorers_out = []

        if total > 0:
            for i in range(total):
                gc1, gc2 = st.columns([4, 1])
                def_p = player_opts[0]
                def_m = 1
                if i < len(existing):
                    es = existing[i]
                    cand = f"{TEAMS[es['team_code']]['name']} — {es['player']}"
                    if cand in player_map: def_p = cand
                    def_m = es.get("minute", 1)
                with gc1:
                    sel = st.selectbox(f"Gol #{i+1}", player_opts,
                                       index=player_opts.index(def_p) if def_p in player_opts else 0,
                                       key=f"{match_key}_sc{i}_p")
                with gc2:
                    minute = st.number_input(f"Min", min_value=1, max_value=120,
                                             value=def_m, key=f"{match_key}_sc{i}_m")
                code, pname = player_map[sel]
                scorers_out.append({"player": pname, "team_code": code, "minute": minute})
        else:
            st.caption("Sin goles registrados.")

        can_save = allow_draw or hs != as_
        if st.button(f"💾 Guardar resultado", key=f"{match_key}_save",
                     disabled=not can_save, type="primary"):
            match["home_score"] = int(hs)
            match["away_score"] = int(as_)
            match["scorers"]    = scorers_out
            match["played"]     = True
            match["winner_code"] = home["code"] if hs > as_ else (away["code"] if as_ > hs else None)
            persist()
            st.success(f"✅  {home['name']} {hs} – {as_} {away['name']}")
            st.rerun()

def render_matches_grid(matches, cols=2):
    if not matches:
        st.info("Los partidos aparecerán aquí.")
        return
    columns = st.columns(cols)
    for i, m in enumerate(matches):
        with columns[i % cols]:
            show_match_result(m)

# ═══════════════════════════════════════════════════════════════════════
# PAGES
# ═══════════════════════════════════════════════════════════════════════

# ── CLASIFICACIÓN ─────────────────────────────────────────────────────
if page == "🏟 Clasificación":
    sec("🏟 Clasificación Inicial", "30 Equipos — Season 2025")
    info("La posición define el camino en el torneo. Top 4 entran directo a Cuartos como locales.")

    rows = []
    for i, code in enumerate(TEAM_ORDER):
        pos = i + 1
        if pos <= 4:   role = "⭐ Cuartos Directo"
        elif pos <= 12: role = "🔵 Fase de Grupos"
        elif pos <= 20: role = "🔸 Ronda 2 — Local"
        elif pos <= 26: role = "⚪ Ronda 2 — Visitante"
        else:           role = "⚡ Ronda 1"
        rows.append({"#": pos, "Equipo": TEAMS[code]["name"], "Código": code, "Rol": role})

    df = pd.DataFrame(rows)
    st.dataframe(df, use_container_width=True, hide_index=True,
                 column_config={"#": st.column_config.NumberColumn(width="small")})

    st.markdown("### 🛡 Escudos")
    gcols = st.columns(6)
    for i, code in enumerate(TEAM_ORDER):
        with gcols[i % 6]:
            st.image(TEAMS[code]["logo"], width=58)
            st.markdown(f"<div style='font-size:.65rem;text-align:center;color:#6b5a8a'>#{i+1} {code}</div>", unsafe_allow_html=True)

# ── RONDA 1 ───────────────────────────────────────────────────────────
elif page == "⚡ Ronda 1":
    sec("⚡ Ronda 1", "Llaves M y N")
    info("Pos 28 vs Pos 29 → Llave M &nbsp;·&nbsp; Pos 27 vs Pos 30 → Llave N — Partido único, sin empates.")

    matches = ts["r1"]["matches"]
    all_played = all(m["played"] for m in matches)

    for i, m in enumerate(matches):
        match_entry_form(m, f"r1_{i}", allow_draw=False)

    st.markdown('<div class="silver-line"></div>', unsafe_allow_html=True)
    st.markdown("### Resultados")
    render_matches_grid(matches, cols=2)

    if all_played and not ts["r1"]["done"]:
        if st.button("✅ Confirmar Ronda 1 y avanzar →", type="primary"):
            ts["r1"]["done"] = True
            ts["r2"]["matches"] = build_r2(matches)
            persist()
            st.success("Ronda 1 completada.")
            st.rerun()
    if ts["r1"]["done"]:
        st.success("✅ Ronda 1 finalizada — clasificados listos")

# ── RONDA 2 ───────────────────────────────────────────────────────────
elif page == "🔥 Ronda 2":
    sec("🔥 Ronda 2", "Llaves E a L")
    if not ts["r1"]["done"]:
        st.warning("⏳ Completa y confirma la Ronda 1 primero.")
        st.stop()
    info("Pos 13–20 son locales. Visitantes: Pos 21–26 + ganadores R1. Sin empates.")

    matches = ts["r2"]["matches"]
    all_played = all(m["played"] for m in matches)

    for i, m in enumerate(matches):
        match_entry_form(m, f"r2_{i}", allow_draw=False)

    st.markdown('<div class="silver-line"></div>', unsafe_allow_html=True)
    st.markdown("### Resultados")
    render_matches_grid(matches, cols=2)

    if all_played and not ts["r2"]["done"]:
        if st.button("✅ Confirmar Ronda 2 y avanzar →", type="primary"):
            ts["r2"]["done"] = True
            persist()
            st.success("Ronda 2 completada.")
            st.rerun()
    if ts["r2"]["done"]:
        st.success("✅ Ronda 2 finalizada")

# ── FASE DE GRUPOS ────────────────────────────────────────────────────
elif page == "🔵 Fase de Grupos":
    sec("🔵 Fase de Grupos", "Ronda 3")
    if not ts["r2"]["done"]:
        st.warning("⏳ Completa la Ronda 2 primero.")
        st.stop()

    if not ts["groups"]["drawn"]:
        info("Asigna los 8 clasificados de R2 en 4 grupos (2 por grupo). Las cabezas son fijas.")
        st.markdown("### Cabezas de Grupo")
        group_colors = {"A":"#cc2233","B":"#9B5EE0","C":"#C0C8D8","D":"#1a9944"}
        sc = st.columns(4)
        for gi, g in enumerate("ABCD"):
            with sc[gi]:
                st.markdown(f"<div style='color:{group_colors[g]};font-family:Bebas Neue,sans-serif;font-size:1rem;letter-spacing:3px'>GRUPO {g}</div>", unsafe_allow_html=True)
                for code in GROUP_SEEDS[g]:
                    c1, c2 = st.columns([1,2])
                    with c1: st.image(TEAMS[code]["logo"], width=36)
                    with c2: st.caption(TEAMS[code]["name"])

        st.markdown("### Asignar Clasificados de R2")
        r2_winners = [m["winner_code"] for m in ts["r2"]["matches"]]
        w_opts = [f"{code} — {TEAMS[code]['name']}" for code in r2_winners]
        w_map  = {f"{code} — {TEAMS[code]['name']}": code for code in r2_winners}

        assignment = {}
        all_sel = []
        draw_valid = True
        dc = st.columns(4)
        for gi, g in enumerate("ABCD"):
            with dc[gi]:
                st.markdown(f"<span style='color:{group_colors[g]};font-family:Bebas Neue,sans-serif'>GRUPO {g}</span>", unsafe_allow_html=True)
                s1 = st.selectbox(f"Equipo 1 — G{g}", w_opts, key=f"draw_{g}_1")
                s2 = st.selectbox(f"Equipo 2 — G{g}", w_opts, key=f"draw_{g}_2")
                assignment[g] = [w_map[s1], w_map[s2]]
                all_sel += [w_map[s1], w_map[s2]]

        if len(set(all_sel)) < 8:
            st.error("⚠️ Cada equipo solo puede estar en un grupo.")
            draw_valid = False

        b1, b2 = st.columns(2)
        with b1:
            if st.button("🎲 Sorteo Aleatorio"):
                sh = r2_winners[:]
                random.shuffle(sh)
                st.session_state["_rand"] = sh
                st.info("Sugerencia generada. Revisa los selectores y confirma.")
        with b2:
            if st.button("✅ Confirmar Sorteo", type="primary", disabled=not draw_valid):
                built = build_groups(assignment)
                for g in "ABCD":
                    ts["groups"][g] = built[g]
                ts["groups"]["assignment"] = assignment
                ts["groups"]["drawn"] = True
                persist()
                st.rerun()
    else:
        if not ts["groups"]["done"]:
            st.markdown("### Registra los partidos de cada grupo")

        group_colors = {"A":"#cc2233","B":"#9B5EE0","C":"#C0C8D8","D":"#1a9944"}
        tabs = st.tabs(["🔴 Grupo A","🟣 Grupo B","⚪ Grupo C","🟢 Grupo D"])
        hdr_cls = ["group-a-hdr","group-b-hdr","group-c-hdr","group-d-hdr"]

        for gi, g in enumerate("ABCD"):
            with tabs[gi]:
                grp = ts["groups"][g]
                st.markdown(f'<div class="{hdr_cls[gi]}">GRUPO {g}</div>', unsafe_allow_html=True)

                for mi, m in enumerate(grp["matches"]):
                    match_entry_form(m, f"g{g}_{mi}", allow_draw=True)

                st.markdown("#### Tabla de Posiciones")
                standing = recalc_group_standing(grp)
                ranking = sorted(standing.items(),
                                 key=lambda x: (-x[1]["pts"],-(x[1]["gf"]-x[1]["ga"]),-x[1]["gf"]))
                rows = []
                for ri, (code, s) in enumerate(ranking):
                    rows.append({"#": ri+1, "Equipo": TEAMS[code]["name"],
                                 "PJ":s["pj"],"G":s["w"],"E":s["d"],"P":s["l"],
                                 "GF":s["gf"],"GA":s["ga"],"DG":s["gf"]-s["ga"],"Pts":s["pts"]})
                st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

                st.markdown("#### Partidos")
                render_matches_grid(grp["matches"], cols=2)

        all_done = all(all(m["played"] for m in ts["groups"][g]["matches"]) for g in "ABCD")
        if all_done and not ts["groups"]["done"]:
            if st.button("✅ Confirmar Fase de Grupos →", type="primary"):
                ts["groups"]["done"] = True
                persist()
                st.rerun()

        if ts["groups"]["done"]:
            st.success("✅ Fase de Grupos finalizada")
            st.markdown("### Clasificados")
            qc = st.columns(4)
            for gi, g in enumerate("ABCD"):
                r = get_group_ranking(ts["groups"][g])
                c1, c2 = r[0][0], r[1][0]
                with qc[gi]:
                    st.markdown(f"<span style='color:{group_colors[g]};font-family:Bebas Neue,sans-serif'>GRUPO {g}</span>", unsafe_allow_html=True)
                    i1, i2 = st.columns(2)
                    with i1:
                        st.image(TEAMS[c1]["logo"], width=44)
                        st.caption(f"1️⃣ {TEAMS[c1]['name']}")
                    with i2:
                        st.image(TEAMS[c2]["logo"], width=44)
                        st.caption(f"2️⃣ {TEAMS[c2]['name']}")

# ── RONDA 4 ───────────────────────────────────────────────────────────
elif page == "🏅 Ronda 4":
    sec("🏅 Ronda 4", "Llaves A a D")
    if not ts["groups"]["done"]:
        st.warning("⏳ Completa la Fase de Grupos primero.")
        st.stop()
    info("1º de cada grupo actúa como local. Los 2º se sortean como visitantes.")

    if not ts["r4"]["drawn"]:
        st.markdown("### Sorteo Ronda 4")
        firsts  = [get_group_ranking(ts["groups"][g])[0][0] for g in "ABCD"]
        seconds = [get_group_ranking(ts["groups"][g])[1][0] for g in "ABCD"]

        st.markdown("**Locales (1º de grupo):**")
        fc = st.columns(4)
        for i, code in enumerate(firsts):
            with fc[i]:
                st.image(TEAMS[code]["logo"], width=50)
                st.caption(f"Llave {'ABCD'[i]}: {TEAMS[code]['name']}")

        st.markdown("**Asigna los visitantes (2º de grupo):**")
        s_opts = [f"{code} — {TEAMS[code]['name']}" for code in seconds]
        s_map  = {f"{code} — {TEAMS[code]['name']}": code for code in seconds}

        draw_pairs = []
        draw_valid2 = True
        all_sel = []
        dc = st.columns(4)
        for i in range(4):
            with dc[i]:
                lbl = "ABCD"[i]
                sel = st.selectbox(f"Visitante Llave {lbl}", s_opts, key=f"r4d_{i}")
                draw_pairs.append((firsts[i], s_map[sel]))
                all_sel.append(s_map[sel])

        if len(set(all_sel)) < 4:
            st.error("⚠️ Cada equipo solo puede estar en una llave.")
            draw_valid2 = False

        b1, b2 = st.columns(2)
        with b1:
            if st.button("🎲 Sorteo Aleatorio R4"):
                sh = seconds[:]
                random.shuffle(sh)
                st.info("Sugerencia generada.")
        with b2:
            if st.button("✅ Confirmar Sorteo R4", type="primary", disabled=not draw_valid2):
                ts["r4"]["matches"] = build_r4(ts["groups"], draw_pairs)
                ts["r4"]["drawn"] = True
                persist()
                st.rerun()
    else:
        matches = ts["r4"]["matches"]
        all_played = all(m["played"] for m in matches)
        for i, m in enumerate(matches):
            match_entry_form(m, f"r4_{i}", allow_draw=False)
        st.markdown('<div class="silver-line"></div>', unsafe_allow_html=True)
        render_matches_grid(matches, cols=2)
        if all_played and not ts["r4"]["done"]:
            if st.button("✅ Confirmar Ronda 4 →", type="primary"):
                ts["r4"]["done"] = True
                ts["qf"]["matches"] = build_qf(matches)
                persist()
                st.rerun()
        if ts["r4"]["done"]:
            st.success("✅ Ronda 4 finalizada")

# ── CUARTOS ───────────────────────────────────────────────────────────
elif page == "⚡ Cuartos de Final":
    sec("⚡ Cuartos de Final", "Ronda 5")
    if not ts["r4"]["done"]:
        st.warning("⏳ Completa la Ronda 4 primero.")
        st.stop()
    info("Pos 1 vs R4-LlaveD · Pos 2 vs R4-LlaveC · Pos 3 vs R4-LlaveB · Pos 4 vs R4-LlaveA")

    matches = ts["qf"]["matches"]
    all_played = all(m["played"] for m in matches)
    for i, m in enumerate(matches):
        match_entry_form(m, f"qf_{i}", allow_draw=False)
    st.markdown('<div class="silver-line"></div>', unsafe_allow_html=True)
    render_matches_grid(matches, cols=2)
    if all_played and not ts["qf"]["done"]:
        if st.button("✅ Confirmar Cuartos →", type="primary"):
            ts["qf"]["done"] = True
            ts["sf"]["matches"] = build_sf(matches)
            persist()
            st.rerun()
    if ts["qf"]["done"]:
        st.success("✅ Cuartos finalizados")

# ── SEMIFINALES ───────────────────────────────────────────────────────
elif page == "🌟 Semifinales":
    sec("🌟 Semifinales", "")
    if not ts["qf"]["done"]:
        st.warning("⏳ Completa los Cuartos primero.")
        st.stop()
    info("Ganador QF-A vs Ganador QF-C &nbsp;·&nbsp; Ganador QF-B vs Ganador QF-D")

    matches = ts["sf"]["matches"]
    all_played = all(m["played"] for m in matches)
    for i, m in enumerate(matches):
        match_entry_form(m, f"sf_{i}", allow_draw=False)
    st.markdown('<div class="silver-line"></div>', unsafe_allow_html=True)
    render_matches_grid(matches, cols=2)
    if all_played and not ts["sf"]["done"]:
        if st.button("✅ Confirmar Semifinales →", type="primary"):
            ts["sf"]["done"] = True
            ts["final"]["match"] = build_final(matches)
            persist()
            st.rerun()
    if ts["sf"]["done"]:
        st.success("✅ Semifinales finalizadas")

# ── FINAL ─────────────────────────────────────────────────────────────
elif page == "🏆 Final":
    sec("🏆 Gran Final", "MMJ Emirates Cup")
    if not ts["sf"]["done"]:
        st.warning("⏳ Completa las Semifinales primero.")
        st.stop()

    m = ts["final"]["match"]
    match_entry_form(m, "final_0", allow_draw=False)
    st.markdown('<div class="silver-line"></div>', unsafe_allow_html=True)
    show_match_result(m)

    if m["played"] and not ts["final"]["done"]:
        if st.button("🏆 Coronar Campeón", type="primary"):
            ts["final"]["done"] = True
            ts["champion_code"] = m["winner_code"]
            persist()
            st.rerun()

    if ts["final"]["done"] and ts["champion_code"]:
        champ = TEAMS[ts["champion_code"]]
        c1, c2, c3 = st.columns([1,2,1])
        with c2:
            st.markdown(f"""
            <div class="champ-box">
                {logo(100)}
                <div class="champ-title" style="margin-top:12px">MMJ Emirates Cup Champion</div>
                <img src="{champ['logo']}" width="90"
                     style="margin:12px 0;filter:drop-shadow(0 0 18px rgba(123,63,196,.7));display:block;margin-left:auto;margin-right:auto">
                <div class="champ-name">{champ['name']}</div>
            </div>""", unsafe_allow_html=True)
        st.balloons()

# ── GOLEADORES ────────────────────────────────────────────────────────
elif page == "⚽ Goleadores":
    sec("⚽ Goleadores", "Tabla de Artilleros")
    scorers = collect_all_scorers(ts)

    if not scorers:
        st.info("⏳ Los goleadores aparecerán aquí una vez se registren partidos.")
    else:
        if len(scorers) >= 3:
            medals = ["🥇","🥈","🥉"]
            pod = st.columns(3)
            for i in range(3):
                s = scorers[i]
                lgo = TEAMS[s["team_code"]]["logo"]
                with pod[i]:
                    st.markdown(f"""
                    <div class="pod-card">
                        <div style="font-size:2rem">{medals[i]}</div>
                        <img src="{lgo}" width="52"
                             style="margin:8px auto;display:block;object-fit:contain;
                             filter:drop-shadow(0 0 8px rgba(123,63,196,.4))">
                        <div class="pod-goals">{s['goals']}</div>
                        <div style="font-family:Barlow Condensed,sans-serif;font-weight:700;font-size:.95rem">{s['player']}</div>
                        <div style="font-size:.75rem;color:#6b5a8a">{s['team_name']}</div>
                    </div>""", unsafe_allow_html=True)

        st.markdown("### 📋 Tabla Completa")
        rows = [{"#": i+1, "Jugador": s["player"], "Equipo": s["team_name"],
                 "Goles": s["goals"], "Partidos": len(set(s["rounds"]))}
                for i, s in enumerate(scorers)]
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True,
                     column_config={
                         "#":      st.column_config.NumberColumn(width="small"),
                         "Goles":  st.column_config.NumberColumn(width="small"),
                     })

        st.markdown("### 📊 Goles por Equipo")
        from collections import defaultdict
        tg = defaultdict(int)
        for s in scorers:
            tg[s["team_name"]] += s["goals"]
        chart_df = pd.DataFrame(sorted(tg.items(), key=lambda x:-x[1]), columns=["Equipo","Goles"])
        st.bar_chart(chart_df.set_index("Equipo"), color="#7B3FC4")

# ── EQUIPOS ───────────────────────────────────────────────────────────
elif page == "🛡 Equipos":
    sec("🛡 Los 30 Clubes", "Dream League Selection")
    search = st.text_input("🔍 Buscar equipo o código", "")

    gcols = st.columns(3)
    for i, code in enumerate(TEAM_ORDER):
        t = TEAMS[code]
        if search and search.lower() not in t["name"].lower() and search.lower() not in code.lower():
            continue
        with gcols[i % 3]:
            with st.expander(f"#{i+1}  {t['name']}  ({code})"):
                cc1, cc2 = st.columns([1, 3])
                with cc1:
                    st.image(t["logo"], width=68)
                with cc2:
                    st.markdown(f"**{t['name']}**")
                    st.markdown(f"Código: `{code}` · Posición: **#{i+1}**")
                st.markdown("**Plantilla:**")
                for p in t["players"]:
                    st.markdown(f"<span style='color:#9B5EE0'>▸</span> {p}", unsafe_allow_html=True)
