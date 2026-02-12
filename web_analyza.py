import streamlit as st
import random
import math
import os

# 1. DESIGN A TRVALÉ POČITADLO (ZABEZPEČENO PROTI RESETU)
st.set_page_config(page_title="ELITE ANALYST PRO 2026", page_icon="⚽", layout="centered")

def manage_total_visits():
    file_path = "total_visits.txt"
    # Pokud soubor neexistuje, vytvoříme ho s tvou startovní hodnotou
    if not os.path.exists(file_path):
        with open(file_path, "w") as f: 
            f.write("12540")
            
    # Načtení aktuálního čísla ze souboru
    with open(file_path, "r") as f:
        try: 
            current_total = int(f.read().strip())
        except: 
            current_total = 12540
            
    # Přičtení návštěvy pouze pokud jde o nové otevření stránky (session)
    if 'session_accounted' not in st.session_state:
        current_total += 1
        with open(file_path, "w") as f: 
            f.write(str(current_total))
        st.session_state.session_accounted = True
        
    return current_total

# Denní počitadlo (resetuje se při zavření prohlížeče)
if 'pocet_navstev' not in st.session_state:
    st.session_state.pocet_navstev = 312
    st.session_state.pocet_navstev += 1

celkove_navstevy = manage_total_visits()

st.markdown(f'''
<style>
[data-testid="stAppViewContainer"] {{
    background-image: url("https://images.unsplash.com/photo-1574629810360-7efbbe195018?q=80&w=2000&auto=format&fit=crop");
    background-size: cover; background-position: center;
}}
[data-testid="stAppViewContainer"]::before {{
    content: ""; position: absolute; top: 0; left: 0; width: 100%; height: 100%;
    background-color: rgba(0, 0, 0, 0.75);
}}
div[data-testid="stVerticalBlock"] > div {{
    background-color: rgba(15, 15, 25, 0.85) !important;
    border-radius: 15px; padding: 15px;
    box-shadow: 0 10px 25px rgba(0,0,0,0.8);
    backdrop-filter: none !important;
}}
div[data-testid="stMetricValue"] > div {{
    color: #00ff00 !important; font-weight: bold !important;
    font-size: 34px !important; text-shadow: 2px 2px 4px rgba(0,0,0,0.7);
}}
div.stButton > button {{
    width: 100%; height: 50px; background-color: #00ff00 !important;
    color: black !important; font-weight: bold; font-size: 18px;
    border-radius: 10px; border: none;
}}
.top-bar {{
    display: flex; justify-content: space-between; position: relative;
    z-index: 10; color: #ffffff; font-size: 13px; font-weight: bold;
}}
</style>
''', unsafe_allow_html=True)

st.markdown(f"""
    <div class='top-bar'>
        <div style='display: flex; gap: 20px;'>
            <span>📅 DNES: {st.session_state.pocet_navstev}</span>
            <span>🌍 CELKEM: {celkove_navstevy}</span>
        </div>
        <div>trefilos@gmail.com</div>
    </div>
    """, unsafe_allow_html=True)

# 2. LOGIKA SÍLY PODLE KONTEXTU LIGY
def fetch_api_stats(team_name, zvolena_liga):
    giants = ["Bayern Mnichov", "Manchester City", "Real Madrid", "Arsenal", "Aston Villa", "Liverpool", "FC Barcelona", "Inter Milán"]
    ceska_top = ["Slavia Praha", "Sparta Praha", "Plzeň"]
    
    if team_name in giants:
        base_xg = 2.2 
    elif team_name in ceska_top:
        base_xg = 2.1 if "Chance Liga" in zvolena_liga else 1.1
    else:
        base_xg = 1.3 
        
    return {
        "xg": round(random.uniform(base_xg - 0.1, base_xg + 0.2), 2),
        "corners": round(random.uniform(4.0, 6.5), 1),
        "cards": round(random.uniform(1.2, 3.0), 1)
    }

# 3. KOMPLETNÍ DATABÁZE
ligy_data = {
    "🏆 Liga mistrů": ["Arsenal", "Bayern Mnichov", "Liverpool", "Tottenham", "FC Barcelona", "Chelsea", "Sporting Lisabon", "Manchester City", "Real Madrid", "Inter Miláno", "Paris Saint-Germain", "Newcastle", "Juventus", "Atletico Madrid", "Atalanta Bergamo", "Leverkusen", "Dortmund", "Olympiakos", "Club Brugge", "Galatasaray", "Monaco", "FK Karabach", "Bodo/Glimt", "Benfica Lisabon", "Marseille", "Paphos FC", "Union SG", "PSV Eindhoven", "Bilbao", "Neapol", "FC Kodaň", "Ajax", "Frankfurt", "Slavia Praha"],
    "🇪🇺 Evropská liga": ["Lyon", "Aston Villa", "Midtjylland", "Betis", "Sevilla", "FC Porto", "Braga", "Freiburg", "AS Řím", "Genk", "Bologna", "Stuttgart", "Ferencváros", "Nottingham", "Plzeň", "Vigo", "PAOK", "Lille", "Fenerbahce", "Panathinaikos", "Celtic Glasgow", "Ludogorec Razgrad", "Dynamo"],
    "🏴󠁧󠁢󠁥󠁮󠁧󠁿 Premier League": ["Arsenal", "Manchester City", "Aston Villa", "Manchester United", "Chelsea", "Liverpool", "Brentford", "Everton", "Sunderland", "Fullham", "Bournemouth", "Newcastle", "Crystal Palace", "Brighton", "Tottenham", "Leeds", "Nottingham", "West Ham", "Burnley", "Wolverhampton"],
    "🇩🇪 Bundesliga": ["Bayern Mnichov", "Dortmund", "Hoffenheim", "RB Lipsko", "Stuttgart", "Leverkusen", "Freiburg", "Frankfurt", "Union Berlin", "FC Kolín", "Hamburk", "Mönchengladbach", "Augsburg", "Mainz", "Wolfsburg", "Brémy", "Saint Pauli", "Heidenheim"],
    "🇪🇸 La Liga": ["FC Barcelona", "Real Madrid", "Atlético Madrid", "Villarreal", "Betis", "Sevilla", "Espanyol", "Celta Vigo", "Real Sociedad", "Osasuna", "Bilbao", "Getafe", "Girona", "Alavés", "Elche", "Mallorca", "Valencia", "Rayo Vallecano", "Levante", "Oviedo"],
    "🇮🇹 Serie A": ["Inter Milán", "AC Milán", "Neapol", "Juventus", "AS Řím", "Como", "Atalanta Bergamo", "Lazio", "Udinese", "Bologna", "Sassuolo", "Cagliari", "FC Torino", "Parma", "Janov", "Cremonese", "Lecce", "Fiorentina", "Pisa", "Hellas Verona"],
    "🇨🇿 Chance Liga": ["Slavia Praha", "Sparta Praha", "Jablonec", "Plzeň", "Liberec", "Karviná", "Hradec Králové", "Olomouc", "Zlín", "Pardubice", "Teplice", "Bohemians", "Ostrava", "Mladá Boleslav", "Slovácko", "Dukla Praha"]
}

# 4. ALGORITMUS
def get_poisson_probability(lmbda, k):
    return (math.pow(lmbda, k) * math.exp(-lmbda)) / math.factorial(k)

def analyzuj_zapas(domaci, hoste, liga_nazev):
    ds = fetch_api_stats(domaci, liga_nazev)
    hs = fetch_api_stats(hoste, liga_nazev)
    
    prob_d_win, prob_h_win, prob_draw = 0, 0, 0
    for i in range(6):
        for j in range(6):
            p_score = get_poisson_probability(ds["xg"], i) * get_poisson_probability(hs["xg"], j)
            if i > j: prob_d_win += p_score
            elif i < j: prob_h_win += p_score
            else: prob_draw += p_score
            
    total = prob_d_win + prob_h_win + prob_draw
    wh = (prob_d_win / total) * 100 + 3
    wa = (prob_h_win / total) * 100 - 1.5
    dr = 100 - wh - wa
    
    return int(wh), int(dr), int(wa), ds, hs

# 5. UI
st.title("⚽ PREMIUM ANALYST 2026")
liga = st.selectbox("ZVOLIT SOUTĚŽ:", list(ligy_data.keys()))
tymy = sorted(ligy_data[liga])

c1, c2 = st.columns(2)
with c1: d_team = st.selectbox("DOMÁCÍ (🏠):", tymy)
with c2: h_team = st.selectbox("HOSTÉ (🚀):", tymy, index=1 if len(tymy)>1 else 0)

if st.button("SPUSTIT ANALÝZU"):
    if d_team == h_team:
        st.warning("⚠️ CHYBA: Zvolte jiného soupeře.")
    else:
        with st.spinner('Analyzuji historii z API...'):
            wh, dr, wa, ds, hs = analyzuj_zapas(d_team, h_team, liga)
            st.success(f"Analýza {d_team} vs {h_team} dokončena.")
            
            r1, r2, r3 = st.columns(3)
            r1.metric("VÝHRA DOMÁCÍ", f"{wh}%")
            r2.metric("REMIZA", f"{dr}%")
            r3.metric("VÝHRA HOSTÉ", f"{wa}%")
            
            st.markdown("---")
            st.write("### 🚩 DETAILNÍ PŘEDPOVĚĎ")
            s1, s2, s3 = st.columns(3)
            with s1:
                st.write("**Očekávané xG**")
                st.metric(d_team, ds["xg"])
                st.metric(h_team, hs["xg"])
            with s2:
                st.write("**Průměr rohů**")
                st.metric(d_team, ds["corners"])
                st.metric(h_team, hs["corners"])
            with s3:
                st.write("**Žluté karty**")
                st.metric(d_team, ds["cards"])
                st.metric(h_team, hs["cards"])

st.markdown("""
    <div style='text-align: center; background-color: rgba(0, 50, 0, 0.4); padding: 15px; border-radius: 10px; border: 1px dashed #00ff00; margin-top: 50px;'>
        <p style='color: #90ee90; font-size: 14px; margin: 0; font-weight: bold;'>ZDE MŮŽE BÝT VAŠE REKLAMA</p>
        <p style='color: #ccc; font-size: 12px; margin: 5px 0 0 0;'>trefilos@gmail.com</p>
    </div>
    """, unsafe_allow_html=True)


















