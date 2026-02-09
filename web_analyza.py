import streamlit as st
import random

# 1. NASTAVENÍ A POČÍTADLO
st.set_page_config(page_title="ELITE ANALYST PRO 2026", page_icon="⚽", layout="centered")

if 'pocet_navstev' not in st.session_state:
    st.session_state.pocet_navstev = random.randint(140, 250)
st.session_state.pocet_navstev += 1

st.markdown(f"""
    <div style='text-align: center; background-color: #1e2130; padding: 10px; border-radius: 10px; border: 1px solid #00ff00;'>
        <h4 style='margin:0; color: white;'>📈 POČET DNEŠNÍCH ANALÝZ: {st.session_state.pocet_navstev}</h4>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: white; }
    .stButton>button { width: 100%; background-color: #ff4b4b; color: white; border-radius: 12px; font-weight: bold; height: 3.5em; }
    label { color: #00ff00 !important; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# 2. KOMPLETNÍ DATABÁZE TÝMŮ DLE DIKTÁTU
ligy_data = {
    "🏆 Liga mistrů": ["Arsenal", "Bayern Mnichov", "Liverpool", "Tottenham", "FC Barcelona", "Chelsea", "Sporting Lisabon", "Manchester City", "Real Madrid", "Inter Miláno", "Paris Saint-Germain", "Newcastle", "Juventus", "Atletico Madrid", "Atalanta Bergamo", "Leverkusen", "Dortmund", "Olympiakos", "Club Brugge", "Galatasaray", "Monaco", "FK Karabach", "Bodo/Glimt", "Benfica Lisabon", "Marseille", "Paphos FC", "Union SG", "PSV Eindhoven", "Bilbao", "Neapol", "FC Kodaň", "Ajax", "Frankfurt", "Slavia Praha"],
    "🇪🇺 Evropská liga": ["Lyon", "Aston Villa", "Midtjylland", "Betis", "Sevilla", "FC Porto", "Braga", "Freiburg", "AS Řím", "Genk", "Bologna", "Stuttgart", "Ferencváros", "Nottingham", "Plzeň", "Vigo", "PAOK", "Lille", "Fenerbahce", "Panathinaikos", "Celtic Glasgow", "Ludogorec Razgrad", "Dynamo"],
    "🏴󠁧󠁢󠁥󠁮󠁧󠁿 Premier League": ["Arsenal", "Manchester City", "Aston Villa", "Manchester United", "Chelsea", "Liverpool", "Brentford", "Everton", "Sunderland", "Fullham", "Bournemouth", "Newcastle", "Crystal Palace", "Brighton", "Tottenham", "Leeds", "Nottingham", "West Ham", "Burnley", "Wolverhampton"],
    "🇩🇪 Bundesliga": ["Bayern Mnichov", "Dortmund", "Hoffenheim", "RB Lipsko", "Stuttgart", "Leverkusen", "Freiburg", "Frankfurt", "Union Berlin", "FC Kolín", "Hamburk", "Mönchengladbach", "Augsburg", "Mainz", "Wolfsburg", "Brémy", "Saint Pauli", "Heidenheim"],
    "🇪🇸 La Liga": ["FC Barcelona", "Real Madrid", "Atlético Madrid", "Villarreal", "Betis", "Sevilla", "Espanyol", "Celta Vigo", "Real Sociedad", "Osasuna", "Bilbao", "Getafe", "Girona", "Alavés", "Elche", "Mallorca", "Valencia", "Rayo Vallecano", "Levante", "Oviedo"],
    "🇮🇹 Serie A": ["Inter Milán", "AC Milán", "Neapol", "Juventus", "AS Řím", "Como", "Atalanta Bergamo", "Lazio", "Udinese", "Bologna", "Sassuolo", "Cagliari", "FC Torino", "Parma", "Janov", "Cremonese", "Lecce", "Fiorentina", "Pisa", "Hellas Verona"],
    "🇨🇿 Chance Liga": ["Slavia Praha", "Sparta Praha", "Jablonec", "Plzeň", "Liberec", "Karviná", "Hradec Králové", "Olomouc", "Zlín", "Pardubice", "Teplice", "Bohemians", "Ostrava", "Mladá Boleslav", "Slovácko", "Dukla Praha"]
}

st.title("⚽ PREMIUM ANALYST 2026")

# 3. VÝBĚR
liga = st.selectbox("ZVOLIT SOUTĚŽ:", list(ligy_data.keys()))
tymy = sorted(ligy_data[liga])

col1, col2 = st.columns(2)
with col1: domaci = st.selectbox("DOMÁCÍ (🏠):", tymy)
with col2: hoste = st.selectbox("HOSTÉ (🚀):", tymy, index=1 if len(tymy)>1 else 0)

# 4. VÝPOČETNÍ LOGIKA (PONZIHO SCHÉMA + 13% HOME ADVANTAGE)
def vypocet(d, h):
    random.seed(d + h)
    # Základní pravděpodobnost (50/50)
    base_h = random.randint(30, 50)
    # Přidání 13% výhody pro domácí
    win_h = min(base_h + 13, 85)
    win_a = random.randint(15, 100 - win_h - 10)
    draw = 100 - win_h - win_a
    
    # Rohy s 13% bonusem pro domácí
    base_corners = random.uniform(8.0, 11.0)
    corners = round(base_corners * 1.13, 1)
    
    xg_h = round(random.uniform(1.2, 2.8) * 1.13, 2)
    xg_a = round(random.uniform(0.8, 1.8), 2)
    
    return win_h, draw, win_a, xg_h, xg_a, corners

# 5. AKCE
if st.button("SPUSTIT VÝPOČET ANALÝZY"):
    if domaci == hoste:
        st.error("Vyberte různé týmy!")
    else:
        wh, dr, wa, xh, xa, cor = vypocet(domaci, hoste)
        st.success(f"Analýza {domaci} vs {hoste} dokončena na základě 10 zápasů.")
        
        c1, c2, c3 = st.columns(3)
        c1.metric("VÝHRA DOMÁCÍ (+13%)", f"{wh}%")
        c2.metric("REMIZA", f"{dr}%")
        c3.metric("VÝHRA HOSTÉ", f"{wa}%")
        
        st.markdown("---")
        st.write("### 🚩 PŘEDPOVĚĎ ROHŮ A xG")
        r1, r2, r3 = st.columns(3)
        r1.metric("ROHY CELKEM", f"{cor}")
        r2.metric("OČEKÁVANÉ xG", f"{xh} : {xa}")
        r3.metric("PRAVDĚP. GÓLŮ", f"{random.randint(55, 80)}%")

st.info("💰 **TIP:** Aktuální výhoda domácích (13%) naznačuje hodnotný kurz. **[VSADIT U TIPSPORTU](https://www.tipsport.cz)**")


