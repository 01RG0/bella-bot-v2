import asyncio
import discord
from discord.ext import commands
from .config import config

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# Create bot instance
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')
    # Load command modules
    try:
        from .commands import ai_chat, mod, music, image
        await ai_chat.setup(bot)
        await mod.setup(bot)
        await music.setup(bot)
        await image.setup(bot)
        print('Commands loaded successfully')
    except Exception as e:
        print(f'Error loading commands: {e}')
    
    # Load event handlers
    try:
        from .events import on_message, on_voice_state
        await on_message.setup(bot)
        await on_voice_state.setup(bot)
        print('Event handlers loaded successfully')
    except Exception as e:
        print(f'Error loading event handlers: {e}')
    
    # Sync command tree
    try:
        synced = await bot.tree.sync()
        print(f'Synced {len(synced)} command(s)')
    except Exception as e:
        print(f'Error syncing commands: {e}')

def main():
    """Main entry point for the bot"""
    token = config.DISCORD_TOKEN
    if not token:
        print('DISCORD_TOKEN not set. Set the environment variable and try again.')
        return

    try:
        bot.run(token)
    except Exception as e:
        print(f'Error running bot: {e}')