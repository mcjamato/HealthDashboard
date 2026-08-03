from __future__ import annotations
import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

class DatabaseManager:
    def __init__(self, database_path: Path, schema_path: Path) -> None:
        self.database_path = database_path
        self.schema_path = schema_path

    @contextmanager
    def connection(self) -> Iterator[sqlite3.Connection]:
        self.database_path.parent.mkdir(parents=True, exist_ok=True)
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        try:
            yield connection
            connection.commit()
        except Exception:
            connection.rollback()
            raise
        finally:
            connection.close()

    def initialize(self) -> None:
        with self.connection() as connection:
            connection.executescript(self.schema_path.read_text(encoding="utf-8"))
