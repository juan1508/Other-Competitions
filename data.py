# data.py — MMJ Emirates Cup
TEAM_ORDER = [
    "LAFC","SEA","MIN","VAN","COL","NHS","CLB","SDFC",
    "ATX","CHI","NE","ORL","LA","SKC","CLT","MIA",
    "NYC","RSL","TOR","MTL","DAL","POR","HOU","STL",
    "ATL","PHI","DCU","RBNY","CIN","SJ"
]

TEAMS = {
    "LAFC": {
        "name": "Los Angeles FC",
        "logo": "https://a.espncdn.com/guid/090bf04b-bafb-ac27-0cc5-3fee8a7375ca/logos/primary_logo_on_black_color.png",
        "players": ["U. Simón","J. Musiala","Rodrygo","J. Brandt","P. Dybala","K. Mbappé","P. Hincapié","N. Madueke","J. Enciso","Y. Asprilla"]
    },
    "SEA": {
        "name": "Seattle Sounders",
        "logo": "https://a.espncdn.com/guid/c847331a-0291-a79c-5b8e-22416f8fe26a/logos/primary_logo_on_black_color.png",
        "players": ["Ederson","J. Tah","L. Messi","E. Haaland","J. Bynoe-Gittens","G. Puerta","O. Bobb","J. Durán"]
    },
    "MIN": {
        "name": "Minnesota United",
        "logo": "https://a.espncdn.com/combiner/i?img=/i/teamlogos/soccer/500/17362.png",
        "players": ["G. Mamardashvili","F. Kessié","Raphinha","M. Llorente","J. Maddison","Moleiro","Nico González","Fermín","Marc Guiu"]
    },
    "VAN": {
        "name": "Vancouver Whitecaps",
        "logo": "https://a.espncdn.com/combiner/i?img=/i/teamlogos/soccer/500/9727.png",
        "players": ["N. Pope","R. Andrich","R. Mahrez","Nico Williams","D. Malen","R. Gravenberch","T. Lamptey","A. Pavlovic","K. Gordon"]
    },
    "COL": {
        "name": "Colorado Rapids",
        "logo": "https://a.espncdn.com/i/teamlogos/soccer/500/184.png",
        "players": ["G. Ochoa","João Cancelo","H. Kane","M. Olise","C. Lukeba","T. Gulliksen","R. Bardghji"]
    },
    "NHS": {
        "name": "Nashville SC",
        "logo": "https://a.espncdn.com/i/teamlogos/soccer/500/18986.png",
        "players": ["M. Maignan","N. Schlotterbeck","F. Torres","L. Díaz","A. Davies","L. Romero","A. Scott","Pau Cubarsí","J. Duranville"]
    },
    "CLB": {
        "name": "Columbus Crew",
        "logo": "https://a.espncdn.com/combiner/i?img=/i/teamlogos/soccer/500/183.png",
        "players": ["M. Neuer","E. Tapsoba","Pedri","L. Sané","A. Hložek","Fábio Carvalho","Y. Eduardo","O. Diomande"]
    },
    "SDFC": {
        "name": "San Diego FC",
        "logo": "https://a.espncdn.com/combiner/i?img=/i/teamlogos/soccer/500/22529.png",
        "players": ["L. Hrádecký","R. James","D. Szoboszlai","J. Álvarez","S. Gnabry","H. Elliott","F. Pellistri","Marc Casadó","B. Domínguez"]
    },
    "ATX": {
        "name": "Austin FC",
        "logo": "https://a.espncdn.com/guid/ea2b097a-74d8-3164-b55e-7fd490d63b46/logos/primary_logo_on_primary_color.png",
        "players": ["G. Rulli","N. Barella","H. Son","Vini Jr.","Marquinhos","R. Lewis","E. Millot","V. Barco","B. Doak"]
    },
    "CHI": {
        "name": "Chicago Fire",
        "logo": "https://a.espncdn.com/i/teamlogos/soccer/500/182.png",
        "players": ["J. Oblak","R. Sterling","İ. Gündoğan","K. Kvaratskhelia","X. Simons","L. Badé","P. Wanner","P. Brunner"]
    },
    "NE": {
        "name": "New England Revolution",
        "logo": "https://a.espncdn.com/combiner/i?img=/i/teamlogos/soccer/500/189.png",
        "players": ["A. Lopes","A. Rüdiger","F. Valverde","T. Kubo","K. Benzema","J. Doku","Yeremy Pino","A. Gray","A. Gómez"]
    },
    "ORL": {
        "name": "Orlando City",
        "logo": "https://a.espncdn.com/combiner/i?img=/i/teamlogos/soccer/500/12011.png",
        "players": ["P. Gulácsi","A. Rabiot","M. Depay","J. Koundé","A. Balde","A. Ezzalzouli","D. Moreira","L. Miley"]
    },
    "LA": {
        "name": "LA Galaxy",
        "logo": "https://a.espncdn.com/combiner/i?img=/i/teamlogos/soccer/500/187.png",
        "players": ["M. ter Stegen","V. van Dijk","L. Modrić","Rafael Leão","J. Frimpong","K. Coman","P. Barrios","N. Zalewski","Á. Alarcón","G. Scalvini"]
    },
    "SKC": {
        "name": "Sporting Kansas City",
        "logo": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/09/Sporting_Kansas_City_logo.svg/1280px-Sporting_Kansas_City_logo.svg.png",
        "players": ["T. Courtois","Kim Min Jae","F. de Jong","T. Alexander-Arnold","H. Ekitike","C. Medina","Afonso Moreira","M. Tel"]
    },
    "CLT": {
        "name": "Charlotte FC",
        "logo": "https://a.espncdn.com/combiner/i?img=/i/teamlogos/soccer/500/21300.png&h=200&w=200",
        "players": ["A. Onana","A. Laporte","V. Osimhen","R. Araujo","João Félix","Stefan Bajcetic","L. Abada","C. Bradley","C. Cassano"]
    },
    "MIA": {
        "name": "Inter Miami",
        "logo": "https://a.espncdn.com/combiner/i?img=/i/teamlogos/soccer/500/20232.png",
        "players": ["Alisson","Casemiro","C. Nkunku","Rúben Dias","Neymar Jr","G. Reyna","B. Castro","O. Cortés","K. Páez"]
    },
    "NYC": {
        "name": "New York City FC",
        "logo": "https://a.espncdn.com/guid/d902d6f8-8673-29e3-15d9-3ef4c12ce9d0/logos/primary_logo_on_primary_color.png",
        "players": ["K. Navas","M. de Ligt","N. Okafor","J. Bellingham","T. Baldanzi","Talles Magno","E. Mbappé","I. Babadi"]
    },
    "RSL": {
        "name": "Real Salt Lake",
        "logo": "https://a.espncdn.com/combiner/i?img=/i/teamlogos/soccer/500/4771.png",
        "players": ["Y. Bounou","N. Süle","Diogo Jota","M. Ødegaard","A. Meret","O. Dembélé","Gonçalo Inácio","S. Magassa","R. Cherki","B. Norton-Cuffy"]
    },
    "TOR": {
        "name": "Toronto FC",
        "logo": "https://a.espncdn.com/i/teamlogos/soccer/500/7318.png",
        "players": ["G. Donnarumma","Éder Militão","Á. Di María","Rodri","J. Grealish","N. Rovella","D. Udogie","D. Washington","Ângelo"]
    },
    "MTL": {
        "name": "CF Montreal",
        "logo": "https://a.espncdn.com/combiner/i?img=/i/teamlogos/soccer/500/9720.png",
        "players": ["E. Martínez","S. Milinković-Savić","Bruno Fernandes","S. Chukwueze","R. Lewandowski","D. Alaba","Antony","R. Højlund","T. Pembélé","Y. Moukoko","Matheus França"]
    },
    "DAL": {
        "name": "FC Dallas",
        "logo": "https://a.espncdn.com/guid/fa2f128b-c698-3d43-2910-5561f4442748/logos/primary_logo_on_primary_color.png",
        "players": ["M. Flekken","Brahim","S. Mané","E. Fernández","Bernardo Silva","C. Palmer","A. Velasco","K. Yıldız","S. Charles"]
    },
    "POR": {
        "name": "Portland Timbers",
        "logo": "https://a.espncdn.com/guid/67f3641d-0e73-f4c3-39ca-e0ad4020d315/logos/secondary_logo_on_black_color.png",
        "players": ["W. Szczęsny","F. Tomori","J. Kimmich","L. Martínez","Gavi","Vitor Roque","Héctor Fort","I. Fresneda"]
    },
    "HOU": {
        "name": "Houston Dynamo",
        "logo": "https://a.espncdn.com/combiner/i?img=/i/teamlogos/soccer/500/6077.png",
        "players": ["G. Kobel","K. Trippier","G. Martinelli","K. Havertz","L. Goretzka","F. Chiesa","Ansu Fati","A. Kalimuendo","S. Pafundi","D. Doué"]
    },
    "STL": {
        "name": "St. Louis City",
        "logo": "https://a.espncdn.com/combiner/i?img=/i/teamlogos/soccer/500/21812.png",
        "players": ["J. Pickford","Sergio Ramos","H. Lozano","K. Adeyemi","M. Hummels","António Silva","M. Thiaw","C. Chukwuemeka","B. El Khannouss"]
    },
    "ATL": {
        "name": "Atlanta United",
        "logo": "https://a.espncdn.com/i/teamlogos/soccer/500-dark/18418.png",
        "players": ["Y. Sommer","T. Hernández","B. Saka","K. De Bruyne","M. Salah","K. Casteels","J. Castrop","B. Brobbey","M. Soulé","W. Zaïre-Emery"]
    },
    "PHI": {
        "name": "Philadelphia Union",
        "logo": "https://a.espncdn.com/combiner/i?img=/i/teamlogos/soccer/500/10739.png",
        "players": ["A. Ramsdale","K. Walker","M. Diaby","C. Gakpo","P. Foden","A. Lafont","B. Barcola","Q. Sullivan","Iker Bravo","T. Land"]
    },
    "DCU": {
        "name": "DC United",
        "logo": "https://a.espncdn.com/combiner/i?img=/i/teamlogos/soccer/500/193.png",
        "players": ["É. Mendy","A. Griezmann","L. Paqueta","Grimaldo","A. Hakimi","M. Rashford","A. Correa","Sávio","A. Richardson","C. Echeverri","J. Hato"]
    },
    "RBNY": {
        "name": "New York Red Bulls",
        "logo": "https://a.espncdn.com/combiner/i?img=/i/teamlogos/soccer/500/190.png&h=200&w=200",
        "players": ["Diogo Costa","Gabriel","Cristiano Ronaldo","A. Robertson","Peter","K. Mainoo","V. Carboni","A. van Axel Dongen"]
    },
    "CIN": {
        "name": "FC Cincinnati",
        "logo": "https://a.espncdn.com/i/teamlogos/soccer/500/18267.png",
        "players": ["H. Lloris","Gabriel Jesús","N. Kanté","G. Xhaka","S. Haller","A. Garnacho","M. Kerkez","M. Del Blanco","Y. Bonny"]
    },
    "SJ": {
        "name": "San Jose Earthquakes",
        "logo": "https://a.espncdn.com/i/teamlogos/soccer/500/191.png",
        "players": ["Alex Remiro","D. Silva","D. Rice","R. Kolo Muani","F. Wirtz","A. Güler","M. Caicedo","Newerton","E. Ferguson"]
    }
}

def get_by_pos(pos):
    code = TEAM_ORDER[pos - 1]
    t = TEAMS[code].copy()
    t["code"] = code
    return t

def get_team(code):
    t = TEAMS[code].copy()
    t["code"] = code
    return t
