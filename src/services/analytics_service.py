import math
import pandas as pd

class AnalyticsService:
    @staticmethod
    def latest_value(frame: pd.DataFrame, column: str):
        if frame.empty or column not in frame: return None
        values = pd.to_numeric(frame[column], errors='coerce').dropna()
        return None if values.empty else float(values.iloc[0])
    @staticmethod
    def mean(frame: pd.DataFrame, column: str):
        if frame.empty or column not in frame: return None
        value = pd.to_numeric(frame[column], errors='coerce').mean()
        return None if math.isnan(value) else float(value)
    @staticmethod
    def percent_change(values):
        clean = [float(v) for v in values if pd.notna(v)]
        if len(clean) < 2 or clean[-2] == 0: return None
        return ((clean[-1]-clean[-2])/abs(clean[-2]))*100
    @staticmethod
    def prepare_chronological(frame: pd.DataFrame) -> pd.DataFrame:
        if frame.empty: return frame
        result = frame.copy(); result['recorded_on'] = pd.to_datetime(result['recorded_on'])
        return result.sort_values('recorded_on')
