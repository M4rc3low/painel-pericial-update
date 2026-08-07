# -*- coding: utf-8 -*-
from __future__ import annotations

import re
from datetime import date, datetime, timedelta


def detect_deadline_and_risk(movement_text: str, movement_date: str, *, today: date | None = None):
    if not movement_text:
        return "", "SEM PRAZO", "SEM PRAZO"

    text = movement_text.lower()
    if "laudo" in text:
        deadline_type = "LAUDO"
    elif "manifest" in text:
        deadline_type = "MANIFESTACAO"
    elif "esclarecimento" in text:
        deadline_type = "ESCLARECIMENTOS"
    elif "honor" in text:
        deadline_type = "HONORARIOS"
    else:
        deadline_type = "PRAZO_GERAL"

    patterns = [
        r"prazo de (\d+) dias",
        r"em (\d+) dias",
        r"no prazo de (\d+) dias",
        r"manifest(?:e|em-se).*?(\d+) dias",
        r"laudo.*?(\d+) dias",
        r"esclarecimentos?.*?(\d+) dias",
        r"honor[aá]rios?.*?(\d+) dias",
    ]
    days = next((int(m.group(1)) for p in patterns if (m := re.search(p, text))), None)
    if days is None:
        return "", "SEM PRAZO", deadline_type

    try:
        movement_day = datetime.strptime(movement_date, "%d/%m/%Y").date()
    except (TypeError, ValueError):
        movement_day = today or date.today()

    deadline_day = movement_day + timedelta(days=days)
    remaining = (deadline_day - (today or date.today())).days

    if remaining < 0:
        risk = "ATRASADO"
    elif remaining <= 2:
        risk = "CRITICO"
    elif remaining <= 5:
        risk = "ALTO"
    elif remaining <= 15:
        risk = "MEDIO"
    else:
        risk = "BAIXO"

    return deadline_day.strftime("%d/%m/%Y"), risk, deadline_type


def classify_alert_type(movement_text: str, deadline_type: str, risk_level: str):
    text = (movement_text or "").lower()
    if deadline_type != "SEM PRAZO" and risk_level in {"CRITICO", "ALTO", "ATRASADO"}:
        return "NOVO_PRAZO_URGENTE"
    if deadline_type != "SEM PRAZO":
        return "NOVO_PRAZO"
    if any(k in text for k in ("intima", "nomea", "laudo", "manifest", "esclarecimento", "honor", "prazo")):
        return "MOVIMENTACAO_RELEVANTE"
    return ""
