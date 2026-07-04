from __future__ import annotations

import os


def _enabled() -> bool:
    v = os.getenv("RUN_MIGRATIONS_ON_STARTUP", "false").strip().lower()
    return v in {"1", "true", "yes", "y", "on"}


def main() -> int:
    if not _enabled():
        return 0

    from alembic import command
    from alembic.config import Config

    cfg = Config("alembic.ini")
    command.upgrade(cfg, "head")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

