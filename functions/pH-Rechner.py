import math

def ph_from_concentration(concentration: float) -> float:
    """pH aus H⁺-Konzentration (mol L⁻¹)."""
    if concentration <= 0:
        raise ValueError("Konzentration muss positiv sein")
    return -math.log10(concentration)

def concentration_from_ph(ph: float) -> float:
    """H⁺-Konzentration zu einem pH‑Wert."""
    return 10 ** (-ph)