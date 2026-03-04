import streamlit as st
st.title("pH-Wert Berechnung")



st.write("Mit der pH Rechner App berechnest du mühelos pH-Wert, pOH-Wert sowie H₃O⁺- und OH⁻-Konzentrationen. Ideal für Schüler, Studierende, Lehrkräfte, Laborpersonal oder alle, die schnell und zuverlässig chemische Werte bestimmen möchten.")


import streamlit as st
from pathlib import Path
import importlib.util
import sys

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
st.title("pH‑Rechner")

mode = st.radio("Modus wählen",
                ("Konzentration → pH", "pH → Konzentration"))

if mode == "Konzentration → pH":
    conc = st.number_input("Wasserstoffionenkonzentration (mol/L)",
                           min_value=0.0, format="%.6f", step=1e-6)
    if conc > 0:
        try:
            ph = ph_from_concentration(conc)
            st.success(f"pH‑Wert: {ph:.4f}")
        except ValueError as e:
            st.error(str(e))
    else:
        st.info("Bitte eine positive Konzentration eingeben.")
else:
    ph = st.number_input("pH‑Wert", min_value=-2.0, max_value=16.0,
                         format="%.4f", step=0.1)
    conc = concentration_from_ph(ph)
    st.success(f"Konzentration: {conc:.6e} mol/L")