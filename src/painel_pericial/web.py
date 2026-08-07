from __future__ import annotations

import pandas as pd
import streamlit as st
from sqlalchemy import text

from .db import engine, init_db
from .refresh import request_refresh

st.set_page_config(page_title="Painel Pericial Cloud", page_icon="☁️", layout="wide")
st.title("Painel Pericial Cloud")
st.caption("Case de modernização AWS. Classificações de prazo são heurísticas e devem ser validadas na fonte oficial.")
init_db()

left, right = st.columns([1, 3])
with left:
    if st.button("Solicitar atualização", use_container_width=True):
        if request_refresh():
            st.success("Atualização enfileirada com sucesso.")
        else:
            st.info("Fila de atualização não configurada neste ambiente. No modo local, execute o container worker.")
with right:
    st.caption("Na AWS, a solicitação entra no SQS e uma Lambda dispara uma tarefa Fargate isolada para coleta.")

with engine.connect() as conn:
    df = pd.read_sql(text("SELECT * FROM processes ORDER BY updated_at DESC"), conn)
    alerts_df = pd.read_sql(text("SELECT * FROM alerts ORDER BY id DESC LIMIT 250"), conn)

if df.empty:
    st.info("Nenhum processo carregado. Importe o cadastro de demonstração ou execute o worker.")
    st.stop()

search = st.text_input("Buscar por processo, cliente ou apelido")
if search:
    needle = search.lower()
    df = df[
        df["process_number"].fillna("").str.lower().str.contains(needle)
        | df["client"].fillna("").str.lower().str.contains(needle)
        | df["nickname"].fillna("").str.lower().str.contains(needle)
    ]

f1, f2, f3 = st.columns(3)
with f1:
    client = st.selectbox("Cliente", ["Todos"] + sorted(x for x in df["client"].fillna("").unique() if x))
with f2:
    risk = st.selectbox("Risco", ["Todos"] + sorted(x for x in df["risk_level"].fillna("").unique() if x))
with f3:
    deadline_type = st.selectbox("Tipo de prazo", ["Todos"] + sorted(x for x in df["deadline_type"].fillna("").unique() if x))

filtered = df.copy()
if client != "Todos": filtered = filtered[filtered["client"] == client]
if risk != "Todos": filtered = filtered[filtered["risk_level"] == risk]
if deadline_type != "Todos": filtered = filtered[filtered["deadline_type"] == deadline_type]

k1, k2, k3, k4 = st.columns(4)
k1.metric("Processos", len(filtered))
k2.metric("Críticos", int((filtered["risk_level"] == "CRITICO").sum()))
k3.metric("Atrasados", int((filtered["risk_level"] == "ATRASADO").sum()))
k4.metric("Sem prazo", int((filtered["risk_level"] == "SEM PRAZO").sum()))

st.subheader("Resumo dos processos")
columns = ["process_number", "client", "category", "last_movement_date", "deadline", "deadline_type", "risk_level", "last_movement_text"]
st.dataframe(filtered[columns], use_container_width=True, hide_index=True)

c1, c2 = st.columns(2)
with c1:
    st.subheader("Distribuição por risco")
    st.bar_chart(filtered["risk_level"].value_counts())
with c2:
    st.subheader("Distribuição por tipo de prazo")
    st.bar_chart(filtered["deadline_type"].value_counts())

st.subheader("Alertas recentes")
if alerts_df.empty:
    st.info("Nenhum alerta gerado.")
else:
    alert_cols = ["process_number", "client", "movement_date", "deadline", "deadline_type", "risk_level", "alert_type", "movement_text", "created_at"]
    st.dataframe(alerts_df[alert_cols], use_container_width=True, hide_index=True)

st.subheader("Histórico de movimentações")
options = filtered["process_number"].dropna().tolist()
if options:
    selected = st.selectbox("Processo", options)
    with engine.connect() as conn:
        history = pd.read_sql(text("SELECT process_number, movement_date, movement_text, collected_at FROM movements WHERE process_number=:p ORDER BY id DESC"), conn, params={"p": selected})
    st.dataframe(history, use_container_width=True, hide_index=True)
