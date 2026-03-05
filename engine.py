# engine.py — Tournament logic for MMJ Emirates Cup
import random
from data import get_by_pos, get_team, TEAMS

def rand_score(allow_draw=False):
    """Generate a random scoreline. By default no draws (knockout)."""
    while True:
        h = random.randint(0, 5)
        a = random.randint(0, 5)
        if allow_draw or h != a:
            return h, a

def rand_scorers(home_team, away_team, h_goals, a_goals):
    """Assign random scorers from each team's player list."""
    scorers = []
    h_players = home_team["players"]
    a_players = away_team["players"]
    for _ in range(h_goals):
        p = random.choice(h_players)
        minute = random.randint(1, 90)
        scorers.append({"player": p, "team": home_team["code"], "minute": minute})
    for _ in range(a_goals):
        p = random.choice(a_players)
        minute = random.randint(1, 90)
        scorers.append({"player": p, "team": away_team["code"], "minute": minute})
    scorers.sort(key=lambda x: x["minute"])
    return scorers

def make_match(label, home, away):
    return {
        "label": label,
        "home": home,
        "away": away,
        "home_score": None,
        "away_score": None,
        "scorers": [],
        "played": False,
        "winner": None,
    }

def play_match(match):
    h, a = rand_score(allow_draw=False)
    match["home_score"] = h
    match["away_score"] = a
    match["played"] = True
    match["scorers"] = rand_scorers(match["home"], match["away"], h, a)
    match["winner"] = match["home"] if h > a else match["away"]
    return match

def play_group_match(match):
    h, a = rand_score(allow_draw=True)
    match["home_score"] = h
    match["away_score"] = a
    match["played"] = True
    match["scorers"] = rand_scorers(match["home"], match["away"], h, a)
    if h > a:
        match["winner"] = match["home"]
    elif a > h:
        match["winner"] = match["away"]
    else:
        match["winner"] = None  # draw
    return match

# ──────────────── RONDA 1 ────────────────
def init_r1():
    return [
        make_match("Llave M", get_by_pos(28), get_by_pos(29)),
        make_match("Llave N", get_by_pos(27), get_by_pos(30)),
    ]

def simulate_r1(matches):
    return [play_match(m) for m in matches]

# ──────────────── RONDA 2 ────────────────
def init_r2(r1_matches):
    win_m = r1_matches[0]["winner"]
    win_n = r1_matches[1]["winner"]
    return [
        make_match("Llave E", get_by_pos(13), win_n),
        make_match("Llave F", get_by_pos(14), win_m),
        make_match("Llave G", get_by_pos(15), get_by_pos(21)),
        make_match("Llave H", get_by_pos(16), get_by_pos(22)),
        make_match("Llave I", get_by_pos(17), get_by_pos(23)),
        make_match("Llave J", get_by_pos(18), get_by_pos(24)),
        make_match("Llave K", get_by_pos(19), get_by_pos(25)),
        make_match("Llave L", get_by_pos(20), get_by_pos(26)),
    ]

def simulate_r2(matches):
    return [play_match(m) for m in matches]

# ──────────────── RONDA 3 — GRUPOS ────────────────
GROUP_LETTERS = ["A", "B", "C", "D"]

def get_group_seeds():
    """Returns fixed seeds: pos5-8 (1st seed), pos9-12 (2nd seed) per group"""
    seeds = {}
    for i, g in enumerate(GROUP_LETTERS):
        seeds[g] = [get_by_pos(5 + i), get_by_pos(9 + i)]
    return seeds

def draw_groups(r2_winners):
    """Randomly assign 8 R2 winners into 4 groups, 2 per group."""
    shuffled = r2_winners[:]
    random.shuffle(shuffled)
    assignment = {}
    for i, g in enumerate(GROUP_LETTERS):
        assignment[g] = [shuffled[i * 2], shuffled[i * 2 + 1]]
    return assignment

def init_groups(seeds, draw_assignment):
    """Build full group structure: 4 teams per group, round-robin matches."""
    groups = {}
    for g in GROUP_LETTERS:
        teams = seeds[g] + draw_assignment[g]
        # Round robin: 6 matches
        matches = []
        for i in range(len(teams)):
            for j in range(i + 1, len(teams)):
                matches.append(make_match(f"G{g} — {teams[i]['name']} vs {teams[j]['name']}", teams[i], teams[j]))
        standing = {t["code"]: {"team": t, "pts": 0, "pj": 0, "w": 0, "d": 0, "l": 0, "gf": 0, "ga": 0} for t in teams}
        groups[g] = {"teams": teams, "matches": matches, "standing": standing}
    return groups

def simulate_groups(groups):
    for g in GROUP_LETTERS:
        for m in groups[g]["matches"]:
            play_group_match(m)
            h_code = m["home"]["code"]
            a_code = m["away"]["code"]
            hs = m["home_score"]
            as_ = m["away_score"]
            st = groups[g]["standing"]
            st[h_code]["pj"] += 1; st[a_code]["pj"] += 1
            st[h_code]["gf"] += hs; st[h_code]["ga"] += as_
            st[a_code]["gf"] += as_; st[a_code]["ga"] += hs
            if hs > as_:
                st[h_code]["pts"] += 3; st[h_code]["w"] += 1; st[a_code]["l"] += 1
            elif hs < as_:
                st[a_code]["pts"] += 3; st[a_code]["w"] += 1; st[h_code]["l"] += 1
            else:
                st[h_code]["pts"] += 1; st[h_code]["d"] += 1
                st[a_code]["pts"] += 1; st[a_code]["d"] += 1
    return groups

def get_group_ranking(group):
    st = group["standing"]
    ranked = sorted(st.values(), key=lambda x: (
        -x["pts"], -(x["gf"] - x["ga"]), -x["gf"]
    ))
    return ranked

# ──────────────── RONDA 4 ────────────────
def draw_r4(groups):
    """Draw 2nd place teams against 1st place teams (1st are home)."""
    firsts = [get_group_ranking(groups[g])[0]["team"] for g in GROUP_LETTERS]
    seconds = [get_group_ranking(groups[g])[1]["team"] for g in GROUP_LETTERS]
    shuffled_seconds = seconds[:]
    random.shuffle(shuffled_seconds)
    matches = []
    for i, g in enumerate(GROUP_LETTERS):
        matches.append(make_match(f"Llave {g} (R4)", firsts[i], shuffled_seconds[i]))
    return matches

def simulate_r4(matches):
    return [play_match(m) for m in matches]

# ──────────────── CUARTOS ────────────────
def init_qf(r4_matches):
    # Pos1 v LlaveD, Pos2 v LlaveC, Pos3 v LlaveB, Pos4 v LlaveA
    return [
        make_match("Cuartos A — Pos1 vs Llave D", get_by_pos(1), r4_matches[3]["winner"]),
        make_match("Cuartos B — Pos2 vs Llave C", get_by_pos(2), r4_matches[2]["winner"]),
        make_match("Cuartos C — Pos3 vs Llave B", get_by_pos(3), r4_matches[1]["winner"]),
        make_match("Cuartos D — Pos4 vs Llave A", get_by_pos(4), r4_matches[0]["winner"]),
    ]

def simulate_qf(matches):
    return [play_match(m) for m in matches]

# ──────────────── SEMIFINALES ────────────────
def init_sf(qf_matches):
    # W(A) vs W(C), W(B) vs W(D)
    return [
        make_match("Semifinal 1 — W.A vs W.C", qf_matches[0]["winner"], qf_matches[2]["winner"]),
        make_match("Semifinal 2 — W.B vs W.D", qf_matches[1]["winner"], qf_matches[3]["winner"]),
    ]

def simulate_sf(matches):
    return [play_match(m) for m in matches]

# ──────────────── FINAL ────────────────
def init_final(sf_matches):
    return make_match("🏆 Gran Final", sf_matches[0]["winner"], sf_matches[1]["winner"])

def simulate_final(match):
    return play_match(match)

# ──────────────── SCORERS AGGREGATION ────────────────
def collect_all_scorers(state):
    """Walk through all played matches and collect scorer stats."""
    from collections import defaultdict
    stats = defaultdict(lambda: {"player": "", "team_code": "", "team_name": "", "goals": 0, "matches": []})

    all_matches = []
    if state.get("r1"):
        all_matches += state["r1"]
    if state.get("r2"):
        all_matches += state["r2"]
    if state.get("groups"):
        for g in ["A","B","C","D"]:
            if g in state["groups"]:
                all_matches += state["groups"][g]["matches"]
    if state.get("r4"):
        all_matches += state["r4"]
    if state.get("qf"):
        all_matches += state["qf"]
    if state.get("sf"):
        all_matches += state["sf"]
    if state.get("final") and state["final"]:
        all_matches.append(state["final"])

    for m in all_matches:
        if not m.get("played"):
            continue
        for sc in m.get("scorers", []):
            key = f"{sc['player']}|{sc['team']}"
            stats[key]["player"] = sc["player"]
            stats[key]["team_code"] = sc["team"]
            stats[key]["team_name"] = TEAMS[sc["team"]]["name"]
            stats[key]["goals"] += 1
            stats[key]["matches"].append(m["label"])

    result = sorted(stats.values(), key=lambda x: -x["goals"])
    return result
