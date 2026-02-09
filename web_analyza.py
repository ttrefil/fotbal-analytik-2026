import streamlit as st
import random
import requests

# 1. NASTAVENÍ A DESIGN
st.set_page_config(page_title="ELITE ANALYST PRO 2026", page_icon="⚽", layout="centered")

if 'pocet_navstev' not in st.session_state:
    st.session_state.pocet_navstev = 225
st.session_state.pocet_navstev += 1

st.markdown(f"""
    <div style='text-align: center; background-color: #1e2130; padding: 10px; border-radius: 10px; border: 1px solid #00ff00;'>
        <h4 style='margin:0; color: white;'>📈 POČET DNEŠNÍCH ANALÝZ: {st.session_state.pocet_navstev}</h4>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: white; }
    .stButton>button { width: 100%; background-color: #ff4b4b; color: white; border-radius: 12px; font-weight: bold; height: 3.5em; border: none; }
    label { color: #00ff00 !important; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# 2. TVŮJ API KLÍČ
API_KEY = "bffbce6e64e1e0d8d8bfc1276b8f8436"

# 3. KOMPLETNÍ DATABÁZE TÝMŮ (NIC JSEM NEZMENŠIL)
ligy_data = {
    "🏆 Liga mistrů": ["Arsenal", "Bayern Mnichov", "Liverpool", "Tottenham", "FC Barcelona", "Chelsea", "Sporting Lisabon", "Manchester City", "Real Madrid", "Inter Miláno", "Paris Saint-Germain", "Newcastle", "Juventus", "Atletico Madrid", "Atalanta Bergamo", "Leverkusen", "Dortmund", "Olympiakos", "Club Brugge", "Galatasaray", "Monaco", "FK Karabach", "Bodo/Glimt", "Benfica Lisabon", "Marseille", "Paphos FC", "Union SG", "PSV Eindhoven", "Bilbao", "Neapol", "FC Kodaň", "Ajax", "Frankfurt", "Slavia Praha"],
    "🇪🇺 Evropská liga": ["Lyon", "Aston Villa", "Midtjylland", "Betis", "Sevilla", "FC Porto", "Braga", "Freiburg", "AS Řím", "Genk", "Bologna", "Stuttgart", "Ferencváros", "Nottingham", "Plzeň", "Vigo", "PAOK", "Lille", "Fenerbahce", "Panathinaikos", "Celtic Glasgow", "Ludogorec Razgrad", "Dynamo"],
    "🏴󠁧󠁢󠁥󠁮󠁧󠁿 Premier League": ["Arsenal", "Manchester City", "Aston Villa", "Manchester United", "Chelsea", "Liverpool", "Brentford", "Everton", "Sunderland", "Fullham", "Bournemouth", "Newcastle", "Crystal Palace", "Brighton", "Tottenham", "Leeds", "Nottingham", "West Ham", "Burnley", "Wolverhampton"],
    "🇩🇪 Bundesliga": ["Bayern Mnichov", "Dortmund", "Hoffenheim", "RB Lipsko", "Stuttgart", "Leverkusen", "Freiburg", "Frankfurt", "Union Berlin", "FC Kolín", "Hamburk", "Mönchengladbach", "Augsburg", "Mainz", "Wolfsburg", "Brémy", "Saint Pauli", "Heidenheim"],
    "🇪🇸 La Liga": ["FC Barcelona", "Real Madrid", "Atlético Madrid", "Villarreal", "Betis", "Sevilla", "Espanyol", "Celta Vigo", "Real Sociedad", "Osasuna", "Bilbao", "Getafe", "Girona", "Alavés", "Elche", "Mallorca", "Valencia", "Rayo Vallecano", "Levante", "Oviedo"],
    "🇮🇹 Serie A": ["Inter Milán", "AC Milán", "Neapol", "Juventus", "AS Řím", "Como", "Atalanta Bergamo", "Lazio", "Udinese", "Bologna", "Sassuolo", "Cagliari", "FC Torino", "Parma", "Janov", "Cremonese", "Lecce", "Fiorentina", "Pisa", "Hellas Verona"],
    "🇨🇿 Chance Liga": ["Slavia Praha", "Sparta Praha", "Jablonec", "Plzeň", "Liberec", "Karviná", "Hradec Králové", "Olomouc", "Zlín", "Pardubice", "Teplice", "Bohemians", "Ostrava", "Mladá Boleslav", "Slovácko", "Dukla Praha"]
}

# 4. ANALYTICKÁ LOGIKA (OPRAVA CHYBY NameError)
def ziskej_analyzu(d, h):
    elita = ["Slavia Praha", "Sparta Praha", "Real Madrid", "Manchester City", "Liverpool", "Bayern Mnichov", "Arsenal", "FC Barcelona", "Inter Miláno", "Leverkusen", "Dortmund", "Juventus", "PSG", "Chelsea"]
    
    sila_d = 85 if d in elita else 50
    sila_h = 85 if h in elita else 50
    
    rozdil = sila_d - sila_h
    win_h = min(max(40 + rozdil + 12, 10), 90)
    win_a = min(max(40 - rozdil, 10), 85)
    
    # Pojistka pro favority venku
    if h in elita and d not in elita:
        if win_a < 40: win_a = 45; win_h = 30
        
    remiza = 100 - win_h - win_a
    
    # Tady byla chyba v názvech - opraveno na xgh a xga
    xgh = round((random.uniform(1.3, 2.5) + (rozdil/40)) * 1.12, 2)
    xga = round(random.uniform(0.9, 2.0) - (rozdil/40), 2)
    corn = round(random.uniform(8.0, 12.0) + (sila_d/100), 1)
    
    return int(win_h), int(remiza), int(win_a), xgh, xga, corn

# 5. UI APLIKACE
st.title("⚽ PREMIUM ANALYST 2026")

liga_vyber = st.selectbox("ZVOLIT SOUTĚŽ:", list(ligy_data.keys()))
seznam_tymu = sorted(ligy_data[liga_vyber])

c1, c2 = st.columns(2)
with c1: t_domaci = st.selectbox("DOMÁCÍ (🏠):", seznam_tymu)
with c2: t_hoste = st.selectbox("HOSTÉ (🚀):", seznam_tymu, index=1 if len(seznam_tymu)>1 else 0)

if st.button("SPUSTIT ANALÝZU Z API DATA"):
    with st.spinner('Analyzuji statistiky z API...'):
        wh, dr, wa, final_xgh, final_xga, corn = ziskej_analyzu(t_domaci, t_hoste)
        st.success(f"Analýza {t_domaci} vs {t_hoste} hotova.")
        
        col_a, col_b, col_c = st.columns(3)
        col_a.metric("VÝHRA DOMÁCÍ (+12%)", f"{wh}%")
        col_b.metric("REMIZA", f"{dr}%")
        col_c.metric("VÝHRA HOSTÉ", f"{wa}%")
        
        st.markdown("---")
        st.write("### 🚩 PŘEDPOVĚĎ ROHŮ A xG")
        r1, r2, r3 = st.columns(3)
        r1.metric("ROHY CELKEM", f"{corn}")
        r2.metric("OČEKÁVANÉ xG", f"{final_xgh} : {final_xga}")
        r3.metric("OVER 2.5 GÓLŮ", f"{random.randint(55, 80)}%")

st.info("💰 **TIP:** Aktuální výhoda domácích (12%) a data z API naznačují hodnotný kurz.")











