import streamlit as st
import random
import math
import os

# 1. DESIGN A LOGIKA TRVALÉHO POČITADLA
st.set_page_config(page_title="ELITE ANALYST PRO 2026", page_icon="⚽", layout="centered")

def manage_total_visits():
    file_path = "total_visits.txt"
    if not os.path.exists(file_path):
        with open(file_path, "w") as f: f.write("12540")
    with open(file_path, "r") as f:
        try:
            current_total = int(f.read())
        except:
            current_total = 12540
    new_total = current_total + 1
    with open(file_path, "w") as f:
        f.write(str(new_total))
    return new_total

if 'pocet_navstev' not in st.session_state:
    st.session_state.pocet_navstev = 312
st.session_state.pocet_navstev += 1
celkove_navstevy = manage_total_visits()

# CSS OPRAVA: Zdvojené závorky pro f-string a maximální čitelnost
st.markdown(f'''
<style>
[data-testid="stAppViewContainer"] {{
    background-image: url("https://images.unsplash.com/photo-1574629810360-7efbbe195018?q=80&w=2000&auto=format&fit=crop");
    background-size: cover;
    background-position: center;
}}
[data-testid="stAppViewContainer"]::before {{
    content: "";
    position: absolute; top: 0; left: 0; width: 100%; height: 100%;
    background-color: rgba(0, 0, 0, 0.75);
}}
div[data-testid="stVerticalBlock"] > div {{
    background-color: rgba(15, 15, 25, 0.85) !important;
    border-radius: 15px; padding: 15px;
    box-shadow: 0 10px 25px rgba(0,0,0,0.8);
    backdrop-filter: none !important;
}}
div[data-testid="stMetricValue"] > div {{
    color: #00ff00 !important;
    font-weight: bold !important;
    font-size: 34px !important;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.7);
}}
div.stButton > button {{
    width: 100%; height: 50px;
    background-color: #00ff00 !important;
    color: black !important;
    font-weight: bold; font-size: 18px;
    border-radius: 10px; border: none;
}}
.top-bar {{
    display: flex; justify-content: space-between;
    position: relative; z-index: 10;
    color: #ffffff; font-size: 14px; font-weight: bold;
}}
</style>
''', unsafe_allow_html=True)

st.markdown(f"<div class='top-bar'><div>celkem návštěv: {celkove_navstevy}</div><div>připomínky na email: trefilos@gmail.com</div></div>", unsafe_allow_html=True)

st.markdown(f"""
    <div style='text-align: center; background-color: rgba(0, 0, 0, 0.6); padding: 10px; border-radius: 10px; border: 1px solid #00ff00; position: relative; margin-top: 10px;'>
        <h4 style='margin:0; color: #00ff00;'>📈 POČET DNEŠNÍCH ANALÝZ: {st.session_state.pocet_navstev}</h4>
    </div>
    """, unsafe_allow_html=True)

# 2. API LOGIKA, 3. LIGY, 4. ALGORITMUS (BEZE ZMĚN)
def get_poisson_probability(lmbda, k):
    return (math.pow(lmbda, k) * math.exp(-lmbda)) / math.factorial(k)

def get_team_stats(team_name):
    if team_name in ["Plzeň", "Sparta Praha", "Slavia Praha", "Arsenal", "Real Madrid"]: return 2.1
    elif team_name in ["Dukla Praha", "Pardubice", "Mainz", "Alavés"]: return 0.9
    return 1.4

ligy_data = {
    "🏆 Liga mistrů": ["Arsenal", "Bayern Mnichov", "Liverpool", "Tottenham", "FC Barcelona", "Chelsea", "Sporting Lisabon", "Manchester City", "Real Madrid", "Inter Miláno", "Paris Saint-Germain", "Newcastle", "Juventus", "Atletico Madrid", "Atalanta Bergamo", "Leverkusen", "Dortmund", "Olympiakos", "Club Brugge", "Galatasaray", "Monaco", "FK Karabach", "Bodo/Glimt", "Benfica Lisabon", "Marseille", "Paphos FC", "Union SG", "PSV Eindhoven", "Bilbao", "Neapol", "FC Kodaň", "Ajax", "Frankfurt", "Slavia Praha"],
    "🇪🇺 Evropská liga": ["Lyon", "Aston Villa", "Midtjylland", "Betis", "Sevilla", "FC Porto", "Braga", "Freiburg", "AS Řím", "Genk", "Bologna", "Stuttgart", "Ferencváros", "Nottingham", "Plzeň", "Vigo", "PAOK", "Lille", "Fenerbahce", "Panathinaikos", "Celtic Glasgow", "Ludogorec Razgrad", "Dynamo"],
    "🏴󠁧󠁢󠁥󠁮󠁧󠁿 Premier League": ["Arsenal", "Manchester City", "Aston Villa", "Manchester United", "Chelsea", "Liverpool", "Brentford", "Everton", "Sunderland", "Fullham", "Bournemouth", "Newcastle", "Crystal Palace", "Brighton", "Tottenham", "Leeds", "Nottingham", "West Ham", "Burnley", "Sunderland", "Wolverhampton"],
    "🇩🇪 Bundesliga": ["Bayern Mnichov", "Dortmund", "Hoffenheim", "RB Lipsko", "Stuttgart", "Leverkusen", "Freiburg", "Frankfurt", "Union Berlin", "FC Kolín", "Hamburk", "Mönchengladbach", "Augsburg", "Mainz", "Wolfsburg", "Brémy", "Saint Pauli", "Heidenheim"],
    "🇪🇸 La Liga": ["FC Barcelona", "Real Madrid", "Atlético Madrid", "Villarreal", "Betis", "Sevilla", "Espanyol", "Celta Vigo", "Real Sociedad", "Osasuna", "Bilbao", "Getafe", "Girona", "Alavés", "Elche", "Mallorca", "Valencia", "Rayo Vallecano", "Levante", "Oviedo"],
    "🇮🇹 Serie A": ["Inter Milán", "AC Milán", "Neapol", "Juventus", "AS Řím", "Como", "Atalanta Bergamo", "Lazio", "Udinese", "Bologna", "Sassuolo", "Cagliari", "FC Torino", "Parma", "Janov", "Cremonese", "Lecce", "Fiorentina", "Pisa", "Hellas Verona"],
    "🇨🇿 Chance Liga": ["Slavia Praha", "Sparta Praha", "Jablonec", "Plzeň", "Liberec", "Karviná", "Hradec Králové", "Olomouc", "Zlín", "Pardubice", "Teplice", "Bohemians", "Ostrava", "Mladá Boleslav", "Slovácko", "Dukla Praha"]
}

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

# 5. UI
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

# REKLAMNÍ OKNO
st.markdown("""
    <div style='text-align: center; background-color: rgba(0, 50, 0, 0.4); padding: 15px; border-radius: 10px; border: 1px dashed #00ff00; margin-top: 50px;'>
        <p style='color: #90ee90; font-size: 14px; margin: 0; font-weight: bold;'>ZDE MŮŽE BÝT VAŠE REKLAMA</p>
        <p style='color: #ccc; font-size: 12px; margin: 5px 0 0 0;'>Kontaktujte nás pro exkluzivní spolupráci</p>
    </div>
    """, unsafe_allow_html=True)















