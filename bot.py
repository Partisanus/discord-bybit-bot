import discord
import requests
import pandas as pd
import ta
import asyncio
from discord.ext import commands
from datetime import datetime, timezone

# Discord bot keys
TOKEN = 'YOUR_DISCORD_BOT_TOKEN'
CHANNEL_ID = YOUR_DISCORD_CHANNEL_ID

# Bybit API settings
SYMBOL = 'SOLUSDT'
TIMEFRAME = '60'  # in minutes

# Delay parameter
STARTUP_FREQUENCY = 1  # in seconds

# Variables for tracking the last message
last_message = None
last_message_time = None

# Initializing the bot
intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents)


# Function for obtaining K-line data
def get_klines(symbol, interval):
    url = f"https://api.bybit.com/v5/market/kline?category=spot&symbol={symbol}&interval={interval}"
    response = requests.get(url)
    data = response.json()
    kline_list = data['result']['list']
    df = pd.DataFrame(kline_list, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'turnover'])
    df['timestamp'] = pd.to_numeric(df['timestamp'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms', utc=True)
    df['close'] = pd.to_numeric(df['close'])
    return df


# Function for RSI calculation
def calculate_rsi(data):
    rsi = ta.momentum.RSIIndicator(data['close'], window=14)
    return rsi.rsi().iloc[-1]


# Function to check RSI and send a message
async def check_rsi():
    global last_message, last_message_time
    await bot.wait_until_ready()
    channel = bot.get_channel(CHANNEL_ID)
    while not bot.is_closed():
        data = get_klines(SYMBOL, TIMEFRAME)
        rsi = calculate_rsi(data)
        last_timestamp = data['timestamp'].iloc[-1]
        current_time = datetime.now(timezone.utc)
        time_diff = (current_time - last_timestamp).total_seconds()

        if time_diff <= 10:
            message = None
            if rsi > 70:
                message = f'The RSI for {SYMBOL} is {rsi:.2f}.'
            elif rsi < 30:
                message = f'The RSI for {SYMBOL} is {rsi:.2f}.'

            if message and (message != last_message or (current_time - last_message_time).total_seconds() > 10):
                await channel.send(message)
                last_message = message
                last_message_time = current_time

        await asyncio.sleep(STARTUP_FREQUENCY)


# Starting a task when the bot is ready
@bot.event
async def on_ready():
    await bot.loop.create_task(check_rsi())
    print(f'Bot {bot.user} is up and running and ready to go!')


# Starting the bot
bot.run(TOKEN)
