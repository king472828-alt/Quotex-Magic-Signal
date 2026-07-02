# signal_engine.py
import MetaTrader5 as mt5
import pandas as pd
import config
import market_filter
import support_resistance

def initialize_mt5():
    if not mt5.initialize(login=config.MT5_LOGIN, password=config.MT5_PASSWORD, server=config.MT5_SERVER):
        print("MT5 Initialization Failed!")
        return False
    return True

def get_market_data(symbol, timeframe=mt5.TIMEFRAME_M5, count=100):
    rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, count)
    if rates is None or len(rates) == 0:
        return None
    df = pd.DataFrame(rates)
    df['time'] = pd.to_datetime(df['time'], unit='s')
    return df

def generate_signals():
    if not initialize_mt5():
        return []
        
    signals = []
    
    for symbol in config.FOREX_PAIRS:
        if market_filter.is_otc_market(symbol):
            continue
            
        df = get_market_data(symbol)
        if df is None:
            continue
            
        if market_filter.is_sideways_market(df):
            continue
            
        support, resistance = support_resistance.calculate_support_resistance(df)
        if support is None or resistance is None:
            continue
            
        current_price = df['close'].iloc[-1]
        
        # Signal conditions based on SR levels
        if current_price <= (support * 1.0002):
            signals.append({"symbol": symbol, "type": "BUY", "price": current_price, "support": support, "resistance": resistance})
        elif current_price >= (resistance * 0.9998):
            signals.append({"symbol": symbol, "type": "SELL", "price": current_price, "support": support, "resistance": resistance})
            
    mt5.shutdown()
    return signals
