from datetime import date

from painel_pericial.rules import classify_alert_type, detect_deadline_and_risk


def test_urgent_deadline_generates_urgent_alert():
    assert classify_alert_type("prazo de 2 dias", "PRAZO_GERAL", "CRITICO") == "NOVO_PRAZO_URGENTE"


def test_non_deadline_relevant_movement():
    assert classify_alert_type("Intimação expedida", "SEM PRAZO", "SEM PRAZO") == "MOVIMENTACAO_RELEVANTE"


def test_deadline_calculation_is_deterministic():
    deadline, risk, kind = detect_deadline_and_risk("Apresente laudo no prazo de 10 dias", "01/08/2026", today=date(2026, 8, 7))
    assert deadline == "11/08/2026"
    assert risk == "ALTO"
    assert kind == "LAUDO"


def test_overdue_deadline():
    _, risk, _ = detect_deadline_and_risk("manifestação em 2 dias", "01/08/2026", today=date(2026, 8, 7))
    assert risk == "ATRASADO"
