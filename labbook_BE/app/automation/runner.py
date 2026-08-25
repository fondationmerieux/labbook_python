#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
automation runner
"""

import time
import logging

from app import app as flask_app
from app.models.Automation import Automation

# ---------------------------------------------------------------------------
# Logging setup
# ---------------------------------------------------------------------------
logger = logging.getLogger("automation_runner")
logging.basicConfig(
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.INFO,
)

# Fixed polling interval in seconds (no env var as requested).
POLL_SEC = 30


def run_once() -> None:
    """One scheduler tick: execute due jobs."""
    processed = Automation.scheduler_process_due(max_jobs=10)
    logger.info("processed=%s", processed)


def run_forever(poll_sec: int = POLL_SEC) -> None:
    """
    Infinite loop:
    - Enter the Flask app context for DB access.
    - Run one scheduler tick.
    - Sleep for the configured interval.
    - Catch and log any unexpected exception to keep the loop alive.
    """
    logger.info("automation runner started (poll=%ds)", poll_sec)
    while True:
        try:
            # Ensure DB/Flask context is available for model calls.
            with flask_app.app_context():
                run_once()
        except Exception:
            logger.exception("unexpected error in runner loop")
        time.sleep(poll_sec)


if __name__ == "__main__":
    run_forever()

