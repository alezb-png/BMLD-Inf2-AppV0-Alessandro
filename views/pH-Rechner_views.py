

import streamlit as st
from pathlib import Path
import importlib.util
import sys
import pandas as pd 

def _load_ph_module():
    """lädt functions/pH-Rechner.py trotz Bindestrich im Namen."""
    fn = Path(__file__).parent.parent / "functions" / "pH-Rechner.py"
    spec = importlib.util.spec_from_file_location("ph_rechner", fn)
    module = importlib.util.module_from_spec(spec)
    sys.modules["ph_rechner"] = module
    spec.loader.exec_module(module)
    return module

ph_mod = _load_ph_module()
ph_from_concentration = ph_mod.ph_from_concentration
concentration_from_ph = ph_mod.concentration_from_ph

# --- Streamlit‑UI ---
st.header("pH-Rechner")
st.write("Berechne pH-Werte und Wasserstoffionenkonzentrationen mit Präzision")

st.divider()

st.subheader("Rechenmodi")
st.write("Wähle den Modus für deine Berechnung:")

mode = st.radio("Modus",
                ("Konzentration → pH", "pH → Konzentration"),
                horizontal=True)

st.divider()

if mode == "Konzentration → pH":
    st.subheader("Konzentration zu pH")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.write("Berechne den pH-Wert aus der Wasserstoffionenkonzentration:")
        st.latex(r"\text{pH} = -\log_{10}([H^+])")
    
    with col2:
        st.info("ℹ️ pH-Skala: 0-14")
    
    st.divider()
    
    conc = st.number_input(
        "Wasserstoffionenkonzentration [H⁺] (mol/L)",
        min_value=0.0, 
        format="%.6f", 
        step=1e-6,
        help="Gib eine positive Konzentration im wissenschaftlichen Format ein"
    )
    
    if conc > 0:
        try:
            result = ph_from_concentration(conc)
            ph = result["Resultat"]
            st.success(f"✅ Berechneter pH-Wert: **{ph:.4f}**")
            
            # Zusätzliche Informationen
            col1, col2, col3 = st.columns(3)
            with col1:
                if ph < 7:
                    st.badge("Sauer 🔴")
                elif ph > 7:
                    st.badge("Basisch 🔵")
                else:
                    st.badge("Neutral ⚪")
            with col2:
                st.metric("Eingabe-Konzentration", f"{conc:.2e} mol/L")
            with col3:
                st.metric("Berechnung", f"-log₁₀({conc:.2e})")
            
            st.session_state['data_df'] = pd.concat([st.session_state['data_df'], pd.DataFrame([result])])
            
        except ValueError as e:
            st.error(f"❌ Fehler: {str(e)}")
    else:
        st.info("ℹ️ Bitte eine positive Konzentration eingeben (> 0).")

else:  # pH → Konzentration
    st.subheader("pH zu Konzentration")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.write("Berechne die Wasserstoffionenkonzentration aus dem pH-Wert:")
        st.latex(r"[H^+] = 10^{-\text{pH}}")
    
    with col2:
        st.info("ℹ️ Eingabe-Bereich: -2 bis 16")
    
    st.divider()
    
    ph = st.number_input(
        "pH-Wert", 
        min_value=-2.0, 
        max_value=16.0,
        format="%.4f", 
        step=0.1,
        help="Wähle einen pH-Wert zwischen -2 und 16"
    )
    
    result = concentration_from_ph(ph)
    conc = result["Resultat"]
    st.success(f"✅ Wasserstoffionenkonzentration: **{conc:.2e} mol/L**")
    
    # Zusätzliche Informationen
    col1, col2, col3 = st.columns(3)
    with col1:
        if ph < 7:
            st.badge("Sauer 🔴")
        elif ph > 7:
            st.badge("Basisch 🔵")
        else:
            st.badge("Neutral ⚪")
    with col2:
        st.metric("Eingabe pH", f"{ph:.2f}")
    with col3:
        st.metric("Berechnung", f"10⁻{ph:.2f}")
    
    st.session_state['data_df'] = pd.concat([st.session_state['data_df'], pd.DataFrame([result])])

# --- NEW CODE to display the history table ---
st.dataframe(st.session_state['data_df'])