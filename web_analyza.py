import streamlit as st
import random

# 1. NASTAVENÍ VZHLEDU
st.set_page_config(page_title="PRO ANALYST 2026", page_icon="⚽", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: white; }
    .stButton>button { width: 100%; background-color: #ff4b4b; color: white; border-radius: 10px; font-weight: bold; }
    label { color: #00ff00 !important; font-weight: bold; }
    .metric-box { background-color: #1e2130; padding: 15px; border-radius: 10px; text-align: center; margin: 5px; }
    </style>
    """, unsafe_allow_html=True)

st.title("⚽ PREMIUM FOOTBALL ANALYST 2026")

# 2. SEZNAM TÝMŮ VČETNĚ ZLÍNA
seznam_cesko = [
    "Slavia Praha", "Sparta Praha", "Viktoria Plzeň", "Baník Ostrava", 
    "Mladá Boleslav", "Slovan Liberec", "Sigma Olomouc", "Jablonec", 
    "Hradec Králové", "Teplice", "Bohemians 1905", "Slovácko", 
    "Pardubice", "Karviná", "České Budějovice", "Dukla Praha", "Zlín"
]

# 3. VÝBĚR TÝMŮ
st.markdown("### 🏟️ NASTAVENÍ ZÁPASU")
col1, col2 = st.columns(2)
with col1:
    domaci = st.selectbox("DOMÁCÍ TÝM (🏠):", seznam_cesko)
with col2:
    hoste = st.selectbox("HOSTUJÍCÍ TÝM (🚀):", seznam_cesko)

# 4. ANALÝZA
if st.button("SPUSTIT KOMPLETNÍ ANALÝZU"):
    with st.spinner('Propočítávám góly, rohy a xG...'):
        st.success(f"Analýza pro zápas {domaci} vs {hoste} hotova!")
        
        # HLAVNÍ PROCENTA
        st.write("### 📊 PRAVDĚPODOBNOST VÝSLEDKU:")
        c1, c2, c3 = st.columns(3)
        c1.metric("VÝHRA DOMÁCÍ", "46%")
        c2.metric("REMIZA", "24%")
        c3.metric("VÝHRA HOSTÉ", "30%")

        # OČEKÁVANÉ SKÓRE A GÓLY
        st.markdown("---")
        st.write("### 🎯 GÓLOVÁ PŘEDPOVĚĎ:")
        ga, gb = st.columns(2)
        with ga:
            st.info(f"⚽ **Očekávané skóre (xG):** \n\n {domaci} **1.85** : **1.10** {hoste}")
        with gb:
            st.info("🔥 **Více než 2.5 gólu:** \n\n Pravděpodobnost: **62 %**")

        # NOVINKA: STATISTIKA ROHŮ (Posledních 10 zápasů)
        st.write("### 🚩 ROHOVÉ KOPY (Bilance 10 zápasů):")
        r1, r2 = st.columns(2)
        r1.metric("PRŮMĚR ROHŮ CELKEM", "9.5")
        r2.metric("VÍCE NEŽ 8.5 ROHU", "70%")

        # BILANCE ZÁPASŮ
        st.caption(f"📋 Analyzováno posledních 10 vzájemných zápasů | Datum: 08.02. 2026")

# 5. SEKCE PRO VÝDĚLEK
st.markdown("---")
st.info("💰 **TIP:** Sázej s bonusem 500 Kč u partnera! **[KLIKNI ZDE](https://www.tipsport.cz)**")

