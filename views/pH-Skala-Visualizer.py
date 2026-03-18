import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import math
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
ph_from_concentration = ph_mod.ph_from_concentration
concentration_from_ph = ph_mod.concentration_from_ph

# Beispiele aus der realen Welt
REAL_WORLD_EXAMPLES = {
    "Batteriesäure": 0,
    "Magensäure": 1.5,
    "Zitronensaft": 2.0,
    "Essig": 2.4,
    "Orangensaft": 3.1,
    "Tomatensaft": 4.1,
    "Schwarzer Kaffee": 5.0,
    "Milch": 6.6,
    "Reines Wasser": 7.0,
    "Blut": 7.4,
    "Seewasser": 8.1,
    "Natriumbikarbonat": 8.3,
    "Ammonia-Lösung": 11.0,
    "Soda-Lye": 13.0,
    "Flüssiger Natriumhydroxid": 14.0,
}

# --- Streamlit UI ---
st.header("pH-Skala Visualizer")
st.write("Eine interaktive Visualisierung der pH-Skala mit praktischen Beispielen")

st.divider()

# Zwei Tabs: Skala-Visualisierung und Berechnung
tab1, tab2 = st.tabs(["📊 pH-Skala", "🔢 Interaktive Berechnungen"])

with tab1:
    st.subheader("Die pH-Skala im Detail")
    st.write("""
    Die pH-Skala reicht von **0 (sehr sauer)** bis **14 (sehr basisch)**.
    Ein pH-Wert von **7 ist neutral** (reines Wasser).
    """)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Sauer", "0-7", "H⁺ > OH⁻")
    with col2:
        st.metric("Neutral", "7", "H⁺ = OH⁻")
    with col3:
        st.metric("Basisch", "7-14", "H⁻ < OH⁻")
    
    st.divider()
    
    # Skala visualisieren
    fig, ax = plt.subplots(figsize=(12, 3))
    
    # Farben definieren (Gradient von rot über grün zu blau)
    colors = []
    for i in range(15):
        if i < 7:
            # Rot zu grün (sauer zu neutral)
            r = 1 - (i / 7) * 0.5
            g = (i / 7)
            b = 0
        else:
            # Grün zu blau (neutral zu basisch)
            r = 0
            g = 1 - ((i - 7) / 7) * 0.5
            b = (i - 7) / 7
        colors.append((r, g, b))
    
    # Rechtecke für jeden pH-Wert zeichnen
    for i in range(15):
        rect = mpatches.Rectangle((i, 0), 1, 1, linewidth=2, 
                                  edgecolor='black', facecolor=colors[i])
        ax.add_patch(rect)
        ax.text(i + 0.5, 0.5, str(i), ha='center', va='center',
               fontsize=12, fontweight='bold', color='white')
    
    ax.set_xlim(0, 15)
    ax.set_ylim(0, 1)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title("pH-Skala (0-14)", fontsize=14, fontweight='bold', pad=20)
    
    st.pyplot(fig, use_container_width=True)
    
    st.divider()
    
    # Beispiele aus der realen Welt
    st.subheader("Praktische Beispiele aus der realen Welt")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Saure Lösungen:**")
        acids = {k: v for k, v in REAL_WORLD_EXAMPLES.items() if v < 7}
        for substance, ph_value in sorted(acids.items(), key=lambda x: x[1]):
            st.write(f"• **{substance}**: pH {ph_value}")
    
    with col2:
        st.write("**Basische Lösungen:**")
        bases = {k: v for k, v in REAL_WORLD_EXAMPLES.items() if v > 7}
        for substance, ph_value in sorted(bases.items(), key=lambda x: x[1], reverse=True):
            st.write(f"• **{substance}**: pH {ph_value}")
    
    # Beispiel auswählen und visualisieren
    st.divider()
    st.write("**Wähle ein Beispiel:**")
    selected_example = st.selectbox(
        "Beispiel",
        options=list(REAL_WORLD_EXAMPLES.keys()),
        label_visibility="collapsed"
    )
    
    if selected_example:
        ph_value = REAL_WORLD_EXAMPLES[selected_example]
        try:
            concentration_result = concentration_from_ph(ph_value)
            concentration = concentration_result.get('Resultat', 0)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Substanz", selected_example)
            with col2:
                st.metric("pH-Wert", f"{ph_value:.1f}")
            with col3:
                st.metric("[H⁺] Konzentration", f"{concentration:.2e}", "mol/L")
            
            # Mini-Skala für diesen Wert
            fig2, ax2 = plt.subplots(figsize=(10, 2))
            for i in range(15):
                if i == ph_value:
                    rect = mpatches.Rectangle((i, 0), 1, 1, linewidth=3,
                                            edgecolor='yellow', facecolor=colors[i])
                else:
                    rect = mpatches.Rectangle((i, 0), 1, 1, linewidth=1,
                                            edgecolor='black', facecolor=colors[i])
                ax2.add_patch(rect)
                ax2.text(i + 0.5, 0.5, str(i), ha='center', va='center',
                       fontsize=10, fontweight='bold', color='white')
            
            ax2.set_xlim(0, 15)
            ax2.set_ylim(0, 1)
            ax2.set_aspect('equal')
            ax2.axis('off')
            ax2.set_title(f"Position von {selected_example} (pH {ph_value})", 
                         fontsize=12, fontweight='bold')
            
            st.pyplot(fig2, use_container_width=True)
            
        except Exception as e:
            st.error(f"Fehler bei der Berechnung: {e}")

with tab2:
    st.subheader("Berechne pH-Wert und Konzentration")
    
    mode = st.radio(
        "Berechnungsmodus",
        ("pH → Konzentration", "Konzentration → pH"),
        horizontal=True
    )
    
    st.divider()
    
    if mode == "pH → Konzentration":
        st.write("Berechne die Wasserstoffionenkonzentration aus einem pH-Wert")
        
        col1, col2 = st.columns(2)
        with col1:
            ph_slider = st.slider(
                "pH-Wert eingeben",
                min_value=0.0,
                max_value=14.0,
                value=7.0,
                step=0.1
            )
        
        with col2:
            st.write("")
            st.write("")
            try:
                result = concentration_from_ph(ph_slider)
                concentration = result.get('Resultat', 0)
                st.metric("H⁺ Konzentration", f"{concentration:.2e} mol/L")
            except Exception as e:
                st.error(f"Fehler: {e}")
        
        # Visualisierung
        st.divider()
        fig3, ax3 = plt.subplots(figsize=(10, 4))
        
        # Skala mit Markierung
        for i in range(15):
            if i == int(ph_slider):
                rect = mpatches.Rectangle((i, 0), 1, 2, linewidth=3,
                                        edgecolor='yellow', facecolor=colors[i])
            else:
                rect = mpatches.Rectangle((i, 0), 1, 2, linewidth=1,
                                        edgecolor='black', facecolor=colors[i])
            ax3.add_patch(rect)
            ax3.text(i + 0.5, 1, str(i), ha='center', va='center',
                   fontsize=12, fontweight='bold', color='white')
        
        # Konzentrations-Kurve
        ph_values_range = np.linspace(0, 14, 100)
        concentrations = [10**(-ph) for ph in ph_values_range]
        
        # Logarithmische Skala für Visualisierung
        ax3_twin = ax3.twinx()
        ax3_twin.semilogy(ph_values_range, concentrations, 'r-', linewidth=2, label='[H⁺] Konzentration')
        ax3_twin.set_ylabel('[H⁺] Konzentration (mol/L)', fontsize=10, color='red')
        ax3_twin.tick_params(axis='y', labelcolor='red')
        ax3_twin.axvline(x=ph_slider, color='yellow', linestyle='--', linewidth=2, alpha=0.7)
        
        ax3.set_xlim(0, 15)
        ax3.set_ylim(0, 2)
        ax3.set_xticks(range(15))
        ax3.set_xlabel('pH-Wert', fontsize=12)
        ax3.set_ylabel('pH-Skala', fontsize=12)
        ax3.set_title(f'pH-Wert {ph_slider:.1f} → [H⁺] = {concentration:.2e} mol/L',
                     fontsize=13, fontweight='bold')
        
        st.pyplot(fig3, use_container_width=True)
    
    else:  # Konzentration → pH
        st.write("Berechne den pH-Wert aus einer Wasserstoffionenkonzentration")
        
        col1, col2 = st.columns(2)
        with col1:
            concentration = st.number_input(
                "H⁺ Konzentration eingeben (mol/L)",
                min_value=1e-14,
                max_value=1.0,
                value=1e-7,
                format="%.2e"
            )
        
        with col2:
            st.write("")
            st.write("")
            try:
                result = ph_from_concentration(concentration)
                ph_value = result.get('Resultat', 0)
                
                # Geschwindigkeit der Färbung anpassen
                sanitized_ph = max(0, min(14, ph_value))
                st.metric("pH-Wert", f"{sanitized_ph:.2f}")
            except Exception as e:
                st.error(f"Fehler: {e}")
        
        # Visualisierung
        st.divider()
        fig4, ax4 = plt.subplots(figsize=(10, 4))
        
        # Skala mit Markierung
        for i in range(15):
            if i == int(sanitized_ph):
                rect = mpatches.Rectangle((i, 0), 1, 2, linewidth=3,
                                        edgecolor='yellow', facecolor=colors[i])
            else:
                rect = mpatches.Rectangle((i, 0), 1, 2, linewidth=1,
                                        edgecolor='black', facecolor=colors[i])
            ax4.add_patch(rect)
            ax4.text(i + 0.5, 1, str(i), ha='center', va='center',
                   fontsize=12, fontweight='bold', color='white')
        
        # Konzentrationslog-Skala
        concentration_values = np.logspace(-14, 0, 100)
        ph_values_calc = [-math.log10(c) for c in concentration_values]
        
        ax4_twin = ax4.twinx()
        ax4_twin.loglog(concentration_values, ph_values_calc, 'b-', linewidth=2, label='pH Kurve')
        ax4_twin.set_ylabel('pH-Wert', fontsize=10, color='blue')
        ax4_twin.tick_params(axis='y', labelcolor='blue')
        ax4_twin.axhline(y=sanitized_ph, color='yellow', linestyle='--', linewidth=2, alpha=0.7)
        
        ax4.set_xlim(0, 15)
        ax4.set_ylim(0, 2)
        ax4.set_xticks(range(15))
        ax4.set_xlabel('pH-Wert', fontsize=12)
        ax4.set_ylabel('pH-Skala', fontsize=12)
        ax4.set_title(f'[H⁺] = {concentration:.2e} mol/L → pH {sanitized_ph:.2f}',
                     fontsize=13, fontweight='bold')
        
        st.pyplot(fig4, use_container_width=True)

st.divider()
st.info("""
**Über die pH-Skala:**
- **pH < 7**: Saure Lösungen (mehr H⁺-Ionen als OH⁻-Ionen)
- **pH = 7**: Neutrale Lösungen (gleichviele H⁺ und OH⁻-Ionen)
- **pH > 7**: Basische Lösungen (weniger H⁺-Ionen als OH⁻-Ionen)

Die pH-Skala ist logarithmisch, das heißt: jeder Anstieg um 1 bedeutet eine 10x niedrigere
Wasserstoffionenkonzentration.
""")
