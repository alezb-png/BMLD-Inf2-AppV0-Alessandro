import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pandas as pd
from pathlib import Path
import importlib.util
import sys

def _load_ph_module():
    """Lädt functions/pH-Rechner.py trotz Bindestrich im Namen."""
    fn = Path(__file__).parent.parent / "functions" / "pH-Rechner.py"
    spec = importlib.util.spec_from_file_location("ph_rechner", fn)
    module = importlib.util.module_from_spec(spec)
    sys.modules["ph_rechner"] = module
    spec.loader.exec_module(module)
    return module

ph_mod = _load_ph_module()
concentration_from_ph = ph_mod.concentration_from_ph

def get_color_for_ph(ph_value):
    """Gibt Farbe basierend auf pH-Wert zurück."""
    import numpy as np
    
    # pH-Wert auf 0-14 begrenzen
    ph_value = float(ph_value)
    ph_value = max(0.0, min(14.0, ph_value))
    
    if ph_value < 7:
        r = 1.0 - (ph_value / 7.0) * 0.5
        g = ph_value / 7.0
        b = 0.0
    else:
        r = 0.0
        g = 1.0 - ((ph_value - 7.0) / 7.0) * 0.5
        b = (ph_value - 7.0) / 7.0
    
    # Farben auf 0-1 Bereich beschränken
    r = float(np.clip(r, 0.0, 1.0))
    g = float(np.clip(g, 0.0, 1.0))
    b = float(np.clip(b, 0.0, 1.0))
    
    return (r, g, b)

# --- Streamlit UI ---
st.header("pH-Visualizer")
st.write("Visualisiere pH-Werte und berechnete Daten")

# Tabs: Skala und Daten-Grafik
tab1, tab2 = st.tabs(["📊 pH-Skala", "📈 Deine Berechnungen"])

with tab1:
    st.subheader("Die pH-Skala")
    
    # Skala visualisieren
    fig, ax = plt.subplots(figsize=(14, 2.5))
    
    for i in range(15):
        color = get_color_for_ph(i)
        rect = mpatches.Rectangle((i, 0), 1, 1, linewidth=2, 
                                  edgecolor='black', facecolor=color)
        ax.add_patch(rect)
        ax.text(i + 0.5, 0.5, str(i), ha='center', va='center',
               fontsize=14, fontweight='bold', color='white')
    
    ax.set_xlim(0, 15)
    ax.set_ylim(0, 1)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title("pH-Skala (0=Sauer / 7=Neutral / 14=Basisch)", fontsize=13, fontweight='bold')
    
    st.pyplot(fig, use_container_width=True)

with tab2:
    st.subheader("Deine berechneten Werte")
    
    # Daten aus session state laden
    if 'data_df' in st.session_state and not st.session_state['data_df'].empty:
        df = st.session_state['data_df']
        
        if 'Resultat' in df.columns:
            import math
            
            # Trenne Daten nach Berechnungstyp
            ph_calcs = df[df['Typ der Berechnung'].str.contains('pH aus', na=False)] if 'Typ der Berechnung' in df.columns else pd.DataFrame()
            conc_calcs = df[df['Typ der Berechnung'].str.contains('Konzentration', na=False)] if 'Typ der Berechnung' in df.columns else pd.DataFrame()
            
            # --- Grafik 1: Konzentration → pH ---
            if not ph_calcs.empty:
                st.subheader("📊 Konzentration → pH")
                
                fig1, ax1 = plt.subplots(figsize=(12, 5))
                
                ph_results = ph_calcs['Resultat'].tolist()
                indices1 = list(range(len(ph_results)))
                
                # Begrenzte pH-Werte
                ph_values1 = [max(-2, min(16, float(v))) for v in ph_results]
                
                # Farben
                colors1 = [get_color_for_ph(float(ph)) for ph in ph_values1]
                colors1 = [(float(r), float(g), float(b)) for r, g, b in colors1]
                
                ax1.bar(indices1, ph_values1, color=colors1, edgecolor='black', linewidth=1.5)
                ax1.axhline(y=7, color='gray', linestyle='--', linewidth=2, alpha=0.5, label='Neutral (pH 7)')
                
                ax1.set_xlabel('Berechnung #', fontsize=11)
                ax1.set_ylabel('pH-Wert', fontsize=11)
                ax1.set_title('Konzentration → pH Berechnungen', fontsize=13, fontweight='bold')
                ax1.set_ylim(-1, 15)
                ax1.grid(axis='y', alpha=0.3)
                ax1.legend()
                
                st.pyplot(fig1, use_container_width=True)
                
                # Statistiken
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Anzahl", len(ph_values1))
                with col2:
                    st.metric("Ø pH", f"{sum(ph_values1)/len(ph_values1):.2f}")
                with col3:
                    acidic = sum(1 for x in ph_values1 if x < 7)
                    st.metric("Saure Werte", acidic)
            
            # --- Grafik 2: pH → Konzentration ---
            if not conc_calcs.empty:
                st.subheader("📊 pH → Konzentration")
                
                fig2, ax2 = plt.subplots(figsize=(12, 5))
                
                conc_results = conc_calcs['Resultat'].tolist()
                indices2 = list(range(len(conc_results)))
                
                # Konzentrationswerte zu pH konvertieren für Visualisierung
                conc_ph_values = []
                for val in conc_results:
                    try:
                        if val > 0:
                            ph = -math.log10(float(val))
                            conc_ph_values.append(max(-2, min(16, ph)))
                        else:
                            conc_ph_values.append(7)
                    except:
                        conc_ph_values.append(7)
                
                # Farben
                colors2 = [get_color_for_ph(float(ph)) for ph in conc_ph_values]
                colors2 = [(float(r), float(g), float(b)) for r, g, b in colors2]
                
                ax2.bar(indices2, conc_ph_values, color=colors2, edgecolor='black', linewidth=1.5)
                ax2.axhline(y=7, color='gray', linestyle='--', linewidth=2, alpha=0.5, label='Neutral (pH 7)')
                
                ax2.set_xlabel('Berechnung #', fontsize=11)
                ax2.set_ylabel('pH-Wert (aus [H⁺])', fontsize=11)
                ax2.set_title('pH → Konzentration Berechnungen', fontsize=13, fontweight='bold')
                ax2.set_ylim(-1, 15)
                ax2.grid(axis='y', alpha=0.3)
                ax2.legend()
                
                st.pyplot(fig2, use_container_width=True)
                
                # Statistiken
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Anzahl", len(conc_ph_values))
                with col2:
                    st.metric("Ø pH", f"{sum(conc_ph_values)/len(conc_ph_values):.2f}")
                with col3:
                    acidic = sum(1 for x in conc_ph_values if x < 7)
                    st.metric("Saure Werte", acidic)
            
            st.divider()
            st.subheader("Alle Daten")
            st.dataframe(df, use_container_width=True)
        
    else:
        st.info("📊 Noch keine Berechnungen vorhanden. Gehe zum pH-Rechner und erstelle erste Berechnungen!")

