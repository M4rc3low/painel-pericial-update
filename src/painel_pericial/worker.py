from __future__ import annotations

import logging
import time

from .collector import PublicEsajCollector
from .config import settings
from .db import active_processes, add_alert_if_new, add_movement_if_new, init_db, upsert_process
from .notifications import publish_alert
from .rules import classify_alert_type, detect_deadline_and_risk

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("painel.worker")


def process_one(collector: PublicEsajCollector, row: dict[str, str]) -> int:
    result = collector.collect(row)
    movements = result.pop("movements", [])
    latest = movements[0] if movements else {"movement_date": "", "movement_text": ""}
    deadline, risk, deadline_type = detect_deadline_and_risk(latest["movement_text"], latest["movement_date"])
    result.update({
        "last_movement_date": latest["movement_date"],
        "last_movement_text": latest["movement_text"],
        "deadline": deadline,
        "deadline_type": deadline_type,
        "risk_level": risk,
    })
    upsert_process(result)

    new_alerts = 0
    for movement in movements:
        if not add_movement_if_new(result["process_number"], movement["movement_date"], movement["movement_text"]):
            continue
        m_deadline, m_risk, m_type = detect_deadline_and_risk(movement["movement_text"], movement["movement_date"])
        alert_type = classify_alert_type(movement["movement_text"], m_type, m_risk)
        if not alert_type:
            continue
        alert = {
            "process_number": result["process_number"],
            "client": result.get("client", ""),
            "movement_date": movement["movement_date"],
            "movement_text": movement["movement_text"],
            "deadline": m_deadline,
            "deadline_type": m_type,
            "risk_level": m_risk,
            "alert_type": alert_type,
        }
        if add_alert_if_new(alert):
            new_alerts += 1
            publish_alert(alert)
    return new_alerts


def main() -> None:
    init_db()
    if settings.collector_mode != "public":
        raise RuntimeError("Only COLLECTOR_MODE=public is cloud-enabled. Interactive authenticated sessions stay outside the cloud boundary until explicitly redesigned.")

    processes = active_processes()
    log.info("collection_started processes=%s", len(processes))
    collector = PublicEsajCollector()
    alerts = 0
    for index, row in enumerate(processes):
        try:
            alerts += process_one(collector, row)
            log.info("process_collected process=%s", row["process_number"])
        except Exception:
            log.exception("process_failed process=%s", row["process_number"])
        if index + 1 < len(processes):
            time.sleep(settings.collector_delay_seconds)
    log.info("collection_finished processes=%s new_alerts=%s", len(processes), alerts)


if __name__ == "__main__":
    main()
