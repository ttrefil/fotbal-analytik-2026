import streamlit as st
import requests
from datetime import datetime

# --- KONFIGURACE (Stejná jako v PC verzi) ---
API_KEY = "bffbce6e64e1e0d8d8bfc1276b8f8436"
HEADERS = {"x-apisports-key": API_KEY}
BASE_URL = "https://v3.football.api-sports.io/"

LEAGUES = {
    "🇨🇿 Česko (Chance Liga)": {"id": "305", "teams": {"Sparta Praha": 558, "Slavia Praha": 555, "Viktoria Plzeň": 567, "Baník Ostrava": 571, "Jablonec": 566, "Mladá Boleslav": 560, "Slovan Liberec": 559, "Sigma Olomouc": 568, "Hradec Králové": 2244, "Teplice": 570, "Bohemians 1905": 557, "Slovácko": 562, "Karviná": 2245, "Pardubice": 2243, "České Budějovice": 569, "Dukla Praha": 556}},
    "🏴󠁧󠁢󠁥󠁮󠁧󠁿 Anglie (Premier League)": {"id": "39", "teams": {"Arsenal": 42, "Aston Villa": 66, "Bournemouth": 35, "Brentford": 55, "Brighton": 51, "Chelsea": 49, "Crystal Palace": 52, "Everton": 45, "Fulham": 36, "Ipswich": 57, "Leicester": 46, "Liverpool": 40, "Manchester City": 50, "Manchester United": 33, "Newcastle": 34, "Nottingham Forest": 65, "Southampton": 41, "Tottenham": 47, "West Ham": 48, "Wolves": 39}},
    "🇪🇸 Španělsko (La Liga)": {"id": "140", "teams": {"Alavés": 542, "Athletic Bilbao": 531, "Atlético Madrid": 530, "Barcelona": 529, "Betis": 543, "Celta Vigo": 538, "Espanyol": 540, "Getafe": 546, "Girona": 547, "Las Palmas": 537, "Leganés": 545, "Mallorca": 798, "Osasuna": 542, "Rayo Vallecano": 544, "Real Madrid": 541, "Real Sociedad": 548, "Sevilla": 536, "Valencia": 532, "Valladolid": 549, "Villarreal": 533}},
    "🇩🇪 Německo (Bundesliga)": {"id": "78", "teams": {"Augsburg": 170, "Bayern Mnichov": 157, "Bochum": 176, "Werder Brémy": 162, "Dortmund": 165, "Frankfurt": 169, "Freiburg": 160, "Heidenheim": 181, "Hoffenheim": 167, "Holstein Kiel": 192, "RB Lipsko": 173, "Leverkusen": 168, "Mainz": 164, "Mönchengladbach": 163, "St. Pauli": 186, "Stuttgart": 188, "Union Berlín": 182, "Wolfsburg": 161}},
    "🇮🇹 Itálie (Serie A)": {"id": "135", "teams": {"Atalanta": 499, "Bologna": 505, "Cagliari": 490, "Como": 521, "Empoli": 511, "Fiorentina": 502, "Genoa": 495, "Inter Milán": 496, "Juventus": 492, "Lazio": 487, "Lecce": 498, "AC Milán": 489, "Monza": 1579, "Napoli": 492, "Parma": 523, "AS Řím": 497, "Torino": 503, "Udinese": 494, "Venezia": 517, "Verona": 504}},
    "🏆 Liga mistrů": {"id": "2", "teams": {}}
}

# --- POMOCNÉ FUNKCE (Zůstávají stejné jako v PC verzi) ---
def get_h2h_data(id_h, id_a):
    try:
        res = requests.get(f"{BASE_URL}fixtures/headtohead", headers=HEADERS, params={"h2h": f"{id_h}-{id_a}"}, timeout=8).json()
        matches = res.get('response', [])
        recent = matches[-5:] if len(matches) > 5 else matches
        if not recent: return 0.5, 0, 1.0, 1.0
        pts = sum(3 if (m['teams']['home']['winner'] if m['teams']['home']['id'] == id_h else m['teams']['away']['winner']) is True else (1 if m['teams']['home']['winner'] is None else 0) for m in recent)
        gh = sum(m['goals']['home'] if m['teams']['home']['id'] == id_h else m['goals']['away'] for m in recent)
        ga = sum(m['goals']['away'] if m['teams']['home']['id'] == id_h else m['goals']['home'] for m in recent)
        return (pts / (len(recent) * 3)), len(recent), gh/len(recent), ga/len(recent)
    except: return 0.5, 0, 1.0, 1.0

def get_form_stats(t_id, l_id):
    for sn in ["2024", "2023"]:
        try:
            res = requests.get(f"{BASE_URL}fixtures", headers=HEADERS, params={"league": l_id, "season": sn, "team": t_id, "last": 10}, timeout=8).json()
            matches = res.get('response', [])
            if matches:
                count = len(matches)
                pts = sum(3 if (m['teams']['home']['winner'] if m['teams']['home']['id'] == t_id else m['teams']['away']['winner']) is True else (1 if m['teams']['home']['winner'] is None else 0) for m in matches)
                gs = sum(m['goals']['home'] if m['teams']['home']['id'] == t_id else m['goals']['away'] for m in matches)
                gc = sum(m['goals']['away'] if m['teams']['home']['id'] == t_id else m['goals']['home'] for m in matches)
                return pts / (count * 3), gs / count, gc / count
        except: continue
    return 0.5, 1.2, 1.2

# --- WEBSTRÁNKA (Streamlit rozhraní) ---
st.set_page_config(page_title="Pro Analytik 2026", page_icon="⚽")
st.title("⚽ PREMIUM FOOTBALL ANALYST 2026")
st.write("Profesionální analýza fotbalových zápasů v prohlížeči")

# Výběr soutěže
league_name = st.selectbox("ZVOLTE SOUTĚŽ", list(LEAGUES.keys()))

# Příprava týmů pro vybranou ligu
if league_name == "🏆 Liga mistrů":
    all_teams_map = {}
    for l in LEAGUES.values(): all_teams_map.update(l["teams"])
    teams_list = sorted(list(all_teams_map.keys()))
    current_teams_map = all_teams_map
else:
    teams_list = sorted(list(LEAGUES[league_name]["teams"].keys()))
    current_teams_map = LEAGUES[league_name]["teams"]

# Výběr týmů
col1, col2 = st.columns(2)
with col1:
    team_h = st.selectbox("DOMÁCÍ TÝM (🏠)", teams_list)
with col2:
    team_a = st.selectbox("HOSTUJÍCÍ TÝM (✈️)", teams_list, index=1 if len(teams_list)>1 else 0)

if st.button("GENEROVAT ANALÝZU", type="primary"):
    if team_h == team_a:
        st.error("Vyberte dva různé týmy!")
    else:
        with st.spinner('Stahuji data z API...'):
            id_h = current_teams_map[team_h]
            id_a = current_teams_map[team_a]
            l_id = LEAGUES[league_name]["id"]

            f_h, gs_h, gc_h = get_form_stats(id_h, l_id)
            f_a, gs_a, gc_a = get_form_stats(id_a, l_id)
            h2h_s, h2h_c, h2h_gh, h2h_ga = get_h2h_data(id_h, id_a)

            # --- MATEMATIKA (Ta tvoje opravená) ---
            raw_h = (f_h * 40) + (h2h_s * 40) + 10
            raw_a = (f_a * 40) + ((1 - h2h_s) * 40)
            diff = abs(raw_h - raw_a)
            px = 35 - (diff * 0.5)
            total = raw_h + raw_a + px

            xg_h = (gs_h + gc_a + h2h_gh) / 3 if h2h_c > 0 else (gs_h + gc_a) / 2
            xg_a = (gs_a + gc_h + h2h_ga) / 3 if h2h_c > 0 else (gs_a + gc_h) / 2

            # --- ZOBRAZENÍ VÝSLEDKŮ ---
            st.divider()
            st.subheader(f"📊 Výsledek: {team_h} vs {team_a}")
            
            c1, c2, c3 = st.columns(3)
            c1.metric("Domácí", f"{(raw_h/total)*100:.1f} %")
            c2.metric("Remíza", f"{(px/total)*100:.1f} %")
            c3.metric("Hosté", f"{(raw_a/total)*100:.1f} %")

            st.info(f"⚽ **Očekávané skóre (xG):** {team_h} **{xg_h:.2f}** : **{xg_a:.2f}** {team_a}")
            st.write(f"📝 Bilance: {h2h_c} zápasů | Analyzováno: {datetime.now().strftime('%d.%m. %H:%M')}")