import pandas as pd

class ReportRepository:
    def __init__(self, db):
        self.db = db

    def create_schedule(self, client_id, report_type, frequency, next_run_date, output_format):
        with self.db.connection() as connection:
            cursor = connection.execute(
                "INSERT INTO scheduled_reports(client_id, report_type, frequency, next_run_date, output_format) VALUES (?, ?, ?, ?, ?)",
                (client_id, report_type, frequency, next_run_date, output_format),
            )
            return int(cursor.lastrowid)

    def list_active_schedules(self):
        with self.db.connection() as connection:
            return pd.read_sql_query(
                """SELECT scheduled_reports.id,
                clients.first_name || ' ' || clients.last_name AS client,
                report_type, frequency, next_run_date, output_format
                FROM scheduled_reports JOIN clients ON clients.id = scheduled_reports.client_id
                WHERE scheduled_reports.active = 1 ORDER BY next_run_date""",
                connection,
            )

    def deactivate_schedule(self, schedule_id):
        with self.db.connection() as connection:
            connection.execute("UPDATE scheduled_reports SET active = 0 WHERE id = ?", (schedule_id,))
