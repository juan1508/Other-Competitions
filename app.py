# app.py — MMJ Emirates Cup — Registro Manual de Resultados
import streamlit as st
import pandas as pd
import random
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

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Barlow+Condensed:wght@400;600;700&family=Barlow:wght@300;400;500&display=swap');
html,[class*="css"]{font-family:'Barlow',sans-serif;}
section[data-testid="stSidebar"]{background:#0d1528!important;border-right:1px solid #C9A84C44;}
.cup-title{font-family:'Bebas Neue',sans-serif;font-size:1.7rem;letter-spacing:5px;color:#C9A84C;text-align:center;}
.gold-line{height:2px;background:linear-gradient(to right,transparent,#C9A84C,transparent);margin:10px 0 18px 0;}
.sec-title{font-family:'Bebas Neue',sans-serif;font-size:1.5rem;letter-spacing:4px;color:#C9A84C;margin-bottom:2px;}
.badge{display:inline-block;background:rgba(201,168,76,.12);border:1px solid rgba(201,168,76,.35);border-radius:4px;padding:2px 10px;font-family:'Barlow Condensed',sans-serif;font-size:.75rem;letter-spacing:2px;color:#C9A84C;text-transform:uppercase;margin-bottom:14px;}
.match-box{background:#1a2035;border:1px solid #2a3050;border-radius:10px;padding:14px 16px;margin-bottom:10px;}
.match-box:hover{border-color:rgba(201,168,76,.45);}
.mlabel{font-family:'Bebas Neue',sans-serif;letter-spacing:2px;color:#C9A84C;font-size:.82rem;margin-bottom:8px;}
.mteam{display:flex;align-items:center;gap:8px;font-family:'Barlow Condensed',sans-serif;font-weight:700;font-size:1rem;padding:4px 0;}
.mscore{font-family:'Bebas Neue',sans-serif;font-size:1.6rem;min-width:30px;text-align:center;}
.win-score{color:#27ae60!important;}
.win-name{color:#27ae60;}
.pending-score{color:#3a4060;}
.info-box{background:rgba(58,111,255,.08);border:1px solid rgba(58,111,255,.25);border-radius:8px;padding:10px 14px;font-size:.82rem;color:#8aabff;margin-bottom:14px;line-height:1.6;}
.scorer-chip{display:inline-block;background:#1a2035;border:1px solid #2a3050;border-radius:5px;padding:2px 8px;font-size:.75rem;margin:2px;color:#a0b0d0;}
.champ-box{background:linear-gradient(135deg,rgba(201,168,76,.14),rgba(201,168,76,.03));border:2px solid #C9A84C;border-radius:14px;padding:28px;text-align:center;margin:20px auto;max-width:360px;}
.champ-title{font-family:'Bebas Neue',sans-serif;font-size:1.2rem;letter-spacing:5px;color:#C9A84C;margin-bottom:10px;}
.champ-name{font-family:'Bebas Neue',sans-serif;font-size:2rem;letter-spacing:3px;color:#e8eaf0;}
.group-a-hdr{color:#e74c3c;font-family:'Bebas Neue',sans-serif;letter-spacing:3px;font-size:1.1rem;}
.group-b-hdr{color:#3498db;font-family:'Bebas Neue',sans-serif;letter-spacing:3px;font-size:1.1rem;}
.group-c-hdr{color:#2ecc71;font-family:'Bebas Neue',sans-serif;letter-spacing:3px;font-size:1.1rem;}
.group-d-hdr{color:#9b59b6;font-family:'Bebas Neue',sans-serif;letter-spacing:3px;font-size:1.1rem;}
div[data-testid="stNumberInput"] input{font-family:'Bebas Neue',sans-serif;font-size:1.3rem;text-align:center;}
</style>""", unsafe_allow_html=True)

# ──────────────── SESSION STATE ──────────────────────────────────────
if "ts" not in st.session_state:
    st.session_state.ts = load()

ts = st.session_state.ts

def persist():
    save(ts)

# ──────────────── SIDEBAR ────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="cup-title">🏆 MMJ Emirates Cup</div>', unsafe_allow_html=True)
    st.markdown('<div class="gold-line"></div>', unsafe_allow_html=True)

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

    st.markdown('<div class="gold-line"></div>', unsafe_allow_html=True)
    st.markdown("**Progreso del Torneo**")
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
        st.markdown(f"{'✅' if done else '⏳'} {lbl}")

    if ts["champion_code"]:
        st.markdown('<div class="gold-line"></div>', unsafe_allow_html=True)
        st.markdown(f"🏆 **{TEAMS[ts['champion_code']]['name']}**")

    st.markdown('<div class="gold-line"></div>', unsafe_allow_html=True)
    if st.button("🔄 Reiniciar Torneo", type="secondary"):
        st.session_state.ts = reset()
        st.rerun()

# ──────────────── HELPERS ────────────────────────────────────────────
def sec(title, badge=""):
    st.markdown(f'<div class="sec-title">{title}</div>', unsafe_allow_html=True)
    if badge:
        st.markdown(f'<div class="badge">{badge}</div>', unsafe_allow_html=True)
    st.markdown('<div class="gold-line"></div>', unsafe_allow_html=True)

def info(txt):
    st.markdown(f'<div class="info-box">{txt}</div>', unsafe_allow_html=True)

def team_header(code):
    t = TEAMS[code]
    c1, c2 = st.columns([1, 5])
    with c1:
        st.image(t["logo"], width=48)
    with c2:
        st.markdown(f"**{t['name']}**")

def show_match_result(m):
    """Display a played or pending match with logos."""
    me = enrich(m)
    hs = m["home_score"]
    as_ = m["away_score"]
    played = m["played"]
    hw = played and hs > as_
    aw = played and as_ > hs

    h_score_cls = "win-score" if hw else ("pending-score" if not played else "")
    a_score_cls = "win-score" if aw else ("pending-score" if not played else "")
    h_name_cls = "win-name" if hw else ""
    a_name_cls = "win-name" if aw else ""
    h_score_txt = str(hs) if played else "—"
    a_score_txt = str(as_) if played else "—"

    scorers_html = ""
    if played and m.get("scorers"):
        chips = "".join(
            f"<span class='scorer-chip'>⚽ {s['minute']}' {s['player']} ({TEAMS[s['team_code']]['name']})</span>"
            for s in sorted(m["scorers"], key=lambda x: x["minute"])
        )
        scorers_html = f"<div style='margin-top:6px'>{chips}</div>"

    st.markdown(f"""
    <div class="match-box">
      <div class="mlabel">{m['label']}</div>
      <div style="display:flex;align-items:center;gap:10px;padding:4px 0">
        <img src="{me['home']['logo']}" width="32" style="object-fit:contain">
        <span class="mteam {h_name_cls}" style="flex:1">{me['home']['name']}</span>
        <span class="mscore {h_score_cls}">{h_score_txt}</span>
      </div>
      <div style="display:flex;align-items:center;gap:10px;padding:4px 0">
        <img src="{me['away']['logo']}" width="32" style="object-fit:contain">
        <span class="mteam {a_name_cls}" style="flex:1">{me['away']['name']}</span>
        <span class="mscore {a_score_cls}">{a_score_txt}</span>
      </div>
      {scorers_html}
    </div>""", unsafe_allow_html=True)


def match_entry_form(match, match_key, allow_draw=False):
    """
    Form to register result + scorers for a single match.
    Returns True if saved.
    """
    me = enrich(match)
    home = me["home"]
    away = me["away"]

    with st.expander(f"{'✅' if match['played'] else '📝'} Registrar: {match['label']}", expanded=not match["played"]):
        # Team logos side by side
        lc, mc, rc = st.columns([3, 1, 3])
        with lc:
            st.image(home["logo"], width=56)
            st.markdown(f"**{home['name']}**")
        with mc:
            st.markdown("<div style='text-align:center;font-family:Bebas Neue,sans-serif;font-size:1.2rem;color:#6b7a9a;padding-top:16px'>VS</div>", unsafe_allow_html=True)
        with rc:
            st.image(away["logo"], width=56)
            st.markdown(f"**{away['name']}**")

        # Score inputs
        sc1, sc2, sc3 = st.columns([2, 1, 2])
        with sc1:
            hs = st.number_input("Goles local", min_value=0, max_value=20,
                                 value=match["home_score"] if match["home_score"] is not None else 0,
                                 key=f"{match_key}_hs")
        with sc2:
            st.markdown("<div style='text-align:center;padding-top:28px;font-family:Bebas Neue,sans-serif;font-size:1.4rem;color:#C9A84C'>-</div>", unsafe_allow_html=True)
        with sc3:
            as_ = st.number_input("Goles visitante", min_value=0, max_value=20,
                                  value=match["away_score"] if match["away_score"] is not None else 0,
                                  key=f"{match_key}_as")

        if not allow_draw and hs == as_:
            st.warning("⚠️ Este partido no puede terminar en empate (eliminatoria). Ajusta el marcador.")

        # SCORERS
        st.markdown("**⚽ Goleadores**")
        total_goals = hs + as_

        existing_scorers = match.get("scorers", [])
        # Pre-fill existing scorers if count matches
        scorers_out = []
        all_players = [(home["code"], p) for p in home["players"]] + [(away["code"], p) for p in away["players"]]
        player_options = [f"{TEAMS[code]['name']} — {p}" for code, p in all_players]
        player_map = {f"{TEAMS[code]['name']} — {p}": (code, p) for code, p in all_players}

        if total_goals > 0:
            for i in range(total_goals):
                g_col1, g_col2 = st.columns([3, 1])
                # Default values
                def_player = player_options[0]
                def_minute = 1
                if i < len(existing_scorers):
                    es = existing_scorers[i]
                    def_player = f"{TEAMS[es['team_code']]['name']} — {es['player']}"
                    if def_player not in player_map:
                        def_player = player_options[0]
                    def_minute = es.get("minute", 1)

                with g_col1:
                    sel = st.selectbox(f"Gol #{i+1}", player_options,
                                       index=player_options.index(def_player) if def_player in player_options else 0,
                                       key=f"{match_key}_sc{i}_player")
                with g_col2:
                    minute = st.number_input(f"Min #{i+1}", min_value=1, max_value=120,
                                             value=def_minute, key=f"{match_key}_sc{i}_min")
                code, pname = player_map[sel]
                scorers_out.append({"player": pname, "team_code": code, "minute": minute})
        else:
            st.caption("Sin goles — no hay goleadores que registrar.")

        can_save = allow_draw or hs != as_
        if st.button(f"💾 Guardar resultado", key=f"{match_key}_save", disabled=not can_save, type="primary"):
            match["home_score"] = int(hs)
            match["away_score"] = int(as_)
            match["scorers"] = scorers_out
            match["played"] = True
            if hs > as_:
                match["winner_code"] = home["code"]
            elif as_ > hs:
                match["winner_code"] = away["code"]
            else:
                match["winner_code"] = None
            persist()
            st.success(f"✅ Resultado guardado: {home['name']} {hs} – {as_} {away['name']}")
            st.rerun()


def render_matches_display(matches, cols=2):
    columns = st.columns(cols)
    for i, m in enumerate(matches):
        with columns[i % cols]:
            show_match_result(m)


# ═══════════════════════════════════════════════════════════════════════
#  PAGES
# ═══════════════════════════════════════════════════════════════════════

# ── CLASIFICACIÓN ─────────────────────────────────────────────────────
if page == "🏟 Clasificación":
    sec("🏟 Clasificación Inicial", "30 Equipos — Season 2025")
    info("La posición define el camino en el torneo. Top 4 entran directo a Cuartos de Final como locales.")

    rows = []
    for i, code in enumerate(TEAM_ORDER):
        pos = i + 1
        if pos <= 4: role = "⭐ Cuartos Directo (Local)"
        elif pos <= 12: role = "🔵 Fase de Grupos (Cabeza)"
        elif pos <= 20: role = "🔸 Ronda 2 — Local"
        elif pos <= 26: role = "⚪ Ronda 2 — Visitante"
        else: role = "⚡ Ronda 1"
        rows.append({"#": pos, "Equipo": TEAMS[code]["name"], "Código": code, "Rol": role})

    df = pd.DataFrame(rows)
    st.dataframe(df, use_container_width=True, hide_index=True,
                 column_config={"#": st.column_config.NumberColumn(width="small")})

    st.markdown("### Vista de Escudos")
    gcols = st.columns(6)
    for i, code in enumerate(TEAM_ORDER):
        with gcols[i % 6]:
            st.image(TEAMS[code]["logo"], width=60)
            st.caption(f"#{i+1} {code}")

# ── RONDA 1 ───────────────────────────────────────────────────────────
elif page == "⚡ Ronda 1":
    sec("⚡ Ronda 1", "Llaves M y N")
    info("Pos 28 vs Pos 29 → Llave M &nbsp;·&nbsp; Pos 27 vs Pos 30 → Llave N — Partido único, sin empates.")

    matches = ts["r1"]["matches"]
    all_played = all(m["played"] for m in matches)

    # Entry forms
    for i, m in enumerate(matches):
        match_entry_form(m, f"r1_{i}", allow_draw=False)

    st.markdown("---")
    st.markdown("### Resultados")
    render_matches_display(matches, cols=2)

    if all_played and not ts["r1"]["done"]:
        if st.button("✅ Confirmar Ronda 1 y avanzar", type="primary"):
            ts["r1"]["done"] = True
            ts["r2"]["matches"] = build_r2(matches)
            persist()
            st.success("Ronda 1 completada. ¡Ya puedes registrar la Ronda 2!")
            st.rerun()

    if ts["r1"]["done"]:
        st.success("✅ Ronda 1 finalizada")

# ── RONDA 2 ───────────────────────────────────────────────────────────
elif page == "🔥 Ronda 2":
    sec("🔥 Ronda 2", "Llaves E a L")

    if not ts["r1"]["done"]:
        st.warning("⏳ Completa y confirma la Ronda 1 primero.")
        st.stop()

    info("Pos 13–20 son locales. Pos 21–26 + ganadores R1 son visitantes. Sin empates.")
    matches = ts["r2"]["matches"]
    all_played = all(m["played"] for m in matches)

    for i, m in enumerate(matches):
        match_entry_form(m, f"r2_{i}", allow_draw=False)

    st.markdown("---")
    st.markdown("### Resultados")
    render_matches_display(matches, cols=2)

    if all_played and not ts["r2"]["done"]:
        if st.button("✅ Confirmar Ronda 2 y avanzar", type="primary"):
            ts["r2"]["done"] = True
            persist()
            st.success("Ronda 2 completada. ¡Ahora realiza el sorteo de grupos!")
            st.rerun()

    if ts["r2"]["done"]:
        st.success("✅ Ronda 2 finalizada")

# ── FASE DE GRUPOS ────────────────────────────────────────────────────
elif page == "🔵 Fase de Grupos":
    sec("🔵 Fase de Grupos", "Ronda 3")

    if not ts["r2"]["done"]:
        st.warning("⏳ Completa la Ronda 2 primero.")
        st.stop()

    # ── SORTEO ──
    if not ts["groups"]["drawn"]:
        info("Los 8 clasificados de R2 se sortean en 4 grupos (2 por grupo). Las cabezas de grupo son fijas.")
        st.markdown("### Cabezas de grupo (fijas)")
        seed_cols = st.columns(4)
        group_colors = {"A": "#e74c3c", "B": "#3498db", "C": "#2ecc71", "D": "#9b59b6"}
        for gi, g in enumerate("ABCD"):
            with seed_cols[gi]:
                st.markdown(f"<span style='color:{group_colors[g]};font-family:Bebas Neue,sans-serif;font-size:1rem;letter-spacing:2px'>GRUPO {g}</span>", unsafe_allow_html=True)
                for code in GROUP_SEEDS[g]:
                    st.image(TEAMS[code]["logo"], width=40)
                    st.caption(TEAMS[code]["name"])

        st.markdown("### Asigna los clasificados de R2 a cada grupo")
        r2_winners = [m["winner_code"] for m in ts["r2"]["matches"]]
        winner_names = {code: TEAMS[code]["name"] for code in r2_winners}
        winner_opts = [f"{code} — {TEAMS[code]['name']}" for code in r2_winners]
        winner_map = {f"{code} — {TEAMS[code]['name']}": code for code in r2_winners}

        assignment = {}
        draw_valid = True
        all_selected = []
        dcols = st.columns(4)
        for gi, g in enumerate("ABCD"):
            with dcols[gi]:
                st.markdown(f"<span style='color:{group_colors[g]};font-family:Bebas Neue,sans-serif'>GRUPO {g}</span>", unsafe_allow_html=True)
                sel1 = st.selectbox(f"Equipo 1 — G{g}", winner_opts, key=f"draw_{g}_1")
                sel2 = st.selectbox(f"Equipo 2 — G{g}", winner_opts, key=f"draw_{g}_2")
                assignment[g] = [winner_map[sel1], winner_map[sel2]]
                all_selected += [winner_map[sel1], winner_map[sel2]]

        if len(set(all_selected)) < 8:
            st.error("⚠️ Cada equipo solo puede estar en un grupo. Revisa la asignación.")
            draw_valid = False

        bc1, bc2 = st.columns(2)
        with bc1:
            if st.button("🎲 Asignación Aleatoria") :
                shuffled = r2_winners[:]
                random.shuffle(shuffled)
                # We just reshuffle to trigger selectbox defaults on next rerun
                # Store temp random draw in session
                st.session_state["_rand_draw"] = {
                    "A": [shuffled[0], shuffled[1]],
                    "B": [shuffled[2], shuffled[3]],
                    "C": [shuffled[4], shuffled[5]],
                    "D": [shuffled[6], shuffled[7]],
                }
                st.info("Sorteo sugerido generado. Revisa y confirma abajo.")

        with bc2:
            if st.button("✅ Confirmar Sorteo", type="primary", disabled=not draw_valid):
                groups_built = build_groups(assignment)
                for g in "ABCD":
                    ts["groups"][g] = groups_built[g]
                ts["groups"]["assignment"] = assignment
                ts["groups"]["drawn"] = True
                persist()
                st.rerun()

    else:
        # ── GROUPS DRAWN — show tabs ──
        if not ts["groups"]["done"]:
            st.markdown("### Registra los partidos de cada grupo")

        tabs = st.tabs(["Grupo A 🔴", "Grupo B 🔵", "Grupo C 🟢", "Grupo D 🟣"])
        group_colors_cls = ["group-a-hdr","group-b-hdr","group-c-hdr","group-d-hdr"]

        for gi, g in enumerate("ABCD"):
            with tabs[gi]:
                grp = ts["groups"][g]
                st.markdown(f'<div class="{group_colors_cls[gi]}">GRUPO {g}</div>', unsafe_allow_html=True)

                # Entry forms
                for mi, m in enumerate(grp["matches"]):
                    match_entry_form(m, f"grp{g}_{mi}", allow_draw=True)

                # Standings table
                st.markdown("#### Tabla de posiciones")
                standing = recalc_group_standing(grp)
                ranking = sorted(standing.items(), key=lambda x: (-x[1]["pts"], -(x[1]["gf"]-x[1]["ga"]), -x[1]["gf"]))
                rows = []
                for rank_i, (code, s) in enumerate(ranking):
                    rows.append({
                        "#": rank_i+1,
                        "Equipo": TEAMS[code]["name"],
                        "PJ": s["pj"], "G": s["w"], "E": s["d"], "P": s["l"],
                        "GF": s["gf"], "GA": s["ga"], "DG": s["gf"]-s["ga"], "Pts": s["pts"],
                    })
                df = pd.DataFrame(rows)
                st.dataframe(df, use_container_width=True, hide_index=True)

                # Match results display
                st.markdown("#### Partidos")
                render_matches_display(grp["matches"], cols=2)

        # Check all groups complete
        all_group_matches_played = all(
            all(m["played"] for m in ts["groups"][g]["matches"]) for g in "ABCD"
        )
        if all_group_matches_played and not ts["groups"]["done"]:
            if st.button("✅ Confirmar Fase de Grupos", type="primary"):
                ts["groups"]["done"] = True
                persist()
                st.success("Fase de Grupos completada. Ahora realiza el sorteo de Ronda 4.")
                st.rerun()

        if ts["groups"]["done"]:
            st.success("✅ Fase de Grupos finalizada")
            st.markdown("### Clasificados")
            q_cols = st.columns(4)
            for gi, g in enumerate("ABCD"):
                r = get_group_ranking(ts["groups"][g])
                with q_cols[gi]:
                    c1, c2 = (r[0][0], r[1][0])
                    st.image(TEAMS[c1]["logo"], width=40)
                    st.markdown(f"1️⃣ **{TEAMS[c1]['name']}**")
                    st.image(TEAMS[c2]["logo"], width=40)
                    st.markdown(f"2️⃣ {TEAMS[c2]['name']}")

# ── RONDA 4 ───────────────────────────────────────────────────────────
elif page == "🏅 Ronda 4":
    sec("🏅 Ronda 4", "Llaves A a D")

    if not ts["groups"]["done"]:
        st.warning("⏳ Completa la Fase de Grupos primero.")
        st.stop()

    info("1º de cada grupo actúa como local. Los 2º se sortean como visitantes.")

    if not ts["r4"]["drawn"]:
        st.markdown("### Sorteo Ronda 4")
        firsts = [get_group_ranking(ts["groups"][g])[0][0] for g in "ABCD"]
        seconds = [get_group_ranking(ts["groups"][g])[1][0] for g in "ABCD"]

        st.markdown("**Locales (1º de grupo):**")
        fc = st.columns(4)
        for i, code in enumerate(firsts):
            with fc[i]:
                st.image(TEAMS[code]["logo"], width=48)
                st.caption(f"Llave {['A','B','C','D'][i]}: {TEAMS[code]['name']}")

        st.markdown("**Visitantes (2º de grupo — asigna manualmente o sortea):**")
        second_opts = [f"{code} — {TEAMS[code]['name']}" for code in seconds]
        second_map = {f"{code} — {TEAMS[code]['name']}": code for code in seconds}

        draw_pairs = []
        draw_valid2 = True
        all_sel = []
        dc = st.columns(4)
        for i in range(4):
            with dc[i]:
                lbl = ['A','B','C','D'][i]
                sel = st.selectbox(f"Visitante Llave {lbl}", second_opts, key=f"r4draw_{i}")
                draw_pairs.append((firsts[i], second_map[sel]))
                all_sel.append(second_map[sel])

        if len(set(all_sel)) < 4:
            st.error("⚠️ Cada equipo solo puede estar en una llave.")
            draw_valid2 = False

        rc1, rc2 = st.columns(2)
        with rc1:
            if st.button("🎲 Sorteo Aleatorio R4"):
                sh = seconds[:]
                random.shuffle(sh)
                st.session_state["_r4_rand"] = sh
                st.info("Sugerencia aleatoria generada.")
        with rc2:
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

        st.markdown("---")
        st.markdown("### Resultados")
        render_matches_display(matches, cols=2)

        if all_played and not ts["r4"]["done"]:
            if st.button("✅ Confirmar Ronda 4", type="primary"):
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

    info("Pos 1 vs R4-Llave D · Pos 2 vs R4-Llave C · Pos 3 vs R4-Llave B · Pos 4 vs R4-Llave A")
    matches = ts["qf"]["matches"]
    all_played = all(m["played"] for m in matches)

    for i, m in enumerate(matches):
        match_entry_form(m, f"qf_{i}", allow_draw=False)

    st.markdown("---")
    render_matches_display(matches, cols=2)

    if all_played and not ts["qf"]["done"]:
        if st.button("✅ Confirmar Cuartos", type="primary"):
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

    st.markdown("---")
    render_matches_display(matches, cols=2)

    if all_played and not ts["sf"]["done"]:
        if st.button("✅ Confirmar Semifinales", type="primary"):
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

    st.markdown("---")
    show_match_result(m)

    if m["played"] and not ts["final"]["done"]:
        if st.button("🏆 Coronar Campeón", type="primary"):
            ts["final"]["done"] = True
            ts["champion_code"] = m["winner_code"]
            persist()
            st.rerun()

    if ts["final"]["done"] and ts["champion_code"]:
        champ = TEAMS[ts["champion_code"]]
        st.markdown(f"""
        <div class="champ-box">
            <div style="font-size:3rem">🏆</div>
            <div class="champ-title">MMJ Emirates Cup Champion</div>
            <img src="{champ['logo']}" width="90" style="margin:10px 0;filter:drop-shadow(0 0 16px rgba(201,168,76,0.5))">
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
        # Podium
        if len(scorers) >= 3:
            medals = ["🥇","🥈","🥉"]
            pod_cols = st.columns(3)
            for i in range(3):
                s = scorers[i]
                with pod_cols[i]:
                    logo = TEAMS[s["team_code"]]["logo"]
                    st.markdown(f"""
                    <div style="background:#1a2035;border:1px solid #2a3050;border-radius:10px;padding:16px;text-align:center">
                        <div style="font-size:2rem">{medals[i]}</div>
                        <img src="{logo}" width="48" style="margin:6px 0;object-fit:contain">
                        <div style="font-family:'Bebas Neue',sans-serif;font-size:2rem;color:#C9A84C">{s['goals']}</div>
                        <div style="font-weight:700;font-size:.9rem">{s['player']}</div>
                        <div style="color:#6b7a9a;font-size:.75rem">{s['team_name']}</div>
                    </div>""", unsafe_allow_html=True)

        st.markdown("### 📋 Tabla Completa")
        rows = [{"#": i+1, "Jugador": s["player"], "Equipo": s["team_name"],
                 "Goles": s["goals"], "Partidos": len(set(s["rounds"]))}
                for i, s in enumerate(scorers)]
        df = pd.DataFrame(rows)
        st.dataframe(df, use_container_width=True, hide_index=True,
                     column_config={
                         "#": st.column_config.NumberColumn(width="small"),
                         "Goles": st.column_config.NumberColumn(width="small"),
                     })

        st.markdown("### 📊 Goles por Equipo")
        from collections import defaultdict
        tg = defaultdict(int)
        for s in scorers:
            tg[s["team_name"]] += s["goals"]
        chart_df = pd.DataFrame(sorted(tg.items(), key=lambda x: -x[1]), columns=["Equipo","Goles"])
        st.bar_chart(chart_df.set_index("Equipo"), color="#C9A84C")

# ── EQUIPOS ───────────────────────────────────────────────────────────
elif page == "🛡 Equipos":
    sec("🛡 Los 30 Clubes", "Dream League Selection")
    search = st.text_input("🔍 Buscar", "")

    gcols = st.columns(3)
    for i, code in enumerate(TEAM_ORDER):
        t = TEAMS[code]
        if search and search.lower() not in t["name"].lower() and search.lower() not in code.lower():
            continue
        with gcols[i % 3]:
            with st.expander(f"#{i+1} {t['name']} ({code})"):
                cc1, cc2 = st.columns([1,3])
                with cc1:
                    st.image(t["logo"], width=64)
                with cc2:
                    st.markdown(f"**{t['name']}**  \nCódigo: `{code}` · Pos: **#{i+1}**")
                st.markdown("**Plantilla:**")
                for p in t["players"]:
                    st.markdown(f"- {p}")
