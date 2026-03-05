# app.py — MMJ Emirates Cup — Streamlit App
import streamlit as st
from data import TEAM_ORDER, TEAMS, get_by_pos, get_team
from engine import (
    init_r1, simulate_r1,
    init_r2, simulate_r2,
    get_group_seeds, draw_groups, init_groups, simulate_groups, get_group_ranking,
    draw_r4, simulate_r4,
    init_qf, simulate_qf,
    init_sf, simulate_sf,
    init_final, simulate_final,
    collect_all_scorers,
)

# ──────────────── PAGE CONFIG ────────────────
st.set_page_config(
    page_title="MMJ Emirates Cup",
    page_icon="🏆",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ──────────────── CUSTOM CSS ────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Barlow+Condensed:wght@400;600;700&family=Barlow:wght@300;400;500&display=swap');

html, body, [class*="css"] { font-family: 'Barlow', sans-serif; }

.main { background-color: #0a0c10; }
section[data-testid="stSidebar"] { background: #0d1528 !important; border-right: 1px solid #C9A84C33; }

.cup-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 2.8rem;
    letter-spacing: 6px;
    color: #C9A84C;
    text-align: center;
    margin-bottom: 0;
    text-shadow: 0 0 30px rgba(201,168,76,0.4);
}
.cup-sub {
    font-family: 'Barlow Condensed', sans-serif;
    letter-spacing: 4px;
    text-align: center;
    color: #6b7a9a;
    font-size: 0.9rem;
    margin-top: -6px;
    margin-bottom: 24px;
}
.gold-divider {
    height: 2px;
    background: linear-gradient(to right, transparent, #C9A84C, transparent);
    margin: 12px 0 24px 0;
}
.match-card {
    background: #1a2035;
    border: 1px solid #2a3050;
    border-radius: 10px;
    padding: 14px 16px;
    margin-bottom: 12px;
    transition: border-color 0.2s;
}
.match-card:hover { border-color: rgba(201,168,76,0.5); }
.match-label {
    font-family: 'Bebas Neue', sans-serif;
    letter-spacing: 3px;
    color: #C9A84C;
    font-size: 0.85rem;
    margin-bottom: 6px;
}
.match-row {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 5px 0;
    font-family: 'Barlow Condensed', sans-serif;
    font-weight: 600;
    font-size: 0.95rem;
}
.match-score {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.4rem;
    color: #e8eaf0;
    min-width: 28px;
    text-align: center;
}
.score-win { color: #27ae60 !important; }
.team-name-cell { flex: 1; }
.winner-name { color: #27ae60; }
.section-header {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.6rem;
    letter-spacing: 4px;
    color: #C9A84C;
    margin-bottom: 4px;
}
.round-badge {
    display: inline-block;
    background: rgba(201,168,76,0.12);
    border: 1px solid rgba(201,168,76,0.3);
    border-radius: 4px;
    padding: 2px 10px;
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 0.78rem;
    letter-spacing: 2px;
    color: #C9A84C;
    margin-bottom: 16px;
    text-transform: uppercase;
}
.scorer-row {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 8px 12px;
    border-bottom: 1px solid rgba(255,255,255,0.05);
}
.scorer-pos {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.2rem;
    color: #C9A84C;
    min-width: 28px;
}
.scorer-goals {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.5rem;
    color: #e8eaf0;
    min-width: 36px;
    text-align: right;
}
.group-table-header {
    font-family: 'Bebas Neue', sans-serif;
    letter-spacing: 3px;
    font-size: 1.1rem;
    padding: 8px 12px;
    margin-bottom: 0;
}
.group-a { color: #e74c3c; }
.group-b { color: #3498db; }
.group-c { color: #2ecc71; }
.group-d { color: #9b59b6; }
.champion-banner {
    background: linear-gradient(135deg, rgba(201,168,76,0.15), rgba(201,168,76,0.04));
    border: 2px solid #C9A84C;
    border-radius: 16px;
    padding: 32px;
    text-align: center;
    margin: 24px auto;
    max-width: 400px;
}
.champion-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.4rem;
    letter-spacing: 5px;
    color: #C9A84C;
    margin-bottom: 12px;
}
.champion-name {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 2.2rem;
    letter-spacing: 3px;
    color: #e8eaf0;
}
.info-box {
    background: rgba(58,111,255,0.08);
    border: 1px solid rgba(58,111,255,0.25);
    border-radius: 8px;
    padding: 10px 14px;
    font-size: 0.82rem;
    color: #8aabff;
    margin-bottom: 16px;
    line-height: 1.6;
}
.pending { color: #6b7a9a; font-style: italic; }
</style>
""", unsafe_allow_html=True)

# ──────────────── SESSION STATE INIT ────────────────
def init_state():
    defaults = {
        "r1": None, "r1_done": False,
        "r2": None, "r2_done": False,
        "group_seeds": None, "draw_assignment": None,
        "groups": None, "groups_drawn": False, "groups_done": False,
        "r4": None, "r4_drawn": False, "r4_done": False,
        "qf": None, "qf_done": False,
        "sf": None, "sf_done": False,
        "final": None, "final_done": False,
        "champion": None,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

# ──────────────── SIDEBAR ────────────────
with st.sidebar:
    st.markdown('<div class="cup-title" style="font-size:1.6rem">MMJ Emirates Cup</div>', unsafe_allow_html=True)
    st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)

    page = st.radio(
        "Navegación",
        ["🏟 Clasificación", "⚡ Ronda 1", "🔥 Ronda 2", "🔵 Fase de Grupos",
         "🏅 Ronda 4", "⚡ Cuartos de Final", "🌟 Semifinales",
         "🏆 Final", "⚽ Goleadores", "🛡 Equipos"],
        label_visibility="collapsed"
    )

    st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)
    st.markdown("**Estado del Torneo**")
    steps = [
        ("R1", st.session_state.r1_done),
        ("R2", st.session_state.r2_done),
        ("Sorteo Grupos", st.session_state.groups_drawn),
        ("Grupos", st.session_state.groups_done),
        ("Sorteo R4", st.session_state.r4_drawn),
        ("R4", st.session_state.r4_done),
        ("Cuartos", st.session_state.qf_done),
        ("Semis", st.session_state.sf_done),
        ("Final", st.session_state.final_done),
    ]
    for label, done in steps:
        icon = "✅" if done else "⏳"
        st.markdown(f"{icon} {label}")

    if st.session_state.champion:
        st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)
        st.markdown(f"🏆 **Campeón:** {st.session_state.champion['name']}")

# ──────────────── HELPER FUNCTIONS ────────────────
def render_match(m, show_scorers=True):
    if not m["played"]:
        home_n = m["home"]["name"]
        away_n = m["away"]["name"]
        st.markdown(f"""
        <div class="match-card">
            <div class="match-label">{m['label']}</div>
            <div class="match-row"><span class="team-name-cell">{home_n}</span><span class="match-score pending">-</span></div>
            <div class="match-row"><span class="team-name-cell">{away_n}</span><span class="match-score pending">-</span></div>
        </div>""", unsafe_allow_html=True)
        return

    hs, as_ = m["home_score"], m["away_score"]
    hw = hs > as_
    aw = as_ > hs
    home_cls = "winner-name" if hw else ""
    away_cls = "winner-name" if aw else ""
    h_score_cls = "score-win" if hw else ""
    a_score_cls = "score-win" if aw else ""

    scorers_html = ""
    if show_scorers and m.get("scorers"):
        scorer_lines = []
        for s in m["scorers"]:
            team_name = TEAMS[s["team"]]["name"]
            scorer_lines.append(f"<span style='color:#6b7a9a;font-size:0.75rem'>{s['minute']}' {s['player']} ({team_name})</span>")
        scorers_html = "<div style='margin-top:6px;line-height:1.8'>" + " &nbsp;·&nbsp; ".join(scorer_lines) + "</div>"

    st.markdown(f"""
    <div class="match-card">
        <div class="match-label">{m['label']}</div>
        <div class="match-row">
            <span class="team-name-cell {home_cls}">{m['home']['name']}</span>
            <span class="match-score {h_score_cls}">{hs}</span>
        </div>
        <div class="match-row">
            <span class="team-name-cell {away_cls}">{m['away']['name']}</span>
            <span class="match-score {a_score_cls}">{as_}</span>
        </div>
        {scorers_html}
    </div>""", unsafe_allow_html=True)

def render_matches_grid(matches, cols=2):
    if not matches:
        st.info("Los partidos aparecerán aquí una vez configurados.")
        return
    columns = st.columns(cols)
    for i, m in enumerate(matches):
        with columns[i % cols]:
            render_match(m)

def section_header(title, badge=""):
    st.markdown(f'<div class="section-header">{title}</div>', unsafe_allow_html=True)
    if badge:
        st.markdown(f'<div class="round-badge">{badge}</div>', unsafe_allow_html=True)
    st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)

# ──────────────── PAGES ────────────────

# ── CLASIFICACIÓN ──
if page == "🏟 Clasificación":
    section_header("🏟 Clasificación Inicial", "30 Equipos — Season 2025")
    st.markdown('<div class="info-box">Los equipos están ordenados por posición (1–30). La posición determina el camino en el torneo. Top 4 entran directo a Cuartos de Final.</div>', unsafe_allow_html=True)

    data = []
    for i, code in enumerate(TEAM_ORDER):
        pos = i + 1
        t = TEAMS[code]
        if pos <= 4: role = "⭐ Cuartos Directo"
        elif pos <= 12: role = "🔵 Fase de Grupos"
        elif pos <= 20: role = "🔸 Ronda 2 (Local)"
        elif pos <= 26: role = "⚪ Ronda 2 (Visitante)"
        else: role = "⚡ Ronda 1"
        data.append({"#": pos, "Equipo": t["name"], "Código": code, "Entrada al Torneo": role})

    import pandas as pd
    df = pd.DataFrame(data)
    st.dataframe(df, use_container_width=True, hide_index=True,
                 column_config={"#": st.column_config.NumberColumn(width="small")})

# ── RONDA 1 ──
elif page == "⚡ Ronda 1":
    section_header("⚡ Ronda 1", "Llaves M y N")
    st.markdown('<div class="info-box">Pos 28 vs Pos 29 (Llave M) · Pos 27 vs Pos 30 (Llave N) — Partido único, eliminación directa.</div>', unsafe_allow_html=True)

    if st.session_state.r1 is None:
        st.session_state.r1 = init_r1()

    if not st.session_state.r1_done:
        if st.button("⚽ Simular Ronda 1", type="primary", use_container_width=False):
            st.session_state.r1 = simulate_r1(st.session_state.r1)
            st.session_state.r1_done = True
            st.rerun()
    else:
        st.success("✅ Ronda 1 completada")

    render_matches_grid(st.session_state.r1, cols=2)

    if st.session_state.r1_done:
        st.markdown("### Clasificados")
        c1, c2 = st.columns(2)
        for i, m in enumerate(st.session_state.r1):
            with (c1 if i == 0 else c2):
                w = m["winner"]
                st.markdown(f"**{m['label']}:** 🟢 {w['name']}")

# ── RONDA 2 ──
elif page == "🔥 Ronda 2":
    section_header("🔥 Ronda 2", "Llaves E a L")
    st.markdown('<div class="info-box">Pos 13–20 actúan como locales. Visitantes: Pos 21–26 + ganadores de R1 (Llave N → Pos 13, Llave M → Pos 14).</div>', unsafe_allow_html=True)

    if not st.session_state.r1_done:
        st.warning("⏳ Completa la Ronda 1 primero.")
    else:
        if st.session_state.r2 is None:
            st.session_state.r2 = init_r2(st.session_state.r1)

        if not st.session_state.r2_done:
            if st.button("⚽ Simular Ronda 2", type="primary"):
                st.session_state.r2 = simulate_r2(st.session_state.r2)
                st.session_state.r2_done = True
                st.rerun()
        else:
            st.success("✅ Ronda 2 completada")

        render_matches_grid(st.session_state.r2, cols=2)

        if st.session_state.r2_done:
            st.markdown("### Clasificados a Fase de Grupos")
            cols = st.columns(4)
            for i, m in enumerate(st.session_state.r2):
                with cols[i % 4]:
                    st.markdown(f"**{m['label']}**  \n🟢 {m['winner']['name']}")

# ── FASE DE GRUPOS ──
elif page == "🔵 Fase de Grupos":
    section_header("🔵 Fase de Grupos", "Ronda 3 — Grupos A, B, C, D")
    st.markdown('<div class="info-box">Cabezas de grupo: Pos 5–8 (1º) y Pos 9–12 (2º). Los 8 ganadores de R2 se sortean entre los grupos (2 por grupo). Todos contra todos — 6 partidos por grupo. Los 2 mejores pasan.</div>', unsafe_allow_html=True)

    if not st.session_state.r2_done:
        st.warning("⏳ Completa la Ronda 2 primero.")
    else:
        # DRAW
        if not st.session_state.groups_drawn:
            st.markdown("#### 🎲 Sorteo de Grupos")
            seeds = get_group_seeds()
            r2_winners = [m["winner"] for m in st.session_state.r2]

            with st.expander("Ver equipos en el sorteo", expanded=True):
                c1, c2 = st.columns(2)
                with c1:
                    st.markdown("**Cabezas de Grupo (Fijas)**")
                    for g in ["A","B","C","D"]:
                        st.markdown(f"- Grupo {g}: {seeds[g][0]['name']} · {seeds[g][1]['name']}")
                with c2:
                    st.markdown("**Clasificados R2 (a sortear)**")
                    for w in r2_winners:
                        st.markdown(f"- {w['name']}")

            if st.button("🎲 Realizar Sorteo", type="primary"):
                st.session_state.group_seeds = seeds
                st.session_state.draw_assignment = draw_groups(r2_winners)
                st.session_state.groups = init_groups(seeds, st.session_state.draw_assignment)
                st.session_state.groups_drawn = True
                st.rerun()
        else:
            if not st.session_state.groups_done:
                col1, col2 = st.columns([1, 3])
                with col1:
                    if st.button("⚽ Simular Grupos", type="primary"):
                        st.session_state.groups = simulate_groups(st.session_state.groups)
                        st.session_state.groups_done = True
                        st.rerun()
                    if st.button("🎲 Nuevo Sorteo"):
                        st.session_state.groups_drawn = False
                        st.session_state.groups = None
                        st.session_state.draw_assignment = None
                        st.rerun()
            else:
                st.success("✅ Fase de Grupos completada")

            # RENDER GROUPS
            import pandas as pd
            group_colors = {"A": "#e74c3c", "B": "#3498db", "C": "#2ecc71", "D": "#9b59b6"}
            gc1, gc2 = st.columns(2)
            col_map = {"A": gc1, "B": gc2, "C": gc1, "D": gc2}

            for g in ["A","B","C","D"]:
                grp = st.session_state.groups[g]
                ranking = get_group_ranking(grp)
                color = group_colors[g]

                with col_map[g]:
                    st.markdown(f"<div style='color:{color};font-family:Bebas Neue,sans-serif;font-size:1.2rem;letter-spacing:3px;margin-top:20px'>GRUPO {g}</div>", unsafe_allow_html=True)

                    rows = []
                    for rank_i, s in enumerate(ranking):
                        gd = s["gf"] - s["ga"]
                        rows.append({
                            "#": rank_i + 1,
                            "Equipo": s["team"]["name"],
                            "PJ": s["pj"], "G": s["w"], "E": s["d"], "P": s["l"],
                            "GF": s["gf"], "GA": s["ga"], "DG": gd, "Pts": s["pts"]
                        })
                    df = pd.DataFrame(rows)
                    st.dataframe(df, use_container_width=True, hide_index=True,
                                 column_config={"Pts": st.column_config.NumberColumn(width="small"),
                                                "#": st.column_config.NumberColumn(width="small")})

                    with st.expander(f"Ver partidos Grupo {g}"):
                        for m in grp["matches"]:
                            render_match(m, show_scorers=True)

            if st.session_state.groups_done:
                st.markdown("### Clasificados a Ronda 4")
                cols_q = st.columns(4)
                for gi, g in enumerate(["A","B","C","D"]):
                    r = get_group_ranking(st.session_state.groups[g])
                    with cols_q[gi]:
                        st.markdown(f"**Grupo {g}**  \n1️⃣ {r[0]['team']['name']}  \n2️⃣ {r[1]['team']['name']}")

# ── RONDA 4 ──
elif page == "🏅 Ronda 4":
    section_header("🏅 Ronda 4", "Llaves A a D")
    st.markdown('<div class="info-box">1º de cada grupo actúa como local. Los 2º se sortean contra ellos.</div>', unsafe_allow_html=True)

    if not st.session_state.groups_done:
        st.warning("⏳ Completa la Fase de Grupos primero.")
    else:
        if not st.session_state.r4_drawn:
            if st.button("🎲 Sorteo Ronda 4", type="primary"):
                st.session_state.r4 = draw_r4(st.session_state.groups)
                st.session_state.r4_drawn = True
                st.rerun()
        else:
            if not st.session_state.r4_done:
                c1, c2 = st.columns([1, 3])
                with c1:
                    if st.button("⚽ Simular Ronda 4", type="primary"):
                        st.session_state.r4 = simulate_r4(st.session_state.r4)
                        st.session_state.r4_done = True
                        st.rerun()
                    if st.button("🎲 Nuevo Sorteo R4"):
                        st.session_state.r4_drawn = False
                        st.session_state.r4 = None
                        st.rerun()
            else:
                st.success("✅ Ronda 4 completada")

            render_matches_grid(st.session_state.r4, cols=2)

            if st.session_state.r4_done:
                st.markdown("### Clasificados a Cuartos")
                cols_q = st.columns(4)
                for i, m in enumerate(st.session_state.r4):
                    with cols_q[i]:
                        st.markdown(f"**{m['label']}**  \n🟢 {m['winner']['name']}")

# ── CUARTOS ──
elif page == "⚡ Cuartos de Final":
    section_header("⚡ Cuartos de Final", "Ronda 5")
    st.markdown('<div class="info-box">Pos 1 vs Ganador Llave D · Pos 2 vs Llave C · Pos 3 vs Llave B · Pos 4 vs Llave A</div>', unsafe_allow_html=True)

    if not st.session_state.r4_done:
        st.warning("⏳ Completa la Ronda 4 primero.")
    else:
        if st.session_state.qf is None:
            st.session_state.qf = init_qf(st.session_state.r4)

        if not st.session_state.qf_done:
            if st.button("⚽ Simular Cuartos de Final", type="primary"):
                st.session_state.qf = simulate_qf(st.session_state.qf)
                st.session_state.qf_done = True
                st.rerun()
        else:
            st.success("✅ Cuartos completados")

        render_matches_grid(st.session_state.qf, cols=2)

        if st.session_state.qf_done:
            st.markdown("### Clasificados a Semifinales")
            cols_q = st.columns(4)
            for i, m in enumerate(st.session_state.qf):
                with cols_q[i]:
                    st.markdown(f"**{m['label'].split('—')[0]}**  \n🟢 {m['winner']['name']}")

# ── SEMIFINALES ──
elif page == "🌟 Semifinales":
    section_header("🌟 Semifinales", "")
    st.markdown('<div class="info-box">Ganador Cuartos A vs Ganador Cuartos C · Ganador Cuartos B vs Ganador Cuartos D</div>', unsafe_allow_html=True)

    if not st.session_state.qf_done:
        st.warning("⏳ Completa los Cuartos de Final primero.")
    else:
        if st.session_state.sf is None:
            st.session_state.sf = init_sf(st.session_state.qf)

        if not st.session_state.sf_done:
            if st.button("⚽ Simular Semifinales", type="primary"):
                st.session_state.sf = simulate_sf(st.session_state.sf)
                st.session_state.sf_done = True
                st.rerun()
        else:
            st.success("✅ Semifinales completadas")

        render_matches_grid(st.session_state.sf, cols=2)

        if st.session_state.sf_done:
            st.markdown("### Finalistas")
            c1, c2 = st.columns(2)
            for i, m in enumerate(st.session_state.sf):
                with (c1 if i == 0 else c2):
                    st.markdown(f"**{m['label']}**  \n🟢 {m['winner']['name']}")

# ── FINAL ──
elif page == "🏆 Final":
    section_header("🏆 Gran Final", "MMJ Emirates Cup")

    if not st.session_state.sf_done:
        st.warning("⏳ Completa las Semifinales primero.")
    else:
        if st.session_state.final is None:
            st.session_state.final = init_final(st.session_state.sf)

        if not st.session_state.final_done:
            if st.button("⚽ ¡Jugar la Final!", type="primary"):
                st.session_state.final = simulate_final(st.session_state.final)
                st.session_state.champion = st.session_state.final["winner"]
                st.session_state.final_done = True
                st.rerun()

        if st.session_state.final:
            render_match(st.session_state.final)

        if st.session_state.final_done and st.session_state.champion:
            champ = st.session_state.champion
            st.markdown(f"""
            <div class="champion-banner">
                <div style="font-size:3rem">🏆</div>
                <div class="champion-title">MMJ Emirates Cup Champion</div>
                <img src="{champ['logo']}" width="90" style="margin:12px 0">
                <div class="champion-name">{champ['name']}</div>
            </div>""", unsafe_allow_html=True)
            st.balloons()

# ── GOLEADORES ──
elif page == "⚽ Goleadores":
    section_header("⚽ Goleadores", "Tabla de Artilleros")

    import pandas as pd
    from engine import collect_all_scorers

    tournament_state = {
        "r1": st.session_state.r1 or [],
        "r2": st.session_state.r2 or [],
        "groups": st.session_state.groups or {},
        "r4": st.session_state.r4 or [],
        "qf": st.session_state.qf or [],
        "sf": st.session_state.sf or [],
        "final": st.session_state.final,
    }

    scorers = collect_all_scorers(tournament_state)

    if not scorers:
        st.info("⏳ Los goleadores aparecerán aquí una vez se jueguen los partidos.")
    else:
        # Top 3 podium
        if len(scorers) >= 3:
            st.markdown("### 🥇 Top Goleadores")
            medals = ["🥇", "🥈", "🥉"]
            cols_p = st.columns(3)
            for i in range(min(3, len(scorers))):
                s = scorers[i]
                with cols_p[i]:
                    st.markdown(f"""
                    <div style="background:#1a2035;border:1px solid #2a3050;border-radius:10px;padding:16px;text-align:center">
                        <div style="font-size:2rem">{medals[i]}</div>
                        <div style="font-family:'Bebas Neue',sans-serif;font-size:1.8rem;color:#C9A84C">{s['goals']}</div>
                        <div style="font-weight:700;font-size:0.9rem">{s['player']}</div>
                        <div style="color:#6b7a9a;font-size:0.78rem">{s['team_name']}</div>
                    </div>""", unsafe_allow_html=True)

        st.markdown("### 📋 Tabla Completa")
        rows = []
        for i, s in enumerate(scorers):
            rows.append({
                "#": i + 1,
                "Jugador": s["player"],
                "Equipo": s["team_name"],
                "Goles": s["goals"],
                "Partidos": len(set(s["matches"])),
            })
        df = pd.DataFrame(rows)
        st.dataframe(df, use_container_width=True, hide_index=True,
                     column_config={
                         "#": st.column_config.NumberColumn(width="small"),
                         "Goles": st.column_config.NumberColumn(width="small"),
                         "Partidos": st.column_config.NumberColumn(width="small"),
                     })

        # Goals by team
        st.markdown("### 📊 Goles por Equipo")
        from collections import defaultdict
        team_goals = defaultdict(int)
        for s in scorers:
            team_goals[s["team_name"]] += s["goals"]
        sorted_teams = sorted(team_goals.items(), key=lambda x: -x[1])
        teams_df = pd.DataFrame(sorted_teams, columns=["Equipo", "Goles"])
        st.bar_chart(teams_df.set_index("Equipo"), use_container_width=True, color="#C9A84C")

# ── EQUIPOS ──
elif page == "🛡 Equipos":
    section_header("🛡 Los 30 Clubes", "Dream League Selection")

    search = st.text_input("🔍 Buscar equipo", "")
    cols = st.columns(3)

    for i, code in enumerate(TEAM_ORDER):
        t = TEAMS[code]
        if search and search.lower() not in t["name"].lower() and search.lower() not in code.lower():
            continue
        pos = i + 1
        with cols[i % 3]:
            with st.expander(f"#{pos} — {t['name']} ({code})"):
                c1, c2 = st.columns([1, 3])
                with c1:
                    st.image(t["logo"], width=60)
                with c2:
                    st.markdown(f"**{t['name']}**")
                    st.markdown(f"Código: `{code}` · Posición: **#{pos}**")
                st.markdown("**Plantilla:**")
                for p in t["players"]:
                    st.markdown(f"- {p}")
