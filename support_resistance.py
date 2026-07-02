# support_resistance.py
import pandas as pd

def calculate_support_resistance(df):
    """
    Calculates key Support and Resistance levels from the recent price data.
    """
    if len(df) < 5:
        return None, None
        
    highs = df['high'].tolist()
    lows = df['low'].tolist()
    
    # Simple pivot calculation over recent periods
    resistance = max(highs[-5:])
    support = min(lows[-5:])
    
    return support, resistance
