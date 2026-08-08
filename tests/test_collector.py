from painel_pericial.collector import build_detail_url, extract_movements, foro_from_process_number


def test_foro_strips_leading_zeroes():
    assert foro_from_process_number("1001234-12.2024.8.26.0053") == "53"


def test_build_detail_url():
    url = build_detail_url("1001234-12.2024.8.26.0053")
    assert "processo.numero=1001234-12.2024.8.26.0053" in url
    assert "processo.foro=53" in url


def test_extract_movements():
    text = "Movimentações 05/08/2026 Intimação expedida prazo de 5 dias 01/08/2026 Documento juntado"
    rows = extract_movements(text)
    assert rows[0]["movement_date"] == "05/08/2026"
    assert "Intimação" in rows[0]["movement_text"]
