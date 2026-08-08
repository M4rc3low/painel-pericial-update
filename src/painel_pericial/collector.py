from __future__ import annotations

import re
from dataclasses import dataclass

import requests
from bs4 import BeautifulSoup

USER_AGENT = "PainelPericialCloud/1.0 (+portfolio; respectful-public-monitoring)"


def foro_from_process_number(process_number: str) -> str:
    return str(int(process_number.strip()[-4:]))


def build_detail_url(process_number: str) -> str:
    return (
        "https://esaj.tjsp.jus.br/cpopg/show.do"
        f"?processo.numero={process_number.strip()}&processo.foro={foro_from_process_number(process_number)}"
    )


def clean_text(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def extract_movements(page_text: str) -> list[dict[str, str]]:
    text = clean_text(page_text)
    marker = text.lower().find("movimenta")
    if marker >= 0:
        text = text[marker:]
    matches = list(re.finditer(r"\b\d{2}/\d{2}/\d{4}\b", text))
    rows: list[dict[str, str]] = []
    seen: set[tuple[str, str]] = set()
    for idx, match in enumerate(matches):
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(text)
        movement_date = match.group(0)
        description = clean_text(text[match.end():end])[:1200]
        key = (movement_date, description)
        if len(description) >= 3 and key not in seen:
            seen.add(key)
            rows.append({"movement_date": movement_date, "movement_text": description})
    return rows


@dataclass
class PublicEsajCollector:
    timeout: int = 30

    def collect(self, process_row: dict[str, str]) -> dict:
        number = process_row["process_number"].strip()
        url = build_detail_url(number)
        base = {
            "process_number": number,
            "nickname": process_row.get("nickname", ""),
            "client": process_row.get("client", ""),
            "category": process_row.get("category", ""),
            "source_url": url,
        }
        try:
            response = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=self.timeout)
            response.raise_for_status()
        except requests.RequestException as exc:
            return {**base, "status": f"http_error:{type(exc).__name__}", "movements": []}

        soup = BeautifulSoup(response.text, "lxml")
        movements = extract_movements(soup.get_text("\n", strip=True))
        return {**base, "status": "ok" if movements else "sem_movimentacoes", "movements": movements}
