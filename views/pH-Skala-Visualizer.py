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
    if ph_value < 7:
        r = 1 - (ph_value / 7) * 0.5
        g = ph_value / 7
        b = 0
    else:
        r = 0
        g = 1 - ((ph_value - 7) / 7) * 0.5
        b = (ph_value - 7) / 7
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
        
        # Filtere nur die Spalte 'Resultat' (pH oder Konzentration Werte)
        if 'Resultat' in df.columns:
            fig, ax = plt.subplots(figsize=(12, 5))
            
            # Extrahiere pH-Werte (Resultat Spalte)
            results = df['Resultat'].tolist()
            indices = list(range(len(results)))
            
            # Bestimme ob es pH-Werte oder Konzentrationen sind
            # Wenn Werte zwischen 0-14, sind es pH-Werte
            ph_values = []
            for val in results:
                try:
                    if -2 <= val <= 16:  # pH-Wertebereich
                        ph_values.append(val)
                    else:
                        # Ggf. Konzentrationswert - ähnlich wie pH konvertieren
                        import math
                        if val > 0:
                            ph = -math.log10(val)
                            ph_values.append(max(-2, min(16, ph)))
                        else:
                            ph_values.append(7)
                except:
                    ph_values.append(7)
            
            # Farben für jeden Wert
            colors = [get_color_for_ph(ph) for ph in ph_values]
            
            # Balkendiagramm
            bars = ax.bar(indices, ph_values, color=colors, edgecolor='black', linewidth=1.5)
            
            # Neutrale Linie hinzufügen
            ax.axhline(y=7, color='gray', linestyle='--', linewidth=2, alpha=0.5, label='Neutral (pH 7)')
            
            ax.set_xlabel('Berechnung #', fontsize=11)
            ax.set_ylabel('pH-Wert', fontsize=11)
            ax.set_title('Übersicht deiner berechneten pH-Werte', fontsize=13, fontweight='bold')
            ax.set_ylim(-1, 15)
            ax.grid(axis='y', alpha=0.3)
            ax.legend()
            
            st.pyplot(fig, use_container_width=True)
            
            # Statistische Informationen
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Anzahl Berechnungen", len(ph_values))
            with col2:
                st.metric("Durchschnitt pH", f"{sum(ph_values)/len(ph_values):.2f}")
            with col3:
                acidic = sum(1 for x in ph_values if x < 7)
                st.metric("Saure Werte", acidic)
        
        st.divider()
        st.subheader("Alle Daten")
        st.dataframe(df, use_container_width=True)
        
    else:
        st.info("📊 Noch keine Berechnungen vorhanden. Gehe zum pH-Rechner und erstelle erste Berechnungen!")

