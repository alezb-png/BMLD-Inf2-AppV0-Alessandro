import math
from datetime import datetime
import pytz

def ph_from_concentration(concentration: float) -> float:
    """pH aus H⁺-Konzentration (mol L⁻¹)."""
    if concentration <= 0:
        raise ValueError("Konzentration muss positiv sein")
    return {
        "timestamp": datetime.now(pytz.timezone('Europe/Zurich')),  # Current swiss time
        "type": "pH-Rechner",
        "Resultat": -math.log10(concentration),
    } 

def concentration_from_ph(ph: float) -> float:
    """H⁺-Konzentration zu einem pH‑Wert."""
    return {
        "timestamp": datetime.now(pytz.timezone('Europe/Zurich')),  # Current swiss time
        "type": "H⁺-Konzentration zu einem pH‑Wert.",
        "Resultat": 10 ** (-ph),
    } 


