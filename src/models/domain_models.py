from dataclasses import asdict, dataclass
from datetime import date
from typing import Optional

class RecordMixin:
    def to_dict(self) -> dict:
        data = asdict(self)
        data["recorded_on"] = self.recorded_on.isoformat()
        return data

@dataclass
class ExerciseRecord(RecordMixin):
    client_id: int; recorded_on: date; exercise_type: str; duration_minutes: int; intensity: str
    steps: int = 0; distance_km: float = 0; calories_burned: float = 0; notes: str = ""

@dataclass
class HealthRecord(RecordMixin):
    client_id: int; recorded_on: date; weight_kg: Optional[float]; sleep_hours: Optional[float]
    sleep_quality: Optional[int]; resting_heart_rate: Optional[int]; systolic_bp: Optional[int]
    diastolic_bp: Optional[int]; water_liters: float = 0; notes: str = ""

@dataclass
class MentalWellnessRecord(RecordMixin):
    client_id: int; recorded_on: date; mood_score: int; stress_score: int; energy_score: int
    focus_score: int; meditation_minutes: int = 0; journal_entry: str = ""

@dataclass
class NutritionRecord(RecordMixin):
    client_id: int; recorded_on: date; meal_type: str; calories: float; protein_g: float = 0
    carbs_g: float = 0; fat_g: float = 0; fiber_g: float = 0; water_liters: float = 0; notes: str = ""
