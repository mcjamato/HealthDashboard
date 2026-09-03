from __future__ import annotations

INTAKE_SECTIONS = [
    (
        "1. Basic Information",
        [
            {"key": "gender", "label": "Gender", "type": "select", "options": ["", "Female", "Male", "Non-binary", "Prefer not to say", "Other"]},
            {"key": "phone_number", "label": "Phone Number", "type": "text"},
            {"key": "emergency_contact", "label": "Emergency Contact (Name + Phone)", "type": "text"},
            {"key": "occupation", "label": "Occupation", "type": "text"},
            {"key": "work_schedule", "label": "Work Schedule (hours, shifts, travel frequency)", "type": "textarea"},
        ],
    ),
    (
        "2. Primary Goals & Intentions",
        [
            {"key": "wellness_goals", "label": "Top wellness goals", "type": "multiselect", "options": ["Weight loss", "Muscle gain", "Increase energy", "Reduce stress", "Improve sleep", "Hormone balance", "Disease prevention", "Other"]},
            {"key": "goals_other", "label": "Other wellness goal", "type": "text"},
            {"key": "goals_importance", "label": "Why are these goals important to you?", "type": "textarea"},
            {"key": "motivation_now", "label": "What has motivated you to start now?", "type": "textarea"},
            {"key": "success_3_6_months", "label": "What would success look like in 3-6 months?", "type": "textarea"},
        ],
    ),
    (
        "3. Medical & Health History",
        [
            {"key": "medical_conditions", "label": "Diagnosed medical conditions", "type": "multiselect", "options": ["Diabetes", "Hypertension", "Thyroid issues", "Heart disease", "Autoimmune condition", "Digestive disorders", "Other"]},
            {"key": "medical_conditions_other", "label": "Other diagnosed condition", "type": "text"},
            {"key": "past_surgeries_injuries", "label": "Past surgeries or injuries", "type": "textarea"},
            {"key": "current_medications", "label": "Current medications", "type": "textarea"},
            {"key": "supplements", "label": "Supplements currently taking", "type": "textarea"},
            {"key": "allergies", "label": "Allergies (food, medication, environmental)", "type": "textarea"},
            {"key": "family_history", "label": "Family history of major illnesses", "type": "textarea"},
        ],
    ),
    (
        "4. Body Metrics",
        [
            {"key": "height_cm", "label": "Height (cm)", "type": "number", "min": 50.0, "max": 250.0, "step": 0.1},
            {"key": "intake_weight_kg", "label": "Weight (kg)", "type": "number", "min": 20.0, "max": 400.0, "step": 0.1},
            {"key": "body_fat_pct", "label": "Body fat % (if known)", "type": "number_optional", "min": 1.0, "max": 70.0, "step": 0.1},
            {"key": "waist_cm", "label": "Waist measurement (cm)", "type": "number_optional", "min": 20.0, "max": 250.0, "step": 0.1},
            {"key": "blood_pressure", "label": "Blood pressure (if known)", "type": "text"},
            {"key": "recent_lab_work", "label": "Recent lab work?", "type": "select", "options": ["", "Yes", "No"]},
        ],
    ),
    (
        "5. Nutrition & Eating Habits",
        [
            {"key": "diet_description", "label": "How would you describe your current diet?", "type": "textarea"},
            {"key": "typical_meals", "label": "Typical daily meals", "type": "textarea"},
            {"key": "water_intake_daily", "label": "Water intake per day", "type": "text"},
            {"key": "specific_diet", "label": "Specific diet", "type": "select", "options": ["", "Keto", "Vegan", "Vegetarian", "Paleo", "Intermittent fasting", "None"]},
            {"key": "food_preferences", "label": "Food preferences", "type": "textarea"},
            {"key": "foods_avoid", "label": "Foods you avoid", "type": "textarea"},
            {"key": "emotional_eating_triggers", "label": "Emotional eating triggers", "type": "textarea"},
            {"key": "eating_out_frequency", "label": "Frequency of eating out", "type": "text"},
            {"key": "alcohol_consumption", "label": "Alcohol consumption", "type": "select", "options": ["", "None", "Occasionally", "Weekly", "Daily"]},
        ],
    ),
    (
        "6. Physical Activity & Fitness",
        [
            {"key": "activity_level", "label": "Current activity level", "type": "select", "options": ["", "Sedentary", "Lightly active", "Moderately active", "Very active"]},
            {"key": "exercise_types", "label": "Types of exercise you do", "type": "textarea"},
            {"key": "exercise_frequency_weekly", "label": "Frequency per week", "type": "integer_optional", "min": 0, "max": 14},
            {"key": "exercise_session_duration", "label": "Duration of sessions", "type": "text"},
            {"key": "exercise_barriers", "label": "Barriers to exercise", "type": "textarea"},
            {"key": "exercise_limitations", "label": "Injuries or limitations", "type": "textarea"},
        ],
    ),
    (
        "7. Sleep & Recovery",
        [
            {"key": "sleep_hours", "label": "Average hours of sleep per night", "type": "number_optional", "min": 0.0, "max": 24.0, "step": 0.1},
            {"key": "sleep_quality_text", "label": "Sleep quality", "type": "select", "options": ["", "Poor", "Fair", "Good", "Excellent"]},
            {"key": "sleep_difficulties", "label": "Difficulty with", "type": "multiselect", "options": ["Falling asleep", "Staying asleep", "Waking early"]},
            {"key": "bedtime_routine", "label": "Bedtime routine", "type": "textarea"},
            {"key": "screen_use_before_bed", "label": "Screen use before bed", "type": "text"},
            {"key": "wake_rested", "label": "Do you wake feeling rested?", "type": "select", "options": ["", "Yes", "No"]},
        ],
    ),
    (
        "8. Stress & Mental Wellness",
        [
            {"key": "stress_level", "label": "Current stress level (1-10)", "type": "integer_optional", "min": 1, "max": 10},
            {"key": "stress_sources", "label": "Main sources of stress", "type": "textarea"},
            {"key": "stress_management", "label": "How do you manage stress currently?", "type": "textarea"},
            {"key": "stress_practices", "label": "Stress practices", "type": "multiselect", "options": ["Meditation", "Breathing exercises", "Journaling", "Therapy", "None"]},
            {"key": "mood_patterns", "label": "Mood patterns (optional)", "type": "textarea"},
            {"key": "mental_health_history", "label": "History of anxiety, depression, or burnout", "type": "textarea"},
        ],
    ),
    (
        "9. Lifestyle & Habits",
        [
            {"key": "daily_routine", "label": "Daily routine overview", "type": "textarea"},
            {"key": "self_care_time", "label": "Time available for self-care", "type": "text"},
            {"key": "support_system", "label": "Support system", "type": "textarea"},
            {"key": "tobacco_use", "label": "Smoking or tobacco use", "type": "text"},
            {"key": "caffeine_intake", "label": "Caffeine intake", "type": "text"},
            {"key": "screen_time_daily", "label": "Screen time per day", "type": "text"},
        ],
    ),
    (
        "10. Readiness & Commitment",
        [
            {"key": "readiness_score", "label": "Readiness to change (1-10)", "type": "integer_optional", "min": 1, "max": 10},
            {"key": "past_barriers", "label": "What has stopped you in the past?", "type": "textarea"},
            {"key": "support_needed", "label": "What support do you need most?", "type": "textarea"},
            {"key": "coaching_style", "label": "Preferred coaching style", "type": "select", "options": ["", "Structured plan", "Flexible guidance", "Accountability check-ins", "Education-focused"]},
        ],
    ),
    (
        "11. Preferences for Program Design",
        [
            {"key": "preferred_workout_style", "label": "Preferred workout style", "type": "text"},
            {"key": "preferred_nutrition_approach", "label": "Preferred nutrition approach", "type": "text"},
            {"key": "program_options", "label": "Program options", "type": "multiselect", "options": ["Meal plans", "Macro tracking", "Habit coaching", "Mindset coaching"]},
            {"key": "communication_preference", "label": "Communication preference", "type": "select", "options": ["", "Text", "Email", "Calls", "App messaging"]},
        ],
    ),
    (
        "12. Additional Notes",
        [
            {"key": "additional_notes", "label": "Anything else we should know about you?", "type": "textarea"},
            {"key": "injuries_fears_concerns", "label": "Injuries, fears, or concerns", "type": "textarea"},
            {"key": "worked_well_past", "label": "What has worked well for you in the past?", "type": "textarea"},
            {"key": "not_worked_past", "label": "What hasn't worked?", "type": "textarea"},
        ],
    ),
    (
        "13. Consent & Agreement",
        [
            {"key": "information_accurate", "label": "I confirm the information provided is accurate", "type": "checkbox"},
            {"key": "not_medical_treatment", "label": "I understand this program is not medical treatment", "type": "checkbox"},
            {"key": "signature_name", "label": "Signature", "type": "text"},
            {"key": "consent_date", "label": "Date", "type": "date_optional"},
        ],
    ),
]

INTAKE_FIELDS = [field for _, fields in INTAKE_SECTIONS for field in fields]
INTAKE_KEYS = [field["key"] for field in INTAKE_FIELDS]

BASE_CLIENT_COLUMNS = ["first_name", "last_name", "email", "birth_date"]
INTAKE_IMPORT_COLUMNS = BASE_CLIENT_COLUMNS + INTAKE_KEYS

MULTISELECT_FIELDS = {field["key"] for field in INTAKE_FIELDS if field["type"] == "multiselect"}
BOOLEAN_FIELDS = {field["key"] for field in INTAKE_FIELDS if field["type"] == "checkbox"}
NUMERIC_FIELDS = {field["key"] for field in INTAKE_FIELDS if field["type"] in {"number", "number_optional", "integer_optional"}}
DATE_FIELDS = {field["key"] for field in INTAKE_FIELDS if field["type"] == "date_optional"}
