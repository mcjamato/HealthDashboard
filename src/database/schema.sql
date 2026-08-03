PRAGMA foreign_keys = ON;
CREATE TABLE IF NOT EXISTS clients (
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 first_name TEXT NOT NULL,
 last_name TEXT NOT NULL,
 email TEXT UNIQUE,
 birth_date TEXT,
 active INTEGER NOT NULL DEFAULT 1,
 created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS exercise_records (
 id INTEGER PRIMARY KEY AUTOINCREMENT, client_id INTEGER NOT NULL, recorded_on TEXT NOT NULL,
 exercise_type TEXT NOT NULL, duration_minutes INTEGER NOT NULL CHECK(duration_minutes >= 0),
 intensity TEXT NOT NULL, steps INTEGER DEFAULT 0 CHECK(steps >= 0), distance_km REAL DEFAULT 0,
 calories_burned REAL DEFAULT 0, notes TEXT, is_active INTEGER NOT NULL DEFAULT 1,
 created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP, FOREIGN KEY(client_id) REFERENCES clients(id)
);
CREATE TABLE IF NOT EXISTS health_records (
 id INTEGER PRIMARY KEY AUTOINCREMENT, client_id INTEGER NOT NULL, recorded_on TEXT NOT NULL,
 weight_kg REAL, sleep_hours REAL CHECK(sleep_hours >= 0 AND sleep_hours <= 24),
 sleep_quality INTEGER CHECK(sleep_quality BETWEEN 1 AND 10), resting_heart_rate INTEGER,
 systolic_bp INTEGER, diastolic_bp INTEGER, water_liters REAL DEFAULT 0, notes TEXT,
 is_active INTEGER NOT NULL DEFAULT 1, created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
 FOREIGN KEY(client_id) REFERENCES clients(id)
);
CREATE TABLE IF NOT EXISTS mental_wellness_records (
 id INTEGER PRIMARY KEY AUTOINCREMENT, client_id INTEGER NOT NULL, recorded_on TEXT NOT NULL,
 mood_score INTEGER NOT NULL CHECK(mood_score BETWEEN 1 AND 10),
 stress_score INTEGER NOT NULL CHECK(stress_score BETWEEN 1 AND 10),
 energy_score INTEGER NOT NULL CHECK(energy_score BETWEEN 1 AND 10),
 focus_score INTEGER NOT NULL CHECK(focus_score BETWEEN 1 AND 10),
 meditation_minutes INTEGER DEFAULT 0, journal_entry TEXT, is_active INTEGER NOT NULL DEFAULT 1,
 created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP, FOREIGN KEY(client_id) REFERENCES clients(id)
);
CREATE TABLE IF NOT EXISTS nutrition_records (
 id INTEGER PRIMARY KEY AUTOINCREMENT, client_id INTEGER NOT NULL, recorded_on TEXT NOT NULL,
 meal_type TEXT NOT NULL, calories REAL NOT NULL CHECK(calories >= 0), protein_g REAL DEFAULT 0,
 carbs_g REAL DEFAULT 0, fat_g REAL DEFAULT 0, fiber_g REAL DEFAULT 0,
 water_liters REAL DEFAULT 0, notes TEXT, is_active INTEGER NOT NULL DEFAULT 1,
 created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP, FOREIGN KEY(client_id) REFERENCES clients(id)
);
CREATE INDEX IF NOT EXISTS idx_exercise_client_date ON exercise_records(client_id, recorded_on);
CREATE INDEX IF NOT EXISTS idx_health_client_date ON health_records(client_id, recorded_on);
CREATE INDEX IF NOT EXISTS idx_mental_client_date ON mental_wellness_records(client_id, recorded_on);
CREATE INDEX IF NOT EXISTS idx_nutrition_client_date ON nutrition_records(client_id, recorded_on);

CREATE TABLE IF NOT EXISTS scheduled_reports (
 id INTEGER PRIMARY KEY AUTOINCREMENT, client_id INTEGER NOT NULL,
 report_type TEXT NOT NULL, frequency TEXT NOT NULL, next_run_date TEXT NOT NULL,
 output_format TEXT NOT NULL DEFAULT 'PDF', active INTEGER NOT NULL DEFAULT 1,
 created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
 FOREIGN KEY(client_id) REFERENCES clients(id));
CREATE TABLE IF NOT EXISTS import_history (
 id INTEGER PRIMARY KEY AUTOINCREMENT, filename TEXT NOT NULL,
 rows_imported INTEGER NOT NULL DEFAULT 0, rows_rejected INTEGER NOT NULL DEFAULT 0,
 imported_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP);
CREATE TABLE IF NOT EXISTS report_history (
 id INTEGER PRIMARY KEY AUTOINCREMENT, client_id INTEGER NOT NULL,
 report_type TEXT NOT NULL, output_format TEXT NOT NULL, file_name TEXT NOT NULL,
 created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
 FOREIGN KEY(client_id) REFERENCES clients(id));
