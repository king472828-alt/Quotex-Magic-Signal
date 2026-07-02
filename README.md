# Telegram Forex Signal Bot

An automated Python script that scans 24 Forex currency pairs via MetaTrader 5, filters out ranging/OTC structures, and broadcasts high-probability execution indicators directly to a Telegram channel/bot interface.

## Project Structure
- `requirements.txt` - Dependency libraries
- `config.py` - Core configuration and pair selection parameters
- `market_filter.py` - Logic engine identifying ranging/OTC market patterns
- `support_resistance.py` - Calculations determining pricing breakout nodes
- `stats.py` - Metric dashboard mapping accuracy performance indices
- `signal_engine.py` - Data collection integration layer running MT5 pipeline hooks
- `bot.py` - Telegram API application router

## Local Installation Setup
Ensure your virtual architecture environment is configured, then install necessary library nodes using pip package manager:

```bash
pip install -r requirements.txt
```

Update your private API bot tokens and MT5 integration credentials inside `config.py` before executing the primary control hub:

```bash
python bot.py
```
