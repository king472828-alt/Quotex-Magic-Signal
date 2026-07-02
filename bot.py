# bot.py
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import config
import signal_engine
import stats

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 Forex Signal Bot is Active!\nUse /signal to scan manually.")

async def signal_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔍 Scanning markets, please wait...")
    signals = signal_engine.generate_signals()
    if not signals:
        await update.message.reply_text("❌ No valid signals found. Filter criteria not met or market is sideways.")
        return
        
    for sig in signals:
        msg = f"🟢 **SIGNAL DETECTED** 🟢\n\n📌 **Pair:** {sig['symbol']}\n📈 **Action:** {sig['type']}\n💵 **Entry:** {sig['price']}\n🛡️ **Support:** {sig['support']}\n🎯 **Resistance:** {sig['resistance']}"
        await update.message.reply_text(msg, parse_mode="Markdown")

async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    current_stats = stats.load_stats()
    win_rate = stats.get_win_rate()
    msg = f"📊 **Daily Stats:**\n\n✅ Wins: {current_stats['wins']}\n❌ Losses: {current_stats['losses']}\n📈 Total Signals: {current_stats['total_signals']}\n🎯 Win Rate: {win_rate}%"
    await update.message.reply_text(msg, parse_mode="Markdown")

async def pairs_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pairs_list = "\n".join([f"- {p}" for p in config.FOREX_PAIRS])
    await update.message.reply_text(f"📋 **Monitored Forex Pairs ({len(config.FOREX_PAIRS)}):**\n\n{pairs_list}", parse_mode="Markdown")

async def auto_scan_loop(application):
    while True:
        signals = signal_engine.generate_signals()
        # You can add logic to broadcast to a specific chat ID if needed
        await asyncio.sleep(config.SCAN_INTERVAL_MINUTES * 60)

def main():
    application = Application.builder().token(config.TELEGRAM_TOKEN).build()

    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("signal", signal_command))
    application.add_handler(CommandHandler("stats", stats_command))
    application.add_handler(CommandHandler("pairs", pairs_command))

    print("Bot is starting...")
    application.run_polling()

if __name__ == "__main__":
    main()
