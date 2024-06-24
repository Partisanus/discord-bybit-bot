# Discord Bot

This project is a Discord bot that extracts K-line data for SOL/USDT pair with Bybit, calculates RSI and sends notifications to Discord channel.

### Customize bot settings

### Step 1: Configure Discord keys

In bot.py, replace 'YOUR_DISCORD_BOT_TOKEN' and YOUR_DISCORD_CHANNEL_ID with your Discord bot token and channel id.

### Step 2: Bybit API settings
In bot.py you can change the name of the currency pair to be tracked (SYMBOL) and the TIMEFRAME in minutes.

### Step 3: Delay parameter
In bot.py you can change the delay for sending requests for data from Bybit: STARTUP_FREQUENCY parameter is set in seconds.



### Startup in Docker

### Step 1: Clone the repository

`bash
git clone https://github.com/RamanHrynkevich/discord-bybit-bot.git
cd discord-bybit-bot

### Step 2: Build a Docker image
docker build -t discord-bot . 

### Step 3: Start the container
docker run -d --name discord-bot discord-bot 
