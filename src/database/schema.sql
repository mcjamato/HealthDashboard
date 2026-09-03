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



CREATE TABLE IF NOT EXISTS client_intake_profiles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    client_id INTEGER NOT NULL UNIQUE,
    gender TEXT,
    phone_number TEXT,
    emergency_contact TEXT,
    occupation TEXT,
    work_schedule TEXT,
    wellness_goals TEXT,
    goals_other TEXT,
    goals_importance TEXT,
    motivation_now TEXT,
    success_3_6_months TEXT,
    medical_conditions TEXT,
    medical_conditions_other TEXT,
    past_surgeries_injuries TEXT,
    current_medications TEXT,
    supplements TEXT,
    allergies TEXT,
    family_history TEXT,
    height_cm REAL,
    intake_weight_kg REAL,
    body_fat_pct REAL,
    waist_cm REAL,
    blood_pressure TEXT,
    recent_lab_work TEXT,
    diet_description TEXT,
    typical_meals TEXT,
    water_intake_daily TEXT,
    specific_diet TEXT,
    food_preferences TEXT,
    foods_avoid TEXT,
    emotional_eating_triggers TEXT,
    eating_out_frequency TEXT,
    alcohol_consumption TEXT,
    activity_level TEXT,
    exercise_types TEXT,
    exercise_frequency_weekly INTEGER,
    exercise_session_duration TEXT,
    exercise_barriers TEXT,
    exercise_limitations TEXT,
    sleep_hours REAL,
    sleep_quality_text TEXT,
    sleep_difficulties TEXT,
    bedtime_routine TEXT,
    screen_use_before_bed TEXT,
    wake_rested TEXT,
    stress_level INTEGER,
    stress_sources TEXT,
    stress_management TEXT,
    stress_practices TEXT,
    mood_patterns TEXT,
    mental_health_history TEXT,
    daily_routine TEXT,
    self_care_time TEXT,
    support_system TEXT,
    tobacco_use TEXT,
    caffeine_intake TEXT,
    screen_time_daily TEXT,
    readiness_score INTEGER,
    past_barriers TEXT,
    support_needed TEXT,
    coaching_style TEXT,
    preferred_workout_style TEXT,
    preferred_nutrition_approach TEXT,
    program_options TEXT,
    communication_preference TEXT,
    additional_notes TEXT,
    injuries_fears_concerns TEXT,
    worked_well_past TEXT,
    not_worked_past TEXT,
    information_accurate INTEGER NOT NULL DEFAULT 0,
    not_medical_treatment INTEGER NOT NULL DEFAULT 0,
    signature_name TEXT,
    consent_date TEXT,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(client_id) REFERENCES clients(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_client_intake_client ON client_intake_profiles(client_id);

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL CHECK(role IN ('admin', 'client')),
    client_id INTEGER,
    active INTEGER NOT NULL DEFAULT 1,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(client_id) REFERENCES clients(id)
);

CREATE TABLE IF NOT EXISTS exercise_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    client_id INTEGER NOT NULL,
    recorded_on TEXT NOT NULL,
    exercise_type TEXT NOT NULL,
    duration_minutes INTEGER NOT NULL CHECK(duration_minutes >= 0),
    intensity TEXT NOT NULL,
    steps INTEGER DEFAULT 0 CHECK(steps >= 0),
    distance_km REAL DEFAULT 0 CHECK(distance_km >= 0),
    calories_burned REAL DEFAULT 0 CHECK(calories_burned >= 0),
    notes TEXT,
    is_active INTEGER NOT NULL DEFAULT 1,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(client_id) REFERENCES clients(id)
);

CREATE TABLE IF NOT EXISTS health_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    client_id INTEGER NOT NULL,
    recorded_on TEXT NOT NULL,
    weight_kg REAL,
    sleep_hours REAL CHECK(sleep_hours >= 0 AND sleep_hours <= 24),
    sleep_quality INTEGER CHECK(sleep_quality BETWEEN 1 AND 10),
    resting_heart_rate INTEGER,
    systolic_bp INTEGER,
    diastolic_bp INTEGER,
    water_liters REAL DEFAULT 0,
    notes TEXT,
    is_active INTEGER NOT NULL DEFAULT 1,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(client_id) REFERENCES clients(id)
);

CREATE TABLE IF NOT EXISTS mental_wellness_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    client_id INTEGER NOT NULL,
    recorded_on TEXT NOT NULL,
    mood_score INTEGER NOT NULL CHECK(mood_score BETWEEN 1 AND 10),
    stress_score INTEGER NOT NULL CHECK(stress_score BETWEEN 1 AND 10),
    energy_score INTEGER NOT NULL CHECK(energy_score BETWEEN 1 AND 10),
    focus_score INTEGER NOT NULL CHECK(focus_score BETWEEN 1 AND 10),
    meditation_minutes INTEGER DEFAULT 0,
    journal_entry TEXT,
    is_active INTEGER NOT NULL DEFAULT 1,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(client_id) REFERENCES clients(id)
);

CREATE TABLE IF NOT EXISTS nutrition_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    client_id INTEGER NOT NULL,
    recorded_on TEXT NOT NULL,
    meal_type TEXT NOT NULL,
    calories REAL NOT NULL CHECK(calories >= 0),
    protein_g REAL DEFAULT 0,
    carbs_g REAL DEFAULT 0,
    fat_g REAL DEFAULT 0,
    fiber_g REAL DEFAULT 0,
    water_liters REAL DEFAULT 0,
    notes TEXT,
    is_active INTEGER NOT NULL DEFAULT 1,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(client_id) REFERENCES clients(id)
);

CREATE TABLE IF NOT EXISTS scheduled_reports (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    client_id INTEGER NOT NULL,
    report_type TEXT NOT NULL,
    frequency TEXT NOT NULL,
    next_run_date TEXT NOT NULL,
    output_format TEXT NOT NULL DEFAULT 'PDF',
    active INTEGER NOT NULL DEFAULT 1,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(client_id) REFERENCES clients(id)
);

CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
CREATE INDEX IF NOT EXISTS idx_users_client ON users(client_id);
CREATE INDEX IF NOT EXISTS idx_exercise_client_date ON exercise_records(client_id, recorded_on);
CREATE INDEX IF NOT EXISTS idx_health_client_date ON health_records(client_id, recorded_on);
CREATE INDEX IF NOT EXISTS idx_mental_client_date ON mental_wellness_records(client_id, recorded_on);
CREATE INDEX IF NOT EXISTS idx_nutrition_client_date ON nutrition_records(client_id, recorded_on);


CREATE TABLE IF NOT EXISTS blood_work_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    client_id INTEGER NOT NULL,
    recorded_on TEXT NOT NULL,
    test_name TEXT NOT NULL,
    value REAL NOT NULL,
    unit TEXT,
    reference_low REAL,
    reference_high REAL,
    notes TEXT,
    is_active INTEGER NOT NULL DEFAULT 1,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(client_id) REFERENCES clients(id)
);

CREATE INDEX IF NOT EXISTS idx_blood_work_client_date
ON blood_work_records(client_id, recorded_on);
