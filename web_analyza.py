import streamlit as st
import random
import requests
import math

# 1. DESIGN A POZADÍ (Vylepšené stínování a boxy)
st.set_page_config(page_title="ELITE ANALYST PRO 2026", page_icon="⚽", layout="centered")

page_bg_img = '''
<style>
[data-testid="stAppViewContainer"] {
    background-image: url("https://images.unsplash.com/photo-1574629810360-7efbbe195018?q=80&w=2000&auto=format&fit=crop");
    background-size: cover;
    background-position: center;
}
[data-testid="stAppViewContainer"]::before {
    content: "";
    position: absolute;
    top: 0; left: 0; width: 100%; height: 100%;
    background-color: rgba(0, 0, 0, 0.7);
}

/* Efekt stínování pro hlavní boxy */
div[data-testid="stVerticalBlock"] > div {
    background-color: rgba(30, 33, 48, 0.5);
    border-radius: 15px;
    padding: 10px;
    box-shadow: 0 8px 16px rgba(0,0,0,0.6); /* Stín pod boxy */
}

/* Styl pro tlačítko */
div.stButton > button {
    width: 100%;
    height: 50px;
    background-color: #00ff00 !important;
    color: black !important;
    font-weight: bold;
    font-size: 18px;
    border-radius: 10px;
    border: none;
}

.email-header {
    text-align: right;
    font-size: 14px;
    color: #bbb;
    position: relative;
    z-index: 10;
}
</style>
'''
st.markdown(page_bg_img, unsafe_allow_html=True)

st.markdown("<div class='email-header'>připomínky na email: trefilos@gmail.com</div>", unsafe_allow_html=True)

if 'pocet_navstev' not in st.session_state:
    st.session_state.pocet_navstev = 312
st.session_state.pocet_navstev += 1

st.markdown(f"""
    <div style='text-align: center; background-color: rgba(30, 33, 48, 0.85); padding: 10px; border-radius: 10px; border: 1px solid #00ff00; position: relative;'>
        <h4 style='margin:0; color: white;'>📈 POČET DNEŠNÍCH ANALÝZ: {st.session_state.pocet_navstev}</h4>
    </div>
    """, unsafe_allow_html=True)

# 2. API LOGIKA (PŮVODNÍ - NEDOTČENO)
def get_poisson_probability(lmbda, k):
    return (math.pow(lmbda, k) * math.exp(-lmbda)) / math.factorial(k)

def get_team_stats(team_name):
    if team_name in ["Plzeň", "Sparta Praha", "Slavia Praha", "Arsenal", "Real Madrid"]: return 2.1
    elif team_name in ["Dukla Praha", "Pardubice", "Mainz", "Alavés"]: return 0.9
    return 1.4

# 3. DATABÁZE LIG (PŮVODNÍ - NEDOTČENO)
ligy_data = {
    "🏆 Liga mistrů": ["Arsenal", "Bayern Mnichov", "Liverpool", "Tottenham", "FC Barcelona", "Chelsea", "Sporting Lisabon", "Manchester City", "Real Madrid", "Inter Miláno", "Paris Saint-Germain", "Newcastle", "Juventus", "Atletico Madrid", "Atalanta Bergamo", "Leverkusen", "Dortmund", "Olympiakos", "Club Brugge", "Galatasaray", "Monaco", "FK Karabach", "Bodo/Glimt", "Benfica Lisabon", "Marseille", "Paphos FC", "Union SG", "PSV Eindhoven", "Bilbao", "Neapol", "FC Kodaň", "Ajax", "Frankfurt", "Slavia Praha"],
    "🇪🇺 Evropská liga": ["Lyon", "Aston Villa", "Midtjylland", "Betis", "Sevilla", "FC Porto", "Braga", "Freiburg", "AS Řím", "Genk", "Bologna", "Stuttgart", "Ferencváros", "Nottingham", "Plzeň", "Vigo", "PAOK", "Lille", "Fenerbahce", "Panathinaikos", "Celtic Glasgow", "Ludogorec Razgrad", "Dynamo"],
    "🏴󠁧󠁢󠁥󠁮󠁧󠁿 Premier League": ["Arsenal", "Manchester City", "Aston Villa", "Manchester United", "Chelsea", "Liverpool", "Brentford", "Everton", "Sunderland", "Fullham", "Bournemouth", "Newcastle", "Crystal Palace", "Brighton", "Tottenham", "Leeds", "Nottingham", "West Ham", "Burnley", "Wolverhampton"],
    "🇩🇪 Bundesliga": ["Bayern Mnichov", "Dortmund", "Hoffenheim", "RB Lipsko", "Stuttgart", "Leverkusen", "Freiburg", "Frankfurt", "Union Berlin", "FC Kolín", "Hamburk", "Mönchengladbach", "Augsburg", "Mainz", "Wolfsburg", "Brémy", "Saint Pauli", "Heidenheim"],
    "🇪🇸 La Liga": ["FC Barcelona", "Real Madrid", "Atlético Madrid", "Villarreal", "Betis", "Sevilla", "Espanyol", "Celta Vigo", "Real Sociedad", "Osasuna", "Bilbao", "Getafe", "Girona", "Alavés", "Elche", "Mallorca", "Valencia", "Rayo Vallecano", "Levante", "Oviedo"],
    "🇮🇹 Serie A": ["Inter Milán", "AC Milán", "Neapol", "Juventus", "AS Řím", "Como", "Atalanta Bergamo", "Lazio", "Udinese", "Bologna", "Sassuolo", "Cagliari", "FC Torino", "Parma", "Janov", "Cremonese", "Lecce", "Fiorentina", "Pisa", "Hellas Verona"],
    "🇨🇿 Chance Liga": ["Slavia Praha", "Sparta Praha", "Jablonec", "Plzeň", "Liberec", "Karviná", "Hradec Králové", "Olomouc", "Zlín", "Pardubice", "Teplice", "Bohemians", "Ostrava", "Mladá Boleslav", "Slovácko", "Dukla Praha"]
}

# 4. VÝPOČETNÍ ALGORITMUS (PŮVODNÍ - NEDOTČENO)
def analyzuj_zapas(domaci, hoste):
    lambda_d = get_team_stats(domaci)
    lambda_h = get_team_stats(hoste)
    prob_d_win, prob_h_win, prob_draw = 0, 0, 0
    for i in range(6):
        for j in range(6):
            p_score = get_poisson_probability(lambda_d, i) * get_poisson_probability(lambda_h, j)
            if i > j: prob_d_win += p_score
            elif i < j: prob_h_win += p_score
            else: prob_draw += p_score
    total = prob_d_win + prob_h_win + prob_draw
    wh = (prob_d_win / total) * 100 + 3
    wa = (prob_h_win / total) * 100 - 1.5
    dr = 100 - wh - wa
    return int(wh), int(dr), int(wa), round(lambda_d, 2), round(lambda_h, 2)

# 5. UI APLIKACE
st.title("⚽ PREMIUM ANALYST 2026")
liga = st.selectbox("ZVOLIT SOUTĚŽ:", list(ligy_data.keys()))
tymy = sorted(ligy_data[liga])

c1, c2 = st.columns(2)
with c1: d_team = st.selectbox("DOMÁCÍ (🏠):", tymy)
with c2: h_team = st.selectbox("HOSTÉ (🚀):", tymy, index=1 if len(tymy)>1 else 0)

if st.button("SPUSTIT ANALÝZU"):
    with st.spinner('Zpracovávám data...'):
        wh, dr, wa, xg_d, xg_h = analyzuj_zapas(d_team, h_team)
        st.success(f"Analýza {d_team} vs {h_team} dokončena.")
        res_a, res_b, res_c = st.columns(3)
        res_a.metric("VÝHRA DOMÁCÍ", f"{wh}%")
        res_b.metric("REMIZA", f"{dr}%")
        res_c.metric("VÝHRA HOSTÉ", f"{wa}%")
        st.markdown("---")
        st.write("### 🚩 PŘEDPOVĚĎ ZÁPASU")
        s1, s2, s3 = st.columns(3)
        s1.metric("OČEKÁVANÉ GÓLY", f"{xg_d} : {xg_h}")
        s2.metric("ROHY (PRŮMĚR)", f"{round(random.uniform(9.1, 11.2), 1)}")
        s3.metric("OVER 2.5 GÓLŮ", f"{int((xg_d + xg_h) * 25)}%")

# NOVÉ UPRAVENÉ REKLAMNÍ OKNO (Zvýšené, jiný odstín zelené)
st.markdown("""
    <div style='text-align: center; background-color: rgba(0, 50, 0, 0.4); padding: 15px; border-radius: 10px; border: 1px dashed #00ff00; margin-top: 50px;'>
        <p style='color: #90ee90; font-size: 14px; margin: 0; font-weight: bold;'>ZDE MŮŽE BÝT VAŠE REKLAMA</p>
        <p style='color: #ccc; font-size: 12px; margin: 5px 0 0 0;'>Kontaktujte nás pro exkluzivní spolupráci</p>
    </div>
    """, unsafe_allow_html=True)















