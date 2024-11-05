import discord
import requests
import time
from discord.ext import commands, tasks

# Replace these with your own values
DISCORD_TOKEN = '<TOKEN_HERE>' # Token
CHANNEL_ID = <CHANNEL_ID_HERE>  # Channel ID
URL = '<URL_HERE>'  # Replace with the website you want to monitor
USER_ID = '<USER_ID_HERE>' # UID to ping

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

last_size = None

def get_website_size(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return len(response.content)
    except requests.RequestException as e:
        print(f"Error fetching website: {e}")
        return None

@tasks.loop(minutes=1)  # Don't get rate limited
async def monitor_website():
    global last_size
    current_size = get_website_size(URL)
    channel = bot.get_channel(CHANNEL_ID)

    if current_size is None:
        print("Could not retrieve the website size.")
        return

    if last_size is not None and current_size != last_size:
        await channel.send(f"⚠️ <@{USER_ID}> The website at {URL} has changed in size!")
    
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')
    monitor_website.start()

bot.run(DISCORD_TOKEN)
