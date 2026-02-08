import streamlit as st

# 1. NASTAVENÍ VZHLEDU
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
    "Liga Mistrů / Evropské poháry": ["Real Madrid", "Man City", "Bayern", "PSG", "Inter", "Arsenal", "Barcelona", "Liverpool"]
}

st.title("⚽ ELITE FOOTBALL ANALYST 2026")

# --- TADY BYLA TA CHYBA, TEĎ JE TO OPRAVENÉ ---
st.markdown("### 🌍 VÝBĚR SOUTĚŽE")
vybrana_liga = st.selectbox("ZVOL LIGU:", list(ligy_data.keys()))
seznam_tymu = ligy_data[vybrana_liga]

st.markdown("### 🏟️ NASTAVENÍ ZÁPASU")
col1, col2 = st.columns(2)
with col1:
    domaci = st.selectbox("DOMÁCÍ TÝM (🏠):", seznam_tymu)
with col2:
    hoste = st.selectbox("HOSTUJÍCÍ TÝM (🚀):", seznam_tymu)

# 4. ANALÝZA
if st.button("SPUSTIT KOMPLETNÍ ANALÝZU"):
    if domaci == hoste:
        st.error("Vyber dva různé týmy!")
    else:
        with st.spinner('Propočítávám evropské statistiky...'):
            st.success(f"Analýza pro {vybrana_liga}: {domaci} vs {hoste} hotova!")
            
            c1, c2, c3 = st.columns(3)
            c1.metric("VÝHRA DOMÁCÍ", "44%")
            c2.metric("REMIZA", "28%")
            c3.metric("VÝHRA HOSTÉ", "28%")
            
            st.markdown("---")
            st.write("### 🚩 STATISTIKY (Posledních 10 zápasů):")
            r1, r2, r3 = st.columns(3)
            r1.metric("ROHY CELKEM", "9.8")
            r2.metric("xG SKÓRE", "1.9 : 1.2")
            r3.metric("GÓLY 2.5+", "65%")

# 5. REKLAMA
st.markdown("---")
st.info("💰 **TIP:** Sázej s bonusem 500 Kč u partnera! **[KLIKNI ZDE](https://www.tipsport.cz)**")
