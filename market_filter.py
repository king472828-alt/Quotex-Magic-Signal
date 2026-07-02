# market_filter.py
import pandas as pd
import numpy as np

def is_otc_market(symbol):
    """
    Checks if the symbol belongs to an OTC market.
    """
    if "OTC" in symbol.upper():
        return True
    return False

def is_sideways_market(df, period=20):
    """
    Detects if the market is ranging or sideways using ADX or Bollinger Bands width.
    """
    if len(df) < period:
        return True
    
    # Calculate Bollinger Bands Width
    df['MA'] = df['close'].rolling(window=period).mean()
    df['STD'] = df['close'].rolling(window=period).std()
    df['BB_Width'] = (df['STD'] * 4) / df['MA']
    
    # Check if recent volatility is below average (Indicating Sideways)
    recent_width = df['BB_Width'].iloc[-1]
    avg_width = df['BB_Width'].rolling(window=50).mean().iloc[-1]
    
    if recent_width < (avg_width * 0.8):
        return True # Market is sideways/ranging
        
    return False # Market is trending
