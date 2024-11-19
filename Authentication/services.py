# services.py
import joblib
import pandas as pd
from typing import Dict, Tuple
import numpy as np
from datetime import datetime

class PredictionService:
    def __init__(self):
        # Load your trained models
        self.rf_methane_model = joblib.load('path_to_methane_model.joblib')
        self.rf_milk_model = joblib.load('path_to_milk_model.joblib')

    def create_features(self, data: Dict) -> pd.DataFrame:
        df = pd.DataFrame([data])
        df['weight_dmi_ratio'] = df['weight_kg'] / df['dmi_kg_day']
        df['temperature_humidity_index'] = (0.8 * df['temperature'] +
                                          (df['humidity'] / 100) *
                                          (df['temperature'] - 14.4) + 46.4)
        df['feed_efficiency'] = df['milk_yield'] / df['dmi_kg_day']
        df['age_category'] = pd.cut(df['age_months'],
                                   bins=[0, 36, 60, 84, 120],
                                   labels=['Young', 'Prime', 'Mature', 'Old'])
        return df

    def predict(self, data: Dict) -> Tuple[float, float]:
        df = self.create_features(data)
        methane_prediction = self.rf_methane_model.predict(df)[0] / 1000
        milk_prediction = self.rf_milk_model.predict(df)[0]
        return methane_prediction, milk_prediction
