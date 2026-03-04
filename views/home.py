import streamlit as st

st.header("pH-Rechner")
st.write("Eine elegante Anwendung zur Berechnung von pH-Werten und H⁺-Konzentrationen")

st.divider()

st.subheader("Über diese App")
st.write("""
Diese App berechnet schnell und zuverlässig den pH-Wert aus der H⁺-Konzentration sowie die H⁺-Konzentration aus einem gegebenen pH-Wert.
""")

st.subheader("Mathematische Grundlagen")
st.write("Die Anwendung basiert auf der fundamentalen Beziehung:")
st.latex(r"\text{pH} = -\log_{10}([H^+])")
st.write("Dies liefert exakte Ergebnisse für chemische Berechnungen in Schule, Studium und Labor.")

st.divider()

st.subheader("Entwicklung & Credits")

col1, col2 = st.columns(2)
with col1:
    st.write("**Entwickler:**")
    st.badge("Sara Durrer")
    st.write("durresar@students.zhaw.ch")
    st.badge("Alessandro Zandt")
    st.write("zandtale@students.zhaw.ch")
    st.badge("David Hascher")
    st.write("haschdav@students.zhaw.ch")

with col2:
    st.write("**Betreuung:**")
    st.badge("Samuel Wehrli (Dozent)")
    st.caption("wehs@zhaw.ch")

st.divider()

st.subheader("Modul")
st.badge("BMLD-Informatik 2")
st.caption("ZHAW")
