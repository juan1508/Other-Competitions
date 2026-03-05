# state.py — Persist tournament state to a local JSON file
import json, os, copy
from data import get_by_pos, get_team, TEAMS, TEAM_ORDER

SAVE_FILE = "tournament_state.json"

# ── Default empty match ──────────────────────────────────────────────
def empty_match(label, home_code, away_code):
    return {
        "label": label,
        "home_code": home_code,
        "away_code": away_code,
        "home_score": None,
        "away_score": None,
        "scorers": [],   # list of {"player": str, "team_code": str, "minute": int}
        "played": False,
        "winner_code": None,
    }

def enrich(m):
    """Attach full team dicts to a match dict (not stored, only in memory)."""
    m = dict(m)
    m["home"] = get_team(m["home_code"])
    m["away"] = get_team(m["away_code"])
    if m["winner_code"]:
        m["winner"] = get_team(m["winner_code"])
    else:
        m["winner"] = None
    return m

# ── Build initial skeleton ────────────────────────────────────────────
def build_skeleton():
    return {
        "phase": "r1",          # current active phase
        "r1": {
            "matches": [
                empty_match("Llave M", TEAM_ORDER[27], TEAM_ORDER[28]),  # pos28 vs pos29
                empty_match("Llave N", TEAM_ORDER[26], TEAM_ORDER[29]),  # pos27 vs pos30
            ],
            "done": False
        },
        "r2": {
            "matches": [],   # built after r1
            "done": False
        },
        "groups": {
            "drawn": False,
            "done": False,
            "assignment": {},   # {"A": [code1,code2], ...} — the 2 drawn teams per group
            "A": {"matches": [], "standing": {}},
            "B": {"matches": [], "standing": {}},
            "C": {"matches": [], "standing": {}},
            "D": {"matches": [], "standing": {}},
        },
        "r4": {
            "matches": [],
            "drawn": False,
            "done": False
        },
        "qf": {
            "matches": [],
            "done": False
        },
        "sf": {
            "matches": [],
            "done": False
        },
        "final": {
            "match": None,
            "done": False
        },
        "champion_code": None,
    }

# ── Persistence ───────────────────────────────────────────────────────
def save(state):
    with open(SAVE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)

def load():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return build_skeleton()

def reset():
    s = build_skeleton()
    save(s)
    return s

# ── R2 initializer ────────────────────────────────────────────────────
GROUP_SEEDS = {
    "A": [TEAM_ORDER[4], TEAM_ORDER[8]],   # pos5, pos9
    "B": [TEAM_ORDER[5], TEAM_ORDER[9]],   # pos6, pos10
    "C": [TEAM_ORDER[6], TEAM_ORDER[10]],  # pos7, pos11
    "D": [TEAM_ORDER[7], TEAM_ORDER[11]],  # pos8, pos12
}

def build_r2(r1_matches):
    win_m = r1_matches[0]["winner_code"]
    win_n = r1_matches[1]["winner_code"]
    return [
        empty_match("Llave E", TEAM_ORDER[12], win_n),   # pos13 vs winN
        empty_match("Llave F", TEAM_ORDER[13], win_m),   # pos14 vs winM
        empty_match("Llave G", TEAM_ORDER[14], TEAM_ORDER[20]),
        empty_match("Llave H", TEAM_ORDER[15], TEAM_ORDER[21]),
        empty_match("Llave I", TEAM_ORDER[16], TEAM_ORDER[22]),
        empty_match("Llave J", TEAM_ORDER[17], TEAM_ORDER[23]),
        empty_match("Llave K", TEAM_ORDER[18], TEAM_ORDER[24]),
        empty_match("Llave L", TEAM_ORDER[19], TEAM_ORDER[25]),
    ]

def build_groups(assignment):
    """assignment = {"A": [code1,code2], "B": [...], ...}"""
    groups = {}
    for g, extra in assignment.items():
        seeds = GROUP_SEEDS[g]
        teams = seeds + extra  # 4 teams
        matches = []
        for i in range(len(teams)):
            for j in range(i+1, len(teams)):
                matches.append(empty_match(f"G{g}: {TEAMS[teams[i]]['name']} vs {TEAMS[teams[j]]['name']}", teams[i], teams[j]))
        standing = {code: {"pts":0,"pj":0,"w":0,"d":0,"l":0,"gf":0,"ga":0} for code in teams}
        groups[g] = {"matches": matches, "standing": standing}
    return groups

def build_r4(groups_state, draw_order):
    """draw_order: list of (first_code, second_code) per llave A-D"""
    labels = ["Llave A (R4)","Llave B (R4)","Llave C (R4)","Llave D (R4)"]
    return [empty_match(labels[i], draw_order[i][0], draw_order[i][1]) for i in range(4)]

def build_qf(r4_matches):
    # Pos1 vs LlaveD-winner, Pos2 vs LlaveC, Pos3 vs LlaveB, Pos4 vs LlaveA
    return [
        empty_match("Cuartos A — Pos1", TEAM_ORDER[0], r4_matches[3]["winner_code"]),
        empty_match("Cuartos B — Pos2", TEAM_ORDER[1], r4_matches[2]["winner_code"]),
        empty_match("Cuartos C — Pos3", TEAM_ORDER[2], r4_matches[1]["winner_code"]),
        empty_match("Cuartos D — Pos4", TEAM_ORDER[3], r4_matches[0]["winner_code"]),
    ]

def build_sf(qf_matches):
    return [
        empty_match("Semifinal 1", qf_matches[0]["winner_code"], qf_matches[2]["winner_code"]),
        empty_match("Semifinal 2", qf_matches[1]["winner_code"], qf_matches[3]["winner_code"]),
    ]

def build_final(sf_matches):
    return empty_match("🏆 Gran Final", sf_matches[0]["winner_code"], sf_matches[1]["winner_code"])

# ── Standings recalculator ────────────────────────────────────────────
def recalc_group_standing(group_state):
    standing = {code: {"pts":0,"pj":0,"w":0,"d":0,"l":0,"gf":0,"ga":0}
                for code in group_state["standing"].keys()}
    for m in group_state["matches"]:
        if not m["played"]: continue
        h, a = m["home_code"], m["away_code"]
        hs, as_ = m["home_score"], m["away_score"]
        standing[h]["pj"] += 1; standing[a]["pj"] += 1
        standing[h]["gf"] += hs; standing[h]["ga"] += as_
        standing[a]["gf"] += as_; standing[a]["ga"] += hs
        if hs > as_:
            standing[h]["pts"] += 3; standing[h]["w"] += 1; standing[a]["l"] += 1
        elif hs < as_:
            standing[a]["pts"] += 3; standing[a]["w"] += 1; standing[h]["l"] += 1
        else:
            standing[h]["pts"] += 1; standing[h]["d"] += 1
            standing[a]["pts"] += 1; standing[a]["d"] += 1
    return standing

def get_group_ranking(group_state):
    st = recalc_group_standing(group_state)
    return sorted(st.items(), key=lambda x: (-x[1]["pts"], -(x[1]["gf"]-x[1]["ga"]), -x[1]["gf"]))

# ── Scorer aggregation ────────────────────────────────────────────────
def collect_all_scorers(state):
    from collections import defaultdict
    stats = defaultdict(lambda: {"player":"","team_code":"","team_name":"","goals":0,"rounds":[]})
    all_matches = []
    all_matches += state["r1"]["matches"]
    all_matches += state["r2"]["matches"]
    for g in "ABCD":
        all_matches += state["groups"][g]["matches"]
    all_matches += state["r4"]["matches"]
    all_matches += state["qf"]["matches"]
    all_matches += state["sf"]["matches"]
    if state["final"]["match"]:
        all_matches.append(state["final"]["match"])
    for m in all_matches:
        if not m["played"]: continue
        for sc in m.get("scorers", []):
            key = f"{sc['player']}|{sc['team_code']}"
            stats[key]["player"] = sc["player"]
            stats[key]["team_code"] = sc["team_code"]
            stats[key]["team_name"] = TEAMS[sc["team_code"]]["name"]
            stats[key]["goals"] += 1
            stats[key]["rounds"].append(m["label"])
    return sorted(stats.values(), key=lambda x: -x["goals"])
