import pandas as pd
from database.database import DatabaseManager

class ClientRepository:
    def __init__(self, db: DatabaseManager) -> None: self.db = db
    def create(self, first_name: str, last_name: str, email: str, birth_date: str | None) -> int:
        with self.db.connection() as connection:
            cursor = connection.execute(
                "INSERT INTO clients(first_name,last_name,email,birth_date) VALUES (?,?,?,?)",
                (first_name.strip(), last_name.strip(), email.strip() or None, birth_date),
            )
            return int(cursor.lastrowid)
    def list_active(self) -> pd.DataFrame:
        with self.db.connection() as connection:
            return pd.read_sql_query("SELECT id,first_name,last_name,email,birth_date,created_at FROM clients WHERE active=1 ORDER BY last_name,first_name", connection)
    def deactivate(self, client_id: int) -> None:
        with self.db.connection() as connection: connection.execute("UPDATE clients SET active=0 WHERE id=?", (client_id,))
