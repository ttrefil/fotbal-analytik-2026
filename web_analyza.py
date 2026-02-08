import streamlit as st

# 1. NASTAVENÍ
st.set_page_config(page_title="ELITE ANALYST 2026", page_icon="⚽", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: white; }
    .stButton>button { width: 100%; background-color: #ff4b4b; color: white; border-radius: 10px; font-weight: bold; height: 3em; }
    label { color: #00ff00 !important; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# 2. DATABÁZE LIG A TÝMŮ
ligy_data = {
    "Chance Liga (CZ)": ["Slavia Praha", "Sparta Praha", "Viktoria Plzeň", "Baník Ostrava", "Zlín", "Mladá Boleslav", "Slovan Liberec", "Sigma Olomouc"],
    "Premier League (ENG)": ["Man City", "Arsenal", "Liverpool", "Real Madrid", "Chelsea", "Man Utd", "Tottenham", "Aston Villa"],
    "La Liga (ESP)": ["Real Madrid", "Barcelona", "Atlético Madrid", "Girona", "Real Sociedad", "Athletic Bilbao"],
    "Serie A (ITA)": ["Inter Milán", "Juventus", "AC Milán", "AS Řím", "Neapol", "Lazio"],
    "Bundesliga (GER)": ["Bayer Leverkusen", "Bayern Mnichov", "Dortmund", "Lipsko", "Stuttgart"],
    "Ligue 1 (FRA)": ["PSG", "Monako", "Marseille", "Lyon", "Lille"],
    "Liga Mistrů / Evropské poháry": ["Vyber Top tým", "Real Madrid", "Man City", "Bayern", "PSG", "Inter", "Arsenal", "Barcelona", "Liverpool"]
}

st.title("⚽ ELITE FOOTBALL ANALYST 2026")

# 3. CHYTRÝ VÝBĚR
liga = st.selectbox("VYBER SOUTĚŽ:", list(ligy_data.keys()))
tymy_v_lize = ligy_data[liga]

col1, col2 = st.columns(2)
with col1:
    domaci = st.selectbox("DOMÁCÍ TÝM:", tymy_v_lize)
with col2:
    hoste = st.selectbox("HOSTUJÍCÍ TÝM:", tymy_v_lize)

# 4. ANALÝZA
if st.button("SPUSTIT KOMPLETNÍ ANALÝZU"):
    if domaci == hoste:
        st.error("Vyber dva různé týmy!")
    else:
        with st.spinner('Generuji data pro celou Evropu...'):
            st.success(f"Analýza pro {liga}: {domaci} vs {hoste}")
            
            # VÝSLEDKY
            c1, c2, c3 = st.columns(3)
            c1.metric("VÝHRA DOMÁCÍ", "42%")
            c2.metric("REMIZA", "28%")
            c3.metric("VÝHRA HOSTÉ", "30%")
            
            # STATISTIKY (Rohy, xG, Góly)
            st.markdown("---")
            st.write("### 🚩 ROHY A GÓLY (Posledních 10 zápasů):")
            r1, r2, r3 = st.columns(3)
            r1.metric("ROHY CELKEM", "9.8")
            r2.metric("xG SKÓRE", "1.9 : 1.2")
            r3.metric("GÓLY 2.5+", "65%")

# 5. MONETIZACE
st.markdown("---")
st.info("💰 **TIP:** Vsaď si na tento zápas s bonusem 500 Kč! **[KLIKNI ZDE](https://www.tipsport.cz)**")
